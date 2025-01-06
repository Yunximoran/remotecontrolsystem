
"""
初始化配置文件


配置：
通信端口？ 只通过服务器修改
操作系统
本机IP
本机MAC
软件安装位置 根目录
"""

import init
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class Sutep:
    def __init__(self, root):
        self.root = root
        self.root.title("安装程序")
        
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.file_path_var = tk.StringVar(value="请选择软件路径")
        
        self.create_widgets()
    
    def create_widgets(self):
        # 用户名标签和输入框
        username_label = tk.Label(self.root, text="用户名:")
        username_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        username_entry = tk.Entry(self.root, textvariable=self.username_var)
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # 密码标签和输入框
        password_label = tk.Label(self.root, text="用户密码:")
        password_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        
        password_entry = tk.Entry(self.root, textvariable=self.password_var, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # 软件路径标签和输入框
        file_path_label = tk.Label(self.root, text="安装路径")
        file_path_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        
        file_path_entry = tk.Entry(self.root, textvariable=self.file_path_var, state="readonly")
        file_path_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # 选择文件路径按钮
        browse_button = tk.Button(self.root, text="浏览", command=self.browse_file)
        browse_button.grid(row=2, column=2, padx=10, pady=10)
        
        
        
        # 安装按钮
        install_button = tk.Button(self.root, text="安装", command=self.install_software)
        install_button.grid(row=3, column=1, pady=20)
    
    def browse_file(self):
        file_path = filedialog.askdirectory(title="选择软件路径")
        if file_path:
            self.file_path_var.set(file_path)
    
    def install_software(self):
        username = self.username_var.get()
        password = self.password_var.get()
        file_path = self.file_path_var.get()
        
        if not username or not password or file_path == "请选择软件路径":
            messagebox.showwarning("输入错误", "请填写用户名、密码并选择软件路径")
            return
        
        # 这里可以添加安装逻辑
        init.Init(username, password)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Sutep(root)
    root.mainloop()


    