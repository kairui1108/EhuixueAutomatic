import sys
from PyInstaller.__main__ import run

if __name__ == '__main__':
    sys.setrecursionlimit(5000)
    opts = ['src/videos/AppGui.py',
            '-F',
            '--noconsole',
            '--name', 'ehx_video',
            '--add-data', 'ehuixue.ico;.',
            '--hidden-import',
            'pkg_resources.py2_warn',
            '-i', 'ehuixue.ico']
    run(opts)