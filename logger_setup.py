"""
Logger setup cho Bot v7.5
- File: TimedRotatingFileHandler, xoay theo ngày, giữ 30 ngày, ghi TẤT CẢ từ DEBUG
- Console: Hiện INFO trở lên (màu sắc), có thể đặt CONSOLE_LOG_LEVEL=DEBUG trong .env

FIX v7.5:
  ✅ Console mặc định INFO (không phải WARNING) — thấy đầy đủ log bot hoạt động
  ✅ Format log file có timestamp giờ VN rõ ràng (dd/mm/yyyy HH:MM:SS)
  ✅ Không duplicate log khi import nhiều lần (propagate=False)
"""

import logging
import logging.handlers
import os
from dotenv import load_dotenv

load_dotenv()


class ColoredFormatter(logging.Formatter):
    """Formatter màu sắc cho console."""

    COLORS = {
        'DEBUG':    '\033[36m',   # Cyan
        'INFO':     '\033[32m',   # Green
        'WARNING':  '\033[33m',   # Yellow
        'ERROR':    '\033[31m',   # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        # Clone record để không ảnh hưởng file handler
        record = logging.makeLogRecord(record.__dict__)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logger():
    """
    Cấu hình logging hệ thống.
    - File: ghi DEBUG trở lên, xoay lúc nửa đêm, giữ 30 ngày
    - Console: ghi INFO trở lên (mặc định), có thể override bằng CONSOLE_LOG_LEVEL
    """
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("bot_logger")

    # Tránh duplicate nếu setup_logger() bị gọi nhiều lần
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)  # Logger nhận tất cả, handler tự filter

    # ── FILE HANDLER ──────────────────────────────────────────────────────────
    # TimedRotatingFileHandler: xoay lúc 00:00 mỗi ngày (giờ local VN)
    file_handler = logging.handlers.TimedRotatingFileHandler(
        "logs/bot_activity.log",
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
        utc=False,   # Dùng giờ local (VN) để xoay đúng nửa đêm VN
    )
    file_handler.suffix = "%Y-%m-%d"  # logs/bot_activity.log.2026-06-27
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    ))

    # ── CONSOLE HANDLER ───────────────────────────────────────────────────────
    # ✅ FIX: Mặc định INFO (không phải WARNING) để thấy đầy đủ hoạt động bot
    # Đặt CONSOLE_LOG_LEVEL=WARNING trong .env nếu muốn giảm output
    console_level_name = os.getenv("CONSOLE_LOG_LEVEL", "INFO").upper()
    console_level = getattr(logging, console_level_name, logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(ColoredFormatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    ))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False  # Không bubble lên root logger → không duplicate

    return logger


logger = setup_logger()