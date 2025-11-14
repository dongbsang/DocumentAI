const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

let mainWindow;
let backendProcess;
let ollamaProcess;

// 리소스 경로 설정
const isDev = !app.isPackaged;
const resourcePath = isDev 
  ? path.join(__dirname, '..') 
  : process.resourcesPath;

console.log('Resource Path:', resourcePath);
console.log('Is Development:', isDev);

// 서버가 준비되었는지 확인하는 함수
function checkServerReady(url, maxAttempts = 30) {
  return new Promise((resolve) => {
    let attempts = 0;
    
    const check = () => {
      attempts++;
      console.log(`Checking server... Attempt ${attempts}/${maxAttempts}`);
      
      http.get(url, (res) => {
        if (res.statusCode === 200) {
          console.log('✅ Server is ready!');
          resolve(true);
        } else {
          if (attempts < maxAttempts) {
            setTimeout(check, 1000);
          } else {
            console.log('❌ Server check timeout');
            resolve(false);
          }
        }
      }).on('error', () => {
        if (attempts < maxAttempts) {
          setTimeout(check, 1000);
        } else {
          console.log('❌ Server check timeout');
          resolve(false);
        }
      });
    };
    
    check();
  });
}

// Ollama 시작
function startOllama() {
  return new Promise((resolve) => {
    const ollamaExe = process.platform === 'win32' ? 'ollama.exe' : 'ollama';
    const ollamaPath = isDev 
      ? path.join(resourcePath, 'ollama', ollamaExe)
      : path.join(resourcePath, 'ollama', ollamaExe);
    
    console.log('Starting Ollama:', ollamaPath);
    
    try {
      ollamaProcess = spawn(ollamaPath, ['serve'], {
        cwd: path.dirname(ollamaPath),
        env: {
          ...process.env,
          OLLAMA_MODELS: path.join(path.dirname(ollamaPath), 'models')
        },
        stdio: 'pipe'
      });

      ollamaProcess.stdout.on('data', (data) => {
        console.log(`[Ollama] ${data.toString().trim()}`);
      });

      ollamaProcess.stderr.on('data', (data) => {
        console.log(`[Ollama] ${data.toString().trim()}`);
      });

      ollamaProcess.on('error', (error) => {
        console.error('Ollama Error:', error);
      });

      ollamaProcess.on('close', (code) => {
        console.log(`Ollama exited with code ${code}`);
      });

      // Ollama가 시작되는데 시간이 필요하므로 대기
      setTimeout(() => {
        console.log('✅ Ollama started');
        resolve();
      }, 3000);
    } catch (error) {
      console.error('Failed to start Ollama:', error);
      resolve(); // 실패해도 계속 진행
    }
  });
}

// 백엔드 서버 시작
function startBackend() {
  return new Promise((resolve) => {
    const backendExe = process.platform === 'win32' ? 'backend.exe' : 'backend';
    const backendPath = isDev
      ? path.join(resourcePath, 'backend', 'dist', backendExe)
      : path.join(resourcePath, 'backend', backendExe);
    
    console.log('Starting backend:', backendPath);
    
    try {
      backendProcess = spawn(backendPath, [], {
        cwd: path.dirname(backendPath),
        env: {
          ...process.env,
          FLASK_ENV: 'production',
          OLLAMA_BASE_URL: 'http://localhost:11434',
          PORT: '5000'
        },
        stdio: 'pipe'
      });

      backendProcess.stdout.on('data', (data) => {
        console.log(`[Backend] ${data.toString().trim()}`);
      });

      backendProcess.stderr.on('data', (data) => {
        console.log(`[Backend] ${data.toString().trim()}`);
      });

      backendProcess.on('error', (error) => {
        console.error('Backend Error:', error);
      });

      backendProcess.on('close', (code) => {
        console.log(`Backend exited with code ${code}`);
      });

      // 백엔드 서버가 준비될 때까지 대기
      setTimeout(() => {
        console.log('✅ Backend started');
        resolve();
      }, 2000);
    } catch (error) {
      console.error('Failed to start Backend:', error);
      resolve();
    }
  });
}

// 로딩 윈도우 생성
function createLoadingWindow() {
  const loadingWindow = new BrowserWindow({
    width: 400,
    height: 300,
    frame: false,
    transparent: false,
    resizable: false,
    webPreferences: {
      nodeIntegration: true
    }
  });

  // 간단한 로딩 HTML 생성
  const loadingHTML = `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {
          margin: 0;
          padding: 0;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          color: white;
        }
        .container {
          text-align: center;
        }
        h1 {
          margin-bottom: 20px;
          font-size: 32px;
        }
        .spinner {
          border: 4px solid rgba(255,255,255,0.3);
          border-top: 4px solid white;
          border-radius: 50%;
          width: 50px;
          height: 50px;
          animation: spin 1s linear infinite;
          margin: 0 auto;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        p {
          margin-top: 20px;
          font-size: 14px;
          opacity: 0.9;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>📄 DocumentAI</h1>
        <div class="spinner"></div>
        <p>시작하는 중...</p>
      </div>
    </body>
    </html>
  `;

  loadingWindow.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(loadingHTML)}`);
  
  return loadingWindow;
}

// 메인 윈도우 생성
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    show: false // 로드 완료 후 보여주기
  });

  mainWindow.loadURL('http://localhost:5000');

  // 로드 완료 후 윈도우 표시
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // 개발 모드에서는 DevTools 자동 열기
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  return mainWindow;
}

// 앱 시작
app.whenReady().then(async () => {
  console.log('🚀 App is ready');
  
  // 로딩 화면 표시
  const loadingWindow = createLoadingWindow();
  
  try {
    // 1. Ollama 시작
    console.log('Starting Ollama...');
    await startOllama();
    
    // 2. 백엔드 시작
    console.log('Starting Backend...');
    await startBackend();
    
    // 3. 백엔드 서버가 준비될 때까지 대기
    console.log('Waiting for backend server...');
    const serverReady = await checkServerReady('http://localhost:5000', 30);
    
    if (serverReady) {
      // 4. 메인 윈도우 생성
      console.log('Creating main window...');
      createWindow();
      
      // 로딩 윈도우 닫기
      setTimeout(() => {
        if (loadingWindow && !loadingWindow.isDestroyed()) {
          loadingWindow.close();
        }
      }, 500);
    } else {
      console.error('❌ Failed to start backend server');
      loadingWindow.close();
      app.quit();
    }
  } catch (error) {
    console.error('Startup error:', error);
    loadingWindow.close();
    app.quit();
  }

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// 앱 종료 시 프로세스 정리
app.on('window-all-closed', () => {
  console.log('All windows closed');
  
  // 백엔드 종료
  if (backendProcess && !backendProcess.killed) {
    console.log('Killing backend process...');
    backendProcess.kill();
  }
  
  // Ollama 종료
  if (ollamaProcess && !ollamaProcess.killed) {
    console.log('Killing Ollama process...');
    ollamaProcess.kill();
  }

  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  console.log('App is quitting...');
  
  if (backendProcess && !backendProcess.killed) {
    backendProcess.kill('SIGTERM');
  }
  
  if (ollamaProcess && !ollamaProcess.killed) {
    ollamaProcess.kill('SIGTERM');
  }
});

app.on('quit', () => {
  console.log('App quit');
});

// 예외 처리
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
});

process.on('unhandledRejection', (error) => {
  console.error('Unhandled Rejection:', error);
});
