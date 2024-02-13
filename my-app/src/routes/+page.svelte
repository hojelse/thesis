<svg viewBox="0 0 100 100"
	on:click={evt => {
		if (moveMode) return;

		const x2 = (evt.offsetX / evt.currentTarget.clientWidth) * 100;
		const y2 = (evt.offsetY / evt.currentTarget.clientHeight) * 100;

		const dist = 2;
		for (const [k, {x: x1, y: y1}] of Object.entries(embedding)) {
			if (
				(x1-dist <= x2 && x2 <= x1+dist) &&
				(y1-dist <= y2 && y2 <= y1+dist)
			) {
				console.log("too close")
				return;
			}
		}
		addVertex(x2, y2);
	}}

	on:pointermove={evt => {
		if (drag_from != null) {
			const x = (evt.offsetX / evt.currentTarget.clientWidth) * 100;
			const y = (evt.offsetY / evt.currentTarget.clientHeight) * 100;
			if (moveMode) {
				embedding[drag_from] = {x, y};
			} else {
				drag_to = {x, y};
			}
		}
	}}

	on:pointerup={evt => {
		drag_from = null;
		drag_to = null;
	}}
>
	{#if drag_from != null && drag_to != null}
		<line
			x1={embedding[drag_from].x}
			y1={embedding[drag_from].y}
			x2={drag_to.x}
			y2={drag_to.y}
		/>
	{/if}
	<g id="edges_container">
		{#each Object.entries(adj) as [k, v]}
			{#each v as u}
				<line
					on:click={(evt) => {
						evt.stopPropagation();
						removeEdge(Number(k), Number(u));
					}}
					x1={embedding[Number(k)].x}
					y1={embedding[Number(k)].y}
					x2={embedding[u].x}
					y2={embedding[u].y}
				/>
			{/each}
		{/each}
	</g>
	<g id="vertices_container">
		{#each Object.entries(adj) as [k, v]}
			<circle
				on:click={(evt) => {
					if (moveMode) return;
					evt.stopPropagation();
					removeVertex(Number(k));
				}}
				on:pointerdown={(evt) => {
					evt.stopPropagation();
					drag_from = Number(k)
				}}
				on:pointerup={(evt) => {
					if (moveMode) return;
					console.log("hello?")
					if (drag_from) {
						console.log("hello????")
						addEdge(drag_from, Number(k));
					}
				}}
				cx={embedding[Number(k)].x}
				cy={embedding[Number(k)].y}
			/>
		{/each}
	</g>
</svg>
<input type="checkbox" name="move" id="" bind:checked={moveMode}>
<label for="move">Move?</label>
<div>{moveMode ? "move" : "edit"}</div>
<p
	contenteditable
	bind:innerText={error_msg}
	style="color: red"
></p>
<textarea
	on:input={evt => updateGraph(evt.currentTarget.value)}
>{data_string}</textarea>

<script lang="ts">
	$: moveMode = false;

	let N = 3;
	let MaxId = N;

	let adj: Record<number, Set<number>> = {
		0: new Set([1, 2]),
		1: new Set([0, 2]),
		2: new Set([0, 1])
	}

	let embedding: Record<number, {x: number, y: number}> = {
		0: {x: 50, y: 50},
		1: {x: 40, y: 65},
		2: {x: 60, y: 65}
	}

	function addVertex(x: number, y: number) {
		N++;
		const newId = MaxId++;
		console.log("add", newId)
		
		adj[newId] = new Set();
		embedding[newId] = {x, y};

		adj = adj; // force reaction
	}

	function removeVertex(id: number) {
		console.log("remove", id)
		
		N--;
		
		delete adj[id];
		delete embedding[id];
		
		for (const [k, v] of Object.entries(adj)) {
			v.delete(id);
		}

		adj = adj; // force reaction
	}

	function addEdge(u: number, v: number) {
		console.log("add", u, "<-->", v)
		adj[u].add(v);
		adj[v].add(u);
		adj = adj; // force reaction
	}
	
	function removeEdge(u: number, v: number) {
		console.log("remove", u, "<-->", v)
		adj[u].delete(v);
		adj[v].delete(u);
		adj = adj; // force reaction
	}

	$: data_string = String(N) + '\n' +
		Object.entries(embedding)
			.reduce((prev, curr, i) => {
				return prev += `${curr[0]} ${curr[1].x} ${curr[1].y}\n`
			}, "")
		+ Object.entries(adj)
			.reduce((prev, curr, i) => {
				return prev += `${curr[0]} ${Array.from(curr[1]).join(' ')}\n`
			}, "").trim()

	let drag_from: number | null = null;

	let drag_to: {x: number, y: number} | null = null;

	let error_msg = ''

	function updateGraph(data: string) {
		try {
			let lines = data.split('\n')

			const newN = Number(lines[0])

			if (isNaN(newN) || !Number.isInteger(newN)) {
				throw new Error(`Expected an integer, found: ${lines[0]}`);
			}

			lines = lines.splice(1);

			if (lines.length != 2 * newN) {
				throw new Error(`Expected ${2*newN} lines, found: ${lines.length}`);
			}

			const embedding_lines = lines.slice(0, newN);

			const newEmbedding: Record<number, {x: number, y: number}> = {}

			for (let i = 0; i < newN; i++) {
				const tokens = embedding_lines[i].trim().split(' ')
				if (tokens.length != 3)
					throw new Error(`Expected 3 tokens on this line, found ${tokens.length}: ${tokens}`);

				const v = Number(tokens[0]);
				if (isNaN(v) || !Number.isInteger(v))
					throw new Error(`Expected an integer, found: ${tokens[0]}`);
				
				const x = Number(tokens[1]);
				if (isNaN(x))
					throw new Error(`Expected a number, found: ${tokens[1]}`);

				const y = Number(tokens[2]);
				if (isNaN(y))
					throw new Error(`Expected a number, found: ${tokens[2]}`);

				newEmbedding[v] = {x, y};
			}

			const adj_lines = lines.slice(newN);

			const newAdj: Record<number, Set<number>> = {}
			for (let i = 0; i < newN; i++) {
				const tokens = adj_lines[i].trim().split(' ')
				if (tokens.length < 1)
					throw new Error(`Expected 1 token on this line, found ${tokens.length}: ${tokens}`);

				const v = Number(tokens[0]);
				if (isNaN(v) || !Number.isInteger(v))
					throw new Error(`Expected an integer, found: ${tokens[0]}`);
				
				const neighbors = new Set<number>();

				for (let j = 1; j < tokens.length; j++) {
					const u = Number(tokens[j]);
					if (isNaN(u) || !Number.isInteger(u))
						throw new Error(`Expected an integer, found: ${tokens[j]}`);
					if (Object.keys(newEmbedding).find((v) => Number(v) == u) == undefined)
						throw new Error(`Expected an already defined vertex, found: ${tokens[j]}`);
					neighbors.add(u)
				}

				newAdj[v] = neighbors;
			}

			N = newN;
			embedding = newEmbedding;
			adj = newAdj;
			error_msg = ""
		} catch (e) {
			if (
				typeof e === "object" &&
				e &&
				"message" in e &&
				typeof e.message === "string"
			) {
				error_msg = e.message
			}
		}
	}

</script>

<style>
	svg {
		max-height: 80vh;
	}

	textarea {
		width: 100%; min-height: 400px;
	}

	line {
		stroke: black;
	}

	circle {
		r: 1;
	}
</style>