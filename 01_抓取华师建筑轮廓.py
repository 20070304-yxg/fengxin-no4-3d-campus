# -*- coding: utf-8 -*-
"""
3D校园·第1步：从 OpenStreetMap 抓取华中师范大学主校区建筑轮廓
输出：华师_建筑.geojson
"""
import json
import urllib.request

# 华师主校区（桂子山）大致范围：南到珞瑜路，北到广埠屯，东到卓刀泉，西到虎泉
BBOX = (30.505, 114.350, 30.535, 114.385)  # south, west, north, east

QUERY = f"""
[out:json][timeout:60];
(
  way["building"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});
  relation["building"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});
);
out geom;
"""

URLS = [
    'https://overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
]

data = None
for url in URLS:
    try:
        print('trying', url)
        req = urllib.request.Request(url, data=QUERY.encode('utf-8'),
                                     headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read().decode('utf-8'))
        print('ok from', url)
        break
    except Exception as e:
        print('fail:', e)

if data is None:
    raise SystemExit('两个 Overpass 端点都连不上')

features = []
for el in data.get('elements', []):
    geom = el.get('geometry')
    if not geom:
        continue
    coords = [[p['lon'], p['lat']] for p in geom]
    if len(coords) < 3:
        continue
    coords.append(coords[0])  # 闭合
    tags = el.get('tags', {})
    features.append({
        'type': 'Feature',
        'properties': {
            'name': tags.get('name', ''),
            'building': tags.get('building', 'yes'),
        },
        'geometry': {'type': 'Polygon', 'coordinates': [coords]},
    })

out = {
    'type': 'FeatureCollection',
    'features': features,
}
out_path = r'C:\Users\ASUS\Desktop\今天\3D校园\华师_建筑.geojson'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False)

print('建筑数:', len(features))
named = [ft['properties']['name'] for ft in features if ft['properties']['name']]
print('有名字的楼:', len(named))
for n in named[:30]:
    print(' -', n)
print('SAVED:', out_path)
