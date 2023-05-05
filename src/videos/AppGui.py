import src.videos.app
from src.videos.app import *
import logging
import tkinter as tk
from tkinter import ttk
import threading


class VideoApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.version = config['version']
        self.author = "ruikai"

        # 创建三个输入框和一个日志输出框
        input_frame = ttk.LabelFrame(self, text="输入框")
        input_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        self.label1 = ttk.Label(input_frame, text="账号")
        self.label1.pack(side="top", padx=10, pady=5)
        self.entry1 = ttk.Entry(input_frame)
        self.entry1.pack(side="top", padx=10, pady=5)

        self.label2 = ttk.Label(input_frame, text="密码")
        self.label2.pack(side="top", padx=10, pady=5)
        self.entry2 = ttk.Entry(input_frame)
        self.entry2.pack(side="top", padx=10, pady=5)

        self.label3 = ttk.Label(input_frame, text="课程cid")
        self.label3.pack(side="top", padx=10, pady=5)
        self.entry3 = ttk.Entry(input_frame)
        self.entry3.pack(side="top", padx=10, pady=5)

        log_frame = ttk.LabelFrame(input_frame, text="日志输出")
        log_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        self.log_text = tk.Text(log_frame, state="disabled", width=50, height=10)
        self.log_text.tag_configure("INFO", foreground="black")
        self.log_text.tag_configure("WARNING", foreground="orange")
        self.log_text.tag_configure("ERROR", foreground="red")
        self.log_text.pack(side="top", padx=10, pady=5)

        # 将控件布局到界面中
        self.label1.pack()
        self.entry1.pack(side="top", padx=10, pady=5)
        self.label2.pack()
        self.entry2.pack(side="top", padx=10, pady=5)
        self.label3.pack()
        self.entry3.pack(side="top", padx=10, pady=5)
        self.log_text.pack(side="top", padx=10, pady=5)

        # 创建并配置logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(GUITextHandler(self.log_text))

        src.videos.app.log = self.logger

        # 绑定按钮的事件处理函数
        # self.bind("<Return>", self.handle_submit)
        # 添加确认按钮并绑定事件处理函数
        button_frame = ttk.Frame(log_frame)
        button_frame.pack(side="bottom", padx=10, pady=10, fill="x")

        self.exit_button = ttk.Button(button_frame, text="退出", command=self.quit)
        self.exit_button.pack(side="right", padx=10, pady=5)
        self.confirm_button = ttk.Button(button_frame, text="开始", command=self.handle_submit)
        self.confirm_button.pack(side="right", padx=10, pady=5)
        # self.confirm_button.pack(side="top", fill="both", padx=10, pady=5)

    def handle_submit(self):
        # 获取输入框中的数据
        config['phone'] = self.entry1.get()
        config['pwd'] = self.entry2.get()
        config['cid'] = self.entry3.get()

        if len(config['phone']) != 11:
            self.logger.error("账号有误")
            return

        if not (config['phone'] and config['pwd']):
            self.logger.error("输入非法，请检查是否输入为空......")
            return

        # 输出日志
        # self.logger.info(f"账号 : {config['phone']}")
        # self.logger.warning(f"密码 : {config['pwd']}")
        # self.logger.error(f"课程cid : {config['cid']}")

        video_task = threading.Thread(target=src.videos.app.main, args=("win", config['phone'], config['pwd'], config['cid']))
        video_task.start()


class GUITextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", self.format(record) + "\n", record.levelname)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApplication(master=root)
    app.pack()
    app.mainloop()
