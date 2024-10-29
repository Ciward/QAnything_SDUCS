import os
import json
import requests
import time
import random
import string
import argparse

def stream_requests(data_raw):
    url = 'http://localhost:8777/api/local_doc_qa/local_doc_chat'
    response = requests.post(
        url,
        json=data_raw,
        timeout=60,
        stream=True
    )
    for line in response.iter_lines(decode_unicode=False, delimiter=b"\n\n"):
        if line:
            yield line
def not_stream_requests():
    url = 'http://localhost:8777/api/local_doc_qa/local_doc_chat'
    headers = {
        'content-type': 'application/json'
    }
    data = {
	"user_id": "zzp",
	"kb_ids": ["KB5739af62043c48f8ab1a782be7a47874_240625", 
            "KB613148ff494c41d4834f13ea66e21a25_240625", 
            "KBebb756d6b0a744b29c0044e3773c1aee_240625", 
            "KB71908604ea5546778627de248098dd5e_240625"],
	"history": [],
	"question": "社会实践怎么做",
	"streaming": False,
	"networking": False,
	"product_source": "saas",
	"rerank": True,
	"only_need_search_results": True,
	"hybrid_search": True,
	"max_token": 7114,
	"api_base": "http://10.102.33.6:9991/v1",
	"api_key": "EMPTY",
	"model": "custom-glm4-chat",
	"api_context_length": 72704,
	"chunk_size": 2169,
	"top_p": 0.9,
	"top_k": 61,
	"temperature": 0.7
}
    try:
        start_time = time.time()
        response = requests.post(url=url, headers=headers, json=data)
        end_time = time.time()
        res = response.json()
        print(res['response'])
        print(f"响应状态码: {response.status_code}, 响应时间: {end_time - start_time}秒")
    except Exception as e:
        print(f"请求发送失败: {e}")
def write_to_file(data_raw):
    url = 'http://localhost:8777/api/local_doc_qa/local_doc_chat'
    response = requests.post(
        url,
        json=data_raw,
        timeout=60,
        stream=True
    )
    with open('test.txt', 'wb') as f:
        for line in response.iter_lines():
            f.write(line + b'\n')
        f.close()
def test_steam():
    data_raw = {
        "kb_ids": ["KB613148ff494c41d4834f13ea66e21a25_240625",
                    "KBebb756d6b0a744b29c0044e3773c1aee_240625",
                    "KB5739af62043c48f8ab1a782be7a47874_240625"],
        "question": "公交运行时间",
        "user_id": "zzp",
        "streaming": True,
        "history": [],  
        "networking":False,
        "product_source":"saas_qa",
        "rerank":True,
        "only_need_search_results":False,
        "hybrid_search":True,
        "max_token":70000,
        "api_base":"http://10.102.33.6:9991/v1",
        "api_key":"EMPTY",
        "model":"custom-glm4-chat",
        "api_context_length":16384,
        "chunk_size":2000,
        "top_p":0.99,
        "temperature":0.7,
    }
    for i, chunk in enumerate(stream_requests(data_raw)):
        if chunk:
            chunkstr = chunk.decode("utf-8")[6:]
            chunkjs = json.loads(chunkstr)
            print(chunkjs)
    write_to_file(data_raw)


if __name__ == '__main__':
    test_steam()
    #not_stream_requests()
