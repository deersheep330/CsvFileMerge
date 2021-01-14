import csv
from pprint import pprint

filenames = [
    '大腸癌',
    '口腔癌'
]

dicts = {}
for filename in filenames:
    dicts[filename] = {}

def clean_up(str):
    return str.replace("'", "").strip()

def is_missing_data(field):
    if len(field) < 2:
        return True
    else:
        return False

def read_file(filename):
    with open(filename + '.csv', newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            id = clean_up(row['身分證'])
            name = clean_up(row['姓名'])
            birth = clean_up(row['生日'])
            address = clean_up(row['戶籍地址'])
            phones = set()
            phone_fields = {
                '註記電話',
                '註記手機',
                '電話1',
                '電話2',
                '手機1',
                '手機2',
                '電話',
                '手機'
            }
            for field in phone_fields:
                field_value = clean_up(row[field]) if field in row else ''
                if len(field_value) > 4:
                    if field_value.startswith('09'):
                        field_value = field_value[:4] + '-' + field_value[4:]
                    phones.add(field_value)
            dicts[filename][id] = {
                '身分證': id,
                '姓名': name,
                '生日': birth,
                '戶籍地址': address,
                '電話': phones
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
            if is_missing_data(joined_results[id]['姓名']):
                joined_results[id]['姓名'] = obj['姓名']
            if is_missing_data(joined_results[id]['生日']):
                joined_results[id]['生日'] = obj['生日']
            if is_missing_data(joined_results[id]['戶籍地址']):
                joined_results[id]['戶籍地址'] = obj['戶籍地址']
            joined_results[id]['電話'].update(obj['電話'])
            joined_results[id][filename] = 'O'

for id, obj in joined_results.items():
    obj['電話'] = '|'.join(obj['電話'])
    for filename in filenames:
        if filename not in obj:
            obj[filename] = 'X'

#pprint(joined_results)

with open('joined.csv', 'w', newline='') as outfile:
    # output dict needs a list for new column ordering
    headers = ['身分證', '姓名', '生日', '戶籍地址', '電話']
    headers.extend(filenames)
    writer = csv.DictWriter(outfile, fieldnames=headers)
    # reorder the header first
    writer.writeheader()
    for key, value in joined_results.items():
        # writes the reordered rows to the new file
        writer.writerow(value)
