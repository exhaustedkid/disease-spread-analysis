import pytest
import dataclasses
import treelib

from input_processing import *

# @dataclasses.dataclass
# class TreeCase:
#     tree: treelib.Tree
#     result: str

#     def __str__(self) -> str:
#         return "aaa"
#         return str(self.tree) + str(self.colors)


# def get_test_cases():
#     TEST_CASES = []

#     tree = treelib.Tree()
#     tree.create_node(1, 1)
#     tree.create_node(2, 2, parent=1)
#     TEST_CASES.append(TreeCase(tree=tree, result="1->2"))

#     return TEST_CASES


# @pytest.mark.parametrize("t", get_test_cases(), ids=str)
# def test_tree_to_string(t: TreeCase) -> None:
#     assert t.result == tree_to_str(t.tree)


def test_get_color() -> None:
    tree = treelib.Tree()
    tree.create_node("1:1", 1)
    tree.create_node("2:...", 2, parent=1)
    tree.create_node("3:...", 3, parent=2)
    tree.create_node("4:2", 4, parent=2)

    assert get_color(tree.get_node(1)) == 1
    assert get_color(tree.get_node(2)) is None
    assert get_color(tree.get_node(3)) is None
    assert get_color(tree.get_node(4)) == 2
