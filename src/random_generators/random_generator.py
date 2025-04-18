import random
import treelib
import copy

from input_processing import get_node_id

def random_tree(size: int):
    '''
    Generates tree with labels in [1, 2, ... , size]
    '''
    tree = treelib.Tree()
    for i in range(1, size + 1):
        label = f"{i}: ..."
        if i == 1:
            tree.create_node(label, 1)
        else:
            parent_id = random.randint(1, i - 1)
            tree.create_node(label, i, parent=parent_id)

    i = 1
    i2 = size - len(tree.leaves()) + 1
    for node in tree.all_nodes():
    	if node.is_leaf():
    		node.tag = f"{i2}:..."
    		i2 += 1
    	else:
    		node.tag = f"{i}:..."
    		i += 1
    # tree.show()
    assert i == size - len(tree.leaves()) + 1, f"i={i}, expected={size - len(tree.leaves())}"
    assert i2 == size + 1
    return tree


def random_tree_with_leaves(size: int, leaves: int) -> treelib.Tree | None:
    '''
    Generates tree with labels in [1, 2, ... , size]
    With leaves labels in [size - leaves + 1, ... , size]
    '''
    if (size <= leaves):
    	raise ValueError("Number of leaves cannot exceed the total number of nodes")


    it = 0
    tree = random_tree(size)
    while len(tree.leaves()) != leaves:
    	# tree.show()
    	tree = random_tree(size)
    	if it > 10000:
    		return None
    		# raise ValueError("Seems unoble to create tree with such count of leaves"
    	it += 1

    return tree


def color_tree_leaves(tree):
    '''
    Fill colors from 1 to c, where c <= leaves count
    Modifies the input tree
    '''
    colors = []
    leaves = len(tree.leaves())
    while leaves > 0:
        cnt = random.randint(1, leaves)
        colors.append(cnt)
        leaves -= cnt

    for leave in tree.leaves():
        while True:
            color = random.randint(0, len(colors) - 1)
            if colors[color] > 0:
                colors[color] -= 1
                leave.tag = f"{leave.identifier}: {color + 1}"
                break


def color_tree_leaves_exact_colors(tree, colors):
    '''
    Fill colors from 1 to colors exactly
    Modifies the input tree
    '''
    assert len(tree.leaves()) >= colors

    leaves = copy.copy(tree.leaves())
    for color in range(colors):
    	leave = random.choice(leaves)
    	leaves.remove(leave)
    	tree.get_node(leave.identifier).tag = f"{get_node_id(leave)}: {color + 1}"

    while leaves:
    	leave = leaves[0]
    	leaves.remove(leave)
    	color = random.randint(0, colors - 1)
    	tree.get_node(leave.identifier).tag = f"{get_node_id(leave)}: {color + 1}"


def random_problem_tree(size: int):
    tree = random_tree(size)
    color_tree_leaves(tree)
    return tree
