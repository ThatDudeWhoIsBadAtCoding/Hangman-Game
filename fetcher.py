from bs4 import BeautifulSoup as bs
import requests
def get_words(url):
    try:
        fetch = requests.get(url).text
    except:
        while True:
            try:
                fetch = requests.get(url).text
                break
            except:
                pass
    soup = bs(fetch, "html.parser")
    needed = soup.find("div", attrs={"style":"margin:6px 0 3px 0;height:368px;overflow-y:auto"})
    all_li = needed.find_all("li")
    result = []
    for li in all_li:
        result.append(li.find("a").string)
    return result
