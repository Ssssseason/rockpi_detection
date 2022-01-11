# README

1. 运行`rockpi_detection.py`，输入用于登录的账号密码，生成各服务器状态到`states.txt`中

```bash
python rockpi_detection.py  --username rock --password rock > rockpi_d.log 2>&1&
```

需要监控的ip可以使用默认的列表，也可以通过命令行设置

2. 运行`app.py`，提供接口，展示各服务器状态

```
python app.py > app.log 2>&1&
```

默认地址为10.214.211.208:9999

