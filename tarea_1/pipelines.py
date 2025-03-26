from datetime import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Tarea1Pipeline:
    def process_item(self, item, spider):
        if 'title' in item and item['title']:
            item['title'] = item['title'].strip()
        if 'link' in item and item['link']:
            item['link'] = item['link'].strip()
        if 'image' in item and item['image']:
            item['image'] = item['image'].strip()
        # if 'date_published' in item and item['date_published']:
        #     item['date_published'] = datetime.strptime(item['date_published'], '%Y-%m-%dT%H:%M:%S%z')
        
        return item
