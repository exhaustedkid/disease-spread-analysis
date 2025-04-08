import dataclasses
import copy
import itertools

from input_processing import *
from metric_calculation import *

@dataclasses.dataclass
class BruteforceSolver:
    def __init__(self, tree, colors, N):
        self.tree = tree
        self.colors = colors
        self.N = N

        color_to_node = get_colors(colors)
        node_to_color = colors_to_dict(colors)

        self.C = len(color_to_node)
        self.L = len(node_to_color)


    def solve(self) -> int: # TODO: change in to solver output struct
        tree = string_input_to_tree(self.tree, self.colors)
        # DEBUG = True
        tree.show()
        s = 0
        for combination in itertools.product(range(1, self.C + 1), repeat=self.N - self.L):
            # if DEBUG:
            #     self.print_log(list(combination), self.C)

            tree = copy.deepcopy(tree)
            colors = list(combination)

            for i, color in enumerate(colors):
                node_id = i + 1
                tree.get_node(node_id).tag = f"{node_id}:{color}"

            if is_tree_valid(tree):
                cur_s = calculate_s_metric(tree, self.C)
                s = max(s, cur_s)
        
        return s


    # def print_log(combination, C):
    #     if len(combination) > 2:
    #         a, b, *others = combination
    #         cur = 10 * a + b
    #         if cur / (C * C) == 0.1:
    #             print("10%")
    #         if cur / (C * C) == 0.4:
    #             print("40%")
