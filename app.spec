# -*- mode: python ; coding: utf-8 -*-
#
# PRODUCTION NOTE: This spec bundles `.env` into the executable.
# Before building a release, set ENVIRONMENT=production and all required
# env keys with real production values in `.env`, then run:
#   pyinstaller app.spec
#
# NEVER commit `.env` to version control — keep it in .gitignore.


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('src/assets', 'src/assets'), ('.env', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    onefile=True,
)
