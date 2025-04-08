import treelib
import networkx as nx

from input_processing import get_color


def is_tree_valid(tree):
	for node in tree.all_nodes():
		color = get_color(node)
		if color is None:
			return False

		if len(node.fpointer) == 0:
			continue

		found_color = False
		for child_id in node.fpointer:
			child_color = get_color(tree.get_node(child_id))
			if child_color is None:
				return False

			found_color = found_color or child_color == color

		if not found_color:
			return False

	return True


def calculate_s_metric(tree, C) -> int:
	'''
	Considered tree is phylogenic
	'''
	G = nx.Graph()
	for i in range(1, C + 1):
		G.add_node(i)

	for node in tree.all_nodes():
		color = get_color(node)

		for child_id in node.fpointer:
			child_color = get_color(tree.get_node(child_id))

			if color != child_color and not G.has_edge(color, child_color):
				G.add_edge(color, child_color)
	
	s = 0
	for u, v in G.edges():
		s += G.degree(u) * G.degree(v)

	return s
