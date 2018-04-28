from bs4 import BeautifulSoup
import requests
import re
import os
import json
 

artworks_list = []
deleted_imgs = []
counter = 1

def main():
    global artworks_list
    with open("deleted_imgs.txt") as in_file:
        for line in in_file:
            img = line.strip("\n")
            deleted_imgs.append(img)

    with open("artist-list.txt") as in_file:
        for line in in_file:
            artist = line.strip("\n")
            get_artworks(artist)
    artworks = remove_deleted_images(artworks_list)
    export_artworks_as_json(artworks)

    

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
                artwork_dict["level"] = "hard"
                artworks_list.append(artwork_dict)
                print(img_id + " added to artworks_list")
                counter += 1
                #download_img(img_id, src)

def export_artworks_as_json(a):
    artwork_json = json.dumps(a, ensure_ascii=False).encode('utf8')
    outfile = open('artworks.json', 'wb+')
    outfile.write(artwork_json)
    print("SUCCESS")
    outfile.close

def remove_deleted_images(a):
    global artworks_list
    artworks = []
    for img in a: 
        img_id = img['img_id']
        if img_id not in deleted_imgs:
            artworks.append(img)
    return artworks


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
    img_path = './artworks2/' + img_id + '.jpg'
    with open(img_path, 'wb+') as handler:
        handler.write(img_data)
    print(img_id + " successfully downloaded")


if __name__ == "__main__":
    main()