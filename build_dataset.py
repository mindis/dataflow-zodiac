import os
import requests
import time

names = open('allstar_player_names.txt').readlines()

player_birth_dates = []

api_key = os.environ['BB_API_KEY']
base_url = 'https://probasketballapi.com/players?api_key={}'.format(api_key)
url_template = base_url + '&first_name={}&last_name={}'

for name in names:
    first, last = name[:-1].split()

    # Get birthday from probasketballapi.com

    # Replace special characters to comply with the API
    for c in "'.-":
        first = first.replace(c, '')
        last = last.replace(c, '')

    url = url_template.format(first, last)
    r = requests.post(url)
    if r.ok and r.content != b'[]':
        print(first, last)
        player_info = r.json()[0]
        birth_date = time.localtime(player_info['birth_date'])
        day = birth_date.tm_mday
        month = birth_date.tm_mon
        player_birth_dates.append('{} {},{},{}'.format(first,
                                                       last,
                                                       day,
                                                       month))

csv = '\n'.join(player_birth_dates)
open('player_birthdates.csv', 'w').write(csv)



