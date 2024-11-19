import os
from pathlib import Path

# 获取项目根目录
BasePath = Path(__file__).resolve().parent.parent

# 日志文件路径
LOG_DIR = os.path.join(BasePath, "logs")
