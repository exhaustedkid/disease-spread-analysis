import pytest
import dataclasses
import treelib

from metric_calculation import *


@dataclasses.dataclass
class Case:
    tree: treelib.Tree
    result: bool

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
    tree.create_node("2:2", 2, parent=1)

    TEST_CASES.append(Case(tree, False))


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

    TEST_CASES.append(Case(tree, True))


    '''
	1:1
	└── 2:1
	    ├── 3:1
	    ├── 4:2
	    └── 5:2
	        └── 6:3
    '''
    tree = treelib.Tree()
    tree.create_node("1:1", 1)
    tree.create_node("2:1", 2, parent=1)
    tree.create_node("3:1", 3, parent=2)
    tree.create_node("4:2", 4, parent=2)
    tree.create_node("5:2", 5, parent=2)
    tree.create_node("6:3", 6, parent=5)

    TEST_CASES.append(Case(tree, False))


    '''
	1:1
	└── 2:1
	    ├── 3:...
	    ├── 4:2
	    └── 5:2
	        └── 6:3
    '''
    tree = treelib.Tree()
    tree.create_node("1:1", 1)
    tree.create_node("2:1", 2, parent=1)
    tree.create_node("3:...", 3, parent=2)
    tree.create_node("4:2", 4, parent=2)
    tree.create_node("5:2", 5, parent=2)
    tree.create_node("6:3", 6, parent=5)

    TEST_CASES.append(Case(tree, False))

    return TEST_CASES


@pytest.mark.parametrize("t", get_test_cases(), ids=str)
def test_tree_to_string(t: Case) -> None:
    t.tree.show()
    assert t.result == is_tree_valid(t.tree)

