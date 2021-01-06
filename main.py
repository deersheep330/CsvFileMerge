import csv
from pprint import pprint

filenames = [
    'oral_cancer',
    'colon_cancer'
]

dicts = {}
for filename in filenames:
    dicts[filename] = {}

def read_file(filename):
    with open(filename + '.csv', newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            id = row['身分證'].replace("'", "")
            name = row['姓名'].replace("'", "")
            birth = row['生日'].replace("'", "")
            address = row['戶籍地址'].replace("'", "")
            phones = set()
            if len(row['註記電話'].replace("'", "").strip()) > 2:
                phones.add(row['註記電話'].replace("'", "").strip())
            if len(row['註記手機'].replace("'", "").strip()) > 2:
                phones.add(row['註記手機'].replace("'", "").strip())
            if len(row['電話1'].replace("'", "").strip()) > 2:
                phones.add(row['電話1'].replace("'", "").strip())
            if len(row['電話2'].replace("'", "").strip()) > 2:
                phones.add(row['電話2'].replace("'", "").strip())
            if len(row['手機1'].replace("'", "").strip()) > 2:
                phones.add(row['手機1'].replace("'", "").strip())
            if len(row['手機2'].replace("'", "").strip()) > 2:
                phones.add(row['手機2'].replace("'", "").strip())
            dicts[filename][id] = {
                'id': id,
                'name': name,
                'birth': birth,
                'address': address,
                'phones': phones
            }
            #print(id, name, birth, address, list(phones))

for filename in filenames:
    read_file(filename)

for key, value in dicts.items():
    print(key, len(list(value)))

joined_results = {}
for filename, _dict in dicts.items():
    for id, obj in _dict.items():
        if id not in joined_results:
            joined_results[id] = obj
            joined_results[id][filename] = 'O'
        else:
            joined_results[id]['name'] = obj['name'] if len(joined_results[id]['name']) < 2 else joined_results[id]['name']
            joined_results[id]['birth'] = obj['birth'] if len(joined_results[id]['birth']) < 2 else joined_results[id]['birth']
            joined_results[id]['address'] = obj['address'] if len(joined_results[id]['address']) < 2 else joined_results[id]['address']
            joined_results[id]['phones'].update(obj['phones'])
            joined_results[id][filename] = 'O'

for id, obj in joined_results.items():
    obj['phones'] = '|'.join(obj['phones'])
    for filename in filenames:
        if filename not in obj:
            obj[filename] = 'X'

#pprint(joined_results)

with open('joined.csv', 'w', newline='') as outfile:
    # output dict needs a list for new column ordering
    headers = ['id', 'name', 'birth', 'address', 'phones']
    headers.extend(filenames)
    writer = csv.DictWriter(outfile, fieldnames=headers)
    # reorder the header first
    writer.writeheader()
    for key, value in joined_results.items():
        # writes the reordered rows to the new file
        writer.writerow(value)
