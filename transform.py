#encoding: utf-8

import csv
import os
from pytils.translit import slugify

BUF_SIZE = 1024

fields = {
#    'Код'
    'catalog_number': 'Каталожный номер',
    'name': 'Наименование',
    'price': 'Цена',
#    'Диллер'
#    'Нал'
#    'Метка'
    'category': 'Категория',
    'vehicle': 'Машина',
#    'Класс'
    'manufacturer': 'Производитель',
#    'Фото'
}

fields_title = {
    'catalog_number': 'Каталожный номер',
    'name': 'Наименование',
    'price': 'Цена, грн',
    'manufacturer': 'Производитель',
}

visible_fields = ['name', 'catalog_number', 'manufacturer', 'price']
marker_fields = ['vehicle', 'category']
marker_field_choices = {field: {} for field in marker_fields}

def markers(csv_line):
    marker_list = []
    for field in marker_fields:
        choice_name = csv_line[fields[field]]
        choice = slugify(choice_name.decode('utf-8'))
        if choice not in marker_field_choices[field]:
            marker_field_choices[field][choice] = choice_name
        marker_list.append('marker_%s' % choice)
    return ' '.join(marker_list)

def main():
    pricelist_html = open('pricelist.html', 'w')
    pricelist_html.write('<meta charset="utf-8" />\n')
    pricelist_html.write('<link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css">\n')
    pricelist_html.write('<link href="static/css/base.css" rel="stylesheet" type="text/css">\n')

    tmp_pricelist_html = open('~pricelist.html', 'w')
    
    tmp_pricelist_html.write('<div class="table table-striped"><table id="price_table"><thead><tr>')
    for field in visible_fields:
        tmp_pricelist_html.write('<th class="title_%s">%s</th>' % (field, fields_title[field]))
    tmp_pricelist_html.write('</tr></thead><tbody>')
    
    csv_file = open('price.csv', 'r')
    csv_data = csv.DictReader(csv_file) 
    for csv_line in csv_data:
        html_line = '<tr class="priceline ' + markers(csv_line) + '">'
        for field in visible_fields:
            html_line += '<td class="value_%s">%s</td>' % (field, csv_line[fields[field]])
        html_line += '</tr>'
        tmp_pricelist_html.write(html_line)
    csv_file.close()
    tmp_pricelist_html.write('</tbody></table></div>')
    tmp_pricelist_html.close()
    
    for field in marker_fields:
        pricelist_html.write('<label style="float: left; padding: 8px;">%s: <select id="filter_%s" class="filter" style="width: 150px;">' % (fields[field], field))
        pricelist_html.write('<option selected="selected" value="all">Все</option>')
        sorted_choices = marker_field_choices[field].items()
        sorted_choices.sort(key=lambda x: x[1])
        for choice, choice_name in sorted_choices:
            pricelist_html.write('<option value="%s">%s</option>' % (choice, choice_name))
        pricelist_html.write('</select></label>')
    pricelist_html.write('<div style="clear: both;"></div>')
    
    tmp_pricelist_html = open('~pricelist.html', 'r')
    while 1:
        buf = tmp_pricelist_html.read(BUF_SIZE)
        if buf == '':
            break
        pricelist_html.write(buf)
    tmp_pricelist_html.close()
    os.unlink(tmp_pricelist_html.name)

    pricelist_html.write('\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js"></script><script type="text/javascript" src="static/js/jquery.fixheadertable.min.js"></script><script src="static/js/filters.js"></script>')

    pricelist_html.close()


if __name__ == '__main__':
    main()
