from datetime import datetime
import json
import sys


amounts = int(sys.argv[1])
orders = []

print(f'generating {amounts} orders')

# generating data
for n in range(amounts):
    order = {
        'date': datetime.now(),
        # values here..
    }

    orders.append(order)


# saving to .json
with open('mongo-db/data/orders.json', 'w') as fp:
    json.dump(orders, fp)
    print(f'successfully added {len(orders)} promo codes to mongo-db/data/orders.json')
