import React from "react";
import { Link } from "react-router-dom";

export default () => {
	return (
		<header className="beauty_header">
			<div className="logo_box">nemlig2.dk</div>

			<nav className="nav1">
				<a href="http://localhost:3000/">HOME</a>
				<a href="http://localhost:3000/login">LOGIN</a>
				<a href="http://localhost:3000/logout">LOGOUT</a>
				<a href="http://localhost:3000/orders">ORDERS</a>
			</nav>
		</header>
	);
};
