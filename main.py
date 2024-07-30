import json
import threading
import time
import os

from loader import PluginLoader
from ws import WS
from bot import Bot
from util import Util
from processer import Processer

global variable
from variable import variable


def processCommand(cmd):
    cmd = cmd.split(' ')
    if cmd[0] == 'send':
        if len(cmd) > 1:
            cmd = ' '.join(cmd[1:])
            variable.ws.send(cmd)
    elif cmd[0] == 'plugin':
        if len(cmd) > 1:
            cmd = cmd[1:]
            if cmd[0] == 'load':
                cmd = ' '.join(cmd[1:])
                variable.loader.load_plugin(cmd)
            elif cmd[0] == 'reg':
                cmd = ' '.join(cmd[1:])
                variable.loader.register_plugin(cmd)
            elif cmd[0] == 'enable':
                cmd = ' '.join(cmd[1:])
                variable.loader.enable_plugin(cmd)
            elif cmd[0] == 'disable':
                cmd = ' '.join(cmd[1:])
                variable.loader.disable_plugin(cmd)
            elif cmd[0] == 'unreg':
                cmd = ' '.join(cmd[1:])
                variable.loader.unregister_plugin(cmd)
            elif cmd[0] == 'unload':
                cmd = ' '.join(cmd[1:])
                variable.loader.unload_plugin(cmd)
            elif cmd[0] == 'list':
                variable.loader.list_plugins()
            elif cmd[0] == 'view':
                cmd = ' '.join(cmd[1:])
                variable.loader.view_plugin(cmd)
            elif cmd[0] == 'reload':
                cmd = ' '.join(cmd[1:])
                variable.loader.reload_plugin(cmd)
            else:
                print(
                    "子命令:\nload <filename> - 加载插件\nreg <id> - 注册插件\nenable <id> - 启用插件\ndisable <id> - 禁用插件\nunreg <id> - 注销插件\nunload <id> - 卸载插件\nlist - 列出插件\nview <id> - 查看插件信息\nreload <id> - 重载插件")
        else:
            print(
                "子命令:\nload <filename> - 加载插件\nreg <id> - 注册插件\nenable <id> - 启用插件\ndisable <id> - 禁用插件\nunreg <id> - 注销插件\nunload <id> - 卸载插件\nlist - 列出插件\nview <id> - 查看插件信息\nreload <id> - 重载插件")
    elif cmd[0] == 'help' or cmd[0] == '?':
        print("命令列表:\nexit - 退出\nsend <msg> - 发送WebSocket消息\nplugin <op> <arg> - 插件管理")
        for plugin in variable.loader.plugin_commands:
            print(plugin, "的命令:")
            if 'help' in variable.loader.plugin_commands[plugin]:
                print(variable.loader.plugin_commands[plugin]['help'])
            else:
                for command in variable.loader.plugin_commands[plugin]:
                    print(command)
    else:
        variable.loader.processPluginCommand(cmd)


logger = variable.log.getChild("Main")


def main():
    global variable
    if os.path.exists('data') == False:
        os.mkdir('data')
    if os.path.exists('plugins') == False:
        os.mkdir('plugins')
    try:
        open('config.json', 'r').close()
    except:
        logger.info('首次使用，请先进行配置')
        api_url = input('请输入WebSocket地址: ')
        if api_url == '':
            logger.error('WebSocket地址不能为空')
            exit()
        bot_id = input('请输入Bot QQ: ')
        if bot_id == '':
            logger.error('Bot QQ不能为空')
            exit()
        bot_id = int(bot_id)
        token = input('请输入Token(没有请留空): ')
        if token == '':
            token = None
        config = {'conn': {'api_url': api_url, 'bot_id': bot_id, 'token': token}, 'plugin': {}}
        with open('config.json', 'w') as c:
            c.write(json.dumps(config))
    with open('config.json', 'r') as c:
        try:
            variable.config = json.loads(c.read())
        except:
            logger.error('无WebSocket配置')
            exit()
    conn = variable.config['conn']
    api_url = None
    if 'api_url' in conn:
        api_url = conn['api_url']
    variable.bot_id = None
    if 'bot_id' in conn:
        variable.bot_id = conn['bot_id']
    token = None
    if 'token' in conn:
        token = conn['token']
    if os.path.exists('data') == False:
        os.mkdir('data')
    variable.loader = PluginLoader()
    variable.ws = WS(api_url, token)
    variable.bot = Bot()
    variable.processer = Processer()
    websocket_thread = threading.Thread(target=variable.ws.start, args=())
    logger.info("正在启动WebSocket...")
    websocket_thread.start()
    time.sleep(3)
    logger.info("WebSocket启动完成")
    variable.util = Util()
    logger.info("正在启动插件...")
    variable.loader.register_plugins()
    variable.loader.enable_plugins()

    def ws_mon():
        global variable
        logger = variable.log.getChild("WebSocket Monitor")
        ws_retry = 0
        while True:
            if variable.main_stop:
                logger.info("接收到停止命令")
                break
            if not variable.ws.get_status():
                logger.error("WebSocket断开")
                if ws_retry > 3:
                    logger.info("重试次数过多")
                    logger.info("正在退出...")
                    variable.loader.unload_plugins()
                    variable.ws.close()
                    exit()
                ws_retry += 1
                if ws_retry == 1:
                    variable.loader.disable_plugins()
                    variable.loader.unregister_plugins()
                logger.info(f"{ws_retry * 5}秒后重试")
                time.sleep(5 * ws_retry)
                try:
                    logger.info("正在重连WebSocket...")
                    websocket_thread = threading.Thread(target=variable.ws.start, args=())
                    websocket_thread.start()
                    logger.info(f"重试次数: {ws_retry}")
                    time.sleep(3)
                except:
                    pass
            else:
                if ws_retry != 0:
                    logger.info("WebSocket重连成功")
                    ws_retry = 0
                    variable.loader.register_plugins()
                    variable.loader.enable_plugins()
            time.sleep(0.01)

    ws_mon_thread = threading.Thread(target=ws_mon, args=())
    ws_mon_thread.start()

    while True:
        a = ""
        try:
            a = input()
        except:
            a = "exit"
        if a == "exit":
            try:
                logger.info("正在退出...")
                with open('config.json', 'w') as c:
                    c.write(json.dumps(variable.config))
                variable.loader.disable_plugins()
                variable.loader.unregister_plugins()
                variable.loader.unload_plugins()
                variable.main_stop = True
                variable.ws.close()
                websocket_thread.join()
                ws_mon_thread.join()
                exit()
            except Exception as e:
                variable.main_stop = True
                websocket_thread.join()
                ws_mon_thread.join()
                logger.exception(e)
                exit()
        else:
            try:
                processCommand(a)
            except Exception as e:
                logger.exception(e)
        time.sleep(0.01)


if __name__ == '__main__':
    try:
        main()
    except:
        exit()
