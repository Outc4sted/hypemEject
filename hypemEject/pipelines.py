# -*- coding: utf-8 -*-
from datetime import datetime


class HypemejectPipeline(object):

    def process_item(self, data, spider):
        #title
        data['title'] = data['title'].replace(' - go to page for this track', '')

        #name
        data['name'] = '%s - %s' % (data['artist'], data['title'])

        #favCount
        favCount = data['favCount'].replace('K', '00').replace('.', '').strip()
        data['favCount'] = int(favCount)

        #source
        if 'source' in data:
            data['source'] = '/'.join(data['source'].split("/")[:-1])

        #url
        if data['url'] is None:
            del data['url']
        else:
            data['url'] = data['url'].replace('?utm_source=hypem', '')

        #dateLoved
        dateLoved = data['dateLoved'].replace('. also loved by ', '').replace('Loved ', '').replace('on ', '').strip()
        index = -1 
        for ordinal in ['st', 'nd', 'rd', 'th']:
            if dateLoved.rfind(ordinal) > index:
                index = dateLoved.rfind(ordinal)

        if dateLoved[index-2] == ' ':
            dateLoved = dateLoved[:index-2] + ' 0' + dateLoved[index-1:]
            index += 1

        dateLoved = dateLoved[0: index:] + dateLoved[index + 2::]

        if ',' not in dateLoved:
            dateLoved = dateLoved + ', 2020'

        try:
            data['dateLoved'] = datetime.strptime(dateLoved, '%b %d, %Y').strftime('%m/%d/%Y')
        except:
            data['dateLoved'] = dateLoved

        finally:
            return data
