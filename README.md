# DeepLog
极简的深度学习日志记录工具

[简易文档](https://www.mdnice.com/writing/51a2c557ad504acc8f8e036d1c79759c)

# 安装
1. 下载源码

开源地址：https://github.com/MacroHongZ/DeepLog

2. 本地安装
```python
# 需先进入源码文件夹
python setup.py install
```
3. 查看安装
```python
pip list
# 可以看到包名 deeplog
```
# 主要功能


```python
from deeplog import DeepLog, Config

# 初始化
Log = DeepLog(save_path="path") # the 'save_path' parameter sets the parent directory where the log files are saved.
config = Config()

# 配置模型超参数
config.lr = 0.01
config.bathch_size = 50
config.epoch = 100

# 打印模型超参数
config.print_parameters()
'''
lr :  0.01
bathch_size :  50
epoch :  100
'''

# 记录日志,记录 loss 和 metrics 等重要信息
for i in range(50):    
    Log.log("loss", i)
    Log.log("Acc", (i*0.5)**2)
    
# 基于 Elegant-Plot（https://github.com/MacroHongZ/Elegant-Plot） 的可视化
Log.visualization(item="loss")
'''
item: 默认值 all，字符串，会将记录的所有信息可视化。也可以指定可视化项目。
Log.get_log_keys() 可以查看所有记录的项目
'''

# 保存日志
Log.save(config=config, config_save=True)
'''
config: 默认值 None，需传入 Config 对象，传入后会在日志中记录超参数。
config_save：默认值 False，布尔对象。值为 True 会单独存储超参数，用于之后加载复现结果。
'''

# 从文件加载超参数，用于复现结果
config = Log.load_config("2022-09-02_13-11-17config.pickle")
config.print_parameters()

# 重新解析log文件，用于绘图
Log.load_logs('MyProject_log//2022-09-13_14-54-56log.txt')
Log.visualization(item="loss")
```

# 日志展示

![](https://files.mdnice.com/user/13441/2aaf7255-1020-40d2-8bcd-a4ebba31fb36.png)

![](https://files.mdnice.com/user/13441/4eadc9c3-468a-4fbb-8eb4-1d34d7a54ad0.png)

# 绘图展示

![](https://files.mdnice.com/user/13441/a8d59bc9-dd4f-443b-ac78-054f0bfc831e.png)

