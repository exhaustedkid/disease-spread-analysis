import dataclasses
import datetime
import statistics
import time
import io

from solvers.bruteforce import BruteforceSolver
from solvers.optimizing import OptimizingSolver

from random_generators.random_generator import *
from input_processing import *


@dataclasses.dataclass
class Settings:
	N: int
	C: int
	leaves_step: int
	solver_name: str


@dataclasses.dataclass
class Stats:
	min_time: float
	max_time: float
	avg_time: float


def measurement_results_to_str(settings: Settings, stats: Stats):
	settings_str = f"Solver={settings.solver_name},N={settings.N},C={settings.C}"
	solver_str = f"min={stats.min_time}, max={stats.max_time}, avg={stats.avg_time}"
	return f"{settings_str}: {solver_str}\n"
		   

def start_processing(settings: Settings, log_file: io.TextIOWrapper | None) -> Stats:
	times = []
	for leaves in range(settings.C, settings.N, settings.leaves_step):
		if log_file is not None:
			log_file.write(f"{datetime.datetime.now().time()}: Create tree for N={settings.N}, C={settings.C}, L={leaves}\n")
		
		tree = random_tree_with_leaves(size=settings.N, leaves=leaves)
		if tree is None:
			if log_file is not None:
				log_file.write(f"{datetime.datetime.now().time()}: Not found output for leaves={leaves}\n")
			continue
		color_tree_leaves_exact_colors(tree, settings.C)
		t, c = tree_to_str(tree)
		
		if log_file is not None:
			log_file.write(f"{datetime.datetime.now().time()}: Start solving for N={settings.N}, C={settings.C}, L={leaves}\n")
		
		if settings.solver_name == "Optimizing":
			solver = OptimizingSolver(t, c, settings.N)
		
		start_time = time.time()
		res = solver.solve()
		end_time = time.time()
		times.append(end_time - start_time)

	return Stats(
		min_time = min(times),
		max_time = max(times),
		avg_time = statistics.mean(times))


random.seed(42)

nodes = [5, 10, 15]
colors = [1, 3, 5, 10]

for N in nodes:
	for C in colors:
		if C >= N:
			continue

		settings = Settings(N=N, C=C, leaves_step=1, solver_name="Optimizing")

		log_file = open("log.txt", "a+")
		stats = start_processing(settings, log_file)
		log_file.close()

		file = open("statistics.txt", "a+")
		file.write(measurement_results_to_str(settings, stats))
		file.close()


