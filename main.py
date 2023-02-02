import csv
from pprint import pprint
import re
from pandas import pandas as pd
import itertools


def main(file1):
    """функция для чтения данных и группировки их"""
    with open(file1, mode="r", encoding='utf-8') as file:
        reader = csv.reader(file)
        full_list = list()
        PHONE = r"(\+7|8)\s*?\(?(\d{3})\)?[-|\s]*?(\d{3})[-|\s]*?(\d{2})[-|\s]*?(\d{2})[\s*|-|(]*(добавочный|доб\.)*[\s*|-|(]*(\d{4})*"
        PHONE_SUB = r'+7(\2)\3-\4-\5 \6 \7'

        for item in reader:
            full_name_pre = ' '.join(item[:3]).split(' ')
            test = re.sub(PHONE, PHONE_SUB, item[5])
            result = [full_name_pre[0], full_name_pre[1], full_name_pre[2], item[3], item[4],
                      re.sub(rf'{PHONE}', PHONE_SUB, item[5]),
                      item[6]]
            result[5] = result[5].rstrip()
            full_list.append(result)

    return full_list

def union(contacts: list):
    """функция обработки списка от одинаковых и пустых записях"""
    #------------------------------------------------------------------
    #КАК МОЖНО СДЕЛАТЬ ПОКОРОЧЕ, МОЖЕТ МОЖНО ИСПОЛЬЗОВАТЬ БИБЛИОТЕКУ PANDAS?
    for contact in contacts:
        first_name = contact[0]
        last_name = contact[1]
        for new_contact in contacts:
            new_first_name = new_contact[0]
            new_last_name = new_contact[1]
            if first_name == new_first_name and last_name == new_last_name:
                if contact[2] == "": contact[2] = new_contact[2]
                if contact[3] == "": contact[3] = new_contact[3]
                if contact[4] == "": contact[4] = new_contact[4]
                if contact[5] == "": contact[5] = new_contact[5]
                if contact[6] == "": contact[6] = new_contact[6]
    #-------------------------------------------------------------------
    result_list = list()
    for i in contacts:
        if i not in result_list:
            result_list.append(i)

    # pprint(result_list, width=300)
    return result_list

if __name__ == '__main__':
    result_list = union(main('test_data_file.cvs'))
    with open("phonebook.csv", "w", newline='', encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(result_list)
    df = pd.read_csv("phonebook.csv")
    df.drop_duplicates(subset=None, inplace=True)
    pd.options.display.max_columns = 10
    print(df)