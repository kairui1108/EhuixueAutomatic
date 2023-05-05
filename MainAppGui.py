import tkinter as tk
from tkinter import ttk

from src.exercises.gui import PostmanApplication
from src.videos.AppGui import VideoApplication


if __name__ == '__main__':

    root = tk.Tk()
    root.title("e会学工具箱")
    root.geometry("400x650")

    # 创建 Notebook 控件
    notebook = ttk.Notebook(root)

    # 创建三个 tab
    video_tab = ttk.Frame(notebook)
    notebook.add(video_tab, text="e会学视频")

    postman_tab = ttk.Frame(notebook)
    notebook.add(postman_tab, text="e会学作业")

    # 将 VideoApplication 和 PostmanApplication 添加到对应的 tab 中
    video_app = VideoApplication(video_tab)
    video_app.pack()

    postman_app = PostmanApplication(postman_tab)
    postman_app.pack()

    notebook.pack(expand=True, fill="both")

    root.mainloop()
