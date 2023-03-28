from src.videos.app import *
import logging
import tkinter as tk
from tkinter import ttk
import threading


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.version = "v1.0"
        self.author = "ruikai"

        self.title("e会学-杀手" + self.version)

        # 创建三个输入框和一个日志输出框
        self.label1 = ttk.Label(self, text="账号")
        self.entry1 = ttk.Entry(self)
        self.label2 = ttk.Label(self, text="密码")
        self.entry2 = ttk.Entry(self)
        self.label3 = ttk.Label(self, text="课程cid")
        self.entry3 = ttk.Entry(self)
        self.log_text = tk.Text(self, state="disabled", width=50, height=10)
        self.log_text.tag_configure("INFO", foreground="black")
        self.log_text.tag_configure("WARNING", foreground="orange")
        self.log_text.tag_configure("ERROR", foreground="red")

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

        # 绑定按钮的事件处理函数
        # self.bind("<Return>", self.handle_submit)
        # 添加确认按钮并绑定事件处理函数
        self.confirm_button = ttk.Button(self, text="开始", command=self.handle_submit)
        self.confirm_button.pack(side="top", padx=10, pady=5)

    def handle_submit(self):
        # 获取输入框中的数据
        account = self.entry1.get()
        password = self.entry2.get()
        cid = self.entry3.get()

        if len(account) != 11:
            self.logger.error("账号有误")
            return

        if not (account and password):
            self.logger.error("输入非法，请检查是否输入为空......")
            return

        # 输出日志
        self.logger.info(f"账号 : {account}")
        self.logger.warning(f"密码 : {password}")
        self.logger.error(f"课程cid : {cid}")

        video_task = threading.Thread(target=main, args=("win", account, password, cid))
        video_task.start()

        # 清空输入框
        # self.entry1.delete(0, "end")
        # self.entry2.delete(0, "end")
        # self.entry3.delete(0, "end")


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
    app = Application()
    logging = app.logger
    app.mainloop()
