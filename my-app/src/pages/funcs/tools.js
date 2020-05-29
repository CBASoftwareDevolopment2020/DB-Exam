export const qfetch = async (url, method = "GET", content) => {
	//create option object, and add method type
	const options = {
		method, // *GET, POST, PUT, DELETE, etc.
		headers: {
			"Content-Type": "application/json"
		},
		credentials: "include"
	};

	//add content to options if set
	if (content) options.body = JSON.stringify(content);

	let json;
	try {
		const data = await fetch(url, options);
		json = await data.json();
	} catch (error) {
		json = error;
	}

	return json;
};
