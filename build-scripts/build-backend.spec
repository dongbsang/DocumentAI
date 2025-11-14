# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# 현재 spec 파일이 있는 경로에서 backend 경로 계산
# spec 파일 위치: build-scripts/build-backend.spec
# backend 위치: backend/
spec_root = os.path.abspath(SPECPATH)
project_root = os.path.dirname(spec_root)
backend_root = os.path.join(project_root, 'backend')

a = Analysis(
    [os.path.join(backend_root, 'app', 'main.py')],
    pathex=[backend_root],
    binaries=[],
    datas=[
        (os.path.join(backend_root, 'app'), 'app'),
        (os.path.join(backend_root, '.env'), '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'werkzeug',
        'werkzeug.security',
        'jinja2',
        'click',
        'itsdangerous',
        'markupsafe',
        'blinker',
        'python-dotenv',
        'dotenv',
        'langchain_ollama',
        'langchain_core',
        'langchain_community',
        'langchain_text_splitters',
        'langsmith',
        'pytesseract',
        'easyocr',
        'pdfplumber',
        'fitz',  # PyMuPDF
        'PyMuPDF',
        'docx',
        'python-docx',
        'olefile',
        'chardet',
        'PIL',
        'pillow',
        'cv2',
        'numpy',
        'faiss',
        'sentence_transformers',
        'torch',
        'transformers',
        'httpx',
        'requests',
        'yaml',
        'PyYAML',
        'pyhwp',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'scipy',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Flask 로그를 보려면 True, 배포 시 False로 변경 가능
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 아이콘 파일 경로 추가 가능
)
