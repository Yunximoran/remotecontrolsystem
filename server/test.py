from multiprocessing import Process

#自定义类
class MyProcess(Process):

	def __init__(self,value):
		self.value = value
		#自己写__init__(self)会将父类的__init__覆盖，为了不丢失父类的一些属性，需要用super()加载
		super().__init__()

	def f1(self):
		print('步骤1')

	def f2(self):
		print('步骤2')
	
	#run()是Process类专门留出来让你重写的接口函数
	def run(self):
		self.f1()
		self.f2()
if __name__ == "__main__":
    p = MyProcess(2)
    #start()和join()都是从父类中继承过来的
    #调用start(）自动执行run(),将f1()和f2()作为子进程执行
    p.start()
    p.join()
