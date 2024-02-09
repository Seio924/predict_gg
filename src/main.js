const { app, BrowserWindow, ipcMain, globalShortcut, screen } = require("electron");
const path = require("path");
const { SEND_MAIN_PING, SEND_WINDOW_MINIMIZE, SEND_WINDOW_MAXIMIZE, SEND_WINDOW_CLOSE } = require("./constants");
const { getSummonerInfo } = require("../backend/riot_api"); // riot_api.js 파일의 경로를 적절히 수정
const axios = require('axios');

let win;
let overlayWindow;
let isOverlayCreated = false;

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

    ipcMain.on(SEND_MAIN_PING, async (event, arg) => {
        console.log('Button clicked!');

        try {
            const response = await axios.post('http://localhost:4000/', { data: 'hello' });
            console.log('server res:', response.data);
        } catch (error) {
            console.error('server error:', error);
        }
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
        }
    });

    ipcMain.on(SEND_WINDOW_CLOSE, (event, arg) => {
        win.close();
        globalShortcut.unregisterAll();
    });
}

async function createOverlay() {
    if (!isOverlayCreated) {
        const { width, height } = screen.getPrimaryDisplay().workAreaSize;
        const overlayWidth = 500;
        const overlayHeight = 100;
        const xPos = (width - overlayWidth) / 2;
        const yPos = 0;

        overlayWindow = new BrowserWindow({
            width: overlayWidth,
            height: overlayHeight,
            x: xPos,
            y: yPos,
            transparent: true,
            frame: false,
            resizable: false,
            alwaysOnTop: true,
        });

        overlayWindow.loadFile(path.join(__dirname, '../public/overlay.html'));
        //overlayWindow.loadURL("http://localhost:3000");
        overlayWindow.setIgnoreMouseEvents(true);

        isOverlayCreated = true;
    }
}

async function searchProcess(targetName) {
    const { default: psList } = await import('ps-list');
    const processes = await psList();
    const results = processes.filter((process) =>
        process.name.includes(targetName)
    );
    return results.length > 0 ? results : null;
}

app.whenReady().then(() => {
    createWindow();
    setInterval(async () => {
        const foundProcess = await searchProcess('LeagueClient.exe');
        if (foundProcess) {
            if (!overlayWindow) {
                createOverlay();
            }
        } else {
            if (overlayWindow) {
                overlayWindow.close();
                overlayWindow = null;
            }
        }
    }, 5000);
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
