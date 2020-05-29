import React, { useState, useEffect, useContext } from "react";
import { qfetch } from "../funcs/tools.js";
import { CartContext } from "../../App";

export default props => {
	const [basket, setBasket] = useContext(CartContext);

	const items = props.items;
	console.log(items);
	if (items.length <= 0) {
		return "No items found";
	}

	const to_cart = async e => {
		e.preventDefault();
		const ch = e.target.children;
		const item = JSON.parse(ch[0].value);
		const amount = parseInt(ch[1].value);
		item.amount = amount;
		item.item_id = item.id;

		if (amount > 0) {
			await qfetch("http://127.0.0.1:5000/cart/add", "POST", item);
		} else {
			await qfetch("http://127.0.0.1:5000/cart/remove", "POST", item.item_id);
		}

		const res = await qfetch("http://127.0.0.1:5000/cart/get");
		if (res["success"] && res["success"] == false) {
			setBasket([]);
		} else {
			setBasket(res);
		}
	};

	return (
		<>
			<div className="label_box">
				{items &&
					items.map(
						item =>
							item.stock > 0 && (
								<div className="item">
									<img src={item.img} />
									<div>{item.name}</div>
									<div>{item.price}</div>
									<form onSubmit={to_cart}>
										<input
											name="item"
											value={JSON.stringify(item)}
											type="hidden"
										/>
										<input name="amount" type="number"></input>
										<button>Læg i kurv</button>
									</form>
								</div>
							)
					)}
			</div>
		</>
	);
};
