import sys
from PyInstaller.__main__ import run

if __name__ == '__main__':
    sys.setrecursionlimit(5000)
    opts = ['src/exercises/gui.py',
            '-F',
            '--noconsole',
            '--name', 'ehx作业',
            '--add-data', 'ehuixue.ico;.',
            '--hidden-import',
            'pkg_resources.py2_warn',
            '-i', 'ehuixue.ico']
    run(opts)
