import csv
import os
import time
import requests
from bs4 import BeautifulSoup
import schedule

# 定义CSV文件路径
csv_file = 'notifications.csv'
os.makedirs('docs', exist_ok=True)

# 定义API上传的URL和参数
host = "localhost"
upload_url = f"http://{host}:8777/api/local_doc_qa/upload_files"
upload_data = {
    "user_id": "zzp",
    "kb_id": "KB613148ff494c41d4834f13ea66e21a25_240625",  # 知识库ID
    "mode": "soft"
}

# 定义基地址字典
base_urls = {
    'bkjx.sdu.edu.cn': 'https://www.bkjx.sdu.edu.cn/',
    'cs.sdu.edu.cn': 'https://www.cs.sdu.edu.cn/',
    'online.sdu.edu.cn': 'https://www.online.sdu.edu.cn/',
    'youth.sdu.edu.cn': 'https://www.youth.sdu.edu.cn/',
}

def fetch_and_update_notifications():
    # 从urls.txt文件中读取URL
    with open('urls.txt', 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    # 打开CSV文件准备写入
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Date', 'URL'])

        # 遍历每个URL
        for url in urls:
            response = requests.get(url)
            response.encoding = 'utf-8'  # 设置编码为utf-8
            soup = BeautifulSoup(response.content, 'html.parser')

            # 根据不同的URL提取通知信息
            if 'bkjx.sdu.edu.cn' in url:
                for item in soup.select('.leftNews3'):
                    title = item.find('a').get('title')
                    date = item.find('div', style='float:right;').text.strip('[]')
                    relative_url = item.find('a').get('href')

                    if None in (title, date, relative_url):
                        continue

                    full_url = relative_url if relative_url.startswith('http') else base_urls['bkjx.sdu.edu.cn'] + relative_url
                    writer.writerow([title, date, full_url])

            elif 'cs.sdu.edu.cn' in url:
                for item in soup.select('li'):
                    title = item.find('a').get('title')
                    date_span = item.find('span', class_='fr')
                    date = date_span.text if date_span else None
                    relative_url = item.find('a').get('href')

                    if None in (title, date, relative_url):
                        continue

                    full_url = relative_url if relative_url.startswith('http') else base_urls['cs.sdu.edu.cn'] + relative_url
                    writer.writerow([title, date, full_url])

            elif 'online.sdu.edu.cn' in url:
                for item in soup.select('li'):
                    title = item.find('a').get('title')
                    date_span = item.find('span', class_='fr')
                    date = date_span.text if date_span else None
                    relative_url = item.find('a').get('href')

                    if None in (title, date, relative_url):
                        continue

                    full_url = relative_url if relative_url.startswith('http') else base_urls['online.sdu.edu.cn'] + relative_url
                    writer.writerow([title, date, full_url])

            elif 'youth.sdu.edu.cn' in url:
                for item in soup.select('li'):
                    title = item.find('a').text
                    date_div = item.find('div', class_='date')
                    date = date_div.text.strip() if date_div else None
                    # 修正日期格式
                    if date and '\n' in date:
                        day, month_year = date.split('\n')
                        date = f"{month_year.strip()}-{day.strip()}"

                    relative_url = item.find('a').get('href')

                    if None in (title, date, relative_url):
                        continue

                    full_url = relative_url if relative_url.startswith('http') else base_urls['youth.sdu.edu.cn'] + relative_url
                    writer.writerow([title, date, full_url])

    # 读取CSV文件
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 检查行中是否有任何列为'N/A'
            if 'N/A' in row.values():
                continue

            title = row['Title']
            title = title.replace(' ', '_').replace('\n', '_')
            url = row['URL']
            date = row['Date']  # 假设CSV中有Date列
            
            # 构建文件名
            file_name = f"docs/{date}_{title}"

            # 检查文件是否已存在
            if os.path.exists(file_name+'.md'):
                print(f"文件 {file_name}.md 已存在，跳过下载。")
                continue

            # 调用控制台命令下载通知内容
            os.system(f"clean-mark '{url}' -o '{file_name}'")
            

            # 上传文件到知识库
            with open(file_name+'.md', 'rb') as f:
                files = {'files': f}
                response = requests.post(upload_url, files=files, data=upload_data)
                print(f"上传 {file_name}.md 到知识库，响应: {response.text}")
            time.sleep(0.3)

# 设置定时任务
schedule.every().day.at("03:00").do(fetch_and_update_notifications)
fetch_and_update_notifications()
# 运行定时任务
while True:
    schedule.run_pending()
    time.sleep(60)
