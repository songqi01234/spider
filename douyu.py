# coding=utf-8
from selenium import webdriver
import time

class DouyuSpider:
    def __init__(self):
        self.start_url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome()

    #提取数据,a标签
    def get_content_list(self):
        li_list = self.driver.find_elements_by_xpath("//ul[@id='live-list-contentbox']/li")
        content_list =[]
        for li in li_list:
            item = {}
            item["category"] = li.find_element_by_xpath(".//div[@class='mes-tit']/span").text
            if item["category"].endswith("直播"):
                continue
            item["room_href"] = li.find_element_by_xpath("./a").get_attribute("href")
            item["room_name"] = li.find_element_by_xpath("./a").get_attribute("title")
            item["anchor"] = li.find_element_by_xpath(".//div[@class='mes']/p/span[1]").text
            item["watch_num"] = li.find_element_by_xpath(".//div[@class='mes']/p/span[2]").text
            print(item)
            content_list.append(item)
        #获取a标签
        next_url_temp = self.driver.find_elements_by_class_name("shark-pager-next")
        next_url = next_url_temp[0] if len(next_url_temp)>0 else None
        return content_list,next_url

    def save_content_list(self,content_list):
        pass

    def __del__(self):
        self.driver.quit()


    def run(self):
        #1.start_url
        #2.发送起始url的请求，获取响应
        self.driver.get(self.start_url)
        #3.提取数据，下一页的a标签
        content_list,next_url = self.get_content_list()
        #4.保存
        self.save_content_list(content_list)
        #5.判断a标签是否有：循环
        while next_url is not None:
            #有：点击到下一页
            # 2.发下一页的请求，获取响应
            next_url.click()
            time.sleep(2)
            # 3.提取数据，下一页的a标签
            content_list, next_url = self.get_content_list()
            # 4.保存
            self.save_content_list(content_list)
        # self.driver.quit()

if __name__ == '__main__':
    douyu = DouyuSpider()
    douyu.run()


