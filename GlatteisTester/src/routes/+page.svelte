<script lang="ts">
	let content: string | null = $state(null);

	function fetch_next() {
		const endpoint = 'http://127.0.0.1:5000/api/next_content';
		fetch(endpoint)
			.then((response) => response.json())
			.then((data) => {
				console.log('Received data:', data);
				content = data.content;
			})
			.catch((error) => {
				console.error('Error fetching data:', error);
			});
	}
</script>

{content}

<button onclick={fetch_next}>Fetch Next Line</button>

<div>WOW</div>
