import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["base64", "json", "time", "requests", "selenium", "logging", "sqlite3"],
                     "include_files": ["chromedriver"]}
# 打包可能缺依赖

setup(name="app",
      version="0.1",
      description="Description of my program",
      options={"build_exe": build_exe_options},
      install_requires=['rich'],
      executables=[Executable("MainAppGui.py", base=None)])
