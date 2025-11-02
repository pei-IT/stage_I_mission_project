import requests
import csv
import time
from bs4 import BeautifulSoup
from datetime import datetime

# 設定Headers避免被阻擋,並處理 PTT 18 歲確認
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    #Cookie': 'over18=1'  # PTT 18 歲確認
}
BASE_URL = 'https://www.ptt.cc'

# 進入文章頁面取得發文時間
def get_article_time(article_url):    
    try:
        response = requests.get(article_url, headers=HEADERS)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 嘗試找article-meta-tag結構
        meta_tags = soup.find_all('span', class_='article-meta-tag')        
        for tag in meta_tags:
            if tag.text.strip() == '時間':
                # 找到時間標籤的下一個兄弟元素article-meta-value
                time_span = tag.find_next_sibling('span', class_='article-meta-value')
                if time_span:
                    time_str = time_span.text.strip()
                    return format_time(time_str)        
        # 嘗試找f4 b7結構
        # 找到所有可能包含時間的span
        all_spans = soup.find_all('span', class_=['f4', 'b7'])        
        for span in all_spans:
            if '時間' in span.text:
                # 找到下一個兄弟元素
                next_span = span.find_next_sibling('span')
                if next_span:
                    time_str = next_span.text.strip()
                    return format_time(time_str)                 
        return ''        
    except Exception as e:
        print(f"取得文章時間失敗: {article_url}, 錯誤: {e}")
        return ''

# 格式化時間字串
def format_time(time_str):   
    try:
        # PTT的時間格式
        dt = datetime.strptime(time_str, '%a %b %d %H:%M:%S %Y')
        return dt.strftime('%a %b %d %H:%M:%S %Y')
    except Exception as e:
        # 如果無法解析,直接返回原始字串
        print(f"時間格式轉換失敗: {time_str}, 錯誤: {e}")
        return time_str

# 取得單一列表頁的文章資訊
def get_page_articles(url):    
    articles = []    
    try:
        response = requests.get(url, headers=HEADERS)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')      
        article_divs = soup.find_all('div', class_='r-ent') # 找到所有文章區塊        
        for article_div in article_divs:   
            # 取得標題區塊
            title_div = article_div.find('div', class_='title') 
            if not title_div:
                continue        
            title_link = title_div.find('a') # 取得標題連結        
            if not title_link: # 過濾已刪除的文章
                continue            
            title_text = title_link.text.strip()          
            if '本文已被刪除' in title_text or '已被刪除' in title_text: # 再次確認不是刪除文章
                continue            
            # 取得讚數
            nrec_div = article_div.find('div', class_='nrec') 
            nrec_text = nrec_div.text.strip() if nrec_div else ''         
            if nrec_text == '爆': # 處理讚數
                like_count = 100
            elif nrec_text.startswith('X'):                
                try:  # 被噓文,轉為負數
                    like_count = -int(nrec_text[1:])
                except:
                    like_count = 0
            elif nrec_text == '':
                like_count = 0
            else:
                try:
                    like_count = int(nrec_text)
                except:
                    like_count = 0                        
            article_url = BASE_URL + title_link['href'] # 取得文章網址
            
            # 取得發文時間
            publish_time = get_article_time(article_url)            
            articles.append({
                'ArticleTitle': title_text,
                'LikeCount': like_count,
                'PublishTime': publish_time
            })      
        return articles, soup        
    except Exception as e:
        print(f"取得頁面文章失敗: {url}, 錯誤: {e}")
        return [], None

# 找到上一頁的連結
def get_previous_page_url(soup):   
    try:
        # 找到所有的按鈕
        btn_group = soup.find('div', class_='btn-group-paging')
        if not btn_group:
            return None        
        # 找到上一頁的連結
        links = btn_group.find_all('a', class_='btn')        
        # 第二個連結是上一頁
        if len(links) >= 2:
            prev_link = links[1]['href']
            return BASE_URL + prev_link        
        return None
    except Exception as e:
        print(f"取得上一頁連結失敗: {e}")
        return None

# 將資料寫入.csv
def save_to_csv(articles, filename):    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['ArticleTitle', 'LikeCount', 'PublishTime']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)            
            writer.writeheader()
            writer.writerows(articles)        
        print(f"成功儲存 {len(articles)} 篇文章到 {filename}")
    except Exception as e:
        print(f"儲存 CSV 失敗: {e}")

def main():   
    all_articles = []
    url = 'https://www.ptt.cc/bbs/Steam/index.html'    
    # 爬蟲取得前3頁
    for page_num in range(3):   
        articles, soup = get_page_articles(url)
        all_articles.extend(articles)              
        # 如果還沒爬完3頁,取得上一頁連結
        if page_num < 2:
            url = get_previous_page_url(soup)
            if not url:
                print("無法取得上一頁連結,停止爬取")
                break        
    # 儲存到.csv
    save_to_csv(all_articles, 'articles.csv') 

# 呼叫主程式
main()