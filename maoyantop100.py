import json
import re
import requests
from requests.exceptions import RequestException


def get_one_page(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '电影排名': item[0],
            '电影封面': item[1],
            '电影名称': item[2],
            '电影主演': item[3].strip()[3:],
            '上映时间': item[4].strip()[5:],
            '电影评分': item[5] + item[6],
        }


def write_to_file(content):
    # with open('result.txt', 'a', encoding='utf-8') as f:
    #     f.write(json.dumps(content, ensure_ascii=False) + '\n')
    #     f.close()
    pass

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    html = get_one_page(url, headers)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i * 10)
