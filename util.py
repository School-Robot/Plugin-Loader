import json
import time
import uuid

from variable import variable

logger = variable.log.getChild("Util")


class Util(object):
    retmsg = {}

    def check_auth(self, auth, perm):
        try:
            if perm in variable.loader.auths[auth]:
                return True
            else:
                return False
        except Exception as e:
            logger.exception(e)
            return False

    def send_private_msg(self, auth, user_id, message, auto_escape=False, timeout=5):
        if self.check_auth(auth, 'send_private_msg'):
            if type(message) == str and message == "":
                return False, 'message is empty'
            if type(message) == list and len(message) == 0:
                return False, 'message is empty'
            uid = uuid.uuid4().hex
            m = {"action": "send_private_msg",
                 "params": {"user_id": user_id, "message": message, "auto_escape": auto_escape}, "echo": uid}
            logger.info(f"向 ({m['params']['user_id']}) 发送私聊消息: {m['params']['message']}")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def send_private_msg_async(self, auth, user_id, message, auto_escape=False):
        if self.check_auth(auth, 'send_private_msg'):
            if type(message) == str and message == "":
                return False, 'message is empty'
            if type(message) == list and len(message) == 0:
                return False, 'message is empty'
            m = {"action": "send_private_msg_async",
                 "params": {"user_id": user_id, "message": message, "auto_escape": auto_escape}}
            logger.info(f"向 ({m['params']['user_id']}) 发送私聊消息: {m['params']['message']}")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def send_private_msg_rate_limit(self, auth, user_id, message, auto_escape=False):
        if self.check_auth(auth, 'send_private_msg'):
            if type(message) == str and message == "":
                return False, 'message is empty'
            if type(message) == list and len(message) == 0:
                return False, 'message is empty'
            m = {"action": "send_private_msg_rate_limit",
                 "params": {"user_id": user_id, "message": message, "auto_escape": auto_escape}}
            logger.info(f"向 ({m['params']['user_id']}) 发送私聊消息: {m['params']['message']}")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def send_group_msg(self, auth, group_id, message, auto_escape=False, timeout=5):
        if self.check_auth(auth, 'send_group_msg'):
            if type(message) == str and message == "":
                return False, 'message is empty'
            if type(message) == list and len(message) == 0:
                return False, 'message is empty'
            uid = uuid.uuid4().hex
            m = {"action": "send_group_msg",
                 "params": {"group_id": group_id, "message": message, "auto_escape": auto_escape}, "echo": uid}
            logger.info(f"向 [{m['params']['group_id']}] 发送群消息: {m['params']['message']}")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def send_group_msg_async(self, auth, group_id, message, auto_escape=False):
        if self.check_auth(auth, 'send_group_msg'):
            if type(message) == str and message == "":
                return False, 'message is empty'
            if type(message) == list and len(message) == 0:
                return False, 'message is empty'
            m = {"action": "send_group_msg_async",
                 "params": {"group_id": group_id, "message": message, "auto_escape": auto_escape}}
            logger.info(f"向 [{m['params']['group_id']}] 发送群消息: {m['params']['message']}")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def send_group_msg_rate_limit(self, auth, group_id, message, auto_escape=False):
        if self.check_auth(auth, 'send_group_msg'):
            if type(message) == str and message == "":
                return False, 'message is empty'
            if type(message) == list and len(message) == 0:
                return False, 'message is empty'
            m = {"action": "send_group_msg_rate_limit",
                 "params": {"group_id": group_id, "message": message, "auto_escape": auto_escape}}
            logger.info(f"向 [{m['params']['group_id']}] 发送群消息: {m['params']['message']}")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def send_msg(self, auth, message_type, user_id, group_id, message, auto_escape=False, timeout=5):
        if self.check_auth(auth, 'send_msg'):
            if message_type == 'private' and user_id is None:
                return False, 'user_id is None'
            if message_type == 'group' and group_id is None:
                return False, 'group_id is None'
            if message_type is None and user_id is None and group_id is None:
                return False, 'message_type is None'
            if type(message) == str and message == "":
                return False, 'message is empty'
            if type(message) == list and len(message) == 0:
                return False, 'message is empty'
            if message_type == 'private':
                uid = uuid.uuid4().hex
                m = {"action": "send_msg",
                     "params": {"message_type": message_type, "user_id": user_id, "message": message,
                                "auto_escape": auto_escape}, "echo": uid}
                logger.info(f"向 ({m['params']['user_id']}) 发送私聊消息: {m['params']['message']}")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, ret['data']
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
            elif message_type == 'group':
                uid = uuid.uuid4().hex
                m = {"action": "send_msg",
                     "params": {"message_type": message_type, "group_id": group_id, "message": message,
                                "auto_escape": auto_escape}, "echo": uid}
                logger.info(f"向 [{m['params']['group_id']}] 发送群消息: {m['params']['message']}")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, ret['data']
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
            else:
                if user_id is None:
                    uid = uuid.uuid4().hex
                    m = {"action": "send_msg",
                         "params": {"group_id": group_id, "message": message, "auto_escape": auto_escape}, "echo": uid}
                    logger.info(f"向 [{m['params']['group_id']}] 发送群消息: {m['params']['message']}")
                    m = json.dumps(m)
                    variable.ws.send(m)
                    ret = self.waitFor(uid, timeout=timeout)
                    if ret['status'] == 'ok':
                        return True, ret['data']
                    elif ret['status'] == 'async':
                        return True, 'async'
                    elif ret['status'] == 'timeout':
                        return False, 'timeout'
                    else:
                        return False, 'error'
                elif group_id is None:
                    uid = uuid.uuid4().hex
                    m = {"action": "send_msg",
                         "params": {"user_id": user_id, "message": message, "auto_escape": auto_escape}, "echo": uid}
                    logger.info(f"向 ({m['params']['user_id']}) 发送私聊消息: {m['params']['message']}")
                    m = json.dumps(m)
                    variable.ws.send(m)
                    ret = self.waitFor(uid, timeout=timeout)
                    if ret['status'] == 'ok':
                        return True, ret['data']
                    elif ret['status'] == 'async':
                        return True, 'async'
                    elif ret['status'] == 'timeout':
                        return False, 'timeout'
                    else:
                        return False, 'error'
                else:
                    return False, 'message_type is None'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def send_msg_async(self, auth, message_type, user_id, group_id, message, auto_escape=False):
        if self.check_auth(auth, 'send_msg'):
            if message_type == 'private' and user_id is None:
                return False, 'user_id is None'
            if message_type == 'group' and group_id is None:
                return False, 'group_id is None'
            if message_type is None and user_id is None and group_id is None:
                return False, 'message_type is None'
            if type(message) == str and message == "":
                return False, 'message is empty'
            if type(message) == list and len(message) == 0:
                return False, 'message is empty'
            if message_type == 'private':
                m = {"action": "send_msg_async",
                     "params": {"message_type": message_type, "user_id": user_id, "message": message,
                                "auto_escape": auto_escape}}
                logger.info(f"向 ({m['params']['user_id']}) 发送私聊消息: {m['params']['message']}")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
            elif message_type == 'group':
                m = {"action": "send_msg_async",
                     "params": {"message_type": message_type, "group_id": group_id, "message": message,
                                "auto_escape": auto_escape}}
                logger.info(f"向 [{m['params']['group_id']}] 发送群消息: {m['params']['message']}")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
            else:
                if user_id is None:
                    m = {"action": "send_msg_async",
                         "params": {"group_id": group_id, "message": message, "auto_escape": auto_escape}}
                    logger.info(f"向 [{m['params']['group_id']}] 发送群消息: {m['params']['message']}")
                    m = json.dumps(m)
                    variable.ws.send(m)
                    return True, 'async'
                elif group_id is None:
                    m = {"action": "send_msg_async",
                         "params": {"user_id": user_id, "message": message, "auto_escape": auto_escape}}
                    logger.info(f"向 ({m['params']['user_id']}) 发送私聊消息: {m['params']['message']}")
                    m = json.dumps(m)
                    variable.ws.send(m)
                    return True, 'async'
                else:
                    return False, 'message_type is None'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def send_msg_rate_limit(self, auth, message_type, user_id, group_id, message, auto_escape=False):
        if self.check_auth(auth, 'send_msg'):
            if message_type == 'private' and user_id is None:
                return False, 'user_id is None'
            if message_type == 'group' and group_id is None:
                return False, 'group_id is None'
            if message_type is None and user_id is None and group_id is None:
                return False, 'message_type is None'
            if type(message) == str and message == "":
                return False, 'message is empty'
            if type(message) == list and len(message) == 0:
                return False, 'message is empty'
            if message_type == 'private':
                m = {"action": "send_msg_rate_limit",
                     "params": {"message_type": message_type, "user_id": user_id, "message": message,
                                "auto_escape": auto_escape}}
                logger.info(f"向 ({m['params']['user_id']}) 发送私聊消息: {m['params']['message']}")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
            elif message_type == 'group':
                m = {"action": "send_msg_rate_limit",
                     "params": {"message_type": message_type, "group_id": group_id, "message": message,
                                "auto_escape": auto_escape}}
                logger.info(f"向 [{m['params']['group_id']}] 发送群消息: {m['params']['message']}")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
            else:
                if user_id is None:
                    m = {"action": "send_msg_rate_limit",
                         "params": {"group_id": group_id, "message": message, "auto_escape": auto_escape}}
                    logger.info(f"向 [{m['params']['group_id']}] 发送群消息: {m['params']['message']}")
                    m = json.dumps(m)
                    variable.ws.send(m)
                    return True, 'async'
                elif group_id is None:
                    m = {"action": "send_msg_rate_limit",
                         "params": {"user_id": user_id, "message": message, "auto_escape": auto_escape}}
                    logger.info(f"向 ({m['params']['user_id']}) 发送私聊消息: {m['params']['message']}")
                    m = json.dumps(m)
                    variable.ws.send(m)
                    return True, 'async'
                else:
                    return False, 'message_type is None'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def delete_msg(self, auth, message_id, timeout=5):
        if self.check_auth(auth, 'delete_msg'):
            uid = uuid.uuid4().hex
            m = {"action": "delete_msg", "params": {"message_id": message_id}, "echo": uid}
            logger.info(f"撤回消息ID: {m['params']['message_id']}")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, 'success'
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def delete_msg_async(self, auth, message_id):
        if self.check_auth(auth, 'delete_msg'):
            m = {"action": "delete_msg_async", "params": {"message_id": message_id}}
            logger.info(f"撤回消息ID: {m['params']['message_id']}")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_msg(self, auth, message_id, timeout=5):
        if self.check_auth(auth, 'get_msg'):
            uid = uuid.uuid4().hex
            m = {"action": "get_msg", "params": {"message_id": message_id}, "echo": uid}
            logger.debug(f"获取消息ID: {m['params']['message_id']}")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_forward_msg(self, auth, id, timeout=5):
        if self.check_auth(auth, 'get_forward_msg'):
            uid = uuid.uuid4().hex
            m = {"action": "get_forward_msg", "params": {"id": id}, "echo": uid}
            logger.debug(f"获取合并转发消息ID: {m['params']['id']}")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def send_like(self, auth, user_id, times, timeout=5):
        if self.check_auth(auth, 'send_like'):
            if times > 10:
                times = 10
            if times < 1:
                times = 1
            uid = uuid.uuid4().hex
            m = {"action": "send_like", "params": {"user_id": user_id, "times": times}, "echo": uid}
            logger.info(f"向 ({m['params']['user_id']}) 发送赞: {m['params']['times']}")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, 'success'
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def send_like_async(self, auth, user_id, times):
        if self.check_auth(auth, 'send_like'):
            if times > 10:
                times = 10
            if times < 1:
                times = 1
            m = {"action": "send_like_async", "params": {"user_id": user_id, "times": times}}
            logger.info(f"向 ({m['params']['user_id']}) 发送赞: {m['params']['times']}")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_kick(self, auth, group_id, user_id, reject_add_request=False, timeout=5):
        if self.check_auth(auth, 'set_group_kick'):
            uid = uuid.uuid4().hex
            m = {"action": "set_group_kick",
                 "params": {"group_id": group_id, "user_id": user_id, "reject_add_request": reject_add_request},
                 "echo": uid}
            logger.info(f"将 ({m['params']['user_id']}) 移出群 [{m['params']['group_id']}]")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, 'success'
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_kick_async(self, auth, group_id, user_id, reject_add_request=False):
        if self.check_auth(auth, 'set_group_kick'):
            m = {"action": "set_group_kick_async",
                 "params": {"group_id": group_id, "user_id": user_id, "reject_add_request": reject_add_request}}
            logger.info(f"将 ({m['params']['user_id']}) 移出群 [{m['params']['group_id']}]")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_ban(self, auth, group_id, user_id, duration=30 * 60, timeout=5):
        if self.check_auth(auth, 'set_group_ban'):
            if duration > 2592000:
                duration = 2592000
            if duration < 0:
                duration = 0
            uid = uuid.uuid4().hex
            m = {"action": "set_group_ban", "params": {"group_id": group_id, "user_id": user_id, "duration": duration},
                 "echo": uid}
            logger.info(f"在 [{m['params']['group_id']}] 将 [{m['params']['user_id']}] 禁言 {m['params']['duration']} 秒")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, 'success'
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_ban_async(self, auth, group_id, user_id, duration=30 * 60):
        if self.check_auth(auth, 'set_group_ban'):
            if duration > 2592000:
                duration = 2592000
            if duration < 0:
                duration = 0
            m = {"action": "set_group_ban_async",
                 "params": {"group_id": group_id, "user_id": user_id, "duration": duration}}
            logger.info(f"在 [{m['params']['group_id']}] 将 [{m['params']['user_id']}] 禁言 {m['params']['duration']} 秒")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_anonymous_ban(self, auth, group_id, anonymous, anonymous_flag, duration=30 * 60, timeout=5):
        if self.check_auth(auth, 'set_group_anonymous_ban'):
            if duration > 2592000:
                duration = 2592000
            if duration < 0:
                duration = 0
            if anonymous is None and anonymous_flag is None:
                return False,
            if anonymous is None:
                uid = uuid.uuid4().hex
                m = {"action": "set_group_anonymous_ban",
                     "params": {"group_id": group_id, "anonymous_flag": anonymous_flag, "duration": duration},
                     "echo": uid}
                logger.info(
                    f"在 [{m['params']['group_id']}] 将匿名用户 {m['params']['anonymous_flag']} 禁言 {m['params']['duration']} 秒")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, 'success'
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
            else:
                uid = uuid.uuid4().hex
                m = {"action": "set_group_anonymous_ban",
                     "params": {"group_id": group_id, "anonymous": anonymous, "duration": duration}, "echo": uid}
                logger.info(
                    f"在 [{m['params']['group_id']}] 将匿名用户 ({m['params']['anonymous']['anonymous_flag']}) 禁言 {m['params']['duration']} 秒")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid)
                if ret['status'] == 'ok':
                    return True, 'success'
                elif ret['status'] == 'async':
                    return True, 'async'
                else:
                    return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_anonymous_ban_async(self, auth, group_id, anonymous, anonymous_flag, duration=30 * 60):
        if self.check_auth(auth, 'set_group_anonymous_ban'):
            if duration > 2592000:
                duration = 2592000
            if duration < 0:
                duration = 0
            if anonymous is None and anonymous_flag is None:
                return False,
            if anonymous is None:
                m = {"action": "set_group_anonymous_ban",
                     "params": {"group_id": group_id, "anonymous_flag": anonymous_flag, "duration": duration}}
                logger.info(
                    f"在 [{m['params']['group_id']}] 将匿名用户 {m['params']['anonymous_flag']} 禁言 {m['params']['duration']} 秒")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
            else:
                m = {"action": "set_group_anonymous_ban",
                     "params": {"group_id": group_id, "anonymous": anonymous, "duration": duration}}
                logger.info(
                    f"在 [{m['params']['group_id']}] 将匿名用户 ({m['params']['anonymous']['anonymous_flag']}) 禁言 {m['params']['duration']} 秒")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_whole_ban(self, auth, group_id, enable=True, timeout=5):
        if self.check_auth(auth, 'set_group_whole_ban'):
            uid = uuid.uuid4().hex
            m = {"action": "set_group_whole_ban", "params": {"group_id": group_id, "enable": enable}, "echo": uid}
            logger.info(f"在 [{m['params']['group_id']}] 设置全员禁言: {m['params']['enable']}")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, 'success'
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_whole_ban_async(self, auth, group_id, enable=True):
        if self.check_auth(auth, 'set_group_whole_ban'):
            m = {"action": "set_group_whole_ban_async", "params": {"group_id": group_id, "enable": enable}}
            logger.info(f"在 [{m['params']['group_id']}] 设置全员禁言: {m['params']['enable']}")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_admin(self, auth, group_id, user_id, enable=True, timeout=5):
        if self.check_auth(auth, 'set_group_admin'):
            uid = uuid.uuid4().hex
            m = {"action": "set_group_admin", "params": {"group_id": group_id, "user_id": user_id, "enable": enable},
                 "echo": uid}
            logger.info(f"在 [{m['params']['group_id']}] 设置管理员 ({m['params']['user_id']}) 状态: {m['params']['enable']}")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, 'success'
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_admin_async(self, auth, group_id, user_id, enable=True):
        if self.check_auth(auth, 'set_group_admin'):
            m = {"action": "set_group_admin_async",
                 "params": {"group_id": group_id, "user_id": user_id, "enable": enable}}
            logger.info(f"在 [{m['params']['group_id']}] 设置管理员 ({m['params']['user_id']}) 状态: {m['params']['enable']}")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_anonymous(self, auth, group_id, enable=True, timeout=5):
        if self.check_auth(auth, 'set_group_anonymous'):
            uid = uuid.uuid4().hex
            m = {"action": "set_group_anonymous", "params": {"group_id": group_id, "enable": enable}, "echo": uid}
            logger.info(f"在 [{m['params']['group_id']}] 设置匿名聊天状态: {m['params']['enable']}")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, 'success'
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_anonymous_async(self, auth, group_id, enable=True):
        if self.check_auth(auth, 'set_group_anonymous'):
            m = {"action": "set_group_anonymous_async", "params": {"group_id": group_id, "enable": enable}}
            logger.info(f"在 [{m['params']['group_id']}] 设置匿名聊天状态: {m['params']['enable']}")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_card(self, auth, group_id, user_id, card=None, timeout=5):
        if self.check_auth(auth, 'set_group_card'):
            if card is None:
                uid = uuid.uuid4().hex
                m = {"action": "set_group_card", "params": {"group_id": group_id, "user_id": user_id}, "echo": uid}
                logger.info(f"在 [{m['params']['group_id']}] 设置 ({m['params']['user_id']}) 群名片为空")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, 'success'
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
            else:
                uid = uuid.uuid4().hex
                m = {"action": "set_group_card", "params": {"group_id": group_id, "user_id": user_id, "card": card},
                     "echo": uid}
                logger.info(f"在 [{m['params']['group_id']}] 设置 ({m['params']['user_id']}) 群名片为: {m['params']['card']}")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, 'success'
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_card_async(self, auth, group_id, user_id, card=None):
        if self.check_auth(auth, 'set_group_card'):
            if card is None:
                m = {"action": "set_group_card_async", "params": {"group_id": group_id, "user_id": user_id}}
                logger.info(f"在 [{m['params']['group_id']}] 设置 ({m['params']['user_id']}) 群名片为空")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
            else:
                m = {"action": "set_group_card_async",
                     "params": {"group_id": group_id, "user_id": user_id, "card": card}}
                logger.info(f"在 [{m['params']['group_id']}] 设置 ({m['params']['user_id']}) 群名片为: {m['params']['card']}")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_name(self, auth, group_id, group_name, timeout=5):
        if self.check_auth(auth, 'set_group_name'):
            if group_name == "":
                return False, 'group_name is empty'
            uid = uuid.uuid4().hex
            m = {"action": "set_group_name", "params": {"group_id": group_id, "group_name": group_name}, "echo": uid}
            logger.info(f"在 [{m['params']['group_id']}] 设置群名为: {m['params']['group_name']}")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, 'success'
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_name_async(self, auth, group_id, group_name):
        if self.check_auth(auth, 'set_group_name'):
            if group_name == "":
                return False, 'group_name is empty'
            m = {"action": "set_group_name_async", "params": {"group_id": group_id, "group_name": group_name}}
            logger.info(f"在 [{m['params']['group_id']}] 设置群名为: {m['params']['group_name']}")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_leave(self, auth, group_id, is_dismiss=False, timeout=5):
        if self.check_auth(auth, 'set_group_leave'):
            uid = uuid.uuid4().hex
            m = {"action": "set_group_leave", "params": {"group_id": group_id, "is_dismiss": is_dismiss}, "echo": uid}
            logger.info(f"退出群 [{m['params']['group_id']}]")
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, 'success'
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_leave_async(self, auth, group_id, is_dismiss=False):
        if self.check_auth(auth, 'set_group_leave'):
            m = {"action": "set_group_leave_async", "params": {"group_id": group_id, "is_dismiss": is_dismiss}}
            logger.info(f"退出群 [{m['params']['group_id']}]")
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_special_title(self, auth, group_id, user_id, special_title=None, duration=-1, timeout=5):
        if self.check_auth(auth, 'set_group_special_title'):
            if special_title is None:
                uid = uuid.uuid4().hex
                m = {"action": "set_group_special_title", "params": {"group_id": group_id, "user_id": user_id},
                     "echo": uid}
                logger.info(f"在 [{m['params']['group_id']}] 设置 ({m['params']['user_id']}) 群头衔为空")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, 'success'
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
            else:
                uid = uuid.uuid4().hex
                m = {"action": "set_group_special_title",
                     "params": {"group_id": group_id, "user_id": user_id, "special_title": special_title,
                                "duration": duration}, "echo": uid}
                logger.info(
                    f"在 [{m['params']['group_id']}] 设置 ({m['params']['user_id']}) 群头衔为: {m['params']['special_title']}")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, 'success'
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_special_title_async(self, auth, group_id, user_id, special_title=None, duration=-1):
        if self.check_auth(auth, 'set_group_special_title'):
            if special_title is None:
                m = {"action": "set_group_special_title_async", "params": {"group_id": group_id, "user_id": user_id}}
                logger.info(f"在 [{m['params']['group_id']}] 设置 ({m['params']['user_id']}) 群头衔为空")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
            else:
                m = {"action": "set_group_special_title_async",
                     "params": {"group_id": group_id, "user_id": user_id, "special_title": special_title,
                                "duration": duration}}
                logger.info(
                    f"在 [{m['params']['group_id']}] 设置 ({m['params']['user_id']}) 群头衔为: {m['params']['special_title']}")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_friend_add_request(self, auth, flag, approve=True, remark=None, timeout=5):
        if self.check_auth(auth, 'set_friend_add_request'):
            if remark is None:
                uid = uuid.uuid4().hex
                m = {"action": "set_friend_add_request", "params": {"flag": flag, "approve": approve}, "echo": uid}
                logger.info(f"处理好友请求: {m['params']['flag']} {m['params']['approve']}")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, 'success'
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
            else:
                uid = uuid.uuid4().hex
                m = {"action": "set_friend_add_request", "params": {"flag": flag, "approve": approve, "remark": remark},
                     "echo": uid}
                logger.info(f"处理好友请求: {m['params']['flag']} {m['params']['approve']} {m['params']['remark']}")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, 'success'
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_friend_add_request_async(self, auth, flag, approve=True, remark=None):
        if self.check_auth(auth, 'set_friend_add_request'):
            if remark is None:
                m = {"action": "set_friend_add_request_async", "params": {"flag": flag, "approve": approve}}
                logger.info(f"处理好友请求: {m['params']['flag']} {m['params']['approve']}")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
            else:
                m = {"action": "set_friend_add_request_async",
                     "params": {"flag": flag, "approve": approve, "remark": remark}}
                logger.info(f"处理好友请求: {m['params']['flag']} {m['params']['approve']} {m['params']['remark']}")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_add_request(self, auth, flag, sub_type, approve=True, reason=None, timeout=5):
        if self.check_auth(auth, 'set_group_add_request'):
            if reason is None:
                uid = uuid.uuid4().hex
                m = {"action": "set_group_add_request",
                     "params": {"flag": flag, "sub_type": sub_type, "approve": approve}, "echo": uid}
                logger.info(f"处理加群请求: {m['params']['flag']} {m['params']['sub_type']} {m['params']['approve']}")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, 'success'
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
            else:
                uid = uuid.uuid4().hex
                m = {"action": "set_group_add_request",
                     "params": {"flag": flag, "sub_type": sub_type, "approve": approve, "reason": reason}, "echo": uid}
                logger.info(
                    f"处理加群请求: {m['params']['flag']} {m['params']['sub_type']} {m['params']['approve']} {m['params']['reason']}")
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, 'success'
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_group_add_request_async(self, auth, flag, sub_type, approve=True, reason=None):
        if self.check_auth(auth, 'set_group_add_request'):
            if reason is None:
                m = {"action": "set_group_add_request_async",
                     "params": {"flag": flag, "sub_type": sub_type, "approve": approve}}
                logger.info(f"处理加群请求: {m['params']['flag']} {m['params']['sub_type']} {m['params']['approve']}")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
            else:
                m = {"action": "set_group_add_request_async",
                     "params": {"flag": flag, "sub_type": sub_type, "approve": approve, "reason": reason}}
                logger.info(
                    f"处理加群请求: {m['params']['flag']} {m['params']['sub_type']} {m['params']['approve']} {m['params']['reason']}")
                m = json.dumps(m)
                variable.ws.send(m)
                return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_login_info(self, auth, timeout=5):
        if self.check_auth(auth, 'get_login_info'):
            uid = uuid.uuid4().hex
            m = {"action": "get_login_info", "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_stranger_info(self, auth, user_id, timeout=5):
        if self.check_auth(auth, 'get_stranger_info'):
            uid = uuid.uuid4().hex
            m = {"action": "get_stranger_info", "params": {"user_id": user_id}, "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_friend_list(self, auth, timeout=5):
        if self.check_auth(auth, 'get_friend_list'):
            uid = uuid.uuid4().hex
            m = {"action": "get_friend_list", "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_group_info(self, auth, group_id, no_cache=False, timeout=5):
        if self.check_auth(auth, 'get_group_info'):
            uid = uuid.uuid4().hex
            m = {"action": "get_group_info", "params": {"group_id": group_id, "no_cache": no_cache}, "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_group_list(self, auth, timeout=5):
        if self.check_auth(auth, 'get_group_list'):
            uid = uuid.uuid4().hex
            m = {"action": "get_group_list", "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_group_member_info(self, auth, group_id, user_id, no_cache=False, timeout=5):
        if self.check_auth(auth, 'get_group_member_info'):
            uid = uuid.uuid4().hex
            m = {"action": "get_group_member_info",
                 "params": {"group_id": group_id, "user_id": user_id, "no_cache": no_cache}, "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_group_member_list(self, auth, group_id, timeout=5):
        if self.check_auth(auth, 'get_group_member_list'):
            uid = uuid.uuid4().hex
            m = {"action": "get_group_member_list", "params": {"group_id": group_id}, "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_group_honor_info(self, auth, group_id, type, timeout=5):
        if self.check_auth(auth, 'get_group_honor_info'):
            uid = uuid.uuid4().hex
            m = {"action": "get_group_honor_info", "params": {"group_id": group_id, "type": type}, "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_cookies(self, auth, domain=None, timeout=5):
        if self.check_auth(auth, 'get_cookies'):
            if domain is None:
                uid = uuid.uuid4().hex
                m = {"action": "get_cookies", "echo": uid}
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, ret['data']
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
            else:
                uid = uuid.uuid4().hex
                m = {"action": "get_cookies", "params": {"domain": domain}, "echo": uid}
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, ret['data']
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_csrf_token(self, auth, timeout=5):
        if self.check_auth(auth, 'get_csrf_token'):
            uid = uuid.uuid4().hex
            m = {"action": "get_csrf_token", "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_credentials(self, auth, domain=None, timeout=5):
        if self.check_auth(auth, 'get_credentials'):
            if domain is None:
                uid = uuid.uuid4().hex
                m = {"action": "get_credentials", "echo": uid}
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, ret['data']
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
            else:
                uid = uuid.uuid4().hex
                m = {"action": "get_credentials", "params": {"domain": domain}, "echo": uid}
                m = json.dumps(m)
                variable.ws.send(m)
                ret = self.waitFor(uid, timeout=timeout)
                if ret['status'] == 'ok':
                    return True, ret['data']
                elif ret['status'] == 'async':
                    return True, 'async'
                elif ret['status'] == 'timeout':
                    return False, 'timeout'
                else:
                    return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_record(self, auth, file, out_format, timeout=5):
        if self.check_auth(auth, 'get_record'):
            uid = uuid.uuid4().hex
            m = {"action": "get_record", "params": {"file": file, "out_format": out_format}, "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_image(self, auth, file, timeout=5):
        if self.check_auth(auth, 'get_image'):
            uid = uuid.uuid4().hex
            m = {"action": "get_image", "params": {"file": file}, "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def can_send_image(self, timeout=5):
        uid = uuid.uuid4().hex
        m = {"action": "can_send_image", "echo": uid}
        m = json.dumps(m)
        variable.ws.send(m)
        ret = self.waitFor(uid, timeout=timeout)
        if ret['status'] == 'ok':
            return True, ret['data']
        elif ret['status'] == 'async':
            return True, 'async'
        elif ret['status'] == 'timeout':
            return False, 'timeout'
        else:
            return False, 'error'

    def can_send_record(self, timeout=5):
        uid = uuid.uuid4().hex
        m = {"action": "can_send_record", "echo": uid}
        m = json.dumps(m)
        variable.ws.send(m)
        ret = self.waitFor(uid, timeout=timeout)
        if ret['status'] == 'ok':
            return True, ret['data']
        elif ret['status'] == 'async':
            return True, 'async'
        elif ret['status'] == 'timeout':
            return False, 'timeout'
        else:
            return False, 'error'

    def get_status(self, auth, timeout=5):
        if self.check_auth(auth, 'get_status'):
            uid = uuid.uuid4().hex
            m = {"action": "get_status", "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_version_info(self, auth, timeout=5):
        if self.check_auth(auth, 'get_version_info'):
            uid = uuid.uuid4().hex
            m = {"action": "get_version_info", "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, ret['data']
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_restart(self, auth, delay=0, timeout=5):
        if self.check_auth(auth, 'set_restart'):
            uid = uuid.uuid4().hex
            m = {"action": "set_restart", "params": {"delay": delay}, "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, 'success'
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def set_restart_async(self, auth, delay=0):
        if self.check_auth(auth, 'set_restart'):
            m = {"action": "set_restart_async", "params": {"delay": delay}}
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def clear_cache(self, auth, timeout=5):
        if self.check_auth(auth, 'clear_cache'):
            uid = uuid.uuid4().hex
            m = {"action": "clear_cache", "echo": uid}
            m = json.dumps(m)
            variable.ws.send(m)
            ret = self.waitFor(uid, timeout=timeout)
            if ret['status'] == 'ok':
                return True, 'success'
            elif ret['status'] == 'async':
                return True, 'async'
            elif ret['status'] == 'timeout':
                return False, 'timeout'
            else:
                return False, 'error'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def clear_cache_async(self, auth):
        if self.check_auth(auth, 'clear_cache'):
            m = {"action": "clear_cache"}
            m = json.dumps(m)
            variable.ws.send(m)
            return True, 'async'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def plugin_control(self, auth, action, plugin):
        if self.check_auth(auth, 'plugin_control'):
            if action not in ['enable', 'disable', 'reload', 'load', 'unload', 'register', 'unregister']:
                return False, 'action is invalid'
            if action == "get_list":
                try:
                    plugin_list = variable.loader.get_plugin_list()
                    return True, plugin_list
                except Exception as e:
                    return False, str(e)
            if plugin == "":
                return False, 'plugin is empty'
            if action == "load":
                try:
                    variable.loader.load_plugin(plugin)
                    return True, 'success'
                except Exception as e:
                    return False, str(e)
            elif action == "unload":
                try:
                    variable.loader.unload_plugin(plugin)
                    return True, 'success'
                except Exception as e:
                    return False, str(e)
            elif action == "reload":
                try:
                    variable.loader.reload_plugin(plugin)
                    return True, 'success'
                except Exception as e:
                    return False, str(e)
            elif action == "register":
                try:
                    variable.loader.register_plugin(plugin)
                    return True, 'success'
                except Exception as e:
                    return False, str(e)
            elif action == "unregister":
                try:
                    variable.loader.unregister_plugin(plugin)
                    return True, 'success'
                except Exception as e:
                    return False, str(e)
            elif action == "enable":
                try:
                    variable.loader.enable_plugin(plugin)
                    return True, 'success'
                except Exception as e:
                    return False, str(e)
            elif action == "disable":
                try:
                    variable.loader.disable_plugin(plugin)
                    return True, 'success'
                except Exception as e:
                    return False, str(e)
            else:
                return False, 'action is invalid'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def send_ws_msg(self, auth, message):
        if self.check_auth(auth, 'send_ws_msg'):
            m = json.dumps(message)
            variable.ws.send(m)
            return True, 'success'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def get_ws_msg(self, auth, echo):
        if self.check_auth(auth, 'get_ws_msg'):
            if echo in self.retmsg:
                msg = self.retmsg[echo]
                del self.retmsg[echo]
                return True, msg
            else:
                return False, 'echo not found'
        else:
            logger.debug(f'插件权限不足')
            return False, 'Permission Denied'

    def waitFor(self, uid, timeout=5):
        start = time.time()
        while True:
            if time.time() - start > timeout:
                return {'status': 'timeout'}
            if uid in self.retmsg:
                msg = self.retmsg[uid]
                del self.retmsg[uid]
                return msg
            time.sleep(0.01)

    def put_retmsg(self, msg):
        self.retmsg[msg['echo']] = msg

    def escape(self, s):
        return s.replace('&', '&amp;').replace('[', '&#91;').replace(']', '&#93;').replace(',', '&#44;').replace('\n',
                                                                                                                 '\\n')

    def unescape(self, s):
        return s.replace('&amp;', '&').replace('&#91;', '[').replace('&#93;', ']').replace('&#44;', ',').replace('\\n',
                                                                                                                 '\n')

    def seg_text(self, text):
        return [{'type': 'text', 'data': {'text': text}}]

    def cq_text(self, text):
        return text

    def seg_face(self, id):
        return [{'type': 'face', 'data': {'id': id}}]

    def cq_face(self, id):
        return f'[CQ:face,id={id}]'

    def seg_image(self, file, type, cache=1, proxy=1, timeout=None):
        if file == "":
            return [{'type': 'text', 'data': {'text': '[图片]'}}]
        else:
            if file.startswith('http'):
                if type == "flash":
                    if timeout is None:
                        return [
                            {'type': 'image', 'data': {'file': file, 'type': 'flash', 'cache': cache, 'proxy': proxy}}]
                    else:
                        return [{'type': 'image',
                                 'data': {'file': file, 'type': 'flash', 'cache': cache, 'proxy': proxy,
                                          'timeout': timeout}}]
                else:
                    if timeout is None:
                        return [{'type': 'image', 'data': {'file': file, 'cache': cache, 'proxy': proxy}}]
                    else:
                        return [{'type': 'image',
                                 'data': {'file': file, 'cache': cache, 'proxy': proxy, 'timeout': timeout}}]
            else:
                if type == "flash":
                    return [{'type': 'image', 'data': {'file': file, 'type': 'flash'}}]
                else:
                    return [{'type': 'image', 'data': {'file': file}}]

    def cq_image(self, file, type, cache=1, proxy=1, timeout=None):
        if file == "":
            return '[图片]'
        else:
            if file.startswith('http'):
                if type == "flash":
                    return f'[CQ:image,file={file},type=flash,cache={cache},proxy={proxy}]'
                else:
                    return f'[CQ:image,file={file},cache={cache},proxy={proxy}]'
            else:
                return f'[CQ:image,file={file}]'

    def seg_record(self, file, magic=0, cache=1, proxy=1, timeout=None):
        if file == "":
            return [{'type': 'text', 'data': {'text': '[语音]'}}]
        else:
            if file.startswith('http'):
                if timeout is None:
                    return [{'type': 'record', 'data': {'file': file, 'magic': magic, 'cache': cache, 'proxy': proxy}}]
                else:
                    return [{'type': 'record', 'data': {'file': file, 'magic': magic, 'cache': cache, 'proxy': proxy,
                                                        'timeout': timeout}}]
            else:
                return [{'type': 'record', 'data': {'file': file, 'magic': magic}}]

    def cq_record(self, file, magic=0, cache=1, proxy=1, timeout=None):
        if file == "":
            return '[语音]'
        else:
            if file.startswith('http'):
                return f'[CQ:record,file={file},magic={magic},cache={cache},proxy={proxy}]'
            else:
                return f'[CQ:record,file={file},magic={magic}]'

    def seg_video(self, file, cache=1, proxy=1, timeout=None):
        if file == "":
            return [{'type': 'text', 'data': {'text': '[视频]'}}]
        else:
            if file.startswith('http'):
                if timeout is None:
                    return [{'type': 'video', 'data': {'file': file, 'cache': cache, 'proxy': proxy}}]
                else:
                    return [
                        {'type': 'video', 'data': {'file': file, 'cache': cache, 'proxy': proxy, 'timeout': timeout}}]
            else:
                return [{'type': 'video', 'data': {'file': file}}]

    def cq_video(self, file, cache=1, proxy=1, timeout=None):
        if file == "":
            return '[视频]'
        else:
            if file.startswith('http'):
                return f'[CQ:video,file={file},cache={cache},proxy={proxy}]'
            else:
                return f'[CQ:video,file={file}]'

    def seg_at(self, qq):
        return [{'type': 'at', 'data': {'qq': qq}}]

    def cq_at(self, qq):
        return f'[CQ:at,qq={qq}]'

    def seg_rps(self):
        return [{'type': 'rps', 'data': {}}]

    def cq_rps(self):
        return '[CQ:rps]'

    def seg_dice(self):
        return [{'type': 'dice', 'data': {}}]

    def cq_dice(self):
        return '[CQ:dice]'

    def seg_shake(self):
        return [{'type': 'shake', 'data': {}}]

    def cq_shake(self):
        return '[CQ:shake]'

    def seg_poke(self, type, id):
        return [{'type': 'poke', 'data': {'type': type, 'id': id}}]

    def cq_poke(self, type, id):
        return f'[CQ:poke,type={type},id={id}]'

    def seg_anonymous(self, ignore=0):
        return [{'type': 'anonymous', 'data': {'ignore': ignore}}]

    def cq_anonymous(self, ignore=0):
        return f'[CQ:anonymous,ignore={ignore}]'

    def seg_share(self, url, title, content, image):
        return [{'type': 'share', 'data': {'url': url, 'title': title, 'content': content, 'image': image}}]

    def cq_share(self, url, title, content, image):
        return f'[CQ:share,url={url},title={title},content={content},image={image}]'

    def seg_contact(self, type, id):
        return [{'type': 'contact', 'data': {'type': type, 'id': id}}]

    def cq_contact(self, type, id):
        return f'[CQ:contact,type={type},id={id}]'

    def seg_location(self, lat, lon, title=None, content=None):
        if title is None and content is None:
            return [{'type': 'location', 'data': {'lat': lat, 'lon': lon}}]
        else:
            if title is None:
                return [{'type': 'location', 'data': {'lat': lat, 'lon': lon, 'content': content}}]
            else:
                return [{'type': 'location', 'data': {'lat': lat, 'lon': lon, 'title': title}}]

    def cq_location(self, lat, lon, title, content):
        if title is None and content is None:
            return f'[CQ:location,lat={lat},lon={lon}]'
        else:
            if title is None:
                return f'[CQ:location,lat={lat},lon={lon},content={content}]'
            else:
                return f'[CQ:location,lat={lat},lon={lon},title={title}]'

    def seg_music(self, type, id=None, url=None, audio=None, title=None, content=None, image=None):
        if type == "custom":
            return [{'type': 'music',
                     'data': {'type': type, 'url': url, 'audio': audio, 'title': title, 'content': content,
                              'image': image}}]
        else:
            return [{'type': 'music', 'data': {'type': type, 'id': id}}]

    def cq_music(self, type, id, url, audio, title, content, image):
        if type == "custom":
            return f'[CQ:music,type=custom,url={url},audio={audio},title={title},content={content},image={image}]'
        else:
            return f'[CQ:music,type={type},id={id}]'

    def seg_reply(self, id):
        return [{'type': 'reply', 'data': {'id': id}}]

    def cq_reply(self, id):
        return f'[CQ:reply,id={id}]'

    def seg_node(self, id=None, user_id=None, nickname=None, content=None):
        if id is None:
            return [{'type': 'node', 'data': {'user_id': user_id, 'nickname': nickname, 'content': content}}]
        else:
            return [{'type': 'node', 'data': {'id': id}}]

    def cq_node(self, id, user_id, nickname, content):
        if id is None:
            return f'[CQ:node,user_id={user_id},nickname={nickname},content={content}]'
        else:
            return f'[CQ:node,id={id}]'

    def seg_xml(self, data):
        return [{'type': 'xml', 'data': {'data': data}}]

    def cq_xml(self, data):
        return f'[CQ:xml,data={data}]'

    def seg_json(self, data):
        return [{'type': 'json', 'data': {'data': data}}]

    def cq_json(self, data):
        return f'[CQ:json,data={data}]'
