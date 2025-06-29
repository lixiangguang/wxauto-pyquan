##########auto_like_moments.py: [微信朋友圈自动点赞] ##################
# 变更记录: [2023-11-15 10:30] @李祥光 [初始创建]########
# 输入: 无 | 输出: 无 ###############


###########################文件下的所有函数###########################
"""
主函数：程序入口，执行朋友圈自动点赞功能
获取朋友圈：获取微信朋友圈内容
点赞朋友圈：给最近一条朋友圈内容点赞
"""
###########################文件下的所有函数###########################

#########mermaid格式说明所有函数的调用关系说明开始#########
"""
flowchart TD
    A[程序启动] --> B[main函数]
    B --> C[获取朋友圈]
    C --> D[点赞最近一条朋友圈]
    D --> E[程序结束]
"""
#########mermaid格式说明所有函数的调用关系说明结束#########

import time
import sys
import os
import logging
from datetime import datetime

# 导入配置文件
try:
    from config import BASE_DIR, LOG_DIR, LOG_LEVEL, LOG_FORMAT, LOG_FILE, WAIT_TIME, MAX_RETRIES, RETRY_INTERVAL
except ImportError:
    # 如果配置文件不存在，使用默认配置
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    LOG_FILE = os.path.join(LOG_DIR, f'auto_like_{datetime.now().strftime("%Y%m%d")}.log')
    WAIT_TIME = 2
    MAX_RETRIES = 3
    RETRY_INTERVAL = 2

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)

# 配置日志
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logging.info(f"程序启动，使用配置: 等待时间={WAIT_TIME}秒, 最大重试次数={MAX_RETRIES}, 重试间隔={RETRY_INTERVAL}秒")

try:
    import wxautox

except ImportError:
    logging.error("wxautox模块未安装，请使用pip install wxautox安装")
    print("wxautox模块未安装，请使用pip install wxautox安装")
    sys.exit(1)


"""get_moments_window 功能说明:
获取微信朋友圈窗口对象
输入: 无 | 输出: MomentsWnd对象或None
"""
def get_moments_window():
    try:
        # 获取微信窗口
        logging.info("正在获取微信窗口...")
        wx = wxautox.WeChat()

        
        # 检查微信是否正常打开
        if not wx:
            logging.error("未检测到微信窗口，请确保微信已登录并正常运行")
            print("未检测到微信窗口，请确保微信已登录并正常运行")
            return None
        
        # 打开朋友圈窗口
        logging.info("正在打开朋友圈窗口...")
        print("正在打开朋友圈窗口...")
        moments_window = wx.Moments()  # 使用Moments()方法代替GetMoments()
        
        # 检查朋友圈窗口是否正常打开
        if not moments_window:
            logging.error("打开朋友圈窗口失败，请检查微信版本或手动打开朋友圈后重试")
            print("打开朋友圈窗口失败，请检查微信版本或手动打开朋友圈后重试")
            return None
        
        logging.info("朋友圈窗口已打开")
        print("朋友圈窗口已打开")
        return moments_window
    except Exception as e:
        logging.error(f"获取朋友圈窗口时出错: {str(e)}")
        print(f"获取朋友圈窗口时出错: {str(e)}")
        return None


