import importlib
import os
import sys
import gc
import uuid

from variable import variable

logger=variable.log.getChild("Loader")
class PluginInfo(object):
    plugin_version=None
    plugin_id=None
    plugin_name=None
    plugin_author=None
    plugin_desc=None
    plugin=None
    def __init__(self,plugin_version,plugin_id,plugin_name,plugin_author,plugin_desc,plugin):
        self.plugin_author=plugin_author
        self.plugin_desc=plugin_desc
        self.plugin_id=plugin_id
        self.plugin_name=plugin_name
        self.plugin_version=plugin_version
        self.plugin=plugin

class PluginLoader(object):
    plugin_infos={}
    plugin_methods={}
    plugin_registers={}
    plugin_enables=[]
    plugin_commands={}
    plugin_auths={}
    auths={}
    auth={'send_private_msg':'发送私聊消息','send_group_msg':'发送群消息','send_msg':'发送消息','delete_msg':'撤回消息','get_msg':'获取消息','get_forward_msg':'获取合并转发消息','send_like':'发送好友赞','set_group_kick':'群组踢人','set_group_ban':'群组单人禁言','set_group_anonymous_ban':'群组匿名用户禁言','set_group_whole_ban':'群组全员禁言','set_group_admin':'群组设置管理员','set_group_anonymous':'群组匿名','set_group_card':'设置群名片','set_group_name':'设置群名','set_group_leave':'退出群组','set_group_special_title':'设置群组专属头衔','set_friend_add_request':'处理加好友请求','set_group_add_request':'处理加群请求','get_login_info':'获取登录号信息','get_stranger_info':'获取陌生人信息','get_friend_list':'获取好友列表','get_group_info':'获取群信息','get_group_list':'获取群列表','get_group_member_info':'获取群成员信息','get_group_member_list':'获取群成员列表','get_group_honor_info':'获取群荣耀信息','get_cookies':'获取Cookies','get_csrf_token':'获取CSRF Token','get_credentials':'获取QQ相关接口凭证','get_record':'获取语音','get_image':'获取图片','get_status':'获取运行状态','get_version_info':'获取版本信息','set_restart':'重启OneBot','clean_cache':'清理缓存','plugin_control':'插件控制','send_ws_msg':'发送WebSocket消息','get_ws_msg':'获取WebSocket返回内容'}
    def __init__(self):
        self.load_plugins()

    def load_plugins(self):
        logger.info("正在加载插件...")
        succ=0
        err=0
        for filename in os.listdir('plugins'):
            if filename.endswith('.py'):
                filename=filename[:-3]
            if filename=="__pycache__":
                continue
            try:
                if filename in variable.config['plugin']:
                    if 'load' in variable.config['plugin'][filename]:
                        if not variable.config['plugin'][filename]['load']:
                            continue
                    else:
                        variable.config['plugin'][filename]['load']=True
                else:
                    variable.config['plugin'][filename]={'load':True}
                plugin=importlib.import_module('plugins.'+filename)
                logger.debug(f"正在加载: {plugin}")
                id=plugin.plugin_id
                name=plugin.plugin_name
                version=plugin.plugin_version
                author=plugin.plugin_author
                desc=plugin.plugin_desc
                info=PluginInfo(version,id,name,author,desc,plugin)
                self.plugin_infos[id]={'name':filename,'info':info}
                del name
                del version
                del author
                del desc
                del id
                del plugin
                del info
                succ+=1
            except Exception as e:
                id=""
                for plugin_id in self.plugin_infos:
                    if filename == self.plugin_infos[plugin_id]['name']:
                        id=plugin_id
                if id!='':
                    del self.plugin_infos[id]
                del_modules=[]
                for module_name in sys.modules:
                    if module_name.startswith('plugins.'+filename):
                        del_modules.append(module_name)
                for module_name in del_modules:
                    del sys.modules[module_name]
                logger.error(f"插件: {filename} 出现错误")
                logger.exception(e)
                err+=1
        logger.info(f"加载完成! 加载成功{succ}个插件，加载失败{err}个插件")

    def register_plugins(self):
        logger.info("正在注册插件...")
        succ=0
        err=0
        for id in self.plugin_infos:
            try:
                if self.plugin_infos[id]['name'] in variable.config['plugin']:
                    if 'reg' in variable.config['plugin'][self.plugin_infos[id]['name']]:
                        if not variable.config['plugin'][self.plugin_infos[id]['name']]['reg']:
                            continue
                    else:
                        variable.config['plugin'][self.plugin_infos[id]['name']]['reg']=True
                else:
                    variable.config['plugin'][self.plugin_infos[id]['name']]={'reg':True}
                plugin=self.plugin_infos[id]['info'].plugin.Plugin()
                methods=plugin.plugin_methods
                self.plugin_methods[id]=methods
                if not os.path.exists('data/'+id):
                    os.makedirs('data/'+id)
                data_dir=os.path.abspath('data/'+id)
                plugin_logger=variable.log.getChild(self.plugin_infos[id]['info'].plugin_name)
                register=getattr(plugin,self.plugin_methods[id]['register']['func'])
                register(plugin_logger,variable.util,variable.bot,data_dir)
                plugin.status="registered"
                self.plugin_registers[id]=plugin
                del plugin
                del register
                del methods
                succ+=1
            except Exception as e:
                if id in self.plugin_registers:
                    del self.plugin_registers[id]
                if id in self.plugin_methods:
                    del self.plugin_methods[id]
                logger.error(f"插件: {id} 出现错误")
                logger.exception(e)
                err+=1
        logger.debug(self.plugin_registers)
        logger.info(f"注册完成! 注册成功{succ}个插件，注册失败{err}个插件")

    def enable_plugins(self):
        logger.info("正在启用插件...")
        succ=0
        err=0
        self.plugin_enables=[]
        for id in self.plugin_registers:
            try:
                if self.plugin_infos[id]['name'] in variable.config['plugin']:
                    if 'enable' in variable.config['plugin'][self.plugin_infos[id]['name']]:
                        if not variable.config['plugin'][self.plugin_infos[id]['name']]['enable']:
                            continue
                    else:
                        variable.config['plugin'][self.plugin_infos[id]['name']]['enable']=True
                else:
                    variable.config['plugin'][self.plugin_infos[id]['name']]={'enable':True}
                plugin=self.plugin_registers[id]
                commands=plugin.plugin_commands
                self.plugin_commands[id]=commands
                auths=plugin.plugin_auths
                uid=uuid.uuid4().hex
                self.plugin_auths[id]={"uid":uid,"auths":auths}
                self.auths[uid]=auths
                del auths
                enable=getattr(self.plugin_registers[id],self.plugin_methods[id]['enable']['func'])
                enable(uid)
                self.plugin_registers[id].status="enabled"
                self.plugin_enables.append(id)
                del uid
                del enable
                del plugin
                del commands
                succ+=1
            except Exception as e:
                if id in self.plugin_enables:
                    self.plugin_enables.remove(id)
                if id in self.plugin_commands:
                    del self.plugin_commands[id]
                if id in self.plugin_auths:
                    uid=self.plugin_auths[id]['uid']
                    if uid in self.auths:
                        del self.auths[uid]
                    del uid
                    del self.plugin_auths[id]
                self.plugin_registers[id].status="error"
                logger.error(f"插件: {id} 出现错误")
                logger.exception(e)
                err+=1
        logger.debug(self.plugin_enables)
        logger.info(f"启用完成! 启用成功{succ}个插件，启用失败{err}个插件")
    
    def disable_plugins(self):
        logger.info("正在禁用插件...")
        succ=0
        err=0
        plugin_disables=[]
        for id in self.plugin_enables:
            try:
                disable=getattr(self.plugin_registers[id],self.plugin_methods[id]['disable']['func'])
                disable()
                self.plugin_registers[id].status="registered"
                plugin_disables.append(id)
                del disable
                del self.plugin_commands[id]
                uid=self.plugin_auths[id]['uid']
                del self.auths[uid]
                del uid
                del self.plugin_auths[id]
                succ+=1
            except Exception as e:
                self.plugin_registers[id]="error"
                logger.error(f"插件: {id} 出现错误")
                logger.exception(e)
                err+=1
        
        for id in plugin_disables:
            self.plugin_enables.remove(id)
        logger.info(f"禁用完成! 禁用成功{succ}个插件，禁用失败{err}个插件")
    
    def unregister_plugins(self):
        logger.info("正在注销插件...")
        succ=0
        err=0
        plugin_unregisters=[]
        for id in self.plugin_registers:
            try:
                if self.plugin_registers[id].status!="registered":
                    self.disable_plugins()
                unregister=getattr(self.plugin_registers[id],self.plugin_methods[id]['unregister']['func'])
                unregister()
                plugin_unregisters.append(id)
                del unregister
                succ+=1
            except Exception as e:
                logger.error(f"插件: {id} 出现错误")
                logger.exception(e)
                err+=1
        
        for id in plugin_unregisters:
            del self.plugin_registers[id]
            del self.plugin_methods[id]
            gc.collect()
        logger.info(f"注销完成! 注销成功{succ}个插件，注销失败{err}个插件")
    
    def unload_plugins(self):
        logger.info("正在卸载插件...")
        plugin_unloads=[]
        for id in self.plugin_infos:
            if id in self.plugin_enables:
                self.disable_plugins()
            if id in self.plugin_registers:
                self.unregister_plugins()
            plugin_unloads.append(id)
        
        for id in plugin_unloads:
            del self.plugin_infos[id]['info'].plugin
            info=self.plugin_infos[id]['info']
            del_modules=[]
            for module_name in sys.modules:
                if module_name.startswith('plugins.'+self.plugin_infos[id]['name']):
                    del_modules.append(module_name)
            for module_name in del_modules:
                del sys.modules[module_name]
            del self.plugin_infos[id]
            del info
        
        del_modules=[]
        for module_name in sys.modules:
            if module_name.startswith('plugins'):
                del_modules.append(module_name)
        for module_name in del_modules:
                del sys.modules[module_name]
        gc.collect()
        importlib.invalidate_caches()
        logger.info("卸载完成")
    
    def list_plugins(self):
        for id in self.plugin_infos:
            if id in self.plugin_registers:
                print("ID:",id,"状态:",self.plugin_registers[id].status,"插件名称:",self.plugin_infos[id]['info'].plugin_name,"插件版本:",self.plugin_infos[id]['info'].plugin_version)
            else:
                print("ID:",id,"状态: not register")
    
    def view_plugin(self,id):
        if id in self.plugin_registers:
            print("ID:",id)
            print("状态:",self.plugin_registers[id].status)
            print("插件名称:",self.plugin_infos[id]['info'].plugin_name)
            print("插件版本:",self.plugin_infos[id]['info'].plugin_version)
            print("插件作者:",self.plugin_infos[id]['info'].plugin_author)
            print("插件描述:",self.plugin_infos[id]['info'].plugin_desc)
            print("注册的方法:")
            for method in self.plugin_methods[id]:
                print(method,self.plugin_methods[id][method]['desc'])
            if id in self.plugin_enables:
                print("注册的命令:")
                for command in self.plugin_commands[id]:
                    print(command)
                print("申请的权限:")
                for auth in self.plugin_auths[id]['auths']:
                    print(auth,self.auth[auth])
        elif id in self.plugin_infos:
            print("ID:",id)
            print("状态:","not register")
            print("插件名称:",self.plugin_infos[id]['info'].plugin_name)
            print("插件版本:",self.plugin_infos[id]['info'].plugin_version)
            print("插件作者:",self.plugin_infos[id]['info'].plugin_author)
            print("插件描述:",self.plugin_infos[id]['info'].plugin_desc)
        else:
            print("没有这个插件")
    
    def load_plugin(self,filename):
        logger.info(f"加载插件: {filename}")
        if not os.path.isdir('plugins/'+filename):
            if filename.endswith('.py'):
                filename=filename[:-3]
            if os.path.isfile('plugins/'+filename+'.py.py'):
                filename+='.py'
            elif os.path.isfile('plugins/'+filename+'.py'):
                filename=filename
            else:
                logger.warning(f"插件 {filename} 不存在")
                return
        for id in self.plugin_infos:
            if filename==self.plugin_infos[id]['name']:
                logger.error(f"插件 {filename} 已经被加载")
                return
        try:
            if filename in variable.config['plugin']:
                if 'load' in variable.config['plugin'][filename]:
                    variable.config['plugin'][filename]['load']=True
                else:
                    variable.config['plugin'][filename]['load']=True
            else:
                variable.config['plugin'][filename]={'load':True}
            if 'plugins.'+filename in sys.modules:
                logger.warning(f"插件 {filename} 已经被加载")
                return
            plugin=importlib.import_module('plugins.'+filename)
            logger.debug(plugin)
            id=plugin.plugin_id
            name=plugin.plugin_name
            version=plugin.plugin_version
            author=plugin.plugin_author
            desc=plugin.plugin_desc
            info=PluginInfo(version,id,name,author,desc,plugin)
            self.plugin_infos[id]={'name':filename,'info':info}
            logger.info(f"加载成功: {filename}")
            del name
            del version
            del author
            del desc
            del id
            del plugin
            del info
        except Exception as e:
            id=""
            for plugin_id in self.plugin_infos:
                if filename == self.plugin_infos[plugin_id]['name']:
                    id=plugin_id
            if id!='':
                del self.plugin_infos[id]
            del_modules=[]
            for module_name in sys.modules:
                if module_name.startswith('plugins.'+filename):
                    del_modules.append(module_name)
            for module_name in del_modules:
                del sys.modules[module_name]
            logger.error(f"插件: {filename} 出现错误")
            logger.exception(e)
            logger.info(f"加载失败: {filename}")

    def register_plugin(self,id):
        logger.info(f"注册插件: {id}")
        if id in self.plugin_infos:
            try:
                if self.plugin_infos[id]['name'] in variable.config['plugin']:
                    if 'reg' in variable.config['plugin'][self.plugin_infos[id]['name']]:
                        variable.config['plugin'][self.plugin_infos[id]['name']]['reg']=True
                    else:
                        variable.config['plugin'][self.plugin_infos[id]['name']]['reg']=True
                else:
                    variable.config['plugin'][self.plugin_infos[id]['name']]={'reg':True}
                if id in self.plugin_registers:
                    logger.warning(f"插件 {id} 已经被注册")
                    return
                plugin=self.plugin_infos[id]['info'].plugin.Plugin()
                methods=plugin.plugin_methods
                self.plugin_methods[id]=methods
                plugin_logger=variable.log.getChild(self.plugin_infos[id]['info'].plugin_name)
                if not os.path.exists('data/'+id):
                    os.makedirs('data/'+id)
                data_dir=os.path.abspath('data/'+id)
                register=getattr(plugin,self.plugin_methods[id]['register']['func'])
                register(plugin_logger,variable.util,variable.bot,data_dir)
                plugin.status="registered"
                self.plugin_registers[id]=plugin
                del plugin
                del register
                del methods
                logger.info(f"注册成功: {id}")
            except Exception as e:
                if id in self.plugin_registers:
                    del self.plugin_registers[id]
                if id in self.plugin_methods:
                    del self.plugin_methods[id]
                logger.error(f"插件: {id} 出现错误")
                logger.exception(e)
                logger.info(f"注册失败: {id}")
        else:
            logger.error(f"插件: {id} 未加载")
        logger.debug(self.plugin_registers)

    def enable_plugin(self,id):
        logger.info(f"启用插件: {id}")
        if id in self.plugin_registers:
            try:
                if self.plugin_infos[id]['name'] in variable.config['plugin']:
                    if 'load' in variable.config['plugin'][self.plugin_infos[id]['name']]:
                        variable.config['plugin'][self.plugin_infos[id]['name']]['load']=True
                    else:
                        variable.config['plugin'][self.plugin_infos[id]['name']]['load']=True
                else:
                    variable.config['plugin'][self.plugin_infos[id]['name']]={'load':True}
                if id in self.plugin_enables:
                    logger.warning(f"插件 {id} 已经被启用")
                    return
                plugin=self.plugin_registers[id]
                commands=plugin.plugin_commands
                self.plugin_commands[id]=commands
                auths=plugin.plugin_auths
                uid=uuid.uuid4().hex
                self.plugin_auths[id]={'uid':uid,'auths':auths}
                self.auths[uid]=auths
                del auths
                enable=getattr(self.plugin_registers[id],self.plugin_methods[id]['enable']['func'])
                enable(uid)
                self.plugin_registers[id].status="enabled"
                self.plugin_enables.append(id)
                del uid
                del enable
                del plugin
                del commands
                logger.info(f"启用成功: {id}")
            except Exception as e:
                if id in self.plugin_commands:
                    del self.plugin_commands[id]
                if id in self.plugin_auths:
                    uid=self.plugin_auths[id]['uid']
                    if uid in self.auths:
                        del self.auths[uid]
                    del uid
                    del self.plugin_auths[id]
                if id in self.plugin_enables:
                    self.plugin_enables.remove(id)
                self.plugin_registers[id].status="error"
                logger.error(f"插件: {id} 出现错误")
                logger.exception(e)
                logger.info(f"启用失败: {id}")
        else:
            logger.error(f"插件: {id} 未注册")
        logger.debug(self.plugin_enables)
    
    def disable_plugin(self,id):
        logger.info(f"禁用插件: {id}")
        if id in self.plugin_enables:
            try:
                if self.plugin_infos[id]['name'] in variable.config['plugin']:
                    if 'load' in variable.config['plugin'][self.plugin_infos[id]['name']]:
                        variable.config['plugin'][self.plugin_infos[id]['name']]['load']=False
                    else:
                        variable.config['plugin'][self.plugin_infos[id]['name']]['load']=False
                else:
                    variable.config['plugin'][self.plugin_infos[id]['name']]={'load':False}
                disable=getattr(self.plugin_registers[id],self.plugin_methods[id]['disable']['func'])
                disable()
                self.plugin_registers[id].status="registered"
                del disable
                del self.plugin_commands[id]
                uid=self.plugin_auths[id]['uid']
                del self.auths[uid]
                del uid
                del self.plugin_auths[id]
                self.plugin_enables.remove(id)
                logger.info(f"禁用成功: {id}")
            except Exception as e:
                self.plugin_registers[id]="error"
                logger.error(f"插件: {id} 出现错误")
                logger.exception(e)
                logger.info(f"禁用失败: {id}")
        else:
            logger.error(f"插件: {id} 未启用")
    
    def unregister_plugin(self,id):
        logger.info(f"正在注销插件: {id}")
        if id in self.plugin_registers:
            try:
                if self.plugin_infos[id]['name'] in variable.config['plugin']:
                    if 'reg' in variable.config['plugin'][self.plugin_infos[id]['name']]:
                        variable.config['plugin'][self.plugin_infos[id]['name']]['reg']=False
                    else:
                        variable.config['plugin'][self.plugin_infos[id]['name']]['reg']=False
                else:
                    variable.config['plugin'][self.plugin_infos[id]['name']]={'reg':False}
                if self.plugin_registers[id].status!="registered":
                    self.disable_plugin(id)
                unregister=getattr(self.plugin_registers[id],self.plugin_methods[id]['unregister']['func'])
                unregister()
                p = self.plugin_registers[id]
                del p
                del self.plugin_registers[id]
                del self.plugin_methods[id]
                del unregister
                gc.collect()
                logger.info(f"注销成功: {id}")
            except Exception as e:
                logger.error(f"插件: {id} 出现错误")
                logger.exception(e)
                logger.info(f"注销失败: {id}")
        else:
            logger.error(f"插件: {id} 未注册")
            return
        
    
    def unload_plugin(self,id):
        logger.info("正在卸载插件...")
        if id in self.plugin_infos:
            if self.plugin_infos[id]['name'] in variable.config['plugin']:
                if 'load' in variable.config['plugin'][self.plugin_infos[id]['name']]:
                    variable.config['plugin'][self.plugin_infos[id]['name']]['load']=False
                else:
                    variable.config['plugin'][self.plugin_infos[id]['name']]['load']=False
            else:
                variable.config['plugin'][self.plugin_infos[id]['name']]={'load':False}
            if id in self.plugin_enables:
                self.disable_plugin(id)
            if id in self.plugin_registers:
                self.unregister_plugin(id)
            del self.plugin_infos[id]['info'].plugin
            info=self.plugin_infos[id]['info']
            del_modules=[]
            for module_name in sys.modules:
                if module_name.startswith('plugins.'+self.plugin_infos[id]['name']):
                    del_modules.append(module_name)
            for module_name in del_modules:
                del sys.modules[module_name]
            del self.plugin_infos[id]
            del info
        else:
            logger.error(f"插件 {id} 未加载")
        gc.collect()
        importlib.invalidate_caches()
        logger.info(f"卸载成功: {id}")
    
    def reload_plugin(self,id):
        name=""
        if id in self.plugin_infos:
            name=self.plugin_infos[id]['name']
        else:
            logger.error(f"插件 {id} 未加载")
        if id in self.plugin_enables:
            self.disable_plugin(id)
            self.unregister_plugin(id)
            self.unload_plugin(id)
            self.load_plugin(name)
            for plugin_id in self.plugin_infos:
                if name==self.plugin_infos[plugin_id]['name']:
                    id=plugin_id
            self.register_plugin(id)
            self.enable_plugin(id)
        elif id in self.plugin_registers:
            self.unregister_plugin(id)
            self.unload_plugin(id)
            self.load_plugin(name)
            for plugin_id in self.plugin_infos:
                if name==self.plugin_infos[plugin_id]['name']:
                    id=plugin_id
            self.register_plugin(id)
        else:
            self.unload_plugin(id)
            self.load_plugin(name)
        logger.info("重载完成")
    
    def processPluginCommand(self,cmd):
        for plugin in self.plugin_enables:
            for command in self.plugin_commands[plugin]:
                if command==cmd[0]:
                    logger.debug(f'命令匹配到 {plugin}')
                    process=getattr(self.plugin_registers[plugin],self.plugin_commands[plugin][command])
                    process(cmd[1:])
                    del process
