import ast
import tkinter as tk
from tkinter import ttk
from threading import Thread

import src.exercises.main
from src.exercises.saveInfo import Client
from src.exercises.ckGetter import CkGetter
from src.exercises.helper import Helper
from src.exercises.main import *
import logging


def is_any_blank(*args):
    for item in args:
        if item is None:
            return True
    return False


class PostmanApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.course_list = ["点击获取在学课程"]
        self.course_dict = {}
        self.work_list = []
        self.work_dict = {}
        self.is_pioneer_login = False
        self.combo = None
        self.quit_button = None
        self.clear_button = None
        self.run_button = None
        self.input1 = None
        self.input2 = None
        self.input3 = None
        self.input4 = None
        self.input5 = None
        self.input6 = None
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # 创建框架
        input_frame = tk.Frame(self.master)
        input_frame.pack(side=tk.TOP, padx=5, pady=5)

        # 创建输入框框架
        input_frame1 = tk.LabelFrame(input_frame, text="小白鼠信息，用于获取正确答案")
        input_frame1.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        tk.Label(input_frame1, text="phone:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.input1 = tk.Entry(input_frame1)
        self.input1.grid(row=0, column=1, padx=5, pady=5)
        self.input1.insert(1, config["pioneer"]["phone"])
        tk.Label(input_frame1, text="pwd:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.input2 = tk.Entry(input_frame1)
        self.input2.grid(row=1, column=1, padx=5, pady=5)
        self.input2.insert(1, config["pioneer"]["pwd"])

        input_frame2 = tk.LabelFrame(input_frame, text="todo_user信息，需要刷题的用户")
        input_frame2.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        tk.Label(input_frame2, text="phone:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.input3 = tk.Entry(input_frame2)
        self.input3.grid(row=0, column=1, padx=5, pady=5)
        self.input3.insert(1, config["todo_user"]["phone"])
        tk.Label(input_frame2, text="pwd:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.input4 = tk.Entry(input_frame2)
        self.input4.grid(row=1, column=1, padx=5, pady=5)
        self.input4.insert(1, config["todo_user"]["pwd"])

        input_frame3 = tk.LabelFrame(input_frame, text="作业信息")
        input_frame3.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        tk.Label(input_frame3, text="开始:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.input5 = ttk.Combobox(input_frame3, values=self.work_list, state='readonly')
        self.input5.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(input_frame3, text="结束:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.input6 = ttk.Combobox(input_frame3, values=self.work_list, state='readonly')
        self.input6.grid(row=1, column=1, padx=5, pady=5)

        selected_option = tk.StringVar(value=self.course_list[0])
        self.combo = ttk.Combobox(input_frame3, values=self.course_list, textvariable=selected_option, state='readonly')
        self.combo.bind("<<ComboboxSelected>>", self.get_course)
        tk.Label(input_frame3, text="课程:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.combo.grid(row=2, column=1, padx=5, pady=5)

        # 创建日志输出框
        log_frame = tk.LabelFrame(input_frame, text="日志输出")
        log_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        self.log_text = tk.Text(log_frame, state="disabled", width=50, height=10)
        self.log_text.tag_configure("INFO", foreground="black")
        self.log_text.tag_configure("WARNING", foreground="orange")
        self.log_text.tag_configure("ERROR", foreground="red")
        self.log_text.pack(padx=5, pady=5)

        # 创建并配置logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(GUITextHandler(self.log_text))

        src.exercises.main.log = self.logger

        # 创建按钮Frame
        button_frame = tk.Frame(self.master)
        button_frame.pack(side=tk.TOP, padx=5, pady=5)

        # 创建按钮
        self.run_button = tk.Button(button_frame, text="获取正确答案", command=self.get_pioneer_ans)
        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.clear_button = tk.Button(button_frame, text="运行", command=self.run)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.quit_button = tk.Button(button_frame, text="退出", command=self.quit)
        self.quit_button.pack(side=tk.LEFT, padx=5, pady=5)

    def get_pioneer_ans(self):
        config['pioneer']['phone'] = self.input1.get()
        config['pioneer']['pwd'] = self.input2.get()
        self.get_eid()

        if is_any_blank(config['pioneer']['phone'], config['pioneer']['pwd'], config['exercise']['start_eid'], config['exercise']['end_eid']):
            self.logger.error("请检查参数，是否输入正确")
            return

        ans_task = Thread(target=src.exercises.main.get_ans)
        ans_task.start()

    def run(self):
        config['todo_user']['phone'] = self.input3.get()
        config['todo_user']['pwd'] = self.input4.get()

        run_task = Thread(target=run_post, args=())
        run_task.start()

    def get_course(self, *args):
        src.exercises.helper.loger = self.logger
        option = self.combo.get()
        if option == "点击获取在学课程":
            self.get_course_list()
        else:
            self.get_course_work()

    def get_course_list(self):
        if not self.is_pioneer_login:
            config['pioneer']['phone'] = self.input1.get()
            config['pioneer']['pwd'] = self.input2.get()
            CkGetter(config["pioneer"]["phone"], config["pioneer"]["pwd"], self.logger).post_login("pioneer")
            self.is_pioneer_login = True
        helper = Helper('pioneer')
        # helper.get_detail()
        self.course_list = []
        courses = helper.get_study_course()
        for course in courses:
            name = course["coursename"]
            self.course_list.append(name)
            self.course_dict[name] = course["cid"]
        self.combo.configure(values=self.course_list)
        self.logger.info("获取所有在学课程成功, 请点击选择一门课程")

    def get_course_work(self):
        course_name = self.combo.get()
        cid = self.course_dict[course_name]
        self.logger.info("开始获取{}的作业题".format(course_name))
        self.work_list = []
        work_cache = Client().get_works(cid)
        work_list = []
        if work_cache is not None:
            work_list = ast.literal_eval(work_cache[3])
        else:
            helper = Helper('pioneer')
            work_list = helper.get_detail(cid)
        for work in work_list:
            work_name = work["name"]
            work_eid = work["eid"]
            self.work_list.append(work_name)
            self.work_dict[work_name] = work_eid
        self.input5.configure(values=self.work_list)
        self.input6.configure(values=self.work_list)
        self.logger.info("获取课程{}习题成功, 请点击选择需要完成的作业题".format(course_name))

    def get_eid(self):
        start_eid = self.work_dict[str(self.input5.get())]
        end_eid = self.work_dict[str(self.input6.get())]
        if int(start_eid) > int(end_eid):
            temp = start_eid
            start_eid = end_eid
            end_eid = temp
        config["exercise"]["start_eid"] = start_eid
        config["exercise"]["end_eid"] = end_eid


class GUITextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", self.format(record) + "\n", record.levelname)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")


if __name__ == '__main__':
    root = tk.Tk()
    app = PostmanApplication(master=root)
    src.exercises.helper.loger = app.logger
    app.mainloop()
