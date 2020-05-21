# Usage

## Generate

### Promo Codes

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