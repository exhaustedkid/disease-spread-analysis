import treelib
from utils import revert
from collections import defaultdict
from collections import Counter


#######################
# String processing
#######################

def colors_to_dict(colors_str: str) -> dict[int, int]:
    colors = {}
    for leave in colors_str.split(sep=','):
        num, color = leave.split(':')
        num = int(num)
        color = int(color)
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


def string_input_to_tree(tree_str: str, colors_str: str):
    colors = colors_to_dict(colors_str)

    tree = treelib.Tree()

    root = 1
    tree.create_node("1:...", root)
    for edge in tree_str.split(sep=','):
        i, j = edge.split("->")
        parent_id = int(i)
        node_id = int(j)
        color = str(
            colors.get(node_id)) if (
            colors.get(node_id) is not None) else "..."
        label = f"{node_id}:{color}"
        tree.create_node(label, node_id, parent=parent_id)

    return tree


#######################
# Tree processing
#######################


def tree_to_str(tree) -> tuple:
    tree_str = ""
    for node in tree.all_nodes():
        for child in node.fpointer:
            if tree_str:
                tree_str += ","
            tree_str += f"{get_node_id(node)}->{get_node_id(tree.get_node(child))}"

    colors_str = ""
    for leave in tree.leaves():
        if colors_str:
            colors_str += ","
        colors_str += f"{get_node_id(leave)}:{get_color(leave)}"

    return (tree_str, colors_str)


def get_color(node):
    node_id, color = node.tag.split(":")
    if color == "...":
        return None

    return int(color)


def get_node_id(node):
    node_id, color = node.tag.split(":")
    return int(node_id)
