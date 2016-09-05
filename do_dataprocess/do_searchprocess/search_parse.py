# -*-coding:utf-8 -*-
# 微博搜索页
import re, demjson, json
from bs4 import BeautifulSoup
from weibo_decorator.decorators import parse_decorator


@parse_decorator(1)
def search_page_parse(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'view\((.*)\)')
    search_cont = ''
    for script in scripts:
        m = pattern.search(str(script))
        if m and 'pl_weibo_direct' in script.string and 'S_txt1' in script.string:
            #search_cont = demjson.decode(m.group(1), encoding='utf-8')['html']
            # search_cont = json.loads(m.group(1), encoding='')
            # print(search_cont)
            search_cont = m.group(1)
            print(search_cont.encode('utf-8', 'ignore').decode('unicode-escape', 'ignore'))
            import execjs
            parse_exec = execjs.compile("""
                function get_json(json_str){
                    return JSON.parse(json_str)
                }
            """)
            cont = parse_exec.call("get_json", search_cont)
            print(cont)
    return search_cont


def _get_search_info(html):
    soup = BeautifulSoup(html, "html.parser")
    all_cont = soup.find(attrs={'class': 'search_feed'})
    print(all_cont)

if __name__ == '__main__':
    with open('g:/360data/重要数据/桌面/search.html', 'r', encoding='utf-8') as f:
        my_str = f.read()
    htm = search_page_parse(my_str)

