import requests
import json
import os
import sys
from datetime import datetime, timezone, timedelta

SERVER_CONFIGS = {
    "cn": {
        "base_url": "https://ak-webview.hypergryph.com/api/game",
        "dir": "an"
    },
    "jp": {
        "base_url": "https://ak-webview.arknights.jp/api/game",
        "dir": "jp"
    },
    "tw": {
        "base_url": "https://ak-webview-tw.gryphline.com/api/game",
        "dir": "tw"
    }
}

def fetch_api(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[400] API请求失败: {str(e)}")
        return None

def process_bulletins(server_key):
    config = SERVER_CONFIGS.get(server_key)
    if not config:
        print(f"未知服务器参数: {server_key}")
        return

    targets = ["IOS", "Bilibili", "Android", "Windows"]
    save_path = f"ak/{config['dir']}"
    os.makedirs(save_path, exist_ok=True)

    for target in targets:
        list_url = f"{config['base_url']}/bulletinList?target={target}"
        data = fetch_api(list_url)
        
        if not data or not data.get("data", {}).get("list"):
            continue
            
        for item in data["data"]["list"]:
            cid = item["cid"]
            detail_url = f"{config['base_url']}/bulletin/{cid}"
            detail = fetch_api(detail_url)
            
            if detail:
                time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
                file_name = f"{save_path}/{cid}.json"
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(detail, f, ensure_ascii=False, indent=2)
                print(f"[{time}][{server_key}:{target}] {cid}.json saved successful!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请提供服务器参数 (cn/jp/tw)")
    else:
        target_server = sys.argv[1].lower()
        print(f"[15] Work start for server: {target_server}...")
        process_bulletins(target_server)
