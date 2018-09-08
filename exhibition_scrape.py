from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

data=[]

def get_data(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')

    ex_tables = soup(class_='ltb')
    ex_table = ex_tables[0]

    ex_rows = ex_table('tr')[1:]

    for ex_row in ex_rows:
        #Get each column
        ex_name_and_disc_box = ex_row.td
        ex_cycle_box = ex_name_and_disc_box.next_sibling.next_sibling
        ex_city_location_box = ex_cycle_box.next_sibling.next_sibling
        ex_date_box = ex_city_location_box.next_sibling.next_sibling

        ex_name = str(ex_name_and_disc_box.a.string)
        ex_disc = str(ex_name_and_disc_box.i.string)
        ex_cycle = str(ex_cycle_box.string)
        try:
            ex_city = str(ex_city_location_box.a.string)
        except:
            ex_city = str(ex_city_location_box.contents[0].strip())
        try:
            ex_location = str(ex_city_location_box.a.next_sibling.next_sibling.br.next_sibling)[2:]
        except:
            ex_location = ''
        ex_date = str(ex_date_box.string).rstrip()

        #Get exhibition page's soup.
        ex_url = 'https://www.eventseye.com/fairs/' + ex_name_and_disc_box.a['href']
        ex_page = urlopen(ex_url)
        ex_soup = BeautifulSoup(ex_page, 'lxml')

        web_boxes = ex_soup(class_='ev-web')
        orgweb_link = web_boxes[1]['href']
        officialweb_link = web_boxes[-1]['href']

        tel_boxes = ex_soup(class_='ev-phone')
        org_tel = tel_boxes[1].string

        mail_boxes = ex_soup(class_='ev-mail')
        org_mail = mail_boxes[-2]['href'][7:]

        data.append((ex_name, ex_disc, ex_cycle, ex_city, ex_location, ex_date, orgweb_link, officialweb_link, org_tel, org_mail))
    return data

base_url = 'https://www.eventseye.com/fairs/c1_trade-shows_south-africa'
get_data(base_url + '.html')

i = 1
while True:
    try:
        url = base_url + '_' + str(i) + '.html'
        get_data(url)
        i += 1
    except:
        break

with open('exhibitions.csv', 'a', encoding='utf-8-sig', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['展会名称', '展会简介', '举办周期', '举办城市', '场馆', '日期', '组委会官网', '展会官网', '联系电话', '电子邮箱'])
    for ex_name, ex_disc, ex_cycle, ex_city, ex_location, ex_date, orgweb_link, officialweb_link, org_tel, org_mail in data:
        writer.writerow([ex_name, ex_disc, ex_cycle, ex_city, ex_location, ex_date, orgweb_link, officialweb_link, org_tel, org_mail])