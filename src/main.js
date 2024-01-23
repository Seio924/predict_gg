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

  ipc.on(SEND_WINDOW_MINIMIZE, () => {
    mainWindow.minimize();
  });

  ipc.on(SEND_WINDOW_MAXIMIZE, () => {
    if (mainWindow.isMaximized()) {
      mainWindow.restore();
    } else {
      mainWindow.maximize();
    }
  });

  ipc.on(SEND_WINDOW_CLOSE, () => {
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
