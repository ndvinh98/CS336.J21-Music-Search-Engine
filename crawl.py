from bs4 import BeautifulSoup
import requests
from collections import defaultdict
from selenium import webdriver
import json


def save_as_txt(string,path): 
    with open(path, "w",encoding="utf-8") as fd: 
        fd.write(string)
    fd.close()

def save_as_json(dictionary,path):
    with open(path, "w",encoding='UTF8') as file_write:
        json.dump(dictionary, file_write)

def crawl_names(url):
    titles=[]
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.text,"html.parser")
    musics = parsed_html.find(class_ = "list_show_chart").find_all('a','name_song')
    if musics is not None:
        for idx,music in enumerate(musics):
            title_music=music.get('title')
            titles.append(title_music)
    return titles

def crawl_links(url):
    links=[]
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.text,"html.parser")
    musics = parsed_html.find(class_ = "list_show_chart").find_all('a','name_song')
    if musics is not None:
        for idx,music in enumerate(musics):
            link_music=music.get('href')
            links.append(link_music)
    return links

def crawl_lyric(url):   
    browser = webdriver.PhantomJS(executable_path='phantomjs.exe')
    browser.get(url)
    html = browser.page_source
    lyric=""
    a=BeautifulSoup(html,"html.parser")
    b=a.find("div",id="hiddenLyricHtml", class_="pd_lyric")
    if b is not None:
        for text in b:
            lyric+=text.extract()
    return lyric

#Các hàm crawl data ở trên chỉ phù hợp với link album top 100 bài hát trên trang nhaccuatui.com, 
#link web thay đổi từng ngày nên nếu bị lỗi phải chỉnh sửa lại code các hàm crawl_lyric, crawl_names, crawl_links

urls=[]
urls.append("https://www.nhaccuatui.com/top100/top-100-rap-viet.iY1AnIsXedqE.html")
urls.append("https://www.nhaccuatui.com/top100/top-100-nhac-tre.m3liaiy6vVsF.html")
urls.append("https://www.nhaccuatui.com/top100/top-100-tru-tinh.RKuTtHiGC8US.html")
urls.append("https://www.nhaccuatui.com/top100/top-100-nhac-trinh.v0AGjIhhCegh.html")
urls.append("https://www.nhaccuatui.com/top100/top-100-tien-chien.TDSMAL1lI8F6.html")
urls.append("https://www.nhaccuatui.com/top100/top-100-remix-viet.aY3KIEnpCywU.html")

#crawl link và tên bài hát
links=[]
names=[]
for url in urls:
    links+=crawl_links(url)
    names+=crawl_names(url)


count=0
#biến count để lưu tên dư liệu và sẽ tăng thêm 1 nếu crawl data thành công (0.txt,1.txt...)
#lần sau muốn crawl tiếp dữ liệu mà không xóa file do trùng tên thì thay count bằng số file đã crawl được ở lần trước

dataset=dict()

for index,link in enumerate(links):
    print("Đang crawl dữ liệu bài hát số "+str(index+1)+"|"+names[index],"|....")
    dataset['name']=names[index]
    dataset['link']=link   
    dataset['lyric']=crawl_lyric(link)
    save_as_json(dataset,'./crawl/data/'+str(count)+".json")
    count+=1




