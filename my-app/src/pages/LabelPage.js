import React, { useState, useEffect, useContext } from "react";
import { qfetch } from "./funcs/tools.js";
import Items from "./objects/Items";
import Cart from "./Cart";

export default props => {
	const curPath = props.location.pathname.substring(props.match.path.length + 1);
	console.log(curPath);
	const [items, setItems] = useState([]);

	useEffect(async () => {
		const res = await qfetch("http://127.0.0.1:5000/items/filter-by-label", "POST", {
			label: curPath
		});

		if (!res["error"]) {
			setItems(res);
		}
	}, []);

	return (
		<>
			<div className="content">
				<Items items={items} />
			</div>
			<Cart />
		</>
	);
};
