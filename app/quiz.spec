# -*- mode: python -*-

block_cipher = None


a = Analysis(['quiz.py'],
             pathex=['/Users/yuhki/git_hub/quiz'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='quiz',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='quiz.app',
             icon=None,
             info_plist={ 'NSHighResolutionCapable': 'True'},
             bundle_identifier=None)
