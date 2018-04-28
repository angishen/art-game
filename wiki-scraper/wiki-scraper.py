from bs4 import BeautifulSoup
import requests
import re
import os
 
artworks_list = []
counter = 1

def main():
    with open("artist-list.txt") as in_file:
        for line in in_file:
            artist = line.strip("\n")
            get_artworks(artist)

def get_artworks(artist):
    global counter
    # acceptable file extensions
    file_extensions = ['jpg', 'jpeg', 'png']
    r = requests.get('https://en.wikipedia.org/wiki/' + artist)
    soup = BeautifulSoup(r.text, "html.parser")
    # get all anchor tags with class="image"
    anchor_tags = soup.select("a[class=image]")
    for a in anchor_tags:
        artwork_dict = {}
        # get src from image tag nested inside anchor tags
        src = a.select("img")[0].get('src')
        # resize all images 650px
        src = re.sub(r'[0-9]*px', "650px", src).strip("//")
        href = a.get('href')
        if href[-3:] in file_extensions:
           title = get_img_title(href)
           if title != None:
                n = 4 - len(str(counter))
                img_id = 'img' + n*str(0) + str(counter)
                artwork_dict["img_id"] = img_id
                artwork_dict["title"] = title
                artwork_dict["artist"] = artist
                artwork_dict["is_easy"] = False
                artworks_list.append(artwork_dict)
                counter += 1
                download_img(img_id, src)
                
# get title of image from wikipedia
def get_img_title(href):
    r = requests.get('https://en.wikipedia.org' + href)
    soup = BeautifulSoup(r.text, "html.parser") 
    title_elt = soup.select("td[id=fileinfotpl_art_title] + td > span")
    #artist_elt = soup.select("td[id=fileinfotpl_aut] + td > div > table > tr > th > span")
    if len(title_elt) > 0:
        return title_elt[0].text

# downloads image from url and stores in artworks folder 
def download_img(img_id, url):
    img_data = requests.get('http://' + url).content
    img_path = './artworks/' + img_id + '.jpg'
    with open(img_path, 'wb+') as handler:
        handler.write(img_data)
    print(img_id + " successfully downloaded")


if __name__ == "__main__":
    main()