import tkinter

class _BaseUI:
    def __init__(self, title):
        self.win = tkinter.Tk()
        
        # 设置标题
        self.win.title(title)
    
    
    def runing(self):
        self.win.mainloop()
        


if __name__ == "__main__":
    ui = _BaseUI("test")
    ui.runing()