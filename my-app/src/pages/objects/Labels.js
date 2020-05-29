import React, { useState, useEffect, useContext } from "react";

export default props => {
	const labels = props.labels;

	if (labels.length <= 0) {
		return "No labels found";
	}

	return (
		<>
			<div className="label_box">
				{labels.map(label => (
					<>
						<a href={"http://localhost:3000/label/" + label}>{label}</a>
					</>
				))}
			</div>
		</>
	);
};
