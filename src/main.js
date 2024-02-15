const { app, BrowserWindow, ipcMain, globalShortcut, screen } = require("electron");
const path = require("path");
const { SEND_MAIN_PING, SEND_WINDOW_MINIMIZE, SEND_WINDOW_MAXIMIZE, SEND_WINDOW_CLOSE } = require("./constants");
const axios = require('axios');

let win;
let overlayWindow;
let isOverlayCreated = false;
let ignoreMouseEvents = false;

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
        console.log('File uploaded in Renderer process!');
        console.log('Uploaded file name:', arg.fileName);

        try {
            const response = await axios.post('http://localhost:4000/', { data: arg.fileName });
            console.log('server res:', response.data);
        } catch (error) {
            console.error('server error:', error);
        }
    });

    ipcMain.on(SEND_WINDOW_MINIMIZE, (event, arg) => {
        // console.log("Main received a ping!!!");
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
        const overlayWidth = 180;
        const overlayHeight = 80;
        const xPos = width - overlayWidth - 20;
        const yPos = 10;

        overlayWindow = new BrowserWindow({
            width: overlayWidth,
            height: overlayHeight,
            x: xPos,
            y: yPos,
            frame: false,
            resizable: false,
            alwaysOnTop: true,
        });

        // if (ignoreMouseEvents) {
        //     overlayWindow.setIgnoreMouseEvents(true);
        // }

        // 포커스를 계속 유지하도록 설정
        overlayWindow.on('blur', () => {
            overlayWindow.focus();
        });

        overlayWindow.loadFile(path.join(__dirname, '../public/overlay.html'));

        // 렌더러 프로세스로부터 'start-overlay' 메시지를 수신하여 시작하기 버튼 클릭 이벤트를 처리합니다.
        ipcMain.on('start-overlay', () => {
            startOverlay();
        });

        
        isOverlayCreated = true;
    }
    else {
        // 오버레이 창이 이미 생성되었을 경우, 다시 최상위로 설정
        overlayWindow.setAlwaysOnTop(true);
        overlayWindow.focus();
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

// 시작하기 버튼을 누르면 마우스 이벤트를 무시하도록 설정
async function startOverlay() {
    ignoreMouseEvents = true;
    if (overlayWindow) {
        overlayWindow.setIgnoreMouseEvents(true);
    }
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
                isOverlayCreated = false;
            }
        }
    }, 5000);
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
