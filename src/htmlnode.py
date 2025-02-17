from functools import reduce

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props = ""
        if self.props:
            props = reduce(lambda accumulator, prop_key: f"{accumulator} {prop_key}=\"{self.props[prop_key]}\"", self.props, "")
        return props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value in (None, ""):
            raise ValueError("Leaf node has no value. All leaf nodes must have a value!")
        open_tag = f"<{self.tag}{self.props_to_html()}>" if self.tag not in (None, "") else ""
        close_tag = f"</{self.tag}>" if self.tag not in (None, "") else ""
        return f"{open_tag}{self.value}{close_tag}"