import flet as ft
import requests
from datetime import datetime

AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json"

# -------------------------
# 地方 → 都道府県 階層取得
# -------------------------
def get_area_hierarchy():
    res = requests.get(AREA_URL, timeout=5).json()
    centers = res["centers"]
    offices = res["offices"]

    region_order = [
        "北海道", "東北", "関東甲信", "北陸",
        "東海", "近畿", "中国", "四国", "九州", "沖縄"
    ]

    hierarchy = {}
    for r in region_order:
        for c in centers.values():
            if r in c["name"]:
                hierarchy[c["name"]] = {}

    for code, info in offices.items():
        parent = info.get("parent")
        if parent in centers:
            region = centers[parent]["name"]
            if region in hierarchy:
                hierarchy[region][info["name"]] = code

    return hierarchy