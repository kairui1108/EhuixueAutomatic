import tkinter as tk
from threading import Thread

import src.exercises.main
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

        self.quit_button = None
        self.clear_button = None
        self.run_button = None
        self.input1 = None
        self.input2 = None
        self.input3 = None
        self.input4 = None
        self.input5 = None
        self.input6 = None
        self.input7 = None
        self.input8 = None
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # 创建框架
        input_frame = tk.Frame(self.master)
        input_frame.pack(side=tk.TOP, padx=5, pady=5)

        # 创建输入框框架
        input_frame1 = tk.LabelFrame(input_frame, text="小白鼠信息")
        input_frame1.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        tk.Label(input_frame1, text="phone:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.input1 = tk.Entry(input_frame1)
        self.input1.grid(row=0, column=1, padx=5, pady=5)
        self.input1.insert(1, config["pioneer"]["phone"])
        tk.Label(input_frame1, text="pwd:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.input2 = tk.Entry(input_frame1)
        self.input2.grid(row=1, column=1, padx=5, pady=5)
        self.input2.insert(1, config["pioneer"]["pwd"])

        input_frame2 = tk.LabelFrame(input_frame, text="todo_user信息")
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
        tk.Label(input_frame3, text="start_eid:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.input5 = tk.Entry(input_frame3)
        self.input5.grid(row=0, column=1, padx=5, pady=5)
        self.input5.insert(1, config["exercise"]["start_eid"])
        tk.Label(input_frame3, text="end_eid:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.input6 = tk.Entry(input_frame3)
        self.input6.grid(row=1, column=1, padx=5, pady=5)
        self.input6.insert(1, config["exercise"]["end_eid"])

        input_frame4 = tk.LabelFrame(input_frame, text="验证码api")
        input_frame4.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        tk.Label(input_frame4, text="api_name(可选）").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.input7 = tk.Entry(input_frame4)
        self.input7.grid(row=2, column=1, padx=5, pady=5)
        self.input7.insert(1, config["api"]["uname"])
        tk.Label(input_frame4, text="api_pwd(可选）").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.input8 = tk.Entry(input_frame4)
        self.input8.grid(row=3, column=1, padx=5, pady=5)
        self.input8.insert(1, config["api"]["pwd"])

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
        config['exercise']['start_eid'] = self.input5.get()
        config['exercise']['end_eid'] = self.input6.get()
        config['api']['uname'] = self.input7.get()
        config['api']['pwd'] = self.input8.get()

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
    app.mainloop()
