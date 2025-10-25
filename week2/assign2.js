// 1. 定義座標字典
let dic_left = {
    "貝吉塔": [-4, -1],
    "辛巴": [-3, 3],
    "悟空": [0, 0],
    "特南克斯": [1, -2]
};

let dic_right = {
    "丁滿": [-1, 4],
    "弗利沙": [4, -1]
};

// 2. 合併所有角色座標
let all_characters = { ...dic_left, ...dic_right };

// 3. 計算距離函數
function calculate_distance(name1, name2) {
    // 取得兩個角色的座標
    let pos1 = all_characters[name1];
    let pos2 = all_characters[name2];

    // 解構座標
    let [x1, y1] = pos1;
    let [x2, y2] = pos2;

    // 計算基本曼哈頓距離
    let distance = Math.abs(x1 - x2) + Math.abs(y1 - y2);

    // 判斷是否需要「繞到另一側」
    // 當一個角色在左側字典,另一個在右側字典時,加2
    if ((name1 in dic_left && name2 in dic_right) ||
        (name1 in dic_right && name2 in dic_left)) {
        distance += 2;
    }

    return distance;
}

// 4. 主函數
function func1(name) {
    // 儲存所有距離
    let distances = {};

    // 計算給定角色到所有其他角色的距離
    for (const other_name in all_characters) {
        if (other_name !== name) {  // 排除自己
            distances[other_name] = calculate_distance(name, other_name);
        }
    }

    // 找出最小和最大距離
    let distanceValues = Object.values(distances);
    let min_dist = Math.min(...distanceValues);
    let max_dist = Math.max(...distanceValues);

    // 找出最近和最遠的角色
    let closest = Object.keys(distances).filter(char => distances[char] === min_dist);
    let farthest = Object.keys(distances).filter(char => distances[char] === max_dist);

    // 排序(保持一致性)
    closest.sort();
    farthest.sort();

    // 輸出結果
    console.log(`最遠${farthest.join('、')}；最近${closest.join('、')}`);
}

// 測試
console.log("=== Task 1 ===");
func1("辛巴");      // 最遠弗利沙；最近丁滿、貝吉塔
func1("悟空");      // 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙");    // 最遠辛巴；最近特南克斯
func1("特南克斯");  // 最遠丁滿；最近悟空


// 全域預約記錄
const bookings = {
    "S1": [],
    "S2": [],
    "S3": []
};

function isAvailable(serviceName, start, end) {
    // 檢查該服務在 [start, end) 時間是否可用
    for (const [bookedStart, bookedEnd] of bookings[serviceName]) {
        // 檢查是否有重疊
        if (start < bookedEnd && bookedStart < end) {
            return false;
        }
    }
    return true;
}

function parseCriteria(criteria) {
    // 解析 "field operator value"
    if (criteria.includes(">=")) {
        const [field, value] = criteria.split(">=");
        return [field, ">=", field !== "name" ? parseFloat(value) : value];
    } else if (criteria.includes("<=")) {
        const [field, value] = criteria.split("<=");
        return [field, "<=", field !== "name" ? parseFloat(value) : value];
    } else if (criteria.includes("=")) {
        const [field, value] = criteria.split("=");
        return [field, "=", value];
    }
}

function matchesCriteria(service, field, operator, value) {
    // 檢查服務是否符合條件
    const serviceValue = service[field];
    
    if (operator === "=") {
        return serviceValue === value;
    } else if (operator === ">=") {
        return serviceValue >= value;
    } else if (operator === "<=") {
        return serviceValue <= value;
    }
}

function selectBest(candidates, field, operator) {
    // 根據條件選擇最佳服務
    if (operator === ">=") {
        // 選擇最小值(最接近門檻)
        return candidates.reduce((min, service) => 
            service[field] < min[field] ? service : min
        );
    } else if (operator === "<=") {
        // 選擇最大值(最接近門檻)
        return candidates.reduce((max, service) => 
            service[field] > max[field] ? service : max
        );
    } else {  // operator === "="
        // 名稱匹配只有一個結果
        return candidates[0];
    }
}
console.log("=== Task 2 ===");
function func2(ss, start, end, criteria) {
    // 1. 解析條件
    const [field, operator, value] = parseCriteria(criteria);
    
    // 2. 找出可用且符合條件的服務
    const candidates = [];
    for (const service of ss) {
        const serviceName = service["name"];
        // 檢查時間是否可用
        if (isAvailable(serviceName, start, end)) {
            // 檢查是否符合條件
            if (matchesCriteria(service, field, operator, value)) {
                candidates.push(service);
            }
        }
    }
    
    // 3. 如果沒有符合的服務
    if (candidates.length === 0) {
        console.log("Sorry");
        return;
    }
    
    // 4. 選擇最佳服務
    const bestService = selectBest(candidates, field, operator);
    
    // 5. 記錄預約並輸出
    bookings[bestService["name"]].push([start, end]);
    console.log(bestService["name"]);
}

// 服務定義
const services = [ 
    {"name": "S1", "r": 4.5, "c": 1000}, 
    {"name": "S2", "r": 3, "c": 1200}, 
    {"name": "S3", "r": 3.8, "c": 800} 
];

// 測試呼叫

func2(services, 15, 17, "c>=800");  // S3 
func2(services, 11, 13, "r<=4");    // S3 
func2(services, 10, 12, "name=S3"); // Sorry 
func2(services, 15, 18, "r>=4.5");  // S1 
func2(services, 16, 18, "r>=4");    // Sorry 
func2(services, 13, 17, "name=S1"); // Sorry 
func2(services, 8, 9, "c<=1500");   // S2


 
/** 
 * @param {number} index 
 * @returns {number}
 */
function func3(index) {  
  let value=25; //起始值
  operations=[-2, -3, 1, 2]; //操作模式：-2, -3, +1, +2（循環）
  for (let i=0; i < index; i++) {   // 從索引0開始計算到目標索引 
    operation=operations[i % 4]; //index根據當前位置取得對應的操作
    value+=operation;
  }
  return value;
}
console.log("=== Task 3 ===");
let result;
func3(1)
result=func3(1);
console.log(result);
func3(5)
result=func3(5);
console.log(result);  
func3(10)
result=func3(10);
console.log(result);  
func3(30)
result=func3(30);
console.log(result);


function func4(sp, stat, n) {
    let best_index = -1;
    let best_seats = 10;
    
    for (let i = 0; i < sp.length; i++) {
        let current_seats = sp[i];
        let current_status = stat[i];
        
        if (current_status === "0") {
            current_seats = Math.abs(current_seats - n);
            
            if (best_index === -1 || current_seats < best_seats) {
                best_index = i;
                best_seats = current_seats;
            }
        }
    }
    
    return best_index;
}

func4([3, 1, 5, 4, 3, 2], "101000", 2) // print 5 
func4([1, 0, 5, 1, 3], "10100", 4) // print 4 
func4([4, 6, 5, 8], "1000", 4) // print 2
console.log("=== Task 4 ===");
console.log(func4([3, 1, 5, 4, 3, 2], "101000", 2));  
console.log(func4([1, 0, 5, 1, 3], "10100", 4));      
console.log(func4([4, 6, 5, 8], "1000", 4));         