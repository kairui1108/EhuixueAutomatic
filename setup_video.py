import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["base64", "json", "time", "requests", "selenium", "logging"],
                     "include_files": ["chromedriver"]}

base = 'Win32GUI' if sys.platform == 'win32' else None

setup(name="video",
      version="0.1",
      description="Description of my program",
      options={"build_exe": build_exe_options},
      install_requires=['rich'],
      executables=[Executable("src/videos/AppGui.py", base=base)])
