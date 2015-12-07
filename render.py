#! /usr/local/bin/python3

# tripeasel special codes render

import re
from openpyxl import load_workbook
from subprocess import call

bloggers = []

wb = load_workbook(filename='Special Code.xlsx')
sheet_names = wb.get_sheet_names()
sheet = wb[sheet_names[0]]

p1 = re.compile(r'\.jpg\s*$', re.IGNORECASE)

rowcount = 0
for row in sheet:
    cellcount = 0
    for cell in row:
        if cell.value is None:
            continue

        cellcount += 1

    if cellcount < 1:
        continue

    try:
        if re.search(r'\.jpg\s*$', row[2].value, re.IGNORECASE) is None:
            continue
    except:
        continue

    rowcount += 1
    bloggers.append({
        'name': row[0].value,
        'special_code': row[1].value,
        'image_name': row[2].value,
        'special_code_50': row[3].value,
        'special_code_17': row[4].value,
    })

fi1 = open('fb_markup.html', 'r')
fb_markup = fi1.read()
fi1.close()

fi2 = open('twitter_markup.html', 'r')
twitter_markup = fi2.read()
fi2.close()

formatted_cards = []

common_repl = {
    'image_dir': 'Blogger_Images/',
}

blogger_count = 0;

for blogger in bloggers:
    blogger_count += 1

    for template_dir in ['FB/', 'Twitter/']:
        for template_file in [
            '17pTemplate.jpg', 
            '50pTemplate.jpg', 
        ]:
            def repl(m):
                if m.group('key').strip() == 'template_file':
                    return template_dir + template_file
                elif m.group('key').strip() in common_repl:
                    return common_repl[m.group('key')]
                elif m.group('key').strip() == 'special_code':
                    newkey = m.group('key').strip() + '_' + template_file[:2]
                    return blogger[newkey]
                elif m.group('key').strip() == 'count':
                    return str(blogger_count)
                else:
                    return blogger[m.group('key')]
            _markup = re.sub(r'{{\s*(?P<key>[^}{]+)\s*}}', repl, \
                globals().get(template_dir.strip('/').lower() + '_markup'))
            formatted_cards.append(_markup)

fi3 = open('normalize.css', 'r')
normalize_css = fi3.read()
fi3.close()

formatted_cards = [
    '<style>' + normalize_css + '</style>' + 
'''
<style>
/* print styles */
@media print {
    .card {
        page-break-after: always;
    }
}
</style>
'''
] + formatted_cards[:]


fo = open('output.html', 'w')
fo.write('\n'.join(formatted_cards))
fo.close()

call(['phantomjs', 'savepng.js'])

print('done')





