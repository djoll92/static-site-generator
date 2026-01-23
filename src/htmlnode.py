class HTMLNode():
	def __init__(self, tag=None, value=None, children=None, props=None):
		"""
        Parameters:
            tag (str | None): HTML tag name, like "p", "a", "h1", or None.
            value (str | None): Text inside the tag, or None if using children.
            children (list[HTMLNode] | None): Child HTMLNode objects, or None.
            props (dict[str, str] | None): HTML attributes like {"href": "..."}.
        """
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError("Should be implemented in child classes.")
	
	def props_to_html(self):
		str = ""
		if self.props and isinstance(self.props, dict):
			for key, value in self.props.items():
				str += (f" {key}=\"{value}\"")
		return str
	
	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"