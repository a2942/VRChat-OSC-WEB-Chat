# VRChat-OSC-WEB-Chat

用于便携式设备更方便的在浏览器对VRChat游戏发送聊天内容，**支持几乎任何可以打开浏览器的设备！**

# 让我们开始吧！

在运行**osc viewer.py**之前，您需要先安装\*\*[Python](https://www.python.org/)**，因为这是依赖**[Python](https://www.python.org/)\*\*运行的项目

1. 打开终端，例如**CMD**
2. 在终端输入：

   ```
    pip install pythonosc
   
   ```

   安装**pythonosc**的库
3. 继续在终端输入：

   ```
   pip install flask
   
   ```

   安装**flask**的库，实现在浏览器来发送消息需要靠它来**运行小型WEB服务器**
4. 下载这个项目，进入到 **VRChat-OSC-WEB-Chat-main/HTML osc chat** 文件夹内，输入：

   ```
   python osc_viewer.py
   
   ```
5. 在终端找到例如：

   ```
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:5000
    * Running on http://192.168.2.3:5000
   
   ```

   这些，在浏览器打开上面显示的 **http://192.168.2.3:5000** 就可以使用啦！
