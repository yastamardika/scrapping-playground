from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import json

url = 'http://103.255.15.33/direktori/direktori_list.php?mastertable=sub_kategori&masterkey1=1000032'

driver = webdriver.Chrome('C:\Tools\chromedriver\chromedriver.exe')
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
page_body = soup.body
page_head = soup.head

all_sanggars = []
all_images = []
sanggars = []
img = []
while True:
    sanggars = soup.find(id="grid_block1").select('table > tbody > tr')
    img = soup.find(id="grid_block1").select('table > tbody > tr > td > a > img', src=True)
    images = soup.find_all('img', src=True)
    page = 1
    try:
        page = page + 1
        driver.find_element_by_xpath("//a[contains(@href, 'JavaScript:GotoPage1("+str(page)+");')]").click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sanggars = soup.find(id="grid_block1").select('table > tbody > tr')
        img = soup.find(id="grid_block1").select('table > tbody > tr > td > a > img', src=True)
        print(sanggars)
    except Exception: break
# for imgs in img:
#     print(imgs)


# for image in images:
#     print(image)
# print(img)
# for pics in img: 
#     print(pics)
image_srcs = [x['src'] for x in img]
for image in image_srcs:
    all_images.append({
        "img": image
    })

i = 0
for sanggar, image_src in zip(sanggars, image_srcs):
    name = sanggar.select('td')[2].text.strip()
    address = sanggar.select('td')[3].text.strip()
    postal = sanggar.select('td')[4].text.strip()
    phone = sanggar.select('td')[5].text.strip()
    mail = sanggar.select('td')[7].text.strip()
    service = sanggar.select('td')[9].text.strip()
    
    all_sanggars.append({
        "id" : i,
        "name" : name,
        "address" : address,
        "postal" : postal,
        "phone" : phone,
        "mail" : mail,
        "service" : service,
        "image" : image_src
        })
    i = i+1

print(all_sanggars)
keys = all_sanggars[0].keys()

# with open('sanggar.csv', 'w', newline='') as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(all_sanggars)

# with open('sanggar.json','w') as output_file:
#     json.dump(all_sanggars, output_file, indent=8, ensure_ascii = False)
#     print('JSON Exported!')