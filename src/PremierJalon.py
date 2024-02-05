import requests
from bs4 import BeautifulSoup

url = {
    "https://ultimate-mushroom.com/poisonous/103-abortiporus-biennis.html",
    "https://ultimate-mushroom.com/edible/1010-agaricus-albolutescens.html",
    "https://ultimate-mushroom.com/inedible/452-byssonectria-terrestris.html",
    "https://ultimate-mushroom.com/poisonous/1010-agaricus-albolutescens.html"
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
    
def color(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        div_content = soup.find('div', class_='mprofile')
        if div_content:
            p_tag = div_content.find('p')
            if p_tag:
                a_tag = p_tag.find('a')
                if a_tag and a_tag.find_next_sibling('a'):
                    color = a_tag.text + "-" + a_tag.find_next_sibling('a').text
                else:
                    color = a_tag.text
        return color
    except Exception as e:
        print(f"Error processing URL: {e}")
        return ""


for u in url:
    print(f"{u} -> {comestible(u)}")

for i in url:
    print(f"{i} -> {color(i)}")