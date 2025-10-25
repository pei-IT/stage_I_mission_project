#座標字典
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

#距離計算函數
def calculate_distance(name1, name2):
    pos1 = all_characters[name1]
    pos2 = all_characters[name2]
    x1, y1 = pos1
    x2, y2 = pos2
    distance = abs(x1 - x2) + abs(y1 - y2)
    if (name1 in dic_left and name2 in dic_right) or \
       (name1 in dic_right and name2 in dic_left):
        distance += 2
    return distance

# 函數func1()給定任意角色名稱，找出距離最近跟最遠的角色
def func1(name):
    distances = {}
   
    for other_name in all_characters:
        if other_name != name:  # 排除自己
            dist = calculate_distance(name, other_name)
            distances[other_name] = dist
    min_dist = min(distances.values())
    max_dist = max(distances.values())
    closest = [char for char, dist in distances.items() if dist == min_dist]
    farthest = [char for char, dist in distances.items() if dist == max_dist]
    closest.sort()
    farthest.sort()
    print(f"最遠{'、'.join(farthest)}；最近{'、'.join(closest)}")

# 測試
print("=== Task 1 ===")
func1("辛巴")      
func1("悟空")     
func1("弗利沙")    
func1("特南克斯") 



bookings={
    "S1":[],
    "S2":[],
    "S3":[]
}
def is_available(service_name, start, end):
    # 檢查該服務在 [start, end) 時間是否可用
    for booked_start, booked_end in bookings[service_name]:
        # 檢查是否有重疊
        if start < booked_end and booked_start < end:
            return False
    return True

def parse_criteria(criteria):
    # 解析 "field operator value"
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
    # 檢查服務是否符合條件
    service_value = service[field]
    
    if operator == "=":
        return service_value == value
    elif operator == ">=":
        return service_value >= value
    elif operator == "<=":
        return service_value <= value

def select_best(candidates, field, operator):
    # 根據條件選擇最佳服務
    if operator == ">=":
        # 選擇最小值(最接近門檻)
        return min(candidates, key=lambda s: s[field])
    elif operator == "<=":
        # 選擇最大值(最接近門檻)
        return max(candidates, key=lambda s: s[field])
    else:  # operator == "="
        # 名稱匹配只有一個結果
        return candidates[0]
print("=== Task 2 ===")
def func2(ss, start, end, criteria):
    # 1. 解析條件
    field, operator, value = parse_criteria(criteria)
    
    # 2. 找出可用且符合條件的服務
    candidates = []
    for service in ss:
        service_name = service["name"]
        # 檢查時間是否可用
        if is_available(service_name, start, end):
            # 檢查是否符合條件
            if matches_criteria(service, field, operator, value):
                candidates.append(service)
    
    # 3. 如果沒有符合的服務
    if not candidates:
        print("Sorry")
        return
    
    # 4. 選擇最佳服務
    best_service = select_best(candidates, field, operator)
    
    # 5. 記錄預約並輸出
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




def func3(index):   
  value=25 #起始值
  operations=[-2, -3, 1, 2] #操作模式：-2, -3, +1, +2（循環）
  for i in range(index):  #從索引0開始計算到目標索引 
        operation=operations[i % 4]  #index根據當前位置取得對應的操作
        value+=operation
  return value

print("=== Task 3 ===")
result=0
func3(1)
result=func3(1)
print(result)
func3(5)
result=func3(5)
print(result);  
func3(10)
result=func3(10)
print(result);  
func3(30)
result=func3(30)
print(result)



def func4(sp, stat, n): 
    best_index=-1
    best_seats=10
    for i in range(len(sp)):
        current_seats=sp[i]
        current_status=stat[i]
        if(current_status=="0"):
            current_seats=abs(current_seats-n)
            if(best_index==-1 or current_seats<best_seats):
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