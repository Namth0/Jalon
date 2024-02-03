import requests
from bs4 import BeautifulSoup

url = {
    "https://ultimate-mushroom.com/poisonous/103-abortiporus-biennis.html",
    "https://ultimate-mushroom.com/edible/1010-agaricus-albolutescens.html",
    "https://ultimate-mushroom.com/inedible/452-byssonectria-terrestris.html"
}

def comestible(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        div_content = soup.find('div', class_='cat_link')
        if div_content:
            a_tag = div_content.find('a')
            if a_tag:
                text = a_tag.text.lower()
                if "poisonous" in text:
                    return "P"
                elif "edible" in text and "inedible" not in text:
                    return "E"
                elif "inedible" in text:
                    return "I"
        return ""
    except Exception as e:
        print(f"Error processing URL: {e}")
        return ""


for u in url:
    print(f"{u} -> {comestible(u)}")
