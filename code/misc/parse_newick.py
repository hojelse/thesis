def tokenize_newick(s: str) -> list:
	tokens = []
	token = ''
	for c in s:
		if c.isnumeric():
			token += c
		else:
			if len(token) > 0:
				tokens.append(token)
			token = ''
		if c != ' ':
			pass
		if c == '(':
			tokens.append('(')
		if c == ')':
			tokens.append(')')
		if c == ',':
			tokens.append(',')
	return tokens

def rec(tokens: list[str], i: int) -> tuple:
	if tokens[0].isnumeric():
		return tokens[1:], int(tokens[0])
	
	tail0, t0 = rec(tokens[1:], i+1)

	tail1, t1 = rec(tail0[1:], i+1)

	if i == 0:
		tail2, t2 = rec(tail1[1:], i+1)
		return (tail2[1:], (t0, t1, t2))

	return (tail1[1:], (t0, t1))

def parse_newick(s: str) -> tuple:
	tokens = tokenize_newick(s)
	return rec(tokens, 0)[1]

nw = parse_newick(input())
print(nw)