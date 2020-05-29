import React, { useState, useEffect, useContext } from "react";
import { Redirect } from "react-router-dom";
import { qfetch } from "./funcs/tools.js";

export default () => {
	const [orders, setOrders] = useState([]);

	useEffect(async () => {
		const res = await qfetch("http://127.0.0.1:5000/orders/by-user");
		if (res["success"] && res["success"] == false) {
			setOrders([]);
		} else {
			console.log(res);
			setOrders(res);
		}
	}, []);

	const Item = props => {
		const i = props.item;
		return (
			<tr>
				<td>{i.item_id}</td>
				<td>{i.name}</td>
				<td>{i.price}</td>
				<td>{i.amount}</td>
			</tr>
		);
	};

	const Order = props => {
		const o = props.order;
		return (
			<div className="order">
				<p>Date: {o.date}</p>
				<p>Price: {o.price}</p>
				<table>
					<tr>
						<th>Item id</th>
						<th>Name</th>
						<th>Price</th>
						<th>Amount</th>
					</tr>
					{o.items.map(i => (
						<Item item={i} />
					))}
				</table>
			</div>
		);
	};

	const DisplayOrders = props => {
		console.log(orders);
		if (orders.length <= 0) {
			return <>No orders</>;
		} else {
			return (
				<>
					{orders.length > 0 &&
						orders
							.sort((a, b) => b.date - a.date)
							.map(o => <Order order={o} />)}
				</>
			);
		}
	};

	return (
		<>
			<div className="content">
				<div className="orders">
					<DisplayOrders />
				</div>
			</div>
		</>
	);
};
