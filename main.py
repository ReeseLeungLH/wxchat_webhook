import os
import yaml
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 加载配置
def load_config():
    # 默认配置
    config = {
        'WECOM_CORPID': None,
        'WECOM_AGENTID': None,
        'WECOM_APPSEC': None,
        'AUTH_TOKEN': None
    }
    
    # 尝试从 config.yaml 加载配置
    try:
        # 【修改点】显式指定 encoding='utf-8' 以兼容 Windows
        with open('config.yaml', 'r', encoding='utf-8') as f:
            yaml_config = yaml.safe_load(f)
            if yaml_config:
                config.update(yaml_config)
    except FileNotFoundError:
        print("config.yaml not found, using environment variables.")
        pass
    except Exception as e:
        print(f"Error loading config.yaml: {e}")
        pass

    # 环境变量会覆盖配置文件中的设置
    config['WECOM_CORPID'] = os.getenv('WECOM_CORPID', config.get('WECOM_CORPID'))
    config['WECOM_AGENTID'] = os.getenv('WECOM_AGENTID', config.get('WECOM_AGENTID'))
    config['WECOM_APPSEC'] = os.getenv('WECOM_APPSEC', config.get('WECOM_APPSEC'))
    config['AUTH_TOKEN'] = os.getenv('AUTH_TOKEN', config.get('AUTH_TOKEN'))

    # 检查必要的配置是否存在
    if not all([config['WECOM_CORPID'], config['WECOM_AGENTID'], config['WECOM_APPSEC'], config['AUTH_TOKEN']]):
        raise ValueError("Missing necessary configuration for WeCom or AUTH_TOKEN.")
        
    return config

config = load_config()

# 全局变量存储 access_token
access_token = None

def get_access_token():
    global access_token
    # 实际场景中应该考虑 token 过期时间，这里简化处理
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={config['WECOM_CORPID']}&corpsecret={config['WECOM_APPSEC']}"
    response = requests.get(url)
    data = response.json()
    if data.get("access_token"):
        access_token = data["access_token"]
        print("Access token refreshed successfully.")
        return access_token
    else:
        raise Exception(f"Failed to get access token: {data}")

def send_wecom_message(content):
    global access_token
    if not access_token:
        get_access_token()

    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    payload = {
        "touser": "@all",
        "msgtype": "markdown",
        "agentid": config['WECOM_AGENTID'],
        "markdown": {
            "content": content
        }
    }
    
    response = requests.post(url, json=payload)
    return response.json()

@app.route('/health', methods=['GET'])
def health_check():
    # 只要 Flask 能处理这个请求，就说明服务是活着的
    return jsonify({"status": "ok"}), 200

@app.route('/', methods=['POST'])
def webhook():
    # 鉴权
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f"Bearer {config['AUTH_TOKEN']}":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "Invalid payload, 'content' field is required."}), 400
        
    markdown_content = data['content']
    
    try:
        result = send_wecom_message(markdown_content)
        
        # 发送成功
        if result.get("errcode") == 0:
            return jsonify({"status": "success", "message_id": result.get("msgid")}), 200
            
        # Token 无效或过期 (40014:非法token, 41001:缺少token, 42001:token过期)
        elif result.get("errcode") in [40014, 41001, 42001]: 
            print(f"WeCom Token invalid (errcode: {result.get('errcode')}), retrying...")
            # 刷新 token 并重试一次
            get_access_token()
            result = send_wecom_message(markdown_content)
            if result.get("errcode") == 0:
                return jsonify({"status": "success", "message_id": result.get("msgid")}), 200
            else:
                return jsonify({"status": "error", "wecom_response": result}), 500
        else:
            return jsonify({"status": "error", "wecom_response": result}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        print("Starting application...")
        get_access_token() # 启动时先获取一次 token
        app.run(host='0.0.0.0', port=5000)
    except (ValueError, Exception) as e:
        print(f"Error starting application: {e}")