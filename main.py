import csv
import re
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime


def read_data(csv_file, db):
    with open(csv_file, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            line['Цена'] = int(line['Цена'])
            line['Дата']= datetime.strptime(line['Дата']+'.20', '%d.%m.%y')
            artists.insert_one(line)


def find_cheapest(db, collection):
    return list(collection.find().sort('Цена'))


def find_date(from_date, to_date, db, collection):
    result = []
    for artist in collection.find({"Дата": {"$gte": datetime.strptime(from_date, '%d.%m.%y'), "$lt": datetime.strptime(to_date, '%d.%m.%y')}}).sort('Цена'):
        result.append(artist)
    return result


def find_by_name(name, db, collection):
    symb = re.search('\/|\'', name)
    if symb != None:
        name = name[0:name.find(str(symb))]+'\\'+name[name.find(str(symb)):]
    regx = re.compile(name, re.IGNORECASE)
    result = []
    for artist in collection.find({"Исполнитель": regx}).sort('Цена'):
        result.append(artist)
    return result

if __name__ == '__main__':
    
    client = MongoClient()
    tickets_db = client['tickets']
    artists = tickets_db['artists']
    read_data('artists.csv', tickets_db)
    pprint(find_cheapest(tickets_db, artists))
    pprint(find_by_name('T-', tickets_db, artists))
    pprint(find_date('01.02.20', '29.02.20', tickets_db, artists))
