##########test_wxauto.py: 测试wxautox库是否正常工作 ##################
# 变更记录: [2023-11-22 10:30] @李祥光 初始创建
# 变更记录: [2025-06-29 13:45] @李祥光 添加配置文件支持、增强日志记录
# 变更记录: [2025-06-29 14:05] @李祥光 添加命令行参数支持
# 变更记录: [2025-06-29 14:37] @李祥光 优化微信窗口检测方法，显示可用API
# 输入: 无 | 输出: 微信窗口检测结果 ###############


###########################文件下的所有函数###########################
"""
parse_args：解析命令行参数并应用配置
main：测试wxautox库是否正常工作，检测微信窗口并显示可用方法
"""
###########################文件下的所有函数###########################

#########mermaid格式说明所有函数的调用关系说明开始#########
"""
flowchart TD
    A[程序启动] --> P[parse_args函数]
    P --> Q[解析命令行参数]
    Q --> R[应用参数覆盖配置]
    R --> B[main函数]
    B --> C[导入wxauto库]
    C -->|导入成功| D[获取微信窗口]
    C -->|导入失败| E[显示错误信息]
    D -->|获取成功| H[获取窗口信息]
    D -->|获取失败| G[显示错误信息]
    H --> I[检查可用方法]
    I -->|检查成功| J[显示可用方法]
    I -->|检查失败| K[显示警告信息]
    J --> F[显示成功信息]
    K --> F
"""
#########mermaid格式说明所有函数的调用关系说明结束#########

import sys
import os
import logging
import argparse

"""parse_args 功能说明:
解析命令行参数
输入: 无 | 输出: 解析后的参数对象
"""
def parse_args():
    parser = argparse.ArgumentParser(description='wxautox库测试工具')
    
    # 基本选项
    parser.add_argument('--debug', action='store_true', help='启用调试模式（详细日志）')
    parser.add_argument('--log-file', type=str, help='指定日志文件路径')
    
    return parser.parse_args()

# 解析命令行参数
args = parse_args()

# 尝试导入配置文件，如果不存在则使用默认配置
try:
    from config import LOG_LEVEL, LOG_FORMAT, LOG_DIR, LOG_FILE
    config_imported = True
except ImportError:
    # 默认配置
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'test_wxauto.log')
    config_imported = False

# 应用命令行参数覆盖配置
if args.debug:
    LOG_LEVEL = logging.DEBUG
    print("调试模式已启用")

if args.log_file:
    LOG_FILE = args.log_file
    print(f"日志将写入: {LOG_FILE}")

# 确保日志目录存在
log_dir = os.path.dirname(LOG_FILE)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

"""main 功能说明:
测试wxautox库是否正常工作，检查微信是否能被识别
输入: 无 | 输出: 无
"""
def main():
    logger.info("开始测试wxautox库...")
    
    # 记录配置信息
    if config_imported:
        logger.debug("成功导入配置文件config.py")
    else:
        logger.warning("未找到配置文件config.py，使用默认配置")
    
    # 尝试导入wxautox库
    try:
        import wxautox as wx
        logger.info("✅ wxautox库已成功安装")
    except ImportError as e:
        logger.error(f"❌ wxautox库导入失败: {str(e)}")
        print(f"❌ wxautox库导入失败: {str(e)}")
        print("请确保已安装wxautox库，可以使用 'pip install wxautox' 安装")
        sys.exit(1)
    
    # 尝试获取微信窗口
    try:
        wx_instance = wx.WeChat()
        if wx_instance:
            # 获取微信窗口信息
            try:
                window_info = str(wx_instance)
                logger.info(f"✅ 成功检测到微信窗口: {window_info}")
                print(f"✅ 成功检测到微信窗口: {window_info}")
            except Exception as e:
                logger.info(f"✅ 成功检测到微信窗口，但无法获取窗口信息: {str(e)}")
                print(f"✅ 成功检测到微信窗口，但无法获取窗口信息")
            
            # 尝试获取微信窗口可用方法
            try:
                logger.info("正在检查微信窗口可用方法...")
                # 获取对象的可用方法和属性
                available_methods = [method for method in dir(wx_instance) if not method.startswith('_')]
                logger.info(f"✅ 微信窗口可用方法: {', '.join(available_methods[:10])}{'...' if len(available_methods) > 10 else ''}")
                print(f"✅ 微信窗口可用方法: {', '.join(available_methods[:10])}{'...' if len(available_methods) > 10 else ''}")
                
                # 尝试获取对象的字符串表示
                wx_str = str(wx_instance)
                logger.info(f"✅ 微信窗口对象信息: {wx_str}")
                print(f"✅ 微信窗口对象信息: {wx_str}")
            except Exception as e:
                logger.warning(f"⚠️ 检查微信窗口方法时出错: {str(e)}")
                print(f"⚠️ 检查微信窗口方法时出错: {str(e)}")
            
            print("wxautox库工作正常，可以使用auto_like_moments.py脚本")
            logger.info("wxautox库工作正常，测试完成")
        else:
            logger.warning("❌ 未检测到微信窗口，请确保微信已登录并正常运行")
            print("❌ 未检测到微信窗口，请确保微信已登录并正常运行")
    except Exception as e:
        error_msg = f"❌ 检测微信窗口时出错: {str(e)}"
        logger.error(error_msg)
        print(error_msg)


# 当直接运行此脚本时执行main函数
if __name__ == "__main__":
    try:
        logger.debug("程序开始执行")
        main()
        logger.debug("程序正常结束")
    except Exception as e:
        error_msg = f"程序执行过程中发生未处理的异常: {str(e)}"
        logger.critical(error_msg)
        print(f"❌ {error_msg}")
        sys.exit(1)