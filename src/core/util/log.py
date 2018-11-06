# encoding:utf8

# 多目标的记录日志
# debug 级别的详细记录到日志文件中
# info 级以上的级别记录到控制台中，控制台是否显示有开关

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/tmp/myapp.log',
    filemode='w'
)

# 定义日志处理器将INFO或者以上级别的日志发送到 sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# 设置控制台日志的格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
