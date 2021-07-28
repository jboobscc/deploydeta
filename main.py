
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests
from lxml import etree
import csv

f = open('data.csv', mode='w', encoding='utf-8')
csvwriter = csv.writer(f)
def download_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    }
    resp = requests.get(url, headers=headers)
    html = etree.HTML(resp.text)
    table = html.xpath('/html/body/div[2]/div[4]/div[1]/table')[0]
    trs = table.xpath('./tr')[1:]  
    for tr in trs:
        txt = tr.xpath('./td/text()')
        txt = (item.replace("\\", "").replace("/", "") for item in txt)
        csvwriter.writerow(txt)
    print(url, '提取完毕')


if __name__ == "__main__":
    # for i in range(1, 16964):  # 效率及其低下
    #     download_one_page(f"http://www.xinfadi.com.cn/marketanalysis/0/list/{i}.shtml")
    with ThreadPoolExecutor(80) as t:
        for i in range(1, 101):  # 提取100页数据
            t.submit(download_one_page, f"http://www.xinfadi.com.cn/marketanalysis/0/list/{i}.shtml")
    print('全部下载完毕')
