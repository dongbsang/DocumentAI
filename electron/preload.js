const { contextBridge, ipcRenderer } = require('electron');

// 보안을 위해 제한된 API만 노출
contextBridge.exposeInMainWorld('electronAPI', {
  // Electron 버전 정보
  getVersion: () => process.versions.electron,
  
  // 플랫폼 정보
  getPlatform: () => process.platform,
  
  // 나중에 필요한 API 추가 가능
  // 예: 파일 다이얼로그, 시스템 정보 등
});
