# 微信朋友圈自动点赞工具

## 项目说明

这是一个简单的Python脚本，用于自动给微信朋友圈最近的一条内容点赞。该工具基于wxautox库实现，能够自动操作微信窗口完成点赞操作。

## 功能特点

- 自动打开微信朋友圈窗口
- 获取最新的朋友圈内容
- 自动给最近的一条朋友圈点赞
- 操作完成后自动关闭朋友圈窗口（可配置）
- 完善的日志记录功能
- 灵活的配置选项
- 命令行参数支持
- 异常处理和重试机制

## 使用前提

1. 已安装Python环境（建议Python 3.6+）
2. 已安装wxautox库（可通过`pip install wxautox`安装）
3. 微信客户端已登录并正常运行

## 使用方法

1. 确保微信已登录并处于运行状态
2. 打开命令行，进入项目目录
3. 运行以下命令：

```bash
python auto_like_moments.py
```

4. 程序将自动执行以下操作：
   - 打开微信朋友圈窗口
   - 获取朋友圈内容
   - 给最近的一条朋友圈点赞
   - 关闭朋友圈窗口（除非指定了--no-close参数）

### 命令行参数

可以使用以下命令行参数来自定义程序行为：

```bash
# 启用调试模式（详细日志）
python auto_like_moments.py --debug

# 操作后不关闭朋友圈窗口
python auto_like_moments.py --no-close

```