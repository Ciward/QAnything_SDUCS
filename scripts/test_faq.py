import os
import requests

url = "http://10.102.33.6:8777/api/local_doc_qa/upload_faqs"
data = {
	"user_id": "zzp",
	"kb_id": "KB71908604ea5546778627de248098dd5e_240625_FAQ",
	"faqs": [{
		"question": "北京3月13日天气",
		"answer": "15-29度小雨",
		"nos_key": None
	}],
	"chunk_size": "2169"
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Origin": "http://10.102.33.6:8777"
}
response = requests.post(url, data=data, headers=headers)
print(response.text)