# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import re

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ParserJobPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.db_vacancies
  

    def process_item(self, item, spider):
      if spider.name == 'rabota_ru':
        item['company_name'] = ''.join(re.sub("^\s+|\n|\r|\s+$", '', item['company_name']))
        item['name'] = ''.join(re.sub("^\s+|\n|\r|\s+$", '', item['name']))
      item['company_name'] = ''.join(item['company_name']).replace('\xa0', '')
      salary_dict = {}
      span = self.restructuring_srt(item['salary'])
      salary_dict['от'] = span[0]
      salary_dict['до'] = span[1]
      salary_dict['валюта'] = span[2]
      item['salary'] = salary_dict
      try:
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
      except DuplicateKeyError:
        print(f"Дубль! Запись о вакансии <{item['name']}> уже есть в базе")
        collection = self.mongo_base[spider.name]
        collection.replace_one({'_id': item['_id']}, item)
      return item

    def restructuring_srt(self, vacancy_salary):
        vacancy_salary = ''.join(vacancy_salary)
        minimal_salary, maximal_salary, currency_name_letter, additional_verification = None, None, [], []
        if vacancy_salary:
            string_salary = vacancy_salary.replace('\xa0', ' ').replace('\n', '')
            for letter in string_salary[::-1]:
                if letter.isdigit():
                    additional_verification.append(letter)
                    break
                currency_name_letter.append(letter)
            if additional_verification:
                currency_name = ''.join(currency_name_letter[::-1]).replace('\xa0', '').strip()
                if len(currency_name) > 5:
                    if ' ' in currency_name:
                        currency_name = currency_name[0:currency_name.index(' ')]
                    elif '/' in currency_name:
                        currency_name = currency_name[0:currency_name.index('/')]
            else:
                currency_name = None
            min_split_salary, max_split_salary = '', ''
            for i in string_salary.split(' '):
                if i != 'до' and i != '–' and i !='-' and i != '—':
                    min_split_salary = ''.join(re.findall('(\d+)', string_salary))
                    if min_split_salary:
                        minimal_salary = int(min_split_salary)
                else:
                    min_split_salary = string_salary[:string_salary.index(i)]
                    if min_split_salary:
                        minimal_salary = ''.join(re.findall('(\d+)', min_split_salary))
                        if minimal_salary:
                            minimal_salary = int(minimal_salary)
                    max_split_salary = string_salary[string_salary.index(i):]
                    if max_split_salary:
                        maximal_salary = ''.join(re.findall('(\d+)', max_split_salary))
                        if maximal_salary:
                            maximal_salary = int(maximal_salary)
                    break
            return minimal_salary, maximal_salary, currency_name
        currency_name = None
        return minimal_salary, maximal_salary, currency_name

