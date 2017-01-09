# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import re
import os


"""
TODO

multi thread
handling exception

"""

def download_web_images(file_name, image_url):

    print(file_name)
    urllib.request.urlretrieve(image_url, file_name)


def get_inner_pages(bsObj, url):

    internalLinks = []
    title = []

    for link in bsObj.find("div",{"id":"post"}).\
            find("div",{"class":"contents"}).select("p > a"):
        if link.find("img"):
            pass
        else:
            if link.attrs['href'] is not None:
                if link.attrs['href'] not in internalLinks:
                    convert_title = link.get_text().replace('\u2013','-')
                    if(convert_title != '다음편 보기'):
                        title.append(convert_title)
                        internalLinks.append(link.attrs['href'])

    return internalLinks, title

def get_pages(url):

    title = []

    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    #IS EXIST INNER PAGES ?
    innerPages, title = get_inner_pages(bsObj, url)

    if len(innerPages) == 0:
        go_to_image_url(bsObj, url)

    else:
        for i, page in enumerate(innerPages):
            get_pages(innerPages[i])

def go_to_image_url(bsObj, url):
    global dirname

    # file_name

    # 000.jpg or 000.JPG
    images = bsObj.findAll("img", src=re.compile("(...\.(jpg|JPG))$"))
    title_tag = bsObj.find("div",{"id":"post"}).span
    title = title_tag.get_text()

    os.chdir(dirname)



    if not os.path.isdir(title):
        print(title + " is not exist")
        os.mkdir(title)
        os.chdir(dirname+"\\"+title)

        print("=== 2. download images ===")
        count_filename = 000
        for image in images:
            image_url = image.attrs['src']
            count_filename = int(count_filename) + 1
            file_name = "0"*(3-len(str(count_filename))) + str(count_filename)+".jpg"
            download_web_images(file_name, image_url)

    else:
        print(title + " is exist")



if __name__ == "__main__":

    dirname = os.path.expanduser("~\\Desktop")
    os.chdir(dirname)
    folder_name = "cartoon"
    if os.path.isdir(folder_name):
        pass
    else:
        os.mkdir(dirname+"\\"+folder_name)

    dirname = dirname+"\\"+folder_name

    print("=== 1. page searching ===")

    get_pages("http://zangsisi.net/?page_id=1729")
