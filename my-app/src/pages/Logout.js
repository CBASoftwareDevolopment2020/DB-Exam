import React, { useState, useEffect } from "react";
import { Redirect } from "react-router-dom";
import { qfetch } from "./funcs/tools.js";

export default () => {
	qfetch("http://127.0.0.1:5000/logout");
	localStorage.removeItem("user");

	return (
		<>
			<Redirect to="/login" />
		</>
	);
};
