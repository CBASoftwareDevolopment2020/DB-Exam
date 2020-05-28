def load_data_query(driver):
    query = '''
        LOAD CSV WITH HEADERS FROM 'file:///food.csv' AS r
        MERGE (item: Item { name:r.name, price: toInteger(r.price), stock: toInteger(r.stock), img: r.link })
        MERGE (brand: Brand { brand: r.brand })
        FOREACH(label IN split(r.labels, ";")|MERGE (l:Label { name: label }))

        WITH r
        MATCH (item: Item { name: r.name })
        UNWIND split(r.labels, ";") as l
        MATCH (label: Label { name: l })
        MERGE (item)-[:is]-(label)

        WITH r
        MATCH (item: Item { name: r.name })
        MATCH (brand: Brand { brand:r.brand })
        MERGE (item)-[:by]-(brand)
    '''

    with driver.session() as session:
        results = session.run(query)

    return results


def add_item_query(driver, name, price, stock, image, brand, labels):
    get_item_query = '''
        MATCH(item: Item { name: $name })
        RETURN item
    '''

    add_item_query = '''
        CREATE (item: Item { name: $name })
        SET item.price = $price, item.stock = $stock, item.img = $image
        MERGE (brand: Brand { brand: $brand })
        FOREACH(label IN $labels | MERGE (l:Label { name: label }))

        WITH item
        UNWIND $labels as l
        MATCH (label: Label { name: l })
        MERGE (item)-[:is]-(label)

        WITH item
        MATCH (item: Item { name: $name })
        MATCH (brand: Brand { brand: $brand })
        MERGE (item)-[:by]-(brand)

        RETURN DISTINCT item
    '''

    with driver.session() as session:
        tx = session.begin_transaction()
        results = tx.run(get_item_query, name=name)

        if list(results):
            tx.rollback()

        else:
            results = tx.run(add_item_query, name=name, price=price, stock=stock, image=image, brand=brand, labels=labels)
            tx.commit()

    result = results.single()

    if result:
        return result.value()
    else:
        return None


def update_labels_query(driver, id, labels):
    query = '''
        MATCH (item:Item)
        WHERE ID(item) = $id
        FOREACH(label IN $labels | MERGE (l:Label { name: label }))

        WITH item
        UNWIND $labels as l
        MATCH (label: Label { name: l })
        MERGE (item)-[:is]-(label)

        RETURN item
    '''

    with driver.session() as session:
        results = session.run(query, id=id, labels=labels)

    result = results.single()

    if result:
        return result.value()
    else:
        return None


def update_item_query(driver, id, property, value):
    query = '''
        MATCH (item:Item)
        WHERE ID(item) = $id
        CALL apoc.create.setProperty(item, $property, $value)
        YIELD node
        RETURN item
    '''

    with driver.session() as session:
        results = session.run(query, id=id, value=value, property=property)

    result = results.single()

    if result:
        return result.value()
    else:
        return None


def update_item_amount_query(driver, id, stock):
    query = '''
        MATCH (item:Item)
        WHERE ID(item) = $id
        SET item.stock = $stock
        RETURN item
    '''

    with driver.session() as session:
        results = session.run(query, id=id, stock=stock)

    result = results.single()

    if result:
        return result.value()
    else:
        return None


def remove_unused_labels_query(driver):
    query = '''
        MATCH (label:Label)
        WHERE NOT (label)-[:is]-(:Item)
        DELETE label
        RETURN "SUCCESS"
    '''

    with driver.session() as session:
        results = session.run(query)

    return results


def filter_by_label_query(driver, label):
    query = '''
        match (:Label { name: $label })--(item:Item)
        return item
    '''

    with driver.session() as session:
        results = session.run(query, label=label)

    return results


def filter_by_favorits_query(driver, favorits):
    query = '''
        UNWIND $favorits as fav
        MATCH (:Label { name: fav })--(item:Item)
        RETURN item
    '''

    with driver.session() as session:
        results = session.run(query, favorits=favorits)

    return results


def order_by_price_query(driver):
    query = '''
        MATCH (item:Item)
        RETURN item
        ORDER BY item.price
    '''

    with driver.session() as session:
        results = session.run(query)

    return results


def filter_price_query(driver, minimum, maximum):
    query = '''
        MATCH (item:Item)
        WHERE item.price > $minimum and item.price < $maximum
        RETURN item
    '''

    with driver.session() as session:
        results = session.run(query, minimum=minimum, maximum=maximum)

    return results


def get_items_query(driver, item_ids):
    query = '''
        MATCH (item: Item)
        WHERE ID(item) IN $item_ids
        RETURN item
    '''

    with driver.session() as session:
        results = session.run(query, item_ids=item_ids)

    return results


def get_20_items_query(driver):
    query = '''
        MATCH (item: Item)
        RETURN item LIMIT 20
    '''

    with driver.session() as session:
        results = session.run(query)

    return results


def get_full_item_query(driver, id):
    query = '''
        MATCH (item: Item)-[]-(node)
        WHERE ID(item) = $id
        RETURN item, node
    '''

    with driver.session() as session:
        results = session.run(query, id=id)

    result = results.single()

    if result:
        return result.value()
    else:
        return None


def place_order(driver, order):
    query = '''
        UNWIND $items as arg_item
        MERGE (item: Item)
        WITH arg_item, item
        WHERE ID(item) = arg_item.id AND item.stock >= arg_item.amount
        SET item.stock = item.stock - arg_item.amount
        RETURN item
    '''

    order_items = [{'id': int(key), 'amount': int(item)} for key, item in order.items()]

    with driver.session() as session:
        tx = session.begin_transaction()
        results = session.run(query, items=order_items)
        items = [result['item'] for result in results]

        if len(items) != len(order):
            tx.rollback()
            return []

        else:
            tx.commit()
            return items


def get_by_ids(driver, ids):
    query = '''
        UNWIND $ids as id
        MATCH (node)
        WHERE ID(node) = id
        RETURN ID(node), node
    '''

    with driver.session() as session:
        results = session.run(query, ids=ids)

    return results

def get_all_labels(driver):
    query = '''
        MATCH (label:Label) RETURN label
    '''

    with driver.session() as session:
        results = session.run(query)
        
    return results



