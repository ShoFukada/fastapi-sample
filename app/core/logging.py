# app/core/logging.py

import logging
import sys
from logging.config import dictConfig

def setup_logging():
    """
    Python標準のdictConfigを使ってログの設定を行う。
    """
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                # ログの出力フォーマットを指定
                # %(asctime)s => 日時
                # %(levelname)s => ログレベル (INFO/ERROR等)
                # %(name)s => ロガー名
                # %(message)s => ログ本文
                "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                # sys.stdout に出力 (コンソールに表示)
                "stream": "ext://sys.stdout"
            }
        },
        # ルートロガー (全体)
        "root": {
            "level": "INFO",  # INFOレベル以上を表示
            "handlers": ["console"]
        }
    }
    dictConfig(logging_config)