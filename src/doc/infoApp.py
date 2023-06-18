from tkinter import *
from src.doc.info import msg
from tkinter.scrolledtext import ScrolledText


class InfoApplication(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.text = ScrolledText(self.master, state=DISABLED)
        self.text.pack(fill=BOTH, expand=YES)
        self.render()

    def render(self):

        self.text.configure(state=NORMAL)  # 设置为可编辑，以便插入文本
        self.text.insert(END, msg)
        self.text.configure(state=DISABLED)

        # 为文本添加样式
        self.text.tag_configure("bold", font=("宋体", 16, "bold"), foreground="#6882f2")
        self.text.tag_configure("italic", font=("Times", 14, "italic"), foreground="#0000FF")
        self.text.tag_configure("underline", font=("Verdana", 16), foreground="#6882f2", underline=True)

        # 应用样式到文本
        self.text.tag_add("underline", "1.0", "5.0")
        self.text.tag_add("italic", "5.0", "11.0")
        self.text.tag_add("bold", "12.0", "17.0")


if __name__ == "__main__":
    root = Tk()
    info_app = InfoApplication(root)
    info_app.pack(fill=BOTH, expand=YES)
    root.mainloop()
