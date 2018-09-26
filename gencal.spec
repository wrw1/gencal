# -*- mode: python -*-

block_cipher = None

my_datas = [
    ('Icons/*', 'Icons'),
    ('CREDITS.txt', '.'),
    ('dither_img.nc', '.'),
    ('help.html', '.'),
    ('NEWS.txt', '.'),
    ('README.txt', '.'),
    ('TODO.txt', '.')
    ]

a = Analysis(['gencal.py'],
             pathex=['/home/wrw/python/gencal'],
             binaries=[],
             datas=my_datas,
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
          name='gencal',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
