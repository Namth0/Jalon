import requests
import pandas as pd
from bs4 import BeautifulSoup

# fonction pour récupérer la comestibilité du champignon
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

# fonction pour récupérer la couleur du champignon
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
                    color = a_tag.text + "" + a_tag.find_next_sibling('a').text
                else:
                    color = a_tag.text
        return color
    except Exception as e:
        print(f"Error processing URL: {e}")
    return ""

# fonction pour récupérer la forme du champignon
def shape(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        div_content = soup.find('div', class_='mprofile')
        if div_content:
            p_tags = div_content.find_all('p')
            if len(p_tags) >= 2:  
                second_p_tag = p_tags[1] 
                a_tag = second_p_tag.find('a')
                if a_tag and a_tag.find_next_sibling('a'):
                    shape = a_tag.find_next_sibling('a').text.replace(" ", "").replace("-", "")  # Suppression des espaces et des tirets
                else:
                    shape = a_tag.text.replace(" ", "").replace("-", "")  # Suppression des espaces et des tirets
                return shape
    except Exception as e:
        print(f"Erreur lors du traitement de l'URL : {e}")
    return ""

# fonction pour récupérer la surface du champignon
def surface(url):
     try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            div_content = soup.find('div', class_='mprofile')
            if div_content:
                p_tags = div_content.find_all('p')
                if len(p_tags) >= 3:  
                    third_p_tag = p_tags[2]  
                    a_tag = third_p_tag.find('a')
                    if a_tag and a_tag.find_next_sibling('a'):
                        surface = a_tag.find_next_sibling('a').text.replace(" ", "")  
                    else:
                        surface = a_tag.text.replace(" ", "")  
                    return surface
     except Exception as e:
         print(f"Erreur lors du traitement de l'URL : {e}")
     return ""

# fonction pour récupérer les urls des champignons
def get_mushroom_urls(main_url):
    mushroom_urls = []
    try:
        page = requests.get(main_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if href.startswith("https://ultimate-mushroom.com/") and href.endswith(".html"):
                mushroom_urls.append(href)
    except Exception as e:
        print(f"Error fetching mushroom URLs: {e}")
    return mushroom_urls

# fonction pour créer une ligne csv
def create_csv_line(url):
    if url:
        comestibility = comestible(url)
        color_value = color(url)
        shape_value = shape(url)
        surface_value = surface(url)
        return f"{comestibility},{color_value},{shape_value},{surface_value}"
    return ""

# fonction pour ecrire dans le csv les données
def f():
    main_url = "https://ultimate-mushroom.com/mushroom-alphabet.html"
    mushroom_urls = get_mushroom_urls(main_url)
    
    with open('champignons.csv', 'w') as file:
        for i,url in enumerate(mushroom_urls,start=1):
            print(f"Processing URL {i}/{len(mushroom_urls)}: {url}")
            csv_line = create_csv_line(url)
            file.write(f"{csv_line}\n")

# Ouvrir le fichier CSV en mode append ('a') pour ajouter la première ligne sans supprimer les données existantes
def f2():
    with open('champignons.csv', 'a') as file:
        file.write("Edible,Color,Shape,Surface\n")

# f() # Appel de la fonction pour écrire dans le csv les données
#f2() # Appel de la fonction pour ajouter la première ligne sans supprimer les données existantes

champignons = pd.read_csv('champignons.csv')

print(champignons.head())
print(champignons.tail())
print(champignons.shape)

# Inspection des elements de edibles Q8
print(champignons['Edible'].value_counts())
na_in_Edi = champignons['Edible'].isna().sum()
print("NA    "+ str(na_in_Edi))

# on remplace E I P par 0 1 2
def replace_Edible(champignons):
    champignons['Edible'].replace({'E': 0, 'I': 1, 'P': 2,}, inplace=True)
    if champignons['Edible'].isna().sum() > 0:
        champignons['Edible'].fillna(-1, inplace=True)
    return champignons

# on mets à jour la colonne Edible
champignons = replace_Edible(champignons)

#debug
print(champignons.head())
print(champignons.tail())
print(champignons['Edible'].value_counts())