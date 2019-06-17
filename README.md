# Books Management System(图书管理系统）

## 开发环境

- Python 3.6.5
- PyQt5==5.12.2
- MySQL 8.0

## 实现的功能

- 精美的交互界面，灵活的页面跳转
- 登录和注册功能
- 管理员图书入库，出库和批量入库功能
- 管理员删除普通用户功能
- 用户借书还书，查看借阅状态，修改密码，退出登录等功能
- 书籍查询功能

## 运行方式(Windows)

首先需要建立数据库，可自行安装MySQL，版本其实无所谓(数据库图形界面推荐MySQL WorkBench)  
自行创建新的schema： bookmanagement  
然后执行sqlQuery.txt中的语句  
App的运行方式为  
```
$ python mainWindow.py 
```

有兴趣的同学可以用pyinstaller打包成exe 

## 交互界面展示

更多交互界面可以看我的课程报告
<p align="center"><h1 align="center">登录界面</h1><img src="https://s2.ax1x.com/2019/06/17/VHuamF.png"></p>

## 感谢

我以前用c/c++写过一些Qt的东西，但是用pyqt还是第一次，十分感谢以下博客对我的帮助，感谢博主的辛勤付出！ 

 https://blog.csdn.net/weixin_38312031/column/info/22222 
