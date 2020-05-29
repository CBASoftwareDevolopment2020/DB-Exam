import React, { createContext, useState } from "react";
import "./App.css";
import { Route } from "react-router-dom";
import Login from "./pages/Login";
import Landing from "./pages/Landing";
import Logout from "./pages/Logout";
import Orders from "./pages/Orders";
import Header from "./pages/Header";
import LabelPage from "./pages/LabelPage";

export const CartContext = createContext();

function App() {
	const ContextContainer = ({ children }) => {
		const state = useState([]);
		return <CartContext.Provider value={state}>{children}</CartContext.Provider>;
	};
	return (
		<>
			<Header />
			<ContextContainer>
				<Route exact path="/" component={Landing} />
				<Route path="/login" component={Login} />
				<Route path="/logout" component={Logout} />
				<Route path="/orders" component={Orders} />
				<Route path="/label" component={LabelPage} />
			</ContextContainer>
		</>
	);
}

export default App;
