from time import sleep
class Plugin(object):
    plugin_methods={'register':{'priority':30000,'func':'zhuce','desc':'注册插件'},'enable':{'priority':30000,'func':'qiyong','desc':'启用插件'},'disable':{'priority':30000,'func':'jinyong','desc':'禁用插件'},'unregister':{'priority':30000,'func':'xiezai','desc':'卸载插件'},'group_message':{'priority':30000,'func':'qun','desc':'群消息处理'}}
    plugin_commands={'file':'file_command','help':'file <msg> - 向群里发送消息'}
    plugin_auths={'send_group_msg'}
    auth=''
    log=None
    status=None
    bot=None
    util=None
    dir=None
    def zhuce(self,logger,util,bot,dir):
        self.log=logger
        self.bot=bot
        self.util=util
        self.dir=dir
        self.log.info("Plugin register")

    def qiyong(self,auth):
        self.auth=auth
        self.log.info("Plugin enable")

    def jinyong(self):
        self.log.info("Plugin disable")

    def xiezai(self):
        self.log.info("Plugin unregister")

    def qun(self,time,self_id,sub_type,message_id,group_id,user_id,anonymous,message,raw_message,font,sender):
        sleep(10)
        return False
    
    def file_command(self,cmd):
        cmd=' '.join(cmd)
        self.util.send_group_msg(self.auth,'252855997',cmd)

plugin_name="file plugin"
plugin_id="tk.mcsog.file_plugin"
plugin_version="1.0.01"
plugin_author="f00001111"
plugin_desc="单文件插件"