# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Ragner\\Ragner.py'],
    pathex=[],
    binaries=[],
    datas=[('Ragner', 'Ragner'), ('documentos', 'documentos'), ('faiss_index', 'faiss_index')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'PyQt5', 'scipy', 'pandas', 'PIL', 'notebook', 'IPython', 'tkinter', 'PySide2'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Ragner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
