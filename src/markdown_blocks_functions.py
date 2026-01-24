def markdown_to_blocks(markdown):
	raw_blocks = markdown.split("\n\n")
	filtered_blocks = []
	for i in range(len(raw_blocks)):
		block = raw_blocks[i].strip()
		if block != "":
			filtered_blocks.append(block)
	return filtered_blocks