const { getSummonerInfo } = require("../backend/riot_api"); // riot_api.js 파일의 경로를 적절히 수정

const {
  app,
  BrowserWindow,
  ipcMain,
  globalShortcut,
  screen,
} = require("electron");

const ipc = ipcMain;
const path = require("path");
let win;

const {
  SEND_MAIN_PING,
  SEND_WINDOW_MINIMIZE,
  SEND_WINDOW_MAXIMIZE,
  SEND_WINDOW_CLOSE,
} = require("./constants");

function createWindow() {
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

  ipcMain.on(SEND_MAIN_PING, async (event, arg) => {
    console.log("Main received a ping!!!");
    // 매치 ID를 적절히 변경
    const matchId = "KR_6926468313";
    getSummonerInfo(matchId)
      .then((apiInfo) => {
        console.log("main.js API complete");
      })
      .catch((error) => {
        console.error("error:", error);
      });
  });

  ipcMain.on(SEND_WINDOW_MINIMIZE, (event, arg) => {
    console.log("Main received a ping!!!");
    win.minimize();
  });

  ipcMain.on(SEND_WINDOW_MAXIMIZE, (event, arg) => {
    if (win.isMaximized()) {
      win.unmaximize();
    } else {
      win.maximize();
      //win.setFullScreen(!win.isFullScreen());
    }
  });

  ipcMain.on(SEND_WINDOW_CLOSE, (event, arg) => {
    win.close();
    globalShortcut.unregisterAll();
  });

  win.loadURL("http://localhost:3000");
}
app.whenReady().then(() => {
  createWindow();
});

app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});
