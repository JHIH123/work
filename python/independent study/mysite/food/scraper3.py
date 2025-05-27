import requests
from bs4 import BeautifulSoup
import os
import sys
import django
from django.utils import timezone
from django.core.files import File
from urllib.parse import urljoin
from io import BytesIO

# 獲取當前文件所在目錄
current_directory = os.path.dirname(os.path.abspath(__file__))
# 獲取項目根目錄
project_directory = os.path.dirname(current_directory)
# 添加項目根目錄到 sys.path
sys.path.append(project_directory)

# 設置 Django 環境變量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# 初始化 Django
django.setup()

# 從 food 應用中導入模型
from food.models import Place, Photo

def Vegetarian():
    # 獲取網頁內容
    base_url = 'https://vegemap.merit-times.com'
    url = base_url + '/restaurant_list/%E6%96%B0%E5%8C%97%E5%B8%82-%E8%94%AC%E9%A3%9F%E9%A4%90%E5%BB%B3'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')

    # 選擇包含餐廳信息的 div 元素
    restaurants = soup.select('div.B_item_productlist')

    for restaurant in restaurants:
        # 餐廳名稱
        name_tag = restaurant.find('h3', class_='B_item_title')
        name = name_tag.text if name_tag else 'N/A'

        # 營業時間
        time_tag = restaurant.find('span', class_='fa fa-clock-o')
        if time_tag:
            time = time_tag.find_next_sibling('span').text if time_tag.find_next_sibling('span') else 'N/A'
        else:
            # 如果找不到 fa-clock-o，嘗試找包含“星期”關鍵字的 span
            weekday_tag = restaurant.find('span', string=lambda text: text and "星期" in text)
            if weekday_tag:
                time = weekday_tag.text + '休息'
            else:
                time = 'N/A'

        # 提取地址
        address_tag = restaurant.find('span', itemprop='address')
        address = address_tag.text if address_tag else 'N/A'
        
        # 提取鏈接
        link_tag = name_tag.find_previous('a') if name_tag else None
        url1 = link_tag['href'] if link_tag else 'N/A'
        url='https://vegemap.merit-times.com/'+ url1

        # 提取電話
        phone_tag = restaurant.find('span', itemprop='telephone')
        phone = phone_tag.text if phone_tag else 'N/A'
                
        # 創建 Place 對象
        place = Place.objects.create(
            name=name,
            time=time,
            url=url,
            address=address,
            phone=phone,
            # 設置當前日期時間
            pub_date = timezone.now(),
            food='素'
        )

        # 抓取並存儲圖片
        image_div = restaurant.find('div', class_='B_item_img')  # 根據實際 HTML 結構選擇正確的標籤
        if image_div:
            image_tag = image_div.find('img')
            if image_tag and image_tag['src']:
                image_url = urljoin(base_url, image_tag['src'])
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_name = os.path.basename(image_tag['src'])
                    image_content = BytesIO(image_response.content)
                    photo = Photo(place=place, name=image_name)
                    photo.file.save(image_name, File(image_content), save=True)

def Non_Vegetarian():
    # 目標 URL
    url = "https://www.welcometw.com/%E5%8F%B0%E5%8C%97%E7%BE%8E%E9%A3%9F%E6%8E%A8%E8%96%A6/#%E5%8F%B0%E5%8C%97%E7%BE%8E%E9%A3%9F%EF%BD%9C%E5%8F%B0%E5%8C%97%E7%BE%8E%E5%BC%8F%E9%A4%90%E5%BB%B3"

    # 發送 GET 請求並獲取 HTML 內容
    response = requests.get(url)
    html_content = response.text

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 選擇所有的 <pre> 標籤
    sel = soup.select("pre")

    # 選擇所有的 <h3> 標籤
    h3_tags = soup.find_all('h3')

    # 儲存所有分割後文字的列表
    all_pre_texts = []

    # 遍歷所有的 <pre> 標籤
    for s in sel:
        # 獲取 <pre> 標籤中的文字
        pre_text = s.text

        # 分割文字
        pre_text_parts = pre_text.split('\n')

        # 將分割後的文字加入到列表中
        all_pre_texts.append(pre_text_parts)

    # 定義解析函數
    def parse_store_info(pre_tag):
        store_info = {
            'name': '',
            'time': '',
            'address': '',
            'url': '',
            'off_day': '',
            'phone': '',
            'food': ''
        }
        pre_text_parts = pre_tag.text.split('\n')
        for part in pre_text_parts:
            part = part.replace('\r', '').strip()  # 去除 \r 和前後空格
            
            if '地址：' in part:
                store_info['address'] = part.split('地址：')[1].strip()
                
            elif '時間：' in part:
                store_info['time'] = part.split('時間：')[1].strip()
                
            elif '電話：' in part:
                store_info['phone'] = part.split('電話：')[1].strip()
                
            elif '網址：' in part:
                store_info['url'] = part.split('網址：')[1].strip()
                
            elif '休息：' in part:
                store_info['off_day'] = part.split('休息：')[1].strip()
                
            elif '餐點：' in part:
                store_info['food'] = part.split('餐點：')[1].strip()
                
            else:
                if not store_info['name']:
                    store_info['name'] = part.strip()
                    
        return store_info

    # 解析每一個 <h3> 標籤中的內容並存入資料庫
    for h3_tag in h3_tags:
        store_name = h3_tag.text.strip()
        next_sibling = h3_tag.find_next_sibling()
        image_url = None
        store_info = None

        # 查找圖片
        while next_sibling and next_sibling.name != 'h3':
            if next_sibling.name == 'figure':
                image_tag = next_sibling.find('img')
                if image_tag and image_tag['src']:
                    image_url = urljoin(url, image_tag['src'])
                    break
            next_sibling = next_sibling.find_next_sibling()

        # 查找餐廳資訊
        next_sibling = h3_tag.find_next_sibling()
        while next_sibling and next_sibling.name != 'h3':
            if next_sibling.name == 'pre':
                store_info = parse_store_info(next_sibling)
                break
            next_sibling = next_sibling.find_next_sibling()

        if store_info:
            place = Place(
                name=store_info.get('name', store_name),
                address=store_info.get('address', ''),
                time=store_info.get('time', ''),
                phone=store_info.get('phone', ''),
                url=store_info.get('url', ''),
                pub_date=timezone.now(),
                food='葷'
            )
            place.save()

            if image_url:
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_name = os.path.basename(image_url)
                    image_content = BytesIO(image_response.content)
                    photo = Photo(place=place, name=image_name)
                    photo.file.save(image_name, File(image_content), save=True)

    # 輸出結果
    for index, parts in enumerate(all_pre_texts):
        print(f'Content of <pre> tag {index + 1}:')
        print(parts)
        print('---------------------------')

    

# 執行主函數
if __name__ == "__main__":
    Vegetarian()
    Non_Vegetarian()
