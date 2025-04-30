async function fetchData() {
	try {
		const data = await fetch("https://api.example.come/data").then((res) => res.json());
        console.log(data);
	} catch (error) {
        // Send error response
		console.log("Fetch error:", "Network response was not ok.");
	}
}
