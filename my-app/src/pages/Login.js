import React, { useState, useEffect } from "react";
import { Redirect } from "react-router-dom";
import { qfetch } from "./funcs/tools.js";

export default () => {
	const [email, setEmail] = useState("liana2@abby.net");
	const [password, setPassword] = useState("1234");
	const [msg, setMsg] = useState("");
	const [redirect, setRedirect] = useState("");

	const handleSubmit = async event => {
		event.preventDefault();
		const res = await qfetch("http://127.0.0.1:5000/login/" + email + "/" + password);

		if (res["id"]) {
			localStorage.setItem("user", JSON.stringify(res));
			setRedirect(<Redirect to="/" />);
		} else {
			setMsg("Wrong username or password");
		}
	};

	return (
		<>
			{redirect}
			<form onSubmit={handleSubmit}>
				<input
					name="email"
					type="email"
					value={email}
					onChange={e => setEmail(e.target.value)}
				></input>
				<input
					name="password"
					type="password"
					value={password}
					onChange={e => setPassword(e.target.value)}
				></input>
				<input type="submit" value="Submit" />
			</form>
			<p>{msg}</p>
		</>
	);
};
