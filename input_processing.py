import treelib
from utils import revert
from collections import defaultdict
from collections import Counter


def colors_to_dict(colors_str: str) -> dict[int, int]:
	colors = {}
	for leave in colors_str.split(sep=','):
	    num, color = leave.split(':')
	    num = int(num) - 1 
	    color = int(color) - 1
	    assert colors.get(num) is None, f"repeated leaf{num}"
	    colors[num] = color

	return colors


def get_colors(colors_str: str) -> dict[int, list[int]]:
	return revert(colors_to_dict(colors_str))


def tree_to_dict(tree_str: str) -> dict[int, list[int]]:
	result = defaultdict(list)

	for edge in tree_str.split(sep=','):
		i, j = edge.split("->")
		node_id = int(i) - 1
		child_id = int(j) - 1
		result[node_id].append(child_id)
	
	return result


def print_tree(tree_str: str, colors_str: str):
	colors = colors_to_dict(colors_str)

	tree = treelib.Tree()

	root = 0
	tree.create_node(root, root)
	for edge in tree_str.split(sep=','):
		i, j = edge.split("->")
		parent_id = int(i) - 1
		node_id = int(j) - 1
		color = str(colors.get(node_id)) if (colors.get(node_id) is not None) else "..."
		label = f"{node_id}: {color}"
		tree.create_node(label, node_id, parent=parent_id)		

	tree.show()

tree_raw = '1->2,1->3,2->4,2->5,4->7,4->6,6->8,6->9,5->10,5->11,3->12,3->13'
colors_raw = '7:1,8:2,9:3,10:3,11:4,12:4,13:5'
print_tree(tree_raw, colors_raw)
print(get_colors(colors_raw))
