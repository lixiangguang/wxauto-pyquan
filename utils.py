##########utils.py: 工具函数 ##################
#变更记录: [2023-11-22 11:30] @李祥光 初始创建########
#输入: 无 | 输出: 工具函数###############


###########################文件下的所有函数###########################
"""
retry: 重试装饰器
time_it: 计时装饰器
"""
###########################文件下的所有函数###########################

import time
import logging
import functools
from typing import Callable, Any, Optional

"""
retry 功能说明:
重试装饰器，用于在函数执行失败时自动重试
输入: max_retries(最大重试次数), wait_time(重试间隔), exceptions(捕获的异常类型) | 输出: 装饰器函数
"""
def retry(max_retries: int = 3, wait_time: int = 2, exceptions: tuple = (Exception,)) -> Callable:
    """
    重试装饰器
    :param max_retries: 最大重试次数
    :param wait_time: 重试间隔（秒）
    :param exceptions: 需要捕获的异常类型
    :return: 装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logging.warning(
                            f"{func.__name__} 执行失败，正在重试 ({attempt+1}/{max_retries}): {str(e)}"
                        )
                        time.sleep(wait_time)
                    else:
                        logging.error(
                            f"{func.__name__} 执行失败，已达到最大重试次数: {str(e)}"
                        )
            if last_exception:
                raise last_exception
        return wrapper
    return decorator


"""
time_it 功能说明:
计时装饰器，用于记录函数执行时间
输入: log_level(日志级别) | 输出: 装饰器函数
"""
def time_it(log_level: int = logging.DEBUG) -> Callable:
    """
    计时装饰器
    :param log_level: 日志级别
    :return: 装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.log(log_level, f"{func.__name__} 执行耗时: {elapsed_time:.2f}秒")
            return result
        return wrapper
    return decorator