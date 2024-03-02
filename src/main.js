const { app, BrowserWindow, ipcMain, globalShortcut } = require("electron");
const {
  SEND_MAIN_PING,
  SEND_WINDOW_MINIMIZE,
  SEND_WINDOW_MAXIMIZE,
  SEND_WINDOW_CLOSE,
  SEND_MATCH_INFO,
  SEND_PREDICT_GAME,
  PREDICT_OVER,
} = require("./constants");
const fs = require("fs").promises; // 비동기 파일 쓰기를 위해 fs.promises 사용
const request = require("request");
const { spawn } = require("child_process");

const apiKey = "RGAPI-3faaf49c-8156-4efa-b558-363aaf3c2f6f";

let win;
let overlayProcess; // overlay.py 프로세스 변수
let testProcess;

function runOverlayScript() {
  overlayProcess = spawn("python", ["src/overlay.py"]);

  overlayProcess.stdout.on("data", (data) => {
    console.log(`overlay stdout: ${data}`);
  });

  overlayProcess.stderr.on("data", (data) => {
    console.error(`overlay stderr: ${data}`);
  });

  overlayProcess.on("close", (code) => {
    console.log(`overlay : child process exited with code ${code}`);
  });
}

async function runTestScript() {
  testProcess = spawn("python", ["backend/predict_GRU.py"]);

  testProcess.stdout.on("data", (data) => {
    console.log(`predict_GRU stdout: ${data}`);
  });

  testProcess.stderr.on("data", (data) => {
    console.error(`predict_GRU stderr: ${data}`);
  });

  testProcess.on("close", async (code) => {
    console.log(`predict_GRU : child process exited with code ${code}`);
    if (code === 0) {
      const data = await fs.readFile(
        "C:/GitHub/predict_gg/src/predict_data.txt",
        "utf8"
      );
      const lines = data.split("\r\n");
      const predict_data = lines.map((line) => {
        const numbers = line
          .slice(1, line.length - 1)
          .split(",")
          .map((num) => parseInt(num.trim()));
        //console.log("numbers");
        //console.log(numbers);
        return numbers;
      });

      win.webContents.send(PREDICT_OVER, { predict_data });
      runOverlayScript();
    }
  });
}

async function createWindow() {
  win = new BrowserWindow({
    width: 1072,
    height: 659,
    //frame: false,
    resizable: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  win.loadURL("http://localhost:3000");

  // 이벤트 핸들러 등록
  ipcMain.on(SEND_MAIN_PING, async (event, arg) => {
    console.log("File uploaded in Renderer process!");
    console.log("Uploaded file name:", arg.fileName);

    const matchId = arg.fileName.replace(/-/g, "_").split(".")[0];

    console.log("filename :", matchId);

    const apiUrl = `https://asia.api.riotgames.com/lol/match/v5/matches/${matchId}?api_key=${apiKey}`;
    const apiUrl2 = `https://asia.api.riotgames.com/lol/match/v5/matches/${matchId}/timeline?api_key=${apiKey}`;

    try {
      // 첫 번째 API 요청
      const [matchResponse, timelineResponse] = await Promise.all([
        getRequest(apiUrl),
        getRequest(apiUrl2),
      ]);

      // 데이터를 파일에 비동기적으로 저장
      await Promise.all([
        fs.writeFile(
          `api_data/api_match_info.json`,
          JSON.stringify(matchResponse.data, null, 2)
        ), // 들여쓰기와 줄 바꿈 추가
        fs.writeFile(
          `api_data/api_timeline_info.json`,
          JSON.stringify(timelineResponse.data, null, 2)
        ), // 들여쓰기와 줄 바꿈 추가
      ]);

      console.log("Data saved to files successfully.");

      // 파일 쓰기가 완료되면 파일을 읽고 데이터 처리
      const data = await fs.readFile("api_data/api_match_info.json", "utf8");
      const jsonData = JSON.parse(data);
      const realTimestamp =
        jsonData.info.gameEndTimestamp - jsonData.info.gameStartTimestamp;

      // 밀리초를 분과 초로 변환
      const minutes = Math.floor(realTimestamp / 60000);
      const seconds = ((realTimestamp % 60000) / 1000).toFixed(0);
      console.log(
        "realTimestamp",
        `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`
      );

      const championNameList = new Array(10);
      const summonerNameList = new Array(10);
      const teamIdList = new Array(10);
      const assistsList = new Array(10);
      const deathsList = new Array(10);
      const killsList = new Array(10);

      const participantsList = jsonData.info.participants;

      for (let index = 0; index < 10; index++) {
        championNameList[index] = participantsList[index].championName;
        summonerNameList[index] = participantsList[index].summonerName;
        teamIdList[index] = participantsList[index].teamId;
        assistsList[index] = participantsList[index].assists;
        deathsList[index] = participantsList[index].deaths;
        killsList[index] = participantsList[index].kills;
      }

      win.webContents.send(SEND_MATCH_INFO, {
        championNameList,
        summonerNameList,
        teamIdList,
        assistsList,
        deathsList,
        killsList,
      });
    } catch (error) {
      console.error("Error occurred while fetching or saving data:", error);
    }
  });

  ipcMain.on(SEND_PREDICT_GAME, async (event, arg) => {
    runTestScript();
  });

  // 이벤트 핸들러 등록
  ipcMain.on("stopOverlayProcess", () => {
    if (overlayProcess) {
      overlayProcess.kill();
    }
  });

  ipcMain.on(SEND_WINDOW_MINIMIZE, () => {
    win.minimize();
  });

  ipcMain.on(SEND_WINDOW_MAXIMIZE, () => {
    if (win.isMaximized()) {
      win.unmaximize();
    } else {
      win.maximize();
    }
  });

  ipcMain.on(SEND_WINDOW_CLOSE, () => {
    win.close();
    globalShortcut.unregisterAll();
  });
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (overlayProcess) {
    overlayProcess.stdin.write("exit"); // overlay.py에 종료 신호 보내기
  }

  if (process.platform !== "darwin") {
    app.quit();
  }
});

// request를 프로미스 기반으로 래핑하는 함수
function getRequest(url) {
  return new Promise((resolve, reject) => {
    request(url, (error, response, body) => {
      if (error) {
        reject(error);
      } else {
        resolve({ response, data: JSON.parse(body) });
      }
    });
  });
}
