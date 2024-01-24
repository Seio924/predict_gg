
const { getSummonerInfo } = require("../backend/riot_api");  // riot_api.js 파일의 경로를 적절히 수정

const { app, BrowserWindow, ipcMain, webContents } = require("electron");

const ipc = ipcMain;
const path = require("path");
let win;

const {
  SEND_MAIN_PING,
  SEND_WINDOW_MINIMIZE,
  SEND_WINDOW_MAXIMIZE,
  SEND_WINDOW_CLOSE,
  DEFAULT_WINDOW,
  MAX_WINDOW,
} = require("./constants");

function createWindow() {
  win = new BrowserWindow({
    width: 1072,
    height: 659,
    frame: false,
    resizable: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  ipcMain.on(SEND_MAIN_PING, async (event, arg) => {
    console.log("Main received a ping!!!");
    // 매치 ID를 적절히 변경
    const matchId = 'KR_6916408053';
    getSummonerInfo(matchId)
  .then((apiInfo) => {
    console.log('main.js API complete');
  })
  .catch((error) => {
    console.error('error:', error);
  });
  });

  ipcMain.on(SEND_WINDOW_MINIMIZE, (event, arg) => {
    console.log("Main received a ping!!!");
    win.minimize();
  });

  ipcMain.on(SEND_WINDOW_MAXIMIZE, (event, arg) => {
    if (win.isMaximized()) {
      win.restore();
      win.webContents.send(DEFAULT_WINDOW, "message");
    } else {
      win.maximize();
      win.webContents.send(MAX_WINDOW, "message");
    }
  });

  ipcMain.on(SEND_WINDOW_CLOSE, (event, arg) => {
    win.close();
  });

  win.loadURL("http://localhost:3000");
}
app.whenReady().then(() => {
  createWindow();
});


app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});
