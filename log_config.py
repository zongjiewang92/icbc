import sys
import os
import logging
from datetime import datetime

def init_logging(log_prefix="error", log_dir="log", to_console=True):
    """初始化日志系统，重定向 print 输出与错误信息到日志文件"""

    # 确保日志目录存在
    os.makedirs(log_dir, exist_ok=True)

    # 当前时间字符串（带时分秒）
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log_filename = f"{log_prefix}_{timestamp}.log"
    log_path = os.path.join(log_dir, log_filename)

    # 配置 logging
    handlers = [logging.FileHandler(log_path, mode='a', encoding='utf-8')]
    if to_console:
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )

    # 重定向 print 和错误输出到日志
    class LoggerWriter:
        def __init__(self, level):
            self.level = level
        def write(self, message):
            if message.strip():
                self.level(message)
        def flush(self):
            pass

    sys.stdout = LoggerWriter(logging.info)
    sys.stderr = LoggerWriter(logging.error)

    logging.info(f"日志系统初始化完成，日志文件：{log_path}")
