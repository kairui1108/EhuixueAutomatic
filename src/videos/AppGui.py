import time

import src.videos.app
from src.exercises.config import config as exercise_config
from src.exercises.ckGetter import CkGetter
from src.videos.app import *
from src.exercises.helper import Helper
import logging
import tkinter as tk
from tkinter import ttk
import threading


class VideoApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.course_dict = {}
        self.course_list = ["点击获取在学课程"]
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

        self.label3 = ttk.Label(input_frame, text="课程")
        self.label3.pack(side="top", padx=10, pady=5)

        selected_option = tk.StringVar(value=self.course_list[0])
        self.entry3 = ttk.Combobox(input_frame, values=self.course_list, textvariable=selected_option, state='readonly')
        self.entry3.bind("<<ComboboxSelected>>", self.get_course)
        self.entry3.pack(side="top", padx=10, pady=5)

        input_frame2 = tk.LabelFrame(input_frame, text="验证码api（可选）针对有验证码识别的课程")
        input_frame2.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        tk.Label(input_frame2, text="uname").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.input7 = tk.Entry(input_frame2)
        self.input7.grid(row=2, column=1, padx=5, pady=5)
        self.input7.insert(1, config["uname"])
        tk.Label(input_frame2, text="pwd").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.input8 = tk.Entry(input_frame2)
        self.input8.grid(row=3, column=1, padx=5, pady=5)
        self.input8.insert(1, config["api_pwd"])

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
        self.run_button = ttk.Button(button_frame, text="开始", command=self.handle_run)
        self.run_button.pack(side="right", padx=10, pady=5)
        self.time_button = ttk.Button(button_frame, text="常用时间", command=self.handle_time)
        self.time_button.pack(side="right", padx=10, pady=5)
        # self.confirm_button.pack(side="top", fill="both", padx=10, pady=5)

    def handle_run(self):
        if not self.get_config():
            return

        if config['cid'] == 0:
            self.logger.error("请选择一门课程")
            return

        video_task = threading.Thread(target=src.videos.app.main, args=("win", config['phone'], config['pwd'], config['cid']))
        video_task.start()

    def get_config(self):
        # 获取输入框中的数据
        config['phone'] = self.entry1.get()
        config['pwd'] = self.entry2.get()

        if not self.valid():
            return False

        return True

    def valid(self):
        if len(config['phone']) != 11:
            self.logger.error("账号有误")
            return False

        if not (config['pwd']):
            self.logger.error("输入非法，请检查密码是否输入为空......")
            return False

        return True

    def get_course(self, event):
        option = self.entry3.get()
        if option != "点击获取在学课程":
            config["cid"] = self.course_dict[option]
            return
        src.exercises.helper.loger = self.logger
        config['phone'] = self.entry1.get()
        config['pwd'] = self.entry2.get()
        exercise_config['todo_user']['phone'] = self.entry1.get()
        exercise_config['todo_user']['pwd'] = self.entry2.get()

        if not self.valid():
            return
        self.course_list = []
        courses = Helper(config['phone']).get_study_course()
        for course in courses:
            name = course["coursename"]
            self.course_list.append(name)
            self.course_dict[name] = course["cid"]
        self.entry3.configure(values=self.course_list)
        self.logger.info("获取所有在学课程成功, 请点击选择一门课程")

    def handle_time(self):
        if not self.get_config():
            return
        helper = Helper(config["phone"])
        helper.get_ban_data(config["cid"])
        while not helper.is_available(config["cid"]):
            self.logger.error("当前不在常用时间段内")
            time.sleep(300)
        self.handle_run()


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
