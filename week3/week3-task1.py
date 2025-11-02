import collections
import urllib.request as request
import json
import csv
import re

# 抓取中文資料
src = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
with request.urlopen(src) as response:
    data = json.load(response)  # 利用json模組處理json格式資料
hlist1 = data["list"]  # 依照API網頁結構list[]撰寫結構撈取列表[]中的資料

# 抓取英文資料
src = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
with request.urlopen(src) as response:
    data = json.load(response) 
hlist2 = data["list"]

# API資料是list of dict格式
chinese_data = hlist1
english_data = hlist2

all_ids = [hotel['_id'] for hotel in chinese_data] # 建立只有全部id的list
merged_hotels = [] # 建立空的list
for hotel_id in all_ids: # 用id跑迴圈
    # 找出對應的中英文資料
    ch_info = next((h for h in chinese_data if h['_id'] == hotel_id))
    en_info = next((h for h in english_data if h['_id'] == hotel_id))
    
    # 組合資料並append
    hotel_record = {
        'ChineseName': ch_info['旅宿名稱'],
        'EnglishName': en_info['hotel name'],
        'ChineseAddress': ch_info['地址'],
        'EnglishAddress': en_info['address'],
        'Phone': ch_info['電話或手機號碼'],
        'RoomCount': ch_info['房間數']
    }
    merged_hotels.append(hotel_record)

# 寫入hotels.csv
with open('hotels.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['ChineseName', 'EnglishName', 'ChineseAddress', 
                  'EnglishAddress', 'Phone', 'RoomCount']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged_hotels)

# 從地址中提取區域名稱
def extract_district(address):     
    # 台北市的行政區列表
    taipei_districts = [
        '中正區', '大同區', '中山區', '松山區', '大安區',
        '萬華區', '信義區', '士林區', '北投區', '內湖區',
        '南港區', '文山區'
    ]    
    # 檢查是否包含完整的區名
    for district in taipei_districts:
        if district in address:
            return district
# 使用collections.defaultdict統計各區域的飯店數和房間數
districts_stats = collections.defaultdict(lambda: {'hotel_count': 0, 'room_count': 0})
for hotel in merged_hotels:
    district = extract_district(hotel['ChineseAddress'])
    districts_stats[district]['hotel_count'] += 1    
    # 處理房間數，確保是整數
    room_count = int(hotel['RoomCount'])
    districts_stats[district]['room_count'] += room_count
# 將統計結果轉換為 list，方便寫入 CSV
districts_list = []
for district_name, stats in districts_stats.items():
    districts_list.append({
        'DistrictName': district_name,
        'HotelCount': stats['hotel_count'],
        'RoomCount': stats['room_count']
    })

# 寫入districts.csv
with open('districts.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['DistrictName', 'HotelCount', 'RoomCount']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(districts_list)