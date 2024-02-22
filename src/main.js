const { app, BrowserWindow, ipcMain, globalShortcut } = require("electron");
const {
  SEND_MAIN_PING,
  SEND_WINDOW_MINIMIZE,
  SEND_WINDOW_MAXIMIZE,
  SEND_WINDOW_CLOSE,
  SEND_MATCH_INFO,
  SEND_PREDICT_GAME,
} = require("./constants");
const axios = require("axios");
const fs = require("fs");
const { spawn } = require("child_process");

let win;
let overlayProcess; // overlay.py 프로세스 변수
let testProcess;

// overlay.py를 실행하는 함수
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

function runTestScript() {
  testProcess = spawn("python", ["backend/predict_GRU.py"]);

  testProcess.stdout.on("data", (data) => {
    console.log(`predict_GRU stdout: ${data}`);
  });

  testProcess.stderr.on("data", (data) => {
    console.error(`predict_GRU stderr: ${data}`);
  });

  testProcess.on("close", (code) => {
    console.log(`predict_GRU : child process exited with code ${code}`);
    if(code == 0) {
      runOverlayScript();
    }
  });
}

async function createWindow() {
  win = new BrowserWindow({
    width: 1072,
    height: 659,
    frame: false,
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

    try {
      const response = await axios.post("http://localhost:4000/", {
        data: arg.fileName,
      });
      console.log("server res:", response.data);

      fs.readFile("backend/api_match_info.json", "utf8", (err, data) => {
        if (err) {
          console.error("Error reading file");
          return;
        }

        try {
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
          let championNameList = new Array(10);
          let summonerNameList = new Array(10);
          let teamIdList = new Array(10);
          let assistsList = new Array(10);
          let deathsList = new Array(10);
          let killsList = new Array(10);

          const participantsList = jsonData.info.participants;

          for (index = 0; index < 10; index++) {
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
          console.error("Error JSON data: ", error);
        }
      });
    } catch (error) {
      console.error("server error:", error);
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

  ipcMain.on(SEND_WINDOW_MINIMIZE, (event, arg) => {
    win.minimize();
  });

  ipcMain.on(SEND_WINDOW_MAXIMIZE, (event, arg) => {
    if (win.isMaximized()) {
      win.unmaximize();
    } else {
      win.maximize();
    }
  });

  ipcMain.on(SEND_WINDOW_CLOSE, (event, arg) => {
    win.close();
    globalShortcut.unregisterAll();
  });
}

app.whenReady().then(() => {
  createWindow();
});

app.on("window-all-closed", () => {
  if (overlayProcess) {
    overlayProcess.stdin.write("exit"); // overlay.py에 종료 신호 보내기
  }

  if (process.platform !== "darwin") {
    app.quit();
  }
});
