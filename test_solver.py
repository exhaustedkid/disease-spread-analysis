import pytest
import dataclasses

from solvers.optimizing import OptimizingSolver

@dataclasses.dataclass
class Case:
    tree: str
    colors: str
    N: int
    result: int

    def __str__(self) -> str:
        return str(self.tree) + str(self.colors)

TEST_CASES = [
    Case(tree="1->2",
    	 colors="2:1",
    	 N = 2,
         result=0),
    
    Case(tree="1->2,1->3",
    	 colors="2:1,3:2",
		 N = 3,
         result=1),

    Case(tree="1->2,1->3,2->4,2->5",
    	 colors="3:2,4:1,5:3",
		 N = 5,
         result=4),

    Case(tree="1->2,1->3,2->4,2->5,4->7,4->6,6->8,6->9,5->10,5->11,3->12,3->13",
    	 colors="7:1,8:2,9:3,10:3,11:4,12:4,13:5",
		 N = 13,
         result=44),
]

@pytest.mark.parametrize("t", TEST_CASES, ids=str)
def test_optimizing_solver(t: Case) -> None:
	solver = OptimizingSolver(t.tree, t.colors, t.N)
	assert t.result == solver.solve()
