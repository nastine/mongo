import csv
import re
from pprint import pprint
from pymongo import MongoClient


def read_data(csv_file, db):
    with open(csv_file, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            line['Цена'] = int(line['Цена'])
            collection_artists.insert_one(line)


def find_cheapest(db, collection):
    return list(collection.find().sort('Цена'))


def find_by_name(name, db, collection):
    symb = re.search('\/|\'', name)
    if symb != None:
        name = name[0:name.find(str(symb))]+'\\'+name[name.find(str(symb)):]
    regx = re.compile(name, re.IGNORECASE)
    return collection.find_one({"Исполнитель": regx})


if __name__ == '__main__':
    client = MongoClient()
    tickets_db = client['tickets']
    collection_artists = tickets_db['artists']
    # read_data('artists.csv', tickets_db)
    # pprint(find_cheapest(tickets_db, collection_artists))
    pprint(find_by_name('T-', tickets_db, collection_artists))
