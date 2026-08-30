import requests
from bs4 import BeautifulSoup

def get_news(url="https://ria.ru/"):
    """
    Собирает новости сайта ria.ru из блока: 'Главное'
    Returns:
        result(list) - Список словарей, содержащих заголовок и ссылку на новость
    """
    result = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.find_all("a", class_="cell-list__item-link color-font-hover-only")
    for i in text:
        result.append({
            "title": i.get("title"),
            "url": i.get("href")
        })
        print(f'{i.get("title")} - {i.get("href")}')
    return result


    
def get_news_more_info(news_list):
    """
    Собирает подробную информацию о новостях из списка
    Args:
        news_list - список словарей типа: {"title": "", "url": ""}
    Returns:
        result - Список словарей, содержащих заголовок и подробную информацию
    """
    result = []
    for i in news_list:
        response = requests.get(i["url"])
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.find_all("div", class_ = "article__text")
        info = ""
        for j in text:
            info += f'{j.get_text()}\n'
        result.append({
            "title": i["title"],
            "info": info
        })
    return result

def get_more_info_one(url):
    response = requests.get(url)
    result = ""
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.find_all("div", class_ = "article__text")
    for j in text:
        result += f'{j.get_text()}\n' 
    return result

if __name__ == "__main__":
    test = get_news()
    test2 = get_news_more_info(test)
    print(test2)