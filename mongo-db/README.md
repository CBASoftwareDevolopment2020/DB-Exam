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

```bash
python mongo-db/generate_promo_codes.py <AMOUNT>
```

### Orders
```bash
...
```

## Load to Database

### Promo Codes
```bash
mongoimport --db db_exam --collection promo_codes --file data/promo_codes.json --jsonArray
```

### Orders
```bash
mongoimport --db db_exam --collection orders --file data/orders.json --jsonArray
```