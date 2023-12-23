from flask import Flask, render_template, request
#调用库flask
from pythonosc import udp_client
#调用库pythonosc和udp_client
app = Flask(__name__)
client = None  # 创建一个全局变量
@app.route('/', methods=['GET', 'POST'])#接收来自GET和POST的表单数据
def home():
    global client
    if request.method == 'POST':     #如果接收到POST消息
        if 'message' in request.form:     #如果收到message的数据
            message = request.form['message']     #为message赋值获取的表单信息的message的数据
            typing = int(request.form['typing'])     #为typing赋值获取的表单信息的强制转换为整型的typing的数据
            client.send_message("/chatbox/input", [message, True, True])        #对OSC服务器发送消息
            client.send_message("/chatbox/typing", typing)        #对OSC服务器发送消息
            #消息格式可参考"https://docs.vrchat.com/docs/osc-as-input-controller"(官方帮助文档，推荐)
            #或"https://a2942.top:5904/a2942/OSC/"(自己根据上面的内容写的，可能有翻译错误的位置)

        if 'typing' in request.form:     #如果收到message的数据
            typing = int(request.form['typing'])     #为typing赋值获取的表单信息的强制转换为整型的typing的数据
            client.send_message("/chatbox/typing", typing)        #对OSC服务器发送消息
                
    return render_template('index.html')
oscip = "127.0.0.1" #OSC服务器的IP地址
oscport = "9000"    #OSC服务器的端口
webip = "0.0.0.0"   #WEB服务器的IP地址,"0.0.0.0"代表计算机的任何ip都可连接
webport = "5000"    #WEB服务器的端口
client = udp_client.SimpleUDPClient(oscip, int(oscport)) #准备好OSC客户端的UDP发送
app.run(debug=True, host=webip, port=webport) #运行在本地的网页服务器
