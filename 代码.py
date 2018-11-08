import requests
from lxml import etree
base_domain='http://www.dytt8.net'
# url="http://www.dytt8.net/html/gndy/dyzz/list_23_1.html"
heardes={
    'user-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
}
# 获取详情页地址
def get_detall_urls(url):
    request = requests.get(url, headers=heardes)
    text = request.text
    html = etree.HTML(text)
    detail_urle = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urles=map(lambda url:base_domain+url,detail_urle)
    return detail_urles

#获取详情页内容
def parse_detail_page(url):
    movie={}
    repsone=requests.get(url,headers=heardes)
    text=repsone.content.decode(encoding='gbk',errors="ignore")
    html=etree.HTML(text)
    title=html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    movie['title']=title
    zoom=html.xpath("//div[@id='Zoom']")[0]
    img=zoom.xpath(".//img/@src")
    cover=img[0]
    screenshot=img[1]
    movie['cover']=cover
    movie['screenshot']=screenshot
    infos=zoom.xpath(".//text()")
    def paese_info(info,rule):
        return info.replace(rule,"").strip()
    for indec,info in enumerate(infos):
        if info.startswith("◎产　　地"):
            info=paese_info(info,"◎产　　地")
            movie['coutry']=info
        elif info.startswith("◎类　　别"):
            info=paese_info(info,"◎类　　别")
            movie['type']=info
        elif info.startswith("◎豆瓣评分"):
            info=paese_info(info,"◎豆瓣评分")
            movie['douban']=info
        elif info.startswith("◎片　　长"):
            info=paese_info(info,"◎片　　长")
            movie['movieTime']=info
        elif info.startswith("◎导　　演"):
            info=paese_info(info,"◎导　　演")
            movie['Daoyuan']=info
        elif info.startswith("◎主　　演"):
            info=paese_info(info,"◎主　　演")
            actors=[]
            actors=[info]
            for x in range(indec+1,len(infos)):
                actor=infos[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor)
            movie['actors']=actors
        elif info.startswith("◎简　　介"):
            for x in range(indec+1,len(infos)):
                profile=infos[x].strip()
                if profile.startswith("【下载地址】"):
                    break
            movie['profile']= profile
    downlode_url=html.xpath("//td[@bgcolor='#fdfddf']/a/@href")
    movie['down_url']=downlode_url
    return movie

# 获取内容数组
def spider():
    base_url="http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"
    movies=[]
    for x in range(1,8):
        url=base_url.format(x)
        print(url)
        detail_urls=get_detall_urls(url)
        print(detail_urls)
        for detail_url in detail_urls:
            movie=parse_detail_page(detail_url)
            movies.append(movie)
            print(movie)

if __name__=='__main__':
    spider()
