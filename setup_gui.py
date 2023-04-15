import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["logging", "tkinter", "base64", "json", "threading", "time", "requests", "selenium", "pyaml"],
    "include_files": ["chromedriver"] # 将chromedriver.exe文件包括在打包后的应用程序中
}

base = None
if sys.platform == "win32":
    base = None # 隐藏控制台窗口

setup(
    name="AppGui",
    version="1.0",
    description="video automatic for ehuixue",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/videos/AppGui.py", base=base)]
)
