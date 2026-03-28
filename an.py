import requests
import json
import os
from datetime import datetime, timezone, timedelta

ORGtime = datetime.now(timezone(timedelta(hours=8)))
time = ORGtime.strftime("%Y-%m-%d %H:%M:%S")

def fetch_api(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[{time}][400] API请求失败: {str(e)}")
        return None

def process_bulletins():
    targets = ["IOS", "Bilibili","Android","Windows"]
    for target in targets:
        data1 = fetch_api(f"https://ak-webview.hypergryph.com/api/game/bulletinList?target={target}")
        data2 = fetch_api(f"https://ak-webview.arknights.jp/api/game/bulletinList?target={target}")
        data3 = fetch_api(f"https://ak-webview-tw.gryphline.com/api/game/bulletinList?target={target}")
        if not data1 or not data1.get("data", {}).get("list"):
            continue
            
        os.makedirs("ak", exist_ok=True)
        for item in data1["data"]["list"]:
            cid = item["cid"]
            detail = fetch_api(f"https://ak-webview.hypergryph.com/api/game/bulletin/{cid}")
            if detail:
                with open(f"ak/an/{cid}.json", "w", encoding="utf-8") as f:
                    json.dump(detail, f, ensure_ascii=False, indent=2)
                    print(f"[{time}][0][cn] {cid}.json saved successful!")
                    
        for item in data2["data"]["list"]:
            cid = item["cid"]
            detail = fetch_api(f"https://ak-webview.arknights.jp/api/game/bulletin/{cid}")
            if detail:
                with open(f"ak/jp/{cid}.json", "w", encoding="utf-8") as f:
                    json.dump(detail, f, ensure_ascii=False, indent=2)
                    print(f"[{time}][0][jp] {cid}.json saved successful!")
        for item in data3["data"]["list"]:
            cid = item["cid"]
            detail = fetch_api(f"https://ak-webview-tw.gryphline.com/api/game/bulletin/{cid}")
            if detail:
                with open(f"ak/tw/{cid}.json", "w", encoding="utf-8") as f:
                    json.dump(detail, f, ensure_ascii=False, indent=2)
                    print(f"[{time}][0][tw] {cid}.json saved successful!")

if __name__ == "__main__":
    print(f"[{time}][15]work start......")
    process_bulletins()
