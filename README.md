# Plugin Loader

## 介绍

Python编写的插件加载器，使用WebSocket客户端模式对接上游服务，支持OneBot协议，仿酷Q插件风格，目前处于测试状态，程序运行不稳定，如遇到问题请提issue

## 使用

### 安装依赖

```shell
pip install websocket-client -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 运行

运行`main.py`，首次运行需要配置相关信息

### 安装插件

将插件放入plugins文件夹中

### 命令界面

运行时可以输入命令，内置命令有`help`、`?`、`plugin`、`exit`

使用`plugin`可以对插件进行管理

## 开发

### 插件开发

请参考[开发文档](DEV.md)

### 加载器开发

提交issue或pr

## 致谢/参考

- [OneBot v11](https://11.onebot.dev)
- 酷Q
- 所有测试人员