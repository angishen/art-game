from bs4 import BeautifulSoup
import requests
import re

artist_list = [];  

with open("artist-list.txt") as in_file:
    for line in in_file:
        line = line.strip("\n")
        artist_list.append(line)


def get_artworks(artist):
    paintings_list = [];
    file_extensions = ['jpg', 'jpeg', 'png']
    r = requests.get('https://en.wikipedia.org/wiki/' + artist)
    soup = BeautifulSoup(r.text, "html.parser")
    # get all anchor tags with class="image"
    anchor_tags = soup.select("a[class=image]")
    for a in anchor_tags:
        href = a.get('href')
        if href[-3:] in file_extensions:
           title = get_img_title(href)
           if title != None:
                print(title)

# get title of image
def get_img_title(href):
    r = requests.get('https://en.wikipedia.org' + href)
    soup = BeautifulSoup(r.text, "html.parser")
    title_elt = soup.select("td[id=fileinfotpl_art_title] + td > span")
    artist_elt = soup.select("td[id=fileinfotpl_aut] + td > div > table > tr > th > span")
    if len(title_elt) > 0:
        return title_elt[0].text

    # to do 

get_artworks('Paul Cezanne')
# https://tools.wmflabs.org/magnus-toolserver/commonsapi.php?image=
#get_artworks("Leonardo Da Vinci")

# {'Vincent Van Gogh': [  {'title': 'Starry Night', 'url': 'url.com'},
#                         {'title': 'Sunflowers', 'url': 'url.com'},
#                         {'title': 'Windmills', 'url': 'url.com'} ],
#  "Georgia O'Keefe": [
#                                                     ]
# }

#img['src'] = re.sub(r'[0-9]*px', "512px", img['src']).strip("//")