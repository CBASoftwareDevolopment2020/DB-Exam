from datetime import datetime, timedelta
from random import choice, randint
import string
import json
import sys


amounts = int(sys.argv[1])
promo_codes = []
ids = set()

print(f'generating {amounts} promo codes')

# generate n amounts of unique ids
while len(ids) < amounts:
    letters = string.ascii_lowercase
    random_id = ''.join(choice(letters) for i in range(8))
    ids.add(random_id)


# generating data
for n in range(amounts):
    promo_code = {
        'id': ids.pop(),
        'percentage': randint(1, 15) * 5,
        'active': True,
        'expires': (datetime.now() + timedelta(days=30)).timestamp(),
    }

    promo_codes.append(promo_code)


# saving to .json
with open('mongo-db/data/promo_codes.json', 'w') as fp:
    json.dump(promo_codes, fp)
    print(f'successfully added {len(promo_codes)} promo codes to mongo-db/data/promo_codes.json')
