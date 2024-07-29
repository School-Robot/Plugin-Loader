import json
import threading
from variable import variable

logger=variable.log.getChild("Processer")
class Processer(object):
    
    def processMessage(self,msg):
        try:
            msg=json.loads(msg)
            if msg['self_id']!=variable.bot_id:
                pass
            else:
                raw_thread=threading.Thread(target=self.raw_ws_process,args=(msg,))
                raw_thread.start()
                if "echo" in msg:
                    variable.util.put_retmsg(msg)
                elif "status" in msg:
                    if "meta_event_type" in msg and msg['meta_event_type']=='heartbeat':
                        variable.bot.set_status(msg['status']['online'])
                    else:
                        logger.info(f"返回信息: {msg}")
                else:
                    if msg['post_type']=='meta_event':
                        if msg['meta_event_type']=='lifecycle':
                            if msg['sub_type']=='connect':
                                logger.info(f"WebSocket连接成功")
                            else:
                                logger.debug(msg)
                        else:
                            logger.debug(msg)
                    elif msg['post_type']=='message':
                        if msg['message_type']=='private':
                            logger.info(f"收到 ({msg['user_id']}) 的私聊消息: {msg['raw_message']}")
                            self.private_message(msg['time'],msg['self_id'],msg['sub_type'],msg['message_id'],msg['user_id'],msg['message'],msg['raw_message'],msg['font'],msg['sender'])
                        elif msg['message_type']=='group':
                            logger.info(f"收到 [{msg['group_id']}]({msg['user_id']}) 在群 [{msg['group_id']}] 中的群消息: {msg['raw_message']}")
                            if msg['sub_type']!='anonymous':
                                msg['anonymous']=None
                            self.group_message(msg['time'],msg['self_id'],msg['sub_type'],msg['message_id'],msg['group_id'],msg['user_id'],msg['anonymous'],msg['message'],msg['raw_message'],msg['font'],msg['sender'])
                        else:
                            logger.debug(msg)
                    elif msg['post_type']=='notice':
                        if msg['notice_type']=='group_upload':
                            logger.info(f"({msg['user_id']}) 在群 [{msg['group_id']}] 中上传了文件: {msg['file']['name']}")
                            self.group_upload(msg['time'],msg['self_id'],msg['group_id'],msg['user_id'],msg['file'])
                        elif msg['notice_type']=='group_admin':
                            if msg['sub_type']=='set':
                                logger.info(f"({msg['user_id']}) 在群 [{msg['group_id']}] 中被设置为管理员")
                            else:
                                logger.info(f"({msg['user_id']}) 在群 [{msg['group_id']}] 中被取消管理员")
                            self.group_admin(msg['time'],msg['self_id'],msg['sub_type'],msg['group_id'],msg['user_id'])
                        elif msg['notice_type']=='group_decrease':
                            if msg['sub_type']=='leave':
                                logger.info(f"({msg['user_id']}) 在群 [{msg['group_id']}] 中离开了群")
                            elif msg['sub_type']=='kick_me':
                                logger.info(f"Bot 在群 [{msg['group_id']}] 中被踢出群")
                            else:
                                logger.info(f"({msg['user_id']}) 在群 [{msg['group_id']}] 中被 ({msg['operator_id']}) 踢出群")
                            self.group_decrease(msg['time'],msg['self_id'],msg['sub_type'],msg['group_id'],msg['operator_id'],msg['user_id'])
                        elif msg['notice_type']=='group_increase':
                            if msg['sub_type']=='approve':
                                logger.info(f"({msg['user_id']}) 在群 [{msg['group_id']}] 中通过了入群申请")
                            else:
                                logger.info(f"({msg['user_id']}) 在群 [{msg['group_id']}] 中被 ({msg['operator_id']}) 邀请入群")
                            self.group_increase(msg['time'],msg['self_id'],msg['sub_type'],msg['group_id'],msg['operator_id'],msg['user_id'])
                        elif msg['notice_type']=='group_ban':
                            if msg['sub_type']=='ban':
                                logger.info(f"({msg['user_id']}) 在群 [{msg['group_id']}] 中被 ({msg['operator_id']}) 禁言 {msg['duration']} 秒")
                            else:
                                logger.info(f"({msg['user_id']}) 在群 [{msg['group_id']}] 中被 ({msg['operator_id']}) 解除禁言")
                            self.group_ban(msg['time'],msg['self_id'],msg['sub_type'],msg['group_id'],msg['operator_id'],msg['user_id'],msg['duration'])
                        elif msg['notice_type']=='friend_add':
                            logger.info(f"({msg['user_id']}) 成为了好友")
                            self.friend_add(msg['time'],msg['self_id'],msg['user_id'])
                        elif msg['notice_type']=='group_recall':
                            logger.info(f"({msg['user_id']}) 在群 [{msg['group_id']}] 中撤回了消息")
                            self.group_recall(msg['time'],msg['self_id'],msg['group_id'],msg['user_id'],msg['operator_id'],msg['message_id'])
                        elif msg['notice_type']=='friend_recall':
                            logger.info(f"({msg['user_id']}) 撤回了消息")
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
                            logger.info(f"({msg['user_id']}) 请求添加好友")
                            self.friend_request(msg['time'],msg['self_id'],msg['user_id'],msg['comment'],msg['flag'])
                        elif msg['request_type']=='group':
                            logger.info(f"({msg['user_id']}) 请求加入群 [{msg['group_id']}]")
                            self.group_request(msg['time'],msg['self_id'],msg['sub_type'],msg['group_id'],msg['user_id'],msg['comment'],msg['flag'])
                        else:
                            logger.debug(msg)
                    else:
                        logger.debug(f"未知消息: {msg}")
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
                
    def raw_ws_process(self,msg):
        funcs=self.get_sorted_func('raw_ws_process')
        for priority in sorted(funcs.keys()):
            for plugin in funcs[priority]:
                logger.debug(f"正在调用优先级为 {priority} 中 {plugin[0]} 的 raw_ws_process 方法")
                plugin[1](msg)
