##########config.py: 配置文件 ##################
# 变更记录: [2023-11-22 10:30] @李祥光 初始创建########
# 输入: 无 | 输出: 配置参数###############


###########################文件下的所有函数###########################
"""
无函数，仅包含配置参数
"""
###########################文件下的所有函数###########################

import os
import logging

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 日志配置
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
LOG_FILE = os.path.join(LOG_DIR, 'auto_like.log')

# 微信操作配置
WAIT_TIME = 2  # 操作间隔时间（秒）
MAX_RETRIES = 3  # 最大重试次数
RETRY_INTERVAL = 2  # 重试间隔（秒）

# 功能配置
AUTO_CLOSE_MOMENTS = False  # 点赞后是否自动关闭朋友圈窗口