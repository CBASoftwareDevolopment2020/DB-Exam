import React, { useState, useEffect, useContext } from "react";
import { Redirect } from "react-router-dom";
import { qfetch } from "./funcs/tools.js";
import { CartContext } from "../App";

export default () => {
	const [basket, setBasket] = useContext(CartContext);

	useEffect(async () => {
		const res = await qfetch("http://127.0.0.1:5000/cart/get");
		if (res["success"] && res["success"] == false) {
			setBasket([]);
		} else {
			setBasket(res);
		}
	}, []);

	const clearCart = async () => {
		const res = await qfetch("http://127.0.0.1:5000/cart/clear");
		setBasket([]);
	};

	const createOrder = async () => {
		const res = await qfetch("http://127.0.0.1:5000/orders/create");
		if (res["success"]) {
			qfetch("http://127.0.0.1:5000/cart/clear");
			setBasket([]);
		}
		alert(res["message"]);
	};
	return (
		<>
			<table className="cart">
				<br />
				{basket.length > 0 &&
					basket.map(item => (
						<>
							<tr>
								<td>Name: </td>
								<td>{item.name}</td>
							</tr>
							<tr>
								<td>Amount: </td>
								<td>{item.amount}</td>
							</tr>
							<tr>
								<td>Price: </td>
								<td>{item.price}</td>
							</tr>
							<br />
						</>
					))}
				<button onClick={createOrder}>Confirm order</button>
				<button onClick={clearCart}>Clear Cart</button>
			</table>
		</>
	);
};
