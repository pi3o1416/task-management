
import os
from dotenv import dotenv_values
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Config file
config_file_path = os.path.join(BASE_DIR, '.env')
dev_config_file_path = os.path.join(BASE_DIR, 'dev.env')
CONFIG = ''

if os.path.exists(config_file_path):
    CONFIG = dotenv_values(config_file_path)
    from .production import *
elif os.path.exists(dev_config_file_path):
    CONFIG = dotenv_values(dev_config_file_path)
    from .dev import *
else:
    raise FileNotFoundError("Add '.env' for production or 'dev.env' for development")









