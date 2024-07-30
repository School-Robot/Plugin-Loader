import logging
import logging.handlers
import os

if not os.path.exists('logs'):
    os.mkdir('logs')

loggerClass = logging.getLogger("Plugin-Loader")
loggerClass.setLevel(logging.DEBUG)
log_path = os.path.join("logs", "loader.log")
handler = logging.handlers.TimedRotatingFileHandler(log_path, when="midnight", interval=1, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
loggerClass.addHandler(handler)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
loggerClass.addHandler(console)
