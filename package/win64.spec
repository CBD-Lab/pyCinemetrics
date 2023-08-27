# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['../src/main.py'],
    pathex=[],
    binaries=[
        ('../native/vlc-3.0.18-win64/', '.')
    ],
    datas=[
        ('../resources/', 'resources/')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

splash = Splash('../resources/splash.png',
                binaries=a.binaries,
                datas=a.datas,
                text_pos=(20, 450),
                text_size=12,
                text_color='white')

exe = EXE(
    pyz,
    a.scripts,
    splash,
    splash.binaries,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../resources/icon.ico'
)
