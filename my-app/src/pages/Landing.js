import React, { useState, useEffect, useContext } from "react";
import { Redirect } from "react-router-dom";
import { qfetch } from "./funcs/tools.js";
import Cart from "./Cart";
import { CartContext } from "../App";
import Labels from "./objects/Labels";

let x = 0;

export default () => {
	const [basket, setBasket] = useContext(CartContext);

	const add_chips_to_cart = async () => {
		const item = {
			item_id: x,
			name: "Chips m. havsalt",
			price: 1695,
			amount: 2
		};
		x += 1;
		await qfetch("http://127.0.0.1:5000/cart/add", "POST", item);

		const res = await qfetch("http://127.0.0.1:5000/cart/get");
		if (res["success"] && res["success"] == false) {
			setBasket([]);
		} else {
			setBasket(res);
		}
	};

	const [labels, setLabels] = useState([]);
	useEffect(async () => {
		const res = await qfetch("http://127.0.0.1:5000/labels");
		setLabels(res);
	}, []);

	return (
		<>
			<div className="content">
				<h2>Labels</h2>
				<Labels labels={labels} />
				<button onClick={add_chips_to_cart}>Chips Knap</button>
			</div>
			<Cart />
		</>
	);
};
