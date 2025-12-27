import os, sys, json, uuid
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory
from pythonosc import udp_client

def get_app_path():
    if getattr(sys, 'frozen', False): return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_app_path()
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
DATA_DIR = os.path.join(CONFIG_DIR, 'data')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.json')
os.makedirs(DATA_DIR, exist_ok=True)

DEFAULT_CONFIG = {
    "OSC_IP": "127.0.0.1", "OSC_PORT": 9000,
    "WEB_IP": "0.0.0.0", "WEB_PORT": 5000,
    "user_avatar": "", "system_avatar": "", "chat_bg_image": "",
    "user_avatar_color": "#6c5ce7", "system_avatar_color": "#00b894",
    "user_bubble_color": "#6c5ce7", "system_bubble_color": "#ffffff",
    "chat_bg_color": "#f5f7fa", "chat_bg_size": "cover",
    "theme_mode": "light", "primary_color": "#6c5ce7"
}

def load_config():
    if not os.path.exists(CONFIG_PATH): return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    except: return DEFAULT_CONFIG.copy()

def delete_file(filename):
    if filename:
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            try: os.remove(path)
            except: pass

app = Flask(__name__)
config = load_config()

# === OSC 客户端初始化与重连逻辑 ===
def init_osc(ip, port):
    try:
        print(f"[{datetime.now()}] 尝试连接 OSC: {ip}:{port}")
        return udp_client.SimpleUDPClient(ip, int(port))
    except: return None

osc_client = init_osc(config["OSC_IP"], config["OSC_PORT"])

@app.route('/data/<filename>')
def serve_data(filename):
    return send_from_directory(DATA_DIR, filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    global config, osc_client
    if request.method == 'POST':
        # 1. 发送消息逻辑
        if 'message' in request.form:
            msg = request.form.get('message', '').strip()
            typing = int(request.form.get('typing', 0))
            if osc_client:
                if msg: osc_client.send_message("/chatbox/input", [msg, True, True])
                osc_client.send_message("/chatbox/typing", bool(typing))
            return "ok"

        # 2. 发送输入状态逻辑
        if 'typing' in request.form and 'message' not in request.form:
            typing = int(request.form.get('typing', 0))
            if osc_client: osc_client.send_message("/chatbox/typing", bool(typing))
            return "ok"

        # 3. 保存配置逻辑
        if 'save_config' in request.form:
            new_config = config.copy()
            # 基础字段更新
            fields = ["OSC_IP", "OSC_PORT", "WEB_IP", "WEB_PORT", "user_avatar_color", 
                      "system_avatar_color", "user_bubble_color", "system_bubble_color", 
                      "chat_bg_color", "chat_bg_size", "theme_mode", "primary_color"]
            for key in fields:
                val = request.form.get(key.lower())
                if val is not None:
                    new_config[key] = int(val) if "PORT" in key else val

            # 图片管理逻辑 (物理删除 + 上传)
            for img_key in ['user_avatar', 'system_avatar', 'chat_bg_image']:
                should_remove = request.form.get(f'remove_{img_key}') == '1'
                new_file = request.files.get(img_key)
                has_new_file = new_file and new_file.filename != ''

                if should_remove or has_new_file:
                    delete_file(config.get(img_key))
                    new_config[img_key] = ""
                
                if has_new_file:
                    fname = f"{uuid.uuid4().hex}.{new_file.filename.rsplit('.', 1)[1].lower()}"
                    new_file.save(os.path.join(DATA_DIR, fname))
                    new_config[img_key] = fname

            # 持久化
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=4, ensure_ascii=False)
            
            # 检查是否需要重启 OSC 客户端
            if new_config["OSC_IP"] != config["OSC_IP"] or new_config["OSC_PORT"] != config["OSC_PORT"]:
                osc_client = init_osc(new_config["OSC_IP"], new_config["OSC_PORT"])
            
            config = new_config
            return "success"
            
    return render_template('index.html', config=config)

if __name__ == '__main__':
    app.run(host=config["WEB_IP"], port=config["WEB_PORT"])