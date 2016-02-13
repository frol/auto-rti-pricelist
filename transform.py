#encoding: utf-8

import csv
import os
from pytils.translit import slugify

BUF_SIZE = 1024

PRICE_FIELD_MAPPING = {
#    'Код'
    'catalog_number': u"Каталожный номер",
    'name': u"Наименование",
    'price': u"Цена",
#    "Диллер"
#    "Нал"
#    "Метка"
    'category': u"Категория",
    'vehicle': u"Машина",
#    "Класс"
    'manufacturer': u"Производитель",
#    "Фото"
}

FIELD_TO_TITLE_MAPPING = {
    'catalog_number': u"Каталожный номер",
    'name': u"Наименование",
    'price': u"Цена (опт)",
    'manufacturer': u"Производитель",
}

VISIBLE_FIELDS = ['name', 'catalog_number', 'manufacturer', 'price']
MARKER_FIELDS = ['vehicle', 'category']
MARKER_FIELD_CHOICES = {field: {} for field in MARKER_FIELDS}

def markers(csv_line):
    marker_list = []
    for field in MARKER_FIELDS:
        choice_name = csv_line[PRICE_FIELD_MAPPING[field].encode('utf-8')].decode('utf-')
        choice = slugify(choice_name)
        if choice not in MARKER_FIELD_CHOICES[field]:
            MARKER_FIELD_CHOICES[field][choice] = choice_name
        marker_list.append('marker_%s' % choice)
    return ' '.join(marker_list)

def main():
    with open('pricelist.html', 'w') as pricelist_html_file:
        pricelist_html_file.write('<meta charset="utf-8" />\n')
        pricelist_html_file.write('<link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css">\n')
        pricelist_html_file.write('<link href="static/css/base.css" rel="stylesheet" type="text/css">\n')

        with open('~pricelist.html', 'w') as tmp_pricelist_html_file:
            tmp_pricelist_html_file.write('<div class="table table-striped"><table id="price_table"><thead><tr>')
            for field in VISIBLE_FIELDS:
                tmp_pricelist_html_file.write('<th class="title_%s">%s</th>' % (field, FIELD_TO_TITLE_MAPPING[field].encode('utf-8')))
            tmp_pricelist_html_file.write('</tr></thead><tbody>')

            with open('price.csv', 'r') as csv_file:
                csv_data = csv.DictReader(csv_file, delimiter=';')
                csv_data.fieldnames = [name.strip() for name in csv_data.fieldnames]
                for csv_line in csv_data:
                    tmp_pricelist_html_file.write('<tr class="priceline %s">' % markers(csv_line))
                    for field in VISIBLE_FIELDS:
                        tmp_pricelist_html_file.write(
                            '<td class="value_%s">%s</td>' % (
                                field,
                                csv_line[PRICE_FIELD_MAPPING[field].encode('utf-8')]
                            )
                        )
                    tmp_pricelist_html_file.write('</tr>')

            tmp_pricelist_html_file.write('</tbody></table></div>')

        for field in MARKER_FIELDS:
            pricelist_html_file.write('<label style="float: left; padding: 8px;">%s: <select id="filter_%s" class="filter" style="width: 150px;">' % (PRICE_FIELD_MAPPING[field].encode('utf-8'), field))
            pricelist_html_file.write('<option selected="selected" value="all">Все</option>')
            sorted_choices = MARKER_FIELD_CHOICES[field].items()
            sorted_choices.sort(key=lambda x: x[1])
            for choice, choice_name in sorted_choices:
                pricelist_html_file.write(('<option value="%s">%s</option>' % (choice, choice_name)).encode('utf-8'))
            pricelist_html_file.write('</select></label>')
        pricelist_html_file.write('<div style="clear: both;"></div>')

        with open('~pricelist.html', 'r') as tmp_pricelist_html_file:
            while 1:
                buf = tmp_pricelist_html_file.read(BUF_SIZE)
                if buf == '':
                    break
                pricelist_html_file.write(buf)
            tmp_pricelist_html_file.close()
        os.unlink(tmp_pricelist_html_file.name)

        pricelist_html_file.write('\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js"></script><script type="text/javascript" src="static/js/jquery.fixheadertable.min.js"></script><script src="static/js/filters.js"></script>')


if __name__ == '__main__':
    main()