"""like_latest_moment 功能说明:
给最近的一条朋友圈内容点赞
输入: moments_window(MomentsWnd对象) | 输出: 布尔值(是否点赞成功)
"""
def like_latest_moment(moments_window):
    try:
        # 获取朋友圈内容列表
        logging.info("正在获取朋友圈内容...")
        print("正在获取朋友圈内容...")
        
        # 添加重试机制
        retry_count = 0
        moments_list = None
        
        while retry_count < MAX_RETRIES:
            try:
                # 获取当前页面的朋友圈内容
                moments_list = moments_window.GetMoments()
                if moments_list and len(moments_list) > 0:
                    break
                    
                # 如果当前页面没有内容，尝试获取下一页
                moments_list = moments_window.GetMoments(next_page=True)
                if moments_list and len(moments_list) > 0:
                    break
                    
                retry_count += 1
                logging.warning(f"获取朋友圈内容失败，正在重试 ({retry_count}/{MAX_RETRIES})...")
                print(f"获取朋友圈内容失败，正在重试 ({retry_count}/{MAX_RETRIES})...")
                time.sleep(RETRY_INTERVAL)  # 使用配置的重试间隔
            except Exception as e:
                retry_count += 1
                logging.warning(f"获取朋友圈内容出错，正在重试 ({retry_count}/{MAX_RETRIES}): {str(e)}")
                print(f"获取朋友圈内容出错，正在重试 ({retry_count}/{MAX_RETRIES}): {str(e)}")
                time.sleep(RETRY_INTERVAL)  # 使用配置的重试间隔
        
        # 检查是否成功获取朋友圈内容
        if not moments_list or len(moments_list) == 0:
            logging.error("未获取到朋友圈内容，请检查网络连接或刷新朋友圈")
            print("未获取到朋友圈内容，请检查网络连接或刷新朋友圈")
            return False
        
        # 获取最近的一条朋友圈
        latest_moment = moments_list[2]
        
        # 执行点赞操作
        logging.info("正在给最近的一条朋友圈点赞...")
        print(f"正在给最近的一条朋友圈点赞...")
        try:
            latest_moment.Like()
            logging.info("点赞成功！")
            print("点赞成功！")
            return True
        except Exception as e:
            logging.error(f"点赞失败，错误信息: {str(e)}")
            print(f"点赞失败，错误信息: {str(e)}")
            return False
    except Exception as e:
        logging.error(f"点赞过程中出现未预期的错误: {str(e)}")
        print(f"点赞过程中出现未预期的错误: {str(e)}")
        return False


"""
main 功能说明:
主函数，程序入口
输入: 无 | 输出: 无
"""
def main():
    try:
        # 导入配置
        from config import AUTO_CLOSE_MOMENTS, WAIT_TIME
        
        print("=== 微信朋友圈自动点赞程序 ===\n")
        logging.info("开始执行自动点赞流程")
        
        # 获取朋友圈窗口
        moments_window = get_moments_window()
        if not moments_window:
            logging.error("获取朋友圈窗口失败，程序终止")
            return
        
        # 给最近一条朋友圈点赞
        success = like_latest_moment(moments_window)
        
        # 根据配置决定是否关闭朋友圈窗口
        if AUTO_CLOSE_MOMENTS:
            logging.info("正在关闭朋友圈窗口...")
            print("正在关闭朋友圈窗口...")
            try:
                moments_window.close()
                logging.info("朋友圈窗口已关闭")
                print("朋友圈窗口已关闭")
            except Exception as e:
                logging.error(f"关闭朋友圈窗口时出错: {str(e)}")
                print(f"关闭朋友圈窗口时出错: {str(e)}")
        else:
            logging.info("根据配置保持朋友圈窗口打开")
            print("根据配置保持朋友圈窗口打开")
        
        # 显示操作结果
        if success:
            logging.info("自动点赞完成！")
            print("\n✅ 自动点赞完成！")
        else:
            logging.warning("自动点赞失败")
            print("\n❌ 自动点赞失败，请检查上述错误信息并重试")
    except Exception as e:
        logging.error(f"程序执行过程中出现错误: {str(e)}")
        print(f"程序执行过程中出现错误: {str(e)}")


# 当直接运行此脚本时执行main函数
if __name__ == "__main__":
    try:
        # 导入命令行参数处理模块
        from cli import get_args
        
        # 获取命令行参数并更新配置
        args, config_updates = get_args()
        
        # 更新配置
        if config_updates:
            # 更新全局变量
            for key, value in config_updates.items():
                if key in globals():
                    globals()[key] = value
                    logging.info(f"配置已更新: {key}={value}")
        
        # 执行主函数
        main()
    except Exception as e:
        logging.error(f"程序启动时出错: {str(e)}")
        print(f"程序启动时出错: {str(e)}")
