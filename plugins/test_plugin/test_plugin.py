class Plugin(object):
    plugin_methods={'register':{'priority':30000,'func':'zhuce','desc':'注册插件'},'enable':{'priority':30000,'func':'qiyong','desc':'启用插件'},'disable':{'priority':30000,'func':'jinyong','desc':'禁用插件'},'unregister':{'priority':30000,'func':'xiezai','desc':'卸载插件'},'group_message':{'priority':30000,'func':'qunxiaoxi','desc':'群消息处理'}}
    plugin_commands={'echo':'echo_command'}
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
        self.log.info(f"Bot is : {bot.get_id()}")

    def qiyong(self,auth):
        self.auth=auth
        self.log.info("Plugin enable")
        self.log.info(f"Bot is : {self.bot.get_id()}")

    def jinyong(self):
        self.log.info("Plugin disable")

    def xiezai(self):
        self.log.info("Plugin unregister")
    
    def qunxiaoxi(self,time,self_id,sub_type,message_id,group_id,user_id,anonymous,message,raw_message,font,sender):
        if raw_message.startswith('/echo'):
            msg=raw_message[5:].strip()
            if self.util.send_group_msg(self.auth,group_id,msg)[0]:
                return True
    
    def echo_command(self,cmd):
        msg=input()
        self.util.send_group_msg(self.auth,'252855997',msg)