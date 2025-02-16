import inspect
from projectdesposetool.systool.logger import Logger

# 获取Logger类的__init__方法对象
init_method = Logger.__init__

# 1. 使用inspect模块获取完整参数信息
argspec = inspect.getfullargspec(init_method)
print("参数详细信息:")
print(f"参数列表: {argspec.args}")
print(f"默认参数: {argspec.defaults}")
print(f"可变参数: {argspec.varargs}")
print(f"关键字参数: {argspec.varkw}")

# 2. 获取文档字符串
print("\n文档字符串:")
print(init_method.__doc__)

# 3. 查看方法属性
print("\n方法属性:")
print(dir(init_method))

# 4. 获取参数默认值
print("\n参数默认值:")
print(init_method.__defaults__)

# 5. 类型注解示例（需在代码中添加类型注解）
print("\n类型注解示例:")
if init_method.__annotations__:
    print(init_method.__annotations__)
else:
    print("该方法没有类型注解，示例格式：")
    print("{'name': str, 'log_file': str, 'level': int}")
