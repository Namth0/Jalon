import requests
import pandas as pd
from bs4 import BeautifulSoup

pd.set_option('future.no_silent_downcasting', True)

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
champignons.insert(len(champignons.columns) - 1, "TrueMorels", 0)

# Inspection des elements de edibles Q8
"""print(champignons['Edible'].value_counts())
na_in_Edi = champignons['Edible'].isna().sum()
print("NA    "+ str(na_in_Edi))"""

# on remplace E I P par 0 1 2 , Q9 et Q10 on remplace les valeurs manquantes par -1
def replace_Edible(champignons):
    champignons['Edible'].replace({'E': 0, 'I': 1, 'P': 2,}, inplace=True)
    if champignons['Edible'].isna().sum() > 0:
        champignons['Edible'].fillna(-1, inplace=True)
    return champignons

# on mets à jour la colonne Edible
champignons = replace_Edible(champignons)

#debug
def debug():
    print(champignons.head())
    print("\n")
    print(champignons.tail())
    print("\n")
    print(champignons['Edible'].value_counts())

""" Question 11 -> pd.unique(champignons["Shape"].str.split("-").explode().dropna())

# 1. str.split("-"), Sépare chaque élément de la colonne "Shape" en une liste de sous-chaînes en utilisant le séparateur "-"
# 2. explode(), Transforme les listes résultantes en autant de lignes distinctes que d'éléments dans ces listes
# 3. dropna(), Supprime les valeurs nulles du DataFrame résultant, au cas où il y en aurait
# 4. Renvoie toutes les formes uniques de champignons extraites de la colonne "Shape"

"""

def add_shape_col_and_surface_col(df):
    for shape_value in pd.unique(df["Shape"].str.split("-").explode().dropna()):
        df[shape_value] = df["Shape"].str.contains(shape_value).fillna(False).astype(int)
        
    for surface_value in pd.unique(df["Surface"].str.split("-").explode().dropna()):
        df[surface_value] = df["Surface"].str.contains(surface_value).fillna(False).astype(int)
        
    return df

# Utilisation de la fonction pour ajouter les colonnes de forme,surface de champignon Q12 et Q13
champignons = add_shape_col_and_surface_col(champignons)

# Supprimer les colonnes "Shape" et "Surface"
champignons = champignons.drop(columns=["Shape", "Surface"])

#debug()

# Vérification de la taille du DataFrame
print(champignons.shape)  

# Question 14: Etablir la liste des couleurs individuelles présentes dans notre jeu de données
colors = pd.unique(champignons["Color"].str.split("-").explode().dropna())
num_colors = len(colors)

print(f"Le nombre de couleurs individuelles présentes dans notre jeu de données est de {num_colors}.")
print(colors)

#question 15
COLOR_MAP = {
    "White": (255, 255, 255),
    "Pale": (218, 211, 200),
    "Yellow": (255, 255, 0),
    "Brown": (165, 42, 42),
    "Pink": (255, 192, 203),
    "Purple": (128, 0, 128),
    "Tan": (210, 180, 140),
    "Orange": (255, 165, 0),
    "Gray": (128, 128, 128),
    "Red": (255, 0, 0),
    "Dark": (0, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Violet": (238, 130, 238),
    "Lilac": (227, 191, 242)
}

# Création du DataFrame color_df avec les couleurs et les valeurs RGB correspondantes
color_df = pd.DataFrame(columns=["Color", "R", "G", "B"])

def fill_color_df(color_df, colors):
    for color in colors:
        r, g, b = COLOR_MAP.get(color, (0, 0, 0))  # Valeurs RGB à partir de COLOR_MAP, sinon (0, 0, 0)
        color_df.loc[len(color_df)] = {"Color": color, "R": r, "G": g, "B": b}
    return color_df

colors = list(COLOR_MAP.keys())  # Utilisez les clés du dictionnaire COLOR_MAP comme couleurs
color_df = fill_color_df(color_df, colors) # Remplir le DataFrame color_df avec les couleurs et les valeurs RGB correspondantes
print(color_df)

#question 16

champignons["Color"] = champignons["Color"].fillna("")
champignons["Combined_Colors"] = champignons["Color"].str.split("-").apply(frozenset)
colors = pd.DataFrame(champignons["Combined_Colors"].unique(), columns=["Combined_Colors"])

#question 17

def complete_colors_with_mean(colors, color_df):
    # Créer un DataFrame temporaire en explodant les frozensets dans la colonne 'Combined_Colors'
    temp_df = colors['Combined_Colors'].apply(lambda x: list(x) if x else []).explode().reset_index().rename(columns={'Combined_Colors': 'Color', 'index': 'index'})
    merged_df = pd.merge(temp_df, color_df[['Color', 'R', 'G', 'B']], on='Color', how='left')
    merged_df = merged_df.drop('Color', axis=1)
    grouped_df = merged_df.groupby('index').mean()
    colors = pd.merge(colors, grouped_df, left_index=True, right_index=True, how='left')

    return colors

# Appeler la fonction pour compléter colors avec les moyennes des composantes R, G et B
colors = complete_colors_with_mean(colors, color_df)

# Afficher le DataFrame résultant
print(colors)

def complete_champignons_with_rgb(champignons, colors):
    champignons = pd.merge(champignons, colors, left_on='Combined_Colors', right_on='Combined_Colors', how='left')
    champignons = champignons.drop('Combined_Colors', axis=1)
    champignons = champignons.drop('Color', axis=1)
    champignons[['R', 'G', 'B']] = champignons[['R', 'G', 'B']].fillna(-255)
    
    return champignons

champignons = complete_champignons_with_rgb(champignons, colors)
print(champignons)
print(champignons.isna().values.any())
