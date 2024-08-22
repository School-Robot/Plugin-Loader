import logging
import logging.handlers
import os
import re

if not os.path.exists('logs'):
    os.mkdir('logs')

class Base64Formatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)
        self.base64_pattern = re.compile(r'(base64://)[a-zA-Z0-9+/]*={0,2}')
    def format(self, record):
        message = super().format(record)
        def repl(match):
            base64_data = match.group(0)
            size_bytes = len(base64_data) * 3 // 4  
            if size_bytes < 1024:
                size_str = f"{size_bytes}B"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes/1024:.2f}KB"
            else:
                size_str = f"{size_bytes/(1024*1024):.2f}MB"
            return f"base64://<{size_str}_data>"
        message = self.base64_pattern.sub(repl, message)
        return message

loggerClass = logging.getLogger("Plugin-Loader")
loggerClass.setLevel(logging.DEBUG)
log_path = os.path.join("logs", "loader.log")
handler = logging.handlers.TimedRotatingFileHandler(log_path, when="midnight", interval=1, encoding="utf-8")
formatter = Base64Formatter('%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
loggerClass.addHandler(handler)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
loggerClass.addHandler(console)
