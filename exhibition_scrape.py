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

        data.append((ex_name, ex_disc, ex_cycle, ex_city, ex_location, ex_date))
    return data

get_data('https://www.eventseye.com/fairs/c1_trade-shows_south-africa.html')

with open('exhibitions.csv', 'a', encoding='utf-8-sig', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['展会名称', '简介', '举办周期', '举办城市','场馆', '日期'])
    for ex_name, ex_disc, ex_cycle, ex_city, ex_location, ex_date in data:
        writer.writerow([ex_name, ex_disc, ex_cycle, ex_city, ex_location, ex_date])