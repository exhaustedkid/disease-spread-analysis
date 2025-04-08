import pytest
import dataclasses
import treelib

from metric_calculation import *


@dataclasses.dataclass
class Case:
    tree: treelib.Tree
    C: int
    result: int

    def __str__(self) -> str:
        return ""


def get_test_cases():
    TEST_CASES = []

    '''
    1:1
	└── 2:2
    '''
    tree = treelib.Tree()
    tree.create_node("1:1", 1)
    tree.create_node("2:1", 2, parent=1)

    TEST_CASES.append(Case(tree=tree, C=1, result=0))

    '''
    1:1
    └── 2:1
        ├── 3:1
        └── 4:2
    '''
    tree = treelib.Tree()
    tree.create_node("1:1", 1)
    tree.create_node("2:1", 2, parent=1)
    tree.create_node("3:1", 3, parent=2)
    tree.create_node("4:2", 4, parent=2)

    TEST_CASES.append(Case(tree=tree, C=2, result=1))

    '''
    1:2
    ├── 2:2
    │   ├── 4:1
    │   └── 5:2
    └── 3:4
        ├── 6:3
        └── 7:4
    '''
    tree = treelib.Tree()
    tree.create_node("1:2", 1)
    tree.create_node("2:2", 2, parent=1)
    tree.create_node("3:4", 3, parent=1)
    tree.create_node("4:1", 4, parent=2)
    tree.create_node("5:2", 5, parent=2)
    tree.create_node("6:3", 6, parent=3)
    tree.create_node("7:4", 7, parent=3)

    TEST_CASES.append(Case(tree=tree, C=4, result=8))

    return TEST_CASES


@pytest.mark.parametrize("t", get_test_cases(), ids=str)
def test_tree_to_string(t: Case) -> None:
    t.tree.show()
    assert t.result == calculate_s_metric(t.tree, t.C)
