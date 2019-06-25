import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import hashlib
# URLから画像をDLするやつ
import urllib.error
import urllib.request
def download_image(url, dst_path):
   try:
       data = urllib.request.urlopen(url).read()
       with open(dst_path, mode="wb") as f:
           f.write(data)
   except urllib.error.URLError as e:
       print(e)
md5 = hashlib.md5()
browser = webdriver.Chrome()
url = "https://www.google.co.jp/imghp?hl=ja&tab=wi"
browser.get(url)
# 検索窓はinput[6]&検索ボタンはid(mKlEF)
tmp = browser.find_elements_by_tag_name("input")
going = browser.find_element_by_id("mKlEF")
# ここで検索したいワードを入力し検索後のページに遷移
search = input("保存したい画像を検索できるワードを入力してください")
tmp[6].send_keys(search)
going.click()
# ページソースを扱いやすくする為bsで整形する
source = browser.page_source
soup = BeautifulSoup(source, "html.parser")
# イメージソース入れる配列準備
img_src = []
# たぶん100位取れる
tmp = soup.find_all("img", class_="rg_ic rg_i")
for i in range(len(tmp)):
   img_src.append(str(tmp[i]))
let_num =[0,0]
# ソースだけ抜く
for i in range(len(img_src)):
# for i in range(21):
   # srcの文字列だけ抜き出す為に何文字目かを検索
   let_num[0] = img_src[i].find('" src=') + 7
   if let_num[0] == 6:
       let_num[0] = img_src[i].find('data-src') + 10
       let_num[1] = img_src[i].find("jsaction=") - 2
   else:
       let_num[1] = img_src[i].find("style=") - 2
   # 上で出たソース部分だけをスライスしてimg_srcに収納し直し
   img_src[i] = img_src[i][let_num[0]:let_num[1]]
   md5.update(img_src[i].encode('utf-8'))
   img_hash= md5.hexdigest()
   # 保存先のディレクトリは自分で指定(もっと上手いやり方ありそう)
   dst_dir = 'C:/hoge/hogehoge/Desktop/Application/pictmp/' + img_hash + ".jpg"
   # dst_path = os.path.join(*dst_dir, os.path.basename("ddd"))
   download_image(img_src[i], dst_dir)
   print(i)
   time.sleep(0.5)
