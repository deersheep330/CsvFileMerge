import csv
from pathlib import Path

def clean_up(str):
    return str.replace("'", "").strip()

def is_missing_data(field):
    if len(field) < 2:
        return True
    else:
        return False


class CsvMerger():

    def __init__(self, print=print):
        self.print = print
        self.__reset__()

    def __reset__(self):
        self.dicts = {}
        self.joined_results = {}
        self.category_list = []

    def __read_file__(self, filename, category):
        self.dicts[category] = {}
        with open(filename, newline='') as csvfile:
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
                self.dicts[category][id] = {
                    '身分證': id,
                    '姓名': name,
                    '生日': birth,
                    '戶籍地址': address,
                    '電話': phones
                }
                # print(id, name, birth, address, list(phones))

    def __join_results__(self):
        for category, _dict in self.dicts.items():
            self.print(f'合併類別: {category}')
            for id, record in _dict.items():
                if id not in self.joined_results:
                    self.joined_results[id] = record
                    self.joined_results[id][category] = 'O'
                else:
                    if is_missing_data(self.joined_results[id]['姓名']):
                        self.joined_results[id]['姓名'] = record['姓名']
                    if is_missing_data(self.joined_results[id]['生日']):
                        self.joined_results[id]['生日'] = record['生日']
                    if is_missing_data(self.joined_results[id]['戶籍地址']):
                        self.joined_results[id]['戶籍地址'] = record['戶籍地址']
                    self.joined_results[id]['電話'].update(record['電話'])
                    self.joined_results[id][category] = 'O'

        for id, record in self.joined_results.items():
            record['電話'] = '|'.join(record['電話'])
            for category in self.category_list:
                if category not in record:
                    record[category] = 'X'

    def __write_file__(self, filename):
        self.print(f'合併檔案寫入到: {filename}')
        with open(filename, 'w', newline='') as outfile:
            # output dict needs a list for new column ordering
            headers = ['身分證', '姓名', '生日', '戶籍地址', '電話']
            headers.extend(self.category_list)
            writer = csv.DictWriter(outfile, fieldnames=headers)
            # reorder the header first
            writer.writeheader()
            for key, value in self.joined_results.items():
                # writes the reordered rows to the new file
                writer.writerow(value)

    def merge(self, input_filename_list, output_filename):
        try:
            self.__reset__()
            for filename in input_filename_list:
                category = Path(filename).stem
                self.category_list.append(category)
                self.__read_file__(filename, category)
                self.print(f'取得 {len(list(self.dicts[category]))} 筆記錄從 {filename}')
            self.__join_results__()
            self.__write_file__(output_filename)
            self.print(f'合併成功!')
        except Exception as e:
            self.print(f'!!!! 合併檔案失敗 !!!!')
            self.print(f'{e}')
