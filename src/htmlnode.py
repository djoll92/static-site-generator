import functools


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
		return f"{self.__class__.__name__}(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
	

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		# It still can be an empty string
		if self.value is None:
			raise ValueError("All leaf nodes must have a value.")
		if not self.tag:
			return self.value
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
	
	def __repr__(self):
		return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
	

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if not self.tag:
			raise ValueError("All parent nodes must have a tag.")
		if not self.children:
			raise ValueError("All parent nodes must have children.")
		return f"<{self.tag}{self.props_to_html()}>{functools.reduce(lambda acc, node: acc + node.to_html(), self.children, "")}</{self.tag}>"
