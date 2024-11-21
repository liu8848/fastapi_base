import os
from pathlib import Path

# 获取项目根目录
BasePath = Path(__file__).resolve().parent.parent

# alembic 迁移文件存放路径
ALEMBIC_VERSIONS_DIR=os.path.join(BasePath,'alembic','versions')

# 日志文件路径
LOG_DIR = os.path.join(BasePath, "logs")
