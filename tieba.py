import requests
from lxml import etree


class TiebaSpider():
    def __init__(self):
        self.start_url = 'http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/m?kw=python&lp=9001'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
        self.part_url = 'http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/'

    def get_url(self, url):  # 获取url
        # print(url)
        response = requests.get(url, headers=self.headers)
        r = response.content
        return response.content

    def get_content_list(self, html_str):  # 获取内容
        html = etree.HTML(html_str)
        name_page = html.xpath('//div[@class="i"]')
        content_list = []
        for div in name_page:
            item = {}
            item['title'] = div.xpath('./a/text()')[0]
            item['href'] = self.part_url + div.xpath('./a/@href')[0]
            item['img_list'] = self.get_img_list(item['href'], [])
            item["img_list"] = [requests.utils.unquote(i).split("src=")[-1] for i in item["img_list"]]
            content_list.append(item)
        next_url_temp = html.xpath('//a[text()="下一页"]/@href')
        print(content_list)
        if len(next_url_temp) > 0:
            next_url = self.part_url + next_url_temp[0]
        else:
            next_url = None
        return content_list, next_url

    def get_img_list(self, detail_url, total_img_list):
        detail_html_str = self.get_url(detail_url)
        detail_html = etree.HTML(detail_html_str)
        img_list = detail_html.xpath('//img[@class="BDE-Image"]/@src')
        total_img_list.extend(img_list)
        next_url_temp = detail_html.xpath('//a[text()="下一页"]/@href')
        if len(next_url_temp) > 0:
            next_url = self.part_url + next_url_temp[0]
            return self.get_img_list(next_url, total_img_list)
        else:
            return total_img_list

    def save_content_list(self, content_list):
        for content in content_list:
            print(content)

    def run(self):
        next_url = self.start_url
        while next_url is not None:
            html_str = self.get_url(next_url)
            content_list, next_url = self.get_content_list(html_str)
            self.save_content_list(content_list)


if __name__ == '__main__':
    tiebaspider = TiebaSpider()
    tiebaspider.run()
