
import requests
from bs4 import BeautifulSoup


def download_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
    try:
        r = requests.get(url,timeout = 30,headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding   #指定编码形式
        return r.text
    except:
        return "please inspect your url or setup"


def get_content(html):
    output = """    排名：{}\n    标题：{} \n    热度：{}\n    链接：{}\n------------\n"""
    output2 = """平台：{}    榜单类型：{}\n------------\n"""
    soup = BeautifulSoup(html, 'html.parser')
    con = soup.find('div',attrs={'class':'bc-cc'})
    con_list = con.find_all('div', class_="cc-cd")
    for i in con_list:  
        author = i.find('div', class_='cc-cd-lb').get_text() # 获取平台名字
        link = i.find('div', class_='cc-cd-cb-l').find_all('a') # 获取所有链接  
        gender = i.find('span', class_='cc-cd-sb-st').get_text() # 获取类型 
        num=[]
        title=[]
        hot=[]
        href=[]
        save_txt(output2.format(author, gender))
        for k in link:
            href.append(k['href'])
            num.append(k.find('span', class_='s').get_text())
            title.append(str(k.find('span', class_='t').get_text()))
            hot.append(str(k.find('span', class_='e').get_text()))
        for h in range(len(num)): 
            save_txt(output.format(num[h], title[h], hot[h], href[h]))


def save_txt(*args):
    for i in args:
        with open('hotList.txt', 'a', encoding='utf-8') as f:
            f.write(i)


def main():
    # 我们点击下面链接，在页面下方可以看到共有13页，可以构造如下 url，
    # 当然我们最好是用 Beautiful Soup找到页面底部有多少页。
    url = 'https://tophub.today/c/news'
    html = download_page(url)
    get_content(html)

if __name__ == '__main__':
    main()

