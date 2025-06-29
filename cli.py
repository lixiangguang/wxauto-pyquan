##########cli.py: 命令行参数处理 ##################
#  变更记录: [2023-11-22 10:45] @李祥光 初始创建########
#输入: 命令行参数 | 输出: 解析后的参数对象###############


###########################文件下的所有函数###########################
"""
parse_args: 解析命令行参数
get_args: 获取解析后的参数
"""
###########################文件下的所有函数###########################

import argparse
import logging

"""
parse_args 功能说明:
解析命令行参数
输入: 无 | 输出: 解析后的参数对象
"""
def parse_args():
    parser = argparse.ArgumentParser(description='微信朋友圈自动点赞工具')
    
    # 基本选项
    parser.add_argument('--debug', action='store_true', help='启用调试模式（详细日志）')
    parser.add_argument('--no-close', action='store_true', help='操作后不关闭朋友圈窗口')
    
    # 高级选项
    parser.add_argument('--wait-time', type=int, help='操作间隔时间（秒）')
    parser.add_argument('--max-retries', type=int, help='最大重试次数')
    parser.add_argument('--retry-interval', type=int, help='重试间隔（秒）')
    parser.add_argument('--log-file', type=str, help='指定日志文件路径')
    
    return parser.parse_args()


"""
get_args 功能说明:
获取解析后的参数，并更新配置
输入: 无 | 输出: 解析后的参数对象和更新后的配置
"""
def get_args():
    args = parse_args()
    config_updates = {}
    
    # 处理调试模式
    if args.debug:
        config_updates['LOG_LEVEL'] = logging.DEBUG
        print("调试模式已启用")
    
    # 处理窗口关闭选项
    if args.no_close:
        config_updates['AUTO_CLOSE_MOMENTS'] = False
        print("朋友圈窗口将保持打开")
    
    # 处理其他选项
    if args.wait_time is not None:
        config_updates['WAIT_TIME'] = args.wait_time
    
    if args.max_retries is not None:
        config_updates['MAX_RETRIES'] = args.max_retries
    
    if args.retry_interval is not None:
        config_updates['RETRY_INTERVAL'] = args.retry_interval
    
    if args.log_file is not None:
        config_updates['LOG_FILE'] = args.log_file
    
    return args, config_updates