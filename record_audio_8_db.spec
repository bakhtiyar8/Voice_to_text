# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

a = Analysis(
    ['record_audio_8_db.py'],
    pathex=['.'],
    datas=[('.', 'vosk')],  # Include the entire 'vosk' directory
    hiddenimports=['vosk'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='record_audio_8_db',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='record_audio_8_db',
)

#pyinstaller record_audio_8_db.spec
