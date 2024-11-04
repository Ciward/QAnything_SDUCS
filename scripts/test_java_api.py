import requests
def write_to_file(line):
    with open('test.txt', 'a') as f:
        f.write(line + '\n')
def test_stream_api():
    url = "http://10.102.33.6:8082/api/stream/RAGFileChatStreamNoauth"  # 替换为实际的API地址
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "content": "公交运行时间"  # 替换为实际的测试内容
    }

    with requests.post(url, json=data, headers=headers, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    print(line.decode('utf-8'))
                    write_to_file(line.decode('utf-8'))
        else:
            print(f"请求失败，状态码: {response.status_code}")

if __name__ == "__main__":
    test_stream_api()