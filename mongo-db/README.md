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
    user_id: Number,
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

`<AMOUNT>` argument represents the amount of generated items.

_bash_
```bash
python mongo-db/generate_orders.py <AMOUNT>
```

## Load to Database

### Promo Codes
_bash_
```bash
mongoimport --db db_exam --collection promo_codes --file mongo-db/data/promo_codes.json --jsonArray
```

### Orders
_bash_
```bash
mongoimport --db db_exam --collection orders --file mongo-db/data/orders.json --jsonArray
```


## Query

### Get All Promo Codes

_mongo shell_
```bash
use db_exam
db.promo_codes.find()
```

### Get All Orders

_mongo shell_
```bash
use db_exam
db.orders.find()
```


## Utilities

### Drop Collection
`<DATABASE>` argument represents the target database.
`<COLLECTION>` argument represents the target collection.

_mongo shell_
```bash
use <DATABASE>
db.<COLLECTION>.drop()
```

### Drop Database
`<DATABASE>` argument represents the target database.

_mongo shell_
```bash
use <DATABASE>
db.dropDatabase()
```