##########test_auto_like.py: 自动点赞功能测试 ##################
#变更记录: [2023-11-22 11:00] @李祥光 初始创建########
#输入: 无 | 输出: 测试结果###############


###########################文件下的所有函数###########################
"""
test_config_loading: 测试配置文件加载
test_get_moments_window: 测试获取朋友圈窗口功能
test_like_latest_moment: 测试点赞功能
test_main: 测试主函数
"""
###########################文件下的所有函数###########################

import unittest
import sys
import os
import logging
from unittest.mock import patch, MagicMock

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入被测试模块
import auto_like_moments
from config import *


class TestAutoLikeMoments(unittest.TestCase):
    """
    自动点赞功能测试类
    """
    
    def setUp(self):
        """测试前准备"""
        # 禁用日志输出，避免测试时产生大量日志
        logging.disable(logging.CRITICAL)
    
    def tearDown(self):
        """测试后清理"""
        # 恢复日志输出
        logging.disable(logging.NOTSET)
    
    @patch('auto_like_moments.wxautox.WeChat')
    def test_get_moments_window(self, mock_wechat):
        """测试获取朋友圈窗口功能"""
        # 创建模拟对象
        mock_wechat_instance = MagicMock()
        mock_moments_window = MagicMock()
        
        # 配置模拟对象的行为
        mock_wechat.return_value = mock_wechat_instance
        mock_wechat_instance.Moments.return_value = mock_moments_window
        
        # 调用被测试函数
        result = auto_like_moments.get_moments_window()
        
        # 验证结果
        self.assertEqual(result, mock_moments_window)
        mock_wechat_instance.Moments.assert_called_once()
    
    @patch('auto_like_moments.wxautox.WeChat')
    def test_get_moments_window_failure(self, mock_wechat):
        """测试获取朋友圈窗口失败的情况"""
        # 配置模拟对象返回None
        mock_wechat.return_value = None
        
        # 调用被测试函数
        result = auto_like_moments.get_moments_window()
        
        # 验证结果
        self.assertIsNone(result)
    
    def test_like_latest_moment(self):
        """测试点赞功能"""
        # 创建模拟对象
        mock_moments_window = MagicMock()
        mock_moment = MagicMock()
        
        # 配置模拟对象的行为
        mock_moments_window.GetMoments.return_value = [mock_moment]
        
        # 调用被测试函数
        result = auto_like_moments.like_latest_moment(mock_moments_window)
        
        # 验证结果
        self.assertTrue(result)
        mock_moments_window.GetMoments.assert_called_once()
        mock_moment.Like.assert_called_once()
    
    def test_like_latest_moment_no_moments(self):
        """测试没有朋友圈内容的情况"""
        # 创建模拟对象
        mock_moments_window = MagicMock()
        
        # 配置模拟对象的行为
        mock_moments_window.GetMoments.return_value = []
        
        # 调用被测试函数
        result = auto_like_moments.like_latest_moment(mock_moments_window)
        
        # 验证结果
        self.assertFalse(result)
    
    def test_like_latest_moment_exception(self):
        """测试点赞过程中出现异常的情况"""
        # 创建模拟对象
        mock_moments_window = MagicMock()
        mock_moment = MagicMock()
        
        # 配置模拟对象的行为
        mock_moments_window.GetMoments.return_value = [mock_moment]
        mock_moment.Like.side_effect = Exception("模拟点赞失败")
        
        # 调用被测试函数
        result = auto_like_moments.like_latest_moment(mock_moments_window)
        
        # 验证结果
        self.assertFalse(result)
    
    @patch('auto_like_moments.get_moments_window')
    @patch('auto_like_moments.like_latest_moment')
    def test_main(self, mock_like_latest_moment, mock_get_moments_window):
        """测试主函数"""
        # 创建模拟对象
        mock_moments_window = MagicMock()
        
        # 配置模拟对象的行为
        mock_get_moments_window.return_value = mock_moments_window
        mock_like_latest_moment.return_value = True
        
        # 调用被测试函数
        auto_like_moments.main()
        
        # 验证结果
        mock_get_moments_window.assert_called_once()
        mock_like_latest_moment.assert_called_once_with(mock_moments_window)
        mock_moments_window.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()