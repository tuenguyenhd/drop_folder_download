# Test https://www.dropbox.com/sh/m1e2scmr3lcwgu4/AABKyZyKGeITvpdj_elpPaOta?lst=

from lxml import html
import requests
import pdb
import sys

# Get image names from dropbox shared folder
def get_images(drop_folder_link):
    drop_page = requests.get(drop_folder_link)
    tree = html.fromstring(drop_page.content)
    list_image_tree = tree.xpath('//*[@id="list-view-container"]/ol')
    results = []
    if len(list_image_tree) == 1:
        list_images = list_image_tree[0].xpath('//a[@class="file-link filename-link"]')
        for image in list_images:
            results.append(image.attrib['href'].replace("https://www","https://dl").replace("?dl=0",""))
    return results
    
# Download file with url
def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    return local_filename    

if len(sys.argv) == 2:
    drop_folder_link = sys.argv[1]
    results = get_images(drop_folder_link)
    for url in results:
        print url
        download_file(url)    
else:
    print "python shared_drop shared_link_folder"
    
