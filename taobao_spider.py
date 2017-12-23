import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

driver = webdriver.PhantomJS()
driver.set_window_size(1400, 900)


# 进入淘宝首页 点击搜索框 输入想要搜索的内容
def search():
    try:
        driver.get('https://www.taobao.com/')
        # 获取搜索框
        input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        # 获取搜索按钮
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys('美食')
        button.click()
        # 获取一共多少页
        page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        )
        get_item()
        return page.text
    except:
        return search()


def next_page(page_number):
    try:
        # 获取翻页输入框
        input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        # 获取确定按钮
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        button.click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_item()
    except:
        next_page(page_number)


# 解析淘宝店铺
def get_item():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'))
    )
    html = driver.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        data = {
            '图片': item.find('.pic .img').attr('src'),
            '价格': item.find('.price').text(),
            '成交量': item.find('.deal-cnt').text()[:-3],
            '产品': item.find('.title').text(),
            '店铺': item.find('.shop').text(),
            '店铺所在地': item.find('.location').text()
        }
        print(data)


if __name__ == '__main__':
    try:
        page = search()
        page = int(re.compile('(\d+)').search(page).group(1))
        for i in range(2, page + 1):
            next_page(i)
    finally:
        driver.close()
        # print(page)
