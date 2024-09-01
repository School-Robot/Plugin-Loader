# 插件开发文档

## 插件信息

### 插件基本信息

- `plugin_name` 插件名称
- `plugin_version` 插件版本
- `plugin_id` 插件识别ID
- `plugin_author` 插件作者
- `plugin_desc` 插件描述

插件基本信息应直接暴露，加载器会在加载过程中读取

### 插件类

插件类命名为`Plugin`，应直接暴露，加载器会在注册过程中进行实例化

#### 类属性

- `plugin_methods` 类方法，必需
- `plugin_commands` 类命令，必需
- `plugin_auths` 类权限，必需
- `auth` 插件权限ID，必需
- `status` 插件状态，必需

#### 类方法

类方法使用字典表示，例如

```python
{
    'register':{
        'priority': 30000,
        'func': 'zhuce',
        'desc': '注册插件'
    },
    'enable':{
        'priority': 30000,
        'func': 'qiyong',
        'desc': '启用插件'
    }
}
```

其中`register`为标准方法名，加载器会根据标准方法名获取插件内方法，`priority`为优先级，值为数字，`func`为插件内方法名，`desc`为方法描述

标准方法名见[标准方法名](#标准方法名)

优先级见[优先级](#优先级)

方法信息见[方法信息](#方法信息)

#### 类命令

类命令使用字典表示，例如

```python
{
    'echo': 'echo_command',
    'help': 'echo <msg> - 向控制台输出消息'
}
```

命令使用空格分隔，其中`echo`为命令关键字，即第一个空格之前的内容，`echo_command`为命令处理函数，每个命令对应一个命令处理函数，命令会在去掉第一个参数后以数组形式传入，`help`为保留命令，对应值不会被认为是函数，`help`命令会被加载器拦截，并输出加载器内置命令及所有插件中`help`对应内容，如插件无命令请使用`{}`留空

#### 类权限

类权限使用集合表示，例如

```python
{'send_group_msg'}
```

集合中的每个元素对应一个权限，不申请权限请使用`{}`留空

权限列表见[API列表](#API列表)

#### 权限ID

权限ID为一串随机字符串，在启用插件时分配给插件，插件在调用需要权限的API时需传递权限ID以验证权限是否已经申请

#### 插件状态

插件状态为插件生命周期状态，在注册、启用、禁用时会改变

### 生命周期

插件的生命周期分为六个阶段，分别为加载、注册、启用、禁用、注销、卸载

- 加载：导入插件并加载插件基本信息
- 注册：实例化插件类，传入工具类等，读取插件方法，并调用`register`方法
- 启用：读取插件命令及权限，分配权限ID，并调用`enable`方法
- 禁用：调用`disable`方法，并删除插件命令及权限信息，删除权限ID
- 注销：调用`unregister`方法，并删除插件方法，销毁插件类
- 卸载：删除导入的插件，删除插件基本信息

插件启用前请不要调用工具类中的方法

### 标准方法名

|标准方法名|作用|是否必须|
|-|-|-|
|`register`|注册插件逻辑|是|
|`enable`|启用插件逻辑|是|
|`disable`|禁用插件逻辑|是|
|`unregister`|卸载插件逻辑|是|
|`private_message`|私聊消息处理|否|
|`group_message`|群消息处理|否|
|`group_upload`|群文件上传|否|
|`group_admin`|群管理员变动|否|
|`group_decrease`|群成员减少|否|
|`group_increase`|群成员增加|否|
|`group_ban`|群禁言|否|
|`friend_add`|好友添加|否|
|`group_recall`|群消息撤回|否|
|`friend_recall`|好友消息撤回|否|
|`group_poke`|群内戳一戳|否|
|`lucky_king`|群红包运气王|否|
|`honor`|群成员荣誉变更|否|
|`friend_request`|加好友请求|否|
|`group_request`|加群请求|否|
|`raw_ws_process`|处理原始WebSocket信息|否|

### 优先级

|优先级|值|说明|
|-|-|-|
|最高|10000|监控类应用，无法用于拦截消息。（如：消息数目统计等）|
|高|20000|消息控制类应用，可用于拦截消息。（如：机器人开关等）|
|一般|30000|普通功能类应用。（如：天气查询、游戏类等）|
|低|40000|聊天对话类应用。（如：词库、云词库）|

### 方法信息

#### `register`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`logger`|`object Logger`|-|日志，用于记录插件日志|
|`util`|`object Util`|-|工具类，用于调用API|
|`bot`|`object Bot`|-|Bot类，用于获取机器人基本信息|
|`data_dir`|`str`|-|插件数据目录，用于存放插件数据|

返回值

无

#### `enable`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|

返回值

无

#### `disable`

参数

无

返回值

无

#### `unregister`

参数

无

返回值

无

#### `private_message`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`sub_type`|`str`|`friend`、`group`、`other`|消息子类型，如果是好友则是`friend`，如果是群临时会话则是`group`|
|`message_id`|`int`|-|消息ID|
|`user_id`|`int`|-|发送者QQ号|
|`message`|`list`|-|消息内容|
|`raw_message`|`str`|-|原始消息内容|
|`font`|`int`|-|字体|
|`sender`|`dict`|-|发送人信息|

其中`sender`字段的内容如下：

|字段名|数据类型|说明|
|-|-|-|
|`user_id`|`int`|发送者QQ号|
|`nickname`|`str`|昵称|
|`sex`|`str`|性别，`male`或`female`或`unknown`|
|`age`|`int`|年龄|

根据OneBot协议，`sender`中的内容为尽可能提供，使用前请自行判断是否存在

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `group_message`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`sub_type`|`str`|`normal`、`anonymous`、`notice`|消息子类型，正常消息是`normal`，匿名消息是`anonymous`，系统提示（如「管理员已禁止群内匿名聊天」）是`notice`|
|`message_id`|`int`|-|消息ID|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|发送者QQ号|
|`anonymous`|`dict`|-|匿名信息，如果不是匿名消息则为`None`|
|`message`|`list`|-|消息内容|
|`raw_message`|`str`|-|原始消息内容|
|`font`|`int`|-|字体|
|`sender`|`dict`|-|发送人信息|

其中`anonymous`字段的内容如下：

|字段名|数据类型|说明|
|-|-|-|
|`id`|`int`|匿名用户ID|
|`name`|`str`|匿名用户名称|
|`flag`|`str`|匿名用户flag，在调用禁言API时需要传入|

`sender`字段的内容如下：

|字段名|数据类型|说明|
|-|-|-|
|`user_id`|`int`|发送者QQ号|
|`nickname`|`str`|昵称|
|`card`|`str`|群名片／备注|
|`sex`|`str`|性别，`male`或`female`或`unknown`|
|`age`|`int`|年龄|
|`area`|`str`|地区|
|`level`|`str`|成员等级|
|`role`|`str`|角色，`owner`或`admin`或`member`|
|`title`|`str`|专属头衔|

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `group_upload`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|发送者QQ号|
|`file`|`dict`|-|文件信息|

其中`file`字段的内容如下：

|字段名|数据类型|说明|
|-|-|-|
|`id`|`str`|文件ID|
|`name`|`str`|文件名|
|`size`|`int`|文件大小（字节数）|
|`busid`|`int`|busid（目前不清楚有什么作用）|

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `group_admin`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`sub_type`|`str`|`set`、`unset`|事件子类型，分别表示设置和取消管理员|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|管理员QQ号|

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `group_decrease`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`sub_type`|`str`|`leave`、`kick`、`kick_me`|事件子类型，分别表示主动退群、成员被踢、登录号被踢|
|`group_id`|`int`|-|群号|
|`operator_id`|`int`|-|操作者QQ号（如果是主动退群，则和`user_id`相同）|
|`user_id`|`int`|-|离开者QQ号|

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `group_increase`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`sub_type`|`str`|`approve`、`invite`|事件子类型，分别表示管理员已同意入群、管理员邀请入群|
|`group_id`|`int`|-|群号|
|`operator_id`|`int`|-|操作者QQ号（如果是主动退群，则和`user_id`相同）|
|`user_id`|`int`|-|加入者QQ号|

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `group_ban`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`sub_type`|`str`|`ban`、`lift_ban`|事件子类型，分别表示禁言、解除禁言|
|`group_id`|`int`|-|群号|
|`operator_id`|`int`|-|操作者QQ号|
|`user_id`|`int`|-|被禁言QQ号|
|`duration`|`int`|-|禁言时长，单位秒|

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `friend_add`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`user_id`|`int`|-|新添加好友QQ号

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `group_recall`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|消息发送者QQ号|
|`operator_id`|`int`|-|操作者QQ号|
|`message_id`|`int`|-|被撤回的消息ID|

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `friend_recall`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`user_id`|`int`|-|好友QQ号|
|`message_id`|`int`|-|被撤回的消息ID

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `group_poke`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|发送者QQ号|
|`target_id`|`int`|-|被戳者QQ号

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `lucky_king`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|红包发送者QQ号|
|`target_id`|`int`|-|运气王QQ号|

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `honor`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`group_id`|`int`|-|群号|
|`honor_type`|`str`|`talkative`、`performer`、`emotion`荣誉类型，分别表示龙王、群聊之火、快乐源泉|
|`user_id`|`int`|-|成员QQ号|

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `friend_request`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`user_id`|`int`|-|发送请求的QQ号|
|`comment`|`str`|-|验证信息|
|`flag`|`str`|-|请求flag，在调用处理请求的API时需要传入|

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `group_request`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`time`|`int`|-|事件发生时间|
|`self_id`|`int`|-|收到事件的机器人的QQ号|
|`sub_type`|`str`|`add`、`invite`|请求子类型，分别表示加群请求、邀请登录号入群|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|发送请求的QQ号|
|`comment`|`str`|-|验证信息|
|`flag`|`str`|-|请求flag，在调用处理请求的API时需要传入|

返回值

|返回类型|说明|
|-|-|
|`bool`|是否拦截消息，优先级小于等于`10000`时无法拦截|

#### `raw_ws_process`

参数

|字段名|数据类型|可能的值|说明|
|-|-|-|-|
|`msg`|`dict`|-|原始WebSocket消息|

返回值

无

### API列表

使用工具类`Util`进行API调用，接口的返回类型为元组，分别为状态和数据，对字符串和消息段处理的接口直接返回数据

|名称|是否需要权限|描述|
|-|-|-|
|`send_private_msg`|是|发送私聊消息|
|`send_group_msg`|是|发送群消息|
|`send_msg`|是|发送消息|
|`delete_msg`|是|撤回消息|
|`get_msg`|是|获取消息|
|`get_forward_msg`|是|获取合并转发消息|
|`send_like`|是|发送好友赞|
|`set_group_kick`|是|群组踢人|
|`set_group_ban`|是|群组单人禁言|
|`set_group_anonymous_ban`|是|群组匿名用户禁言|
|`set_group_whole_ban`|是|群组全员禁言|
|`set_group_admin`|是|群组设置管理员|
|`set_group_anonymous`|是|群组匿名|
|`set_group_card`|是|设置群名片|
|`set_group_name`|是|设置群名|
|`set_group_leave`|是|退出群组|
|`set_group_special_title`|是|设置群组专属头衔|
|`set_friend_add_request`|是|处理加好友请求|
|`set_group_add_request`|是|处理加群请求|
|`get_login_info`|是|获取登录号信息|
|`get_stranger_info`|是|获取陌生人信息|
|`get_friend_list`|是|获取好友列表|
|`get_group_info`|是|获取群信息|
|`get_group_list`|是|获取群列表|
|`get_group_member_info`|是|获取群成员信息|
|`get_group_member_list`|是|获取群成员列表|
|`get_group_honor_info`|是|获取群荣耀信息|
|`mark_private_msg_as_read`|是|NapCat扩展api,设置私聊消息已读|
|`get_cookies`|是|获取Cookies|
|`get_csrf_token`|是|获取CSRF Token|
|`get_credentials`|是|获取QQ相关接口凭证|
|`get_record`|是|获取语音|
|`get_image`|是|获取图片|
|`can_send_image`|否| 检查是否可以发送图片|
|`can_send_record`|否| 检查是否可以发送语音|
|`get_status`|是|获取运行状态|
|`get_version_info`|是|获取版本信息|
|`set_restart`|是|重启OneBot|
|`clean_cache`|是|清理缓存|
|`plugin_control`|是|插件控制|
|`send_ws_msg`|是|发送WebSocket消息|
|`get_ws_msg`|是|获取WebSocket返回内容|
|`escape`|否|转义字符|
|`unescape`|否|反转义字符|
|`seg_text`|否|文本消息段|
|`cq_text`|否|文本CQ码|
|`seg_face`|否|表情消息段|
|`cq_face`|否|表情CQ码|
|`seg_image`|否|图片消息段|
|`cq_image`|否|图片CQ码|
|`seg_record`|否|语音消息段|
|`cq_record`|否|语音CQ码|
|`seg_video`|否|视频消息段|
|`cq_video`|否|视频CQ码|
|`seg_at`|否|At消息段|
|`cq_at`|否|At CQ码|
|`seg_rps`|否|猜拳消息段|
|`cq_rps`|否|猜拳CQ码|
|`seg_dice`|否|骰子消息段|
|`cq_dice`|否|骰子CQ码|
|`seg_shake`|否|窗口抖动消息段|
|`cq_shake`|否|窗口抖动CQ码|
|`seg_poke`|否|戳一戳消息段|
|`cq_poke`|否|戳一戳CQ码|
|`seg_anonymous`|否|匿名消息段|
|`cq_anonymous`|否|匿名CQ码|
|`seg_share`|否|分享消息段|
|`cq_share`|否|分享CQ码|
|`seg_contact`|否|推荐消息段|
|`cq_contact`|否|推荐CQ码|
|`seg_location`|否|位置消息段|
|`cq_location`|否|位置CQ码|
|`seg_music`|否|音乐消息段|
|`cq_music`|否|音乐CQ码|
|`seg_reply`|否|回复消息段|
|`cq_reply`|否|回复CQ码|
|`seg_node`|否|转发消息段|
|`cq_node`|否|转发CQ码|
|`seg_xml`|否|XML消息段|
|`cq_xml`|否|XML CQ码|
|`seg_json`|否|JSON消息段|
|`cq_json`|否|JSON CQ码|


#### `send_private_msg`

参数

|字段名|数据类型|默认值|说明
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`user_id`|`int`|-|对方QQ号|
|`message`|`list`、`str`|-|要发送的内容，类型为`list`时以消息段发送，类型为`str`时以CQ码发送|
|`auto_escape`|`bool`|`False`|消息内容是否作为纯文本发送（即不解析 CQ 码），只在`message`字段是字符串时有效|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`message_id`|`int`|消息ID|

额外说明

支持`send_private_msg_async`，返回数据始终为`async`，无`timeout`参数

支持`send_private_msg_rate_limit`，返回数据始终为`async`，无`timeout`参数

#### `send_group_msg`

参数

|字段名|数据类型|默认值|说明
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`message`|`list`、`str`|-|要发送的内容，类型为`list`时以消息段发送，类型为`str`时以CQ码发送|
|`auto_escape`|`bool`|`False`|消息内容是否作为纯文本发送（即不解析 CQ 码），只在`message`字段是字符串时有效|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`message_id`|`int`|消息ID|

额外说明

支持`send_group_msg_async`，返回数据始终为`async`，无`timeout`参数

支持`send_group_msg_rate_limit`，返回数据始终为`async`，无`timeout`参数

#### `send_msg`

参数

|字段名|数据类型|默认值|说明
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`message_type`|`str`、`None`|-|消息类型，支持`private`、`group`，分别对应私聊、群组，如不传入，则根据传入的 *_id 参数判断|
|`user_id`|`int`、`None`|-|对方QQ号（消息类型为`private`时需要）|
|`group_id`|`int`、`None`|-|群号（消息类型为`group`时需要）|
|`message`|`list`、`str`|-|要发送的内容，类型为`list`时以消息段发送，类型为`str`时以CQ码发送|
|`auto_escape`|`bool`|`False`|消息内容是否作为纯文本发送（即不解析 CQ 码），只在`message`字段是字符串时有效|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`message_id`|`int`|消息ID|

额外说明

支持`send_msg_async`，返回数据始终为`async`，无`timeout`参数

支持`send_msg_rate_limit`，返回数据始终为`async`，无`timeout`参数

#### `delete_msg`

参数

|字段名|数据类型|默认值|说明
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`message_id`|`int`|-|消息ID|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`delete_msg_async`，返回数据始终为`async`，无`timeout`参数

#### `get_msg`

参数

|字段名|数据类型|默认值|说明
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`message_id`|`int`|-|消息ID|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`time`|`int`|发送时间|
|`message_type`|`private`、`group`|消息类型|
|`message_id`|`int`|消息ID|
|`real_id`|`int`|消息真实ID|
|`sender`|`dict`|发送人信息|
|`message`|`list`|消息内容|

其中`sender`字段的内容如下：

|字段名|数据类型|说明|
|-|-|-|
|`user_id`|`int`|发送者QQ号|
|`nickname`|`str`|昵称|
|`sex`|`str`|性别，`male`或`female`或`unknown`|
|`age`|`int`|年龄|

#### `get_forward_msg`

参数

|字段名|数据类型|默认值|说明
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`id`|`int`|-|合并转发ID|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`message`|`list`|消息内容|

#### `send_like`

参数

|字段名|数据类型|默认值|说明
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`user_id`|`int`|-|对方QQ号|
|`times`|`int`|`1`|赞的次数，每个好友每天最多 10 次|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`send_like_async`，返回数据始终为`async`，无`timeout`参数

#### `set_group_kick`

参数

|字段名|数据类型|默认值|说明
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|要踢的QQ号|
|`reject_add_request`|`bool`|`False`|拒绝此人的加群请求|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_group_kick_async`，返回数据始终为`async`，无`timeout`参数

#### `set_group_ban`

参数

|字段名|数据类型|默认值|说明
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|要禁言的QQ号|
|`duration`|`int`|`30*60`|禁言时长，单位秒，`0`表示取消禁言|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_group_ban_async`，返回数据始终为`async`，无`timeout`参数

#### `set_group_anonymous_ban`

参数

|字段名|数据类型|默认值|说明
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`anonymous`|`dict`、`None`|-|可选，要禁言的匿名用户对象（群消息上报的`anonymous`字段）|
|`anonymous_flag`|`str`、`None`|-|可选，要禁言的匿名用户的`flag`（需从群消息上报的数据中获得）|
|`duration`|`int`|`30*60`|禁言时长，单位秒，无法取消匿名用户禁言|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

上面的`anonymous`和`anonymous_flag`两者任选其一传入即可，若都传入，则使用 anonymous。

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_group_anonymous_ban_async`，返回数据始终为`async`，无`timeout`参数

#### `set_group_whole_ban`

参数

|字段名|数据类型|默认值|说明
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`enable`|`bool`|`True`|是否禁言|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_group_whole_ban_async`，返回数据始终为`async`，无`timeout`参数

#### `set_group_admin`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-群号|
|`user_id`|`int`|-|要设置管理员的QQ号|
|`enable`|`bool`|`True`|`True`为设置，`False` 为取消|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_group_admin_async`，返回数据始终为`async`，无`timeout`参数

#### `set_group_anonymous`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`enable`|`bool`|`True`|是否允许匿名聊天|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_group_admin_async`，返回数据始终为`async`，无`timeout`参数

#### `set_group_card`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|要设置的QQ号|
|`card`|`str`|空|群名片内容，不填或空字符串表示删除群名片|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_group_card_async`，返回数据始终为`async`，无`timeout`参数

#### `set_group_name`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`group_name`|`str`|-|新群名|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_group_name_async`，返回数据始终为`async`，无`timeout`参数

#### `set_group_leave`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`is_dismiss`|`bool`|`False`|是否解散，如果登录号是群主，则仅在此项为`true`时能够解散|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_group_leave_async`，返回数据始终为`async`，无`timeout`参数

#### `set_group_special_title`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|要设置的QQ号|
|`special_title`|`str`|空|专属头衔，不填或空字符串表示删除专属头衔|
|`duration`|`int`|-1|专属头衔有效期，单位秒，`-1`表示永久，不过此项似乎没有效果，可能是只有某些特殊的时间长度有效，有待测试|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_group_special_async`，返回数据始终为`async`，无`timeout`参数

#### `set_friend_add_request`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`flag`|`str`|-|加好友请求的`flag`（需从上报的数据中获得）|
|`approve`|`bool`|`True`|是否同意请求|
|`remark`|`str`|空|添加后的好友备注（仅在同意时有效）|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_friend_add_request_async`，返回数据始终为`async`，无`timeout`参数

#### `set_group_add_request`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`flag`|`str`|-|加群请求的`flag`（需从上报的数据中获得）|
|`sub_type`|`str`|-|`add`或`invite`，请求类型（需要和上报消息中的`sub_type`字段相符）|
|`approve`|`bool`|`True`|是否同意请求／邀请|
|`reason`|`str`|空|拒绝理由（仅在拒绝时有效）|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`set_group_add_request_async`，返回数据始终为`async`，无`timeout`参数

#### `get_login_info`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`user_id`|`int`|QQ号|
|`nickname`|`str`|QQ昵称|

#### `get_stranger_info`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`user_id`|`int`|-|QQ号|
|`no_cache`|`bool`|`False`|是否不使用缓存（使用缓存可能更新不及时，但响应更快）|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|


数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`user_id`|`int`|QQ号|
|`nickname`|`str`|QQ昵称|
|`sex`|`str`|性别，`male`或`female`或`unknown`|
|`age`|`int`|年龄|

#### `get_friend_list`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`list<dict>`、`str`|返回`list<dict>`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`user_id`|`int`|QQ号|
|`nickname`|`str`|QQ昵称|
|`remark`|`str`|备注名|

#### `get_group_info`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`no_cache`|`bool`|`False`|是否不使用缓存（使用缓存可能更新不及时，但响应更快）|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`group_id`|`int`|群号|
|`group_name`|`str`|群名称|
|`member_count`|`int`|成员数|
|`max_member_count`|`int`|最大成员数（群容量）|

#### `get_group_list`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`no_cache`|`bool`|`False`|是否不使用缓存（使用缓存可能更新不及时，但响应更快）|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`list<dict>`、`str`|返回`list<dict>`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`group_id`|`int`|群号|
|`group_name`|`str`|群名称|
|`member_count`|`int`|成员数|
|`max_member_count`|`int`|最大成员数（群容量）|

#### `get_group_member_info`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`user_id`|`int`|-|QQ号|
|`no_cache`|`bool`|`False`|是否不使用缓存（使用缓存可能更新不及时，但响应更快）|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`group_id`|`int`|群号|
|`user_id`|`int`|QQ号|
|`nickname`|`str`|昵称|
|`card`|`str`|群名片／备注|
|`sex`|`str`|性别，`male`或`female`或`unknown`|
|`age`|`int`|年龄|
|`area`|`str`|地区|
|`join_time`|`int`|加群时间戳|
|`last_sent_time`|`int`|最后发言时间戳|
|`level`|`str`|成员等级|
|`role`|`str`|角色，`owner`或`admin`或`member`|
|`unfriendly`|`bool`|是否不良记录成员|
|`title`|`str`|专属头衔|
|`title_expire_time`|`int`|专属头衔过期时间戳|
|`card_changeable`|`bool`|是否允许修改群名片|

#### `get_group_member_list`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`list<dict>`、`str`|返回`list<dict>`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`group_id`|`int`|群号|
|`user_id`|`int`|QQ号|
|`nickname`|`str`|昵称|
|`card`|`str`|群名片／备注|
|`sex`|`str`|性别，`male`或`female`或`unknown`|
|`age`|`int`|年龄|
|`area`|`str`|地区|
|`join_time`|`int`|加群时间戳|
|`last_sent_time`|`int`|最后发言时间戳|
|`level`|`str`|成员等级|
|`role`|`str`|角色，`owner`或`admin`或`member`|
|`unfriendly`|`bool`|是否不良记录成员|
|`title`|`str`|专属头衔|
|`title_expire_time`|`int`|专属头衔过期时间戳|
|`card_changeable`|`bool`|是否允许修改群名片|

额外说明

对于同一个群组的同一个成员，获取列表时和获取单独的成员信息时，某些字段可能有所不同，例如`area`、`title`等字段在获取列表时无法获得，具体应以单独的成员信息为准。

#### `get_group_honor_info`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`group_id`|`int`|-|群号|
|`type`|`str`|-|要获取的群荣誉类型，可传入`talkative`、`performer`、`legend`、`strong_newbie`、`emotion`以分别获取单个类型的群荣誉数据，或传入`all`获取所有数据
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`group_id`|`int`|群号|
|`current_talkative`|`dict`|当前龙王，仅`type`为`talkative`或`all`时有数据|
|`talkative_list`|`list<dict>`|历史龙王，仅`type`为`talkative`或`all`时有数据|
|`performer_list`|`list<dict>`|群聊之火，仅`type`为`performer`或`all`时有数据|
|`legend_list`|`list<dict>`|群聊炽焰，仅`type`为`legend`或`all`时有数据|
|`strong_newbie_list`|`list<dict>`|冒尖小春笋，仅`type`为`strong_newbie`或`all`时有数据|
|`emotion_list`|`list<dict>`|快乐之源，仅`type`为`emotion`或`all`时有数据|

其中`current_talkative`字段的内容如下：

|字段名|数据类型|说明|
|-|-|-|
|`user_id`|`int`|QQ号|
|`nickname`|`str`|昵称|
|`avatar`|`str`|头像URL|
|`day_count`|`int`|持续天数|

其它各`*_list`字段的内容如下：

|字段名|数据类型|说明|
|-|-|-|
|`user_id`|`int`|QQ号|
|`nickname`|`str`|昵称|
|`avatar`|`str`|头像URL|
|`description`|`str`|荣誉描述|

#### `mark_private_msg_as_read`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`user_id`|`int`|-|QQ号|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

此api为[NapCatQQ](https://github.com/NapNeko/NapCatQQ)的[扩展api](https://napneko.github.io/zh-CN/develop/extends_api)

#### `get_cookies`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`domain`|`str`|空|需要获取`cookies`的域名|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`cookies`|`str`|Cookies|

#### `get_csrf_token`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`token`|`int`|CSRF Token|

#### `get_credentials`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`domain`|`str`|空|需要获取`cookies`的域名|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`cookies`|`str`|Cookies|
|`token`|`int`|CSRF Token|

#### `get_record`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`file`|`str`|-|收到的语音文件名（消息段的`file`参数），如`0B38145AA44505000B38145AA4450500.silk`|
|`out_format`|`str`|-|要转换到的格式，目前支持`mp3`、`amr`、`wma`、`m4a`、`spx`、`ogg`、`wav`、`flac`|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`file`|`str`|转换后的语音文件路径，如`/home/somebody/cqhttp/data/record/0B38145AA44505000B38145AA4450500.mp3`|

#### `get_image`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`file`|`str`|-|收到的图片文件名（消息段的`file`参数），如`6B4DE3DFD1BD271E3297859D41C530F5.jpg`|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`file`|`str`|下载后的图片文件路径，如`/home/somebody/cqhttp/data/image/6B4DE3DFD1BD271E3297859D41C530F5.jpg`|

#### `can_send_image`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`yes`|`bool`|是或否|

#### `can_send_record`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`yes`|`bool`|是或否|

#### `get_status`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`online`|`bool`|当前QQ在线，`None`表示无法查询到在线状态|
|`good`|`bool`|状态符合预期，意味着各模块正常运行、功能正常，且QQ在线|
|`……`|-|OneBot实现自行添加的其它内容|

额外说明

通常情况下建议只使用`online`和`good`这两个字段来判断运行状态，因为根据OneBot实现的不同，其它字段可能完全不同。

#### `get_version_info`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

数据内容

|字段名|类型|说明|
|-|-|-|
|`app_name`|`str`|应用标识，如`mirai-native`|
|`app_version`|`str`|应用版本，如`1.2.3`|
|`protocol_version`|`str`|OneBot标准版本，如`v11`|
|`……`|-|OneBot实现自行添加的其它内容|

#### `set_restart`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`delay`|`int`|`0`|要延迟的毫秒数，如果默认情况下无法重启，可以尝试设置延迟为`2000`左右|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

通常为`async`

额外说明

支持`set_restart_async`，返回数据始终为`async`，无`timeout`参数

#### `clean_cache`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`timeout`|`int`|`5`|获取返回数据超时时间，单位为秒|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

额外说明

支持`clean_cache_async`，返回数据始终为`async`，无`timeout`参数

#### `plugin_control`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`action`|`str`|-|操作，包括`load`、`register`、`enable`、`disable`、`unregister`、`unload`分别对应生命周期,`reload`重载,`get_list`获取插件列表|
|`plugin`|`str`|-|操作为`load`时为文件名或目录名，其他为ID|

数据返回值

|类型|说明|
|-|-|
|`str`、`dict`|状态说明，返回值为`dict`时为数据内容|

数据内容

|字段名|类型|说明|
|-|-|-|
|`infos`|`dict`|插件加载原始信息|
|`methods`|`dict`|插件注册的方法|
|`registers`|`dict`|注册的插件信息|
|`enables`|`list`|启用的插件列表|
|`commands`|`dict`|插件注册的命令|
|`auths`|`dict`|插件注册的权限|

#### `send_ws_msg`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`message`|`str`|-|发送的消息|

数据返回值

|类型|说明|
|-|-|
|`str`|状态说明|

通常为`success`

额外说明

若需要取回返回内容，请在发送的消息中加入`echo`字段，使用`get_ws_msg`取回

#### `get_ws_msg`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`auth`|`str`|-|权限ID|
|`echo`|`str`|-|标识|

数据返回值

|类型|说明|
|-|-|
|`dict`、`str`|返回`dict`时为返回的数据，返回`str`时为状态说明|

#### `escape`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`s`|`str`|-|需要转义的字符串|

数据返回值

|类型|说明|
|-|-|
|`str`|转义后的字符串|

转义说明

|转义前|转义后|
|-|-|
|`&`|`&amp;`|
|`[`|`&#91;`|
|`]`|`&#93;`|
|`,`|`&#44;`|
|`\n`|`\\n`|

#### `unescape`

参数

|字段名|数据类型|默认值|说明|
|-|-|-|-|
|`s`|`str`|-|需要反转义的字符串|

数据返回值

|类型|说明|
|-|-|
|`str`|反转义后的字符串|

转义说明

|转义前|转义后|
|-|-|
|`&`|`&amp;`|
|`[`|`&#91;`|
|`]`|`&#93;`|
|`,`|`&#44;`|
|`\n`|`\\n`|

#### `seg_*`

将消息转换为消息段

#### `cq_*`

将消息转换为CQ码

### Bot类

|名称|描述|
|-|-|
|`get_status`|获取Bot状态|
|`get_id`|获取Bot QQ号|
|`set_status`|设置Bot状态|