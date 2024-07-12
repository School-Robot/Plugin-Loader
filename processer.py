import logging
import json
from variable import variable
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s')
logger=logging.getLogger("Processer")
class Processer(object):
    
    def processMessage(self,msg):
        try:
            msg=json.loads(msg)
            if (not "echo" in msg) and (not "status" in msg):
                if msg['self_id']!=variable.bot_id:
                    pass
                else:
                    if msg['post_type']=='meta_event':
                        if msg['meta_event_type']=='lifecycle':
                            if msg['sub_type']=='connect':
                                logger.debug(f"WebSocket连接成功")
                            else:
                                logger.debug(msg)
                        elif msg['meta_event_type']=='heartbeat':
                            variable.bot.set_status(msg['status']['online'])
                        else:
                            logger.debug(msg)
                    elif msg['post_type']=='message':
                        if msg['message_type']=='private':
                            self.private_message(msg['time'],msg['self_id'],msg['sub_type'],msg['message_id'],msg['user_id'],msg['message'],msg['raw_message'],msg['font'],msg['sender'])
                        elif msg['message_type']=='group':
                            if msg['sub_type']!='anonymous':
                                msg['anonymous']=None
                            self.group_message(msg['time'],msg['self_id'],msg['sub_type'],msg['message_id'],msg['group_id'],msg['user_id'],msg['anonymous'],msg['message'],msg['raw_message'],msg['font'],msg['sender'])
                        else:
                            logger.debug(msg)
                    elif msg['post_type']=='notice':
                        if msg['notice_type']=='group_upload':
                            self.group_upload(msg['time'],msg['self_id'],msg['group_id'],msg['user_id'],msg['file'])
                        elif msg['notice_type']=='group_admin':
                            self.group_admin(msg['time'],msg['self_id'],msg['sub_type'],msg['group_id'],msg['user_id'])
                        elif msg['notice_type']=='group_decrease':
                            self.group_decrease(msg['time'],msg['self_id'],msg['sub_type'],msg['group_id'],msg['operator_id'],msg['user_id'])
                        elif msg['notice_type']=='group_increase':
                            self.group_increase(msg['time'],msg['self_id'],msg['sub_type'],msg['group_id'],msg['operator_id'],msg['user_id'])
                        elif msg['notice_type']=='group_ban':
                            self.group_ban(msg['time'],msg['self_id'],msg['sub_type'],msg['group_id'],msg['operator_id'],msg['user_id'],msg['duration'])
                        elif msg['notice_type']=='friend_add':
                            self.friend_add(msg['time'],msg['self_id'],msg['user_id'])
                        elif msg['notice_type']=='group_recall':
                            self.group_recall(msg['time'],msg['self_id'],msg['group_id'],msg['user_id'],msg['operator_id'],msg['message_id'])
                        elif msg['notice_type']=='friend_recall':
                            self.friend_recall(msg['time'],msg['self_id'],msg['user_id'],msg['message_id'])
                        elif msg['notice_type']=='notify':
                            if msg['sub_type']=='poke':
                                self.group_poke(msg['time'],msg['self_id'],msg['group_id'],msg['user_id'],msg['target_id'])
                            elif msg['sub_type']=='lucky_king':
                                self.lucky_king(msg['time'],msg['self_id'],msg['group_id'],msg['user_id'],msg['target_id'])
                            elif msg['sub_type']=='honor':
                                self.honor(msg['time'],msg['self_id'],msg['group_id'],msg['honor_type'],msg['user_id'])
                            else:
                                logger.debug(msg)                        
                        else:
                            logger.debug(msg)
                    elif msg['post_type']=='request':
                        if msg['request_type']=='friend':
                            self.friend_request(msg['time'],msg['self_id'],msg['user_id'],msg['comment'],msg['flag'])
                        elif msg['request_type']=='group':
                            self.group_request(msg['time'],msg['self_id'],msg['sub_type'],msg['group_id'],msg['user_id'],msg['comment'],msg['flag'])
                        else:
                            logger.debug(msg)
                    else:
                        logger.debug(msg)
            else:
                if 'echo' in msg:
                    variable.util.put_retmsg(msg)
                else:
                    logger.info(msg)
        except Exception as e:
            logger.error(f"消息处理出错: {msg}")
            logger.exception(e)
    
    def get_sorted_func(self,method):
        funcs={}
        for plugin in variable.loader.plugin_enables:
            if method in variable.loader.plugin_methods[plugin]:
                if hasattr(variable.loader.plugin_registers[plugin],variable.loader.plugin_methods[plugin][method]['func']):
                    try:
                        funcs[variable.loader.plugin_methods[plugin][method]['priority']].append((plugin,getattr(variable.loader.plugin_registers[plugin],variable.loader.plugin_methods[plugin][method]['func'])))
                    except:
                        funcs[variable.loader.plugin_methods[plugin][method]['priority']]=[(plugin,getattr(variable.loader.plugin_registers[plugin],variable.loader.plugin_methods[plugin][method]['func']))]
        return funcs
    
    def private_message(self,time,self_id,sub_type,message_id,user_id,message,raw_message,font,sender):
        funcs=self.get_sorted_func('private_message')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 private_message 方法")
                if plugin[1](time,self_id,sub_type,message_id,user_id,message,raw_message,font,sender) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def group_message(self,time,self_id,sub_type,message_id,group_id,user_id,anonymous,message,raw_message,font,sender):
        funcs=self.get_sorted_func('group_message')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 group_message 方法")
                if plugin[1](time,self_id,sub_type,message_id,group_id,user_id,anonymous,message,raw_message,font,sender) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def group_upload(self,time,self_id,group_id,user_id,file):
        funcs=self.get_sorted_func('group_upload')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 group_upload 方法")
                if plugin[1](time,self_id,group_id,user_id,file) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def group_admin(self,time,self_id,sub_type,group_id,user_id):
        funcs=self.get_sorted_func('group_admin')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 group_admin 方法")
                if plugin[1](time,self_id,sub_type,group_id,user_id) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def group_decrease(self,time,self_id,sub_type,group_id,operator_id,user_id):
        funcs=self.get_sorted_func('group_decrease')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 group_decrease 方法")
                if plugin[1](time,self_id,sub_type,group_id,operator_id,user_id) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
        
    def group_increase(self,time,self_id,sub_type,group_id,operator_id,user_id):
        funcs=self.get_sorted_func('group_increase')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 group_increase 方法")
                if plugin[1](time,self_id,sub_type,group_id,operator_id,user_id) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def group_ban(self,time,self_id,sub_type,group_id,operator_id,user_id,duration):
        funcs=self.get_sorted_func('group_ban')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 group_ban 方法")
                if plugin[1](time,self_id,sub_type,group_id,operator_id,user_id,duration) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def friend_add(self,time,self_id,user_id):
        funcs=self.get_sorted_func('friend_add')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 friend_add 方法")
                if plugin[1](time,self_id,user_id) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def group_recall(self,time,self_id,group_id,user_id,operator_id,message_id):
        funcs=self.get_sorted_func('group_recall')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 group_recall 方法")
                if plugin[1](time,self_id,group_id,user_id,operator_id,message_id) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def friend_recall(self,time,self_id,user_id,message_id):
        funcs=self.get_sorted_func('friend_recall')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 friend_recall 方法")
                if plugin[1](time,self_id,user_id,message_id) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def group_poke(self,time,self_id,group_id,user_id,target_id):
        funcs=self.get_sorted_func('group_poke')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 group_poke 方法")
                if plugin[1](time,self_id,group_id,user_id,target_id) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def lucky_king(self,time,self_id,group_id,user_id,target_id):
        funcs=self.get_sorted_func('lucky_king')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 lucky_king 方法")
                if plugin[1](time,self_id,group_id,user_id,target_id) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def honor(self,time,self_id,group_id,honor_type,user_id):
        funcs=self.get_sorted_func('honor')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 honor 方法")
                if plugin[1](time,self_id,group_id,honor_type,user_id) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def friend_request(self,time,self_id,user_id,comment,flag):
        funcs=self.get_sorted_func('friend_request')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 friend_request 方法")
                if plugin[1](time,self_id,user_id,comment,flag) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
    def group_request(self,time,self_id,sub_type,group_id,user_id,comment,flag):
        funcs=self.get_sorted_func('group_request')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 group_request 方法")
                if plugin[1](time,self_id,sub_type,group_id,user_id,comment,flag) and priority>10000:
                    logger.debug(f"插件 {plugin[0]} 阻塞了消息")
                    return
    
