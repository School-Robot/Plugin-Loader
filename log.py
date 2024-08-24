import logging
import logging.handlers
import os
import re

if not os.path.exists('logs'):
    os.mkdir('logs')

class ColoredBase64Formatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',    # 蓝色
        'INFO': '\033[92m',     # 绿色
        'WARNING': '\033[93m',  # 黄色
        'ERROR': '\033[91m',    # 红色
        'CRITICAL': '\033[95m', # 紫色
        'RESET': '\033[0m',     # 重置颜色
        'CYAN': '\033[96m',     # 青色
        'MAGENTA': '\033[95m',  # 洋红
        'BOLD': '\033[1m',      # 粗体
        'UNDERLINE': '\033[4m', # 下划线
        'YELLOW':'\033[33m'     # 黄色
    }

    def __init__(self, fmt=None, datefmt=None, style='%', use_color=True):
        super().__init__(fmt, datefmt, style)
        self.use_color = use_color
        self.base64_pattern = re.compile(r'(base64://)[a-zA-Z0-9+/]*={0,2}')

    def format(self, record):
        if hasattr(record, 'msg'):
            record.msg = self.process_base64(record.msg)
            # record.msg = self._logger_debug_clean_abnormal_data(record.msg)
        message = super().format(record)
        if self.use_color:
            timestamp_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}'
            message = re.sub(timestamp_pattern, lambda m: f"{self.COLORS['INFO']}{m.group()}{self.COLORS['RESET']}", message, 1)
            message = message.replace(f"[{record.levelname}]", f"{self.COLORS[record.levelname]}[{record.levelname}]{self.COLORS['RESET']}")
            message = self.color_special_info(message)
        return message

    def process_base64(self, message):
        if isinstance(message, str):
            return self.base64_pattern.sub(self.repl_base64, message)
        return message
    def process_data_size(self, message):
        if isinstance(message, str):
            return self.data_size_pattern.sub(lambda m: f"<{m.group(1)}>", message)
        return message
    
    def repl_base64(self, match):
        base64_data = match.group(0)
        size_bytes = len(base64_data) * 3 // 4  
        if size_bytes < 1024:
            size_str = f"{size_bytes}B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes/1024:.2f}KB"
        else:
            size_str = f"{size_bytes/(1024*1024):.2f}MB"
        return f"base64://<{size_str}>"

    def color_special_info(self, message):
        message = re.sub(r'\[(Thread-\d+.*?)\]', f"{self.COLORS['MAGENTA']}[\\1]{self.COLORS['RESET']}", message)
        message = re.sub(r'\[(Plugin-Loader\.[^\]]+)\]', f"{self.COLORS['CYAN']}[\\1]{self.COLORS['RESET']}", message)
        message = re.sub(r'(\[)(\d+)(\])', f"\\1{self.COLORS['YELLOW']}\\2{self.COLORS['RESET']}\\3", message)
        message = re.sub(r'(\()(\d+)(\))', f"\\1{self.COLORS['YELLOW']}\\2{self.COLORS['RESET']}\\3", message)
        message = re.sub(r'(撤回消息ID:)', f"{self.COLORS['BOLD']}\\1{self.COLORS['RESET']}", message)
        message = re.sub(r'(收到.*?的群消息:)', f"{self.COLORS['BOLD']}\\1{self.COLORS['RESET']}", message)
        message = re.sub(r'(在群.*?中撤回了消息)', f"{self.COLORS['BOLD']}\\1{self.COLORS['RESET']}", message)
        message = re.sub(r'(\[CQ:[^\]]+\])', f"{self.COLORS['MAGENTA']}\\1{self.COLORS['RESET']}", message)
        message = re.sub(r'(正在.*?插件)', f"{self.COLORS['UNDERLINE']}\\1{self.COLORS['RESET']}", message)
        message = re.sub(r'(WebSocket.*?)', f"{self.COLORS['UNDERLINE']}\\1{self.COLORS['RESET']}", message)
        message = re.sub(r'(<\d+(?:\.\d+)?[BKM]B_data>)', f"{self.COLORS['CYAN']}\\1{self.COLORS['RESET']}", message)
        return message

loggerClass = logging.getLogger("Plugin-Loader")
loggerClass.setLevel(logging.DEBUG)

#文件
log_path = os.path.join("logs", "loader.log")
handler = logging.handlers.TimedRotatingFileHandler(log_path, when="midnight", interval=1, encoding="utf-8")
file_formatter = ColoredBase64Formatter('%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s', use_color=False)
handler.setFormatter(file_formatter)
handler.setLevel(logging.DEBUG)
loggerClass.addHandler(handler)

#控制台
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_formatter = ColoredBase64Formatter('%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s', use_color=True)
console.setFormatter(console_formatter)
loggerClass.addHandler(console)


if __name__ == "__main__":
   loggerClass.debug("debug message")
   loggerClass.info("info message")
   loggerClass.warning("warning message")
   loggerClass.error("error message")
   loggerClass.critical("critical message")
   loggerClass.info("message base64://SGVsbG8gV29ybGQ= data")
