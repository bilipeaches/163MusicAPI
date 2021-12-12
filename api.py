# API - 用于main.py的请求
import json
import requests
from bs4 import BeautifulSoup

# 搜索次数
search_num = 5
# 伪装,不然会被必应拦截
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'
}

# 搜索
def Search(music_name):
    url = "https://cn.bing.com/search?q=site:music.163.com+单曲-%s-网易云音乐&first=%s"
    url_list = []
    for i in range(search_num):
        i += 1
        if i == 1:
             index = ""
        else:
            index = str(i - 1)
        _url = url % (music_name, index + "1")
        url_list.append(_url)
    return url_list

# 返回链接
def GetLinks(music_name):
    urls = Search(music_name)
    music_links = []
    for i in urls:
        text = requests.get(i, headers=header).text
        soup = BeautifulSoup(text, "lxml")
        links = soup.find_all('a')
        for link in links:
            try:
                if "song" in link["href"] and link["href"] not in music_links:
                    music_links.append(link["href"])
            except:
                pass
    return music_links

# 信息
def GetInfo(urls):
    info = {}
    titles = []
    images = []
    singer = []
    ids = []
    # 如有不符,则减掉
    index = len(urls)
    for url in urls:
        if "music.163.com" in url:
            html = requests.get(url, headers=header).text
            soup = BeautifulSoup(html, "lxml")
            titles.append(soup.title.string.replace(" - 网易云音乐", ""))
            images.append(soup.select(".u-cover-6 img")[0]["data-src"])
            singer.append(soup.select(".m-lycifo .des span")[0].string)
            ids.append(url.replace("https://", "").replace("music.163.com/song?id=", ""))
        else:
            index -= 1
    info["titles"] = titles
    info["images"] = images
    info["singer"] = singer
    info["ids"] = ids
    return [info, index]

# 返回歌词
def GetLyric(id):
    url = "http://music.163.com/api/song/media?id=" + id
    text = requests.get(url, headers=header).text
    json_data = json.loads(text)
    try:
        # 无歌词
        return {
            "nolyric":json_data["nolyric"],
            "lyric":"纯音乐,请欣赏"
        }
    except:
        return {
            "nolyric":False,
            "lyric":json_data["lyric"]
        }

# 返回搜索结果
def GetRes(music_name, search_num=5):
    res = []
    search_num = search_num
    music_links = GetLinks(music_name)
    # 信息
    info = GetInfo(music_links)
    for i in range(info[1]):
        res.append({
            "title":info[0]["titles"][i],
            "image":info[0]["images"][i],
            "singer":info[0]["singer"][i],
            "id":info[0]["ids"][i]
        })
    return res
