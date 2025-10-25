#=== Task 1 ===
#宣告左右兩邊角色的座標字典
dic_left = {
    "貝吉塔": (-4, -1),
    "辛巴": (-3, 3),
    "悟空": (0, 0),
    "特南克斯": (1, -2)
}
dic_right = {
    "丁滿": (-1, 4),
    "弗利沙": (4, -1)
}
all_characters = {**dic_left, **dic_right}
#宣告距離計算函數
def calculate_distance(name1, name2):
    pos1 = all_characters[name1]
    pos2 = all_characters[name2]
    x1, y1 = pos1
    x2, y2 = pos2
    distance = abs(x1 - x2) + abs(y1 - y2)  #曼哈頓距離計算公式
#給定角色在左邊字典且另一個給定角色在右邊字典，代表跨過斜線距離+2
    if (name1 in dic_left and name2 in dic_right) or \
       (name1 in dic_right and name2 in dic_left):
        distance += 2
    return distance
# 宣告函數func1()給定任意角色名稱，找出距離最近跟最遠的角色並印出角色名稱
def func1(name):
    distances = {}
    for other_name in all_characters:
        if other_name != name:  # 排除自己的角色名稱
            dist = calculate_distance(name, other_name)
            distances[other_name] = dist
    min_dist = min(distances.values())
    max_dist = max(distances.values())
    closest = [char for char, dist in distances.items() if dist == min_dist]
    farthest = [char for char, dist in distances.items() if dist == max_dist]
    closest.sort()
    farthest.sort()
    print(f"最遠{'、'.join(farthest)}；最近{'、'.join(closest)}")
print("=== Task 1 ===")
func1("辛巴") # print 最遠弗利沙；最近丁滿、貝吉塔    
func1("悟空") # print 最遠丁滿、弗利沙；最近特南克斯     
func1("弗利沙") # print 最遠辛巴；最近特南克斯         
func1("特南克斯") # print 最遠丁滿；最近悟空  


#=== Task 2 ===
#宣告服務預約時段字典
bookings={  
    "S1":[],
    "S2":[],
    "S3":[]
}
def is_available(service_name, start, end):
    for booked_start, booked_end in bookings[service_name]:  # 檢查該服務在 [start, end) 時間是否可用
        if start < booked_end and booked_start < end:  # 檢查是否有重疊
            return False
    return True
def parse_criteria(criteria):
    # 解析"field operator value"
    if ">=" in criteria:
        field, value = criteria.split(">=")
        return field, ">=", float(value) if field != "name" else value
    elif "<=" in criteria:
        field, value = criteria.split("<=")
        return field, "<=", float(value) if field != "name" else value
    elif "=" in criteria:
        field, value = criteria.split("=")
        return field, "=", value
def matches_criteria(service, field, operator, value):
    service_value = service[field]   # 檢查服務是否符合條件
    if operator == "=":
        return service_value == value
    elif operator == ">=":
        return service_value >= value
    elif operator == "<=":
        return service_value <= value
def select_best(candidates, field, operator):
    if operator == ">=":  # 根據條件選擇最佳服務
        return min(candidates, key=lambda s: s[field]) # 選擇最小值(最接近criteria)
    elif operator == "<=":
        return max(candidates, key=lambda s: s[field]) # 選擇最大值(最接近criteria)
    else:   # operator == "="
        return candidates[0]  # 名稱匹配只有一個結果
print("=== Task 2 ===")
def func2(ss, start, end, criteria):
    field, operator, value = parse_criteria(criteria) # 解析criteria
    candidates = []   # 找出可用且符合criteria的服務
    for service in ss:
        service_name = service["name"]
        if is_available(service_name, start, end):  # 檢查時間是否可用
            if matches_criteria(service, field, operator, value):  # 檢查是否符合criteria
                candidates.append(service)
    # 如果沒有符合的服務
    if not candidates:
        print("Sorry")
        return
    best_service = select_best(candidates, field, operator)  # 選擇最佳服務
    # 記錄預約時段並印出服務名稱
    bookings[best_service["name"]].append([start, end])
    print(best_service["name"])
            
services=[ 
    {"name":"S1", "r":4.5, "c":1000}, 
    {"name":"S2", "r":3, "c":1200}, 
    {"name":"S3", "r":3.8, "c":800} 
] 
func2(services, 15, 17, "c>=800") # S3 
func2(services, 11, 13, "r<=4") # S3 
func2(services, 10, 12, "name=S3") # Sorry 
func2(services, 15, 18, "r>=4.5") # S1 
func2(services, 16, 18, "r>=4") # Sorry 
func2(services, 13, 17, "name=S1") # Sorry 
func2(services, 8, 9, "c<=1500") # S2


#=== Task 3 ===
def func3(index):   
  value=25 
  operations=[-2, -3, 1, 2] # 操作模式 -2, -3, +1, +2（循環）
  for i in range(index):  # 從索引0開始計算到目標索引 
        operation=operations[i % 4]  # index根據當前位置取得對應的操作
        value+=operation
  return value

print("=== Task 3 ===")
result=0
func3(1) # print 23
result=func3(1)
print(result)
func3(5) # print 21
result=func3(5)
print(result);  
func3(10) # print 16
result=func3(10)
print(result);  
func3(30) # print 6
result=func3(30)
print(result)


#=== Task 4 ===
##定義函式func4, 找出對入境乘客最適合的車廂
def func4(sp, stat, n): 
    best_index=-1  # 初始化最佳索引為 -1 代表尚未找到
    best_seats=10  # 初始化最佳座位差距為 10 當作比較基準值
    for i in range(len(sp)):
        current_seats=sp[i]
        current_status=stat[i]
        if(current_status=="0"):
            current_seats=abs(current_seats-n)  # 計算當前座位數與目標座位數 n 的差距絕對值
            if(best_index==-1 or current_seats<best_seats):  # 如果還沒找到任何符合的座位或者當前座位差距比之前找到的更小
                best_index=i
                best_seats=current_seats                    
    return best_index
    
func4([3, 1, 5, 4, 3, 2], "101000", 2) # print 5 
func4([1, 0, 5, 1, 3], "10100", 4) # print 4 
func4([4, 6, 5, 8], "1000", 4) # print 2
print("=== Task 4 ===")
print(func4([3, 1, 5, 4, 3, 2], "101000", 2))
print(func4([1, 0, 5, 1, 3], "10100", 4))
print(func4([4, 6, 5, 8], "1000", 4))
