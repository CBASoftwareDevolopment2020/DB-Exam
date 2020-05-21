# Usage

## Formats

### Promo Codes
```js
promo_codes {
	id: String,
	percentage: Number,
	active: Boolean
	expires: Number
}
```

### Orders
```js
Order {
    id: String,
    user_id: String,
    date: Number,
    items: [
            {type: _id, amount: Number, price: Number},
            ...
        ],
    discount: Number,
}
```

## Generate

### Promo Codes

`<AMOUNT>` argument represents the amount of generated items.

_bash_
```bash
python mongo-db/generate_promo_codes.py <AMOUNT>
```

### Orders

_**note: not implemented yet!**_

`<AMOUNT>` argument represents the amount of generated items.

_bash_
```bash
python mongo-db/generate_orders.py <AMOUNT>
```

## Load to Database

### Promo Codes
_bash_
```bash
mongoimport --db db_exam --collection promo_codes --file data/promo_codes.json --jsonArray
```

### Orders
_bash_
```bash
mongoimport --db db_exam --collection orders --file data/orders.json --jsonArray
```