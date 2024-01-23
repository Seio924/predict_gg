const { app, BrowserWindow, ipcMain } = require("electron");

const ipc = ipcMain;
const path = require("path");

const {
  SEND_MAIN_PING,
  SEND_WINDOW_MINIMIZE,
  SEND_WINDOW_MAXIMIZE,
  SEND_WINDOW_CLOSE,
} = require("./constants");

function createWindow() {
  const win = new BrowserWindow({
    width: 1072,
    height: 659,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  ipcMain.on(SEND_MAIN_PING, (event, arg) => {
    console.log("Main received a ping!!!");
  });

  ipcMain.on(SEND_WINDOW_MINIMIZE, () => {
    mainWindow.minimize();
  });

  ipcMain.on(SEND_WINDOW_MAXIMIZE, () => {
    if (mainWindow.isMaximized()) {
      mainWindow.restore();
    } else {
      mainWindow.maximize();
    }
  });

  ipcMain.on(SEND_WINDOW_CLOSE, () => {
    mainWindow.close();
  });

  win.loadURL("http://localhost:3000");
}
app.whenReady().then(() => {
  createWindow();
});
app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});
