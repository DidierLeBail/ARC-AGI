"""
See https://github.com/arcprize/ARC-AGI-2/tree/main for a detailed description of the dataset.

The tasks are stored in JSON format.
Each task JSON file contains a dictionary with two fields:

"train": demonstration input/output pairs. It is a list of "pairs" (typically 3 pairs).
"test": test input/output pairs. It is a list of "pairs" (typically 1-2 pair).
A "pair" is a dictionary with two fields:

"input": the input "grid" for the pair.
"output": the output "grid" for the pair.
A "grid" is a rectangular matrix (list of lists) of integers between 0 and 9 (inclusive).
The smallest possible grid size is 1x1 and the largest is 30x30.

When looking at a task, a test-taker has access to inputs & outputs of the demonstration pairs,
plus the input(s) of the test pair(s).
The goal is to construct the output grid(s) corresponding to the test input grid(s),
using 3 trials for each test input.
"Constructing the output grid" involves picking the height and width of the output grid,
then filling each cell in the grid with a symbol 
(integer between 0 and 9, which are visualized as colors).
Only exact solutions (all cells match the expected answer) can be said to be correct.
"""

import numpy as np
from json import load
from typing import List

import matplotlib.pyplot as plt

def draw_grid(ax, nrows, ncols):
	x_m, x_M = ax.get_xlim()
	y_m, y_M = ax.get_ylim()
	xs = np.linspace(x_m, x_M, ncols + 1)
	ys = np.linspace(y_m, y_M, nrows + 1)
	for x in xs:
		ax.plot([x]*2, [y_m, y_M], color='white')
	for y in ys:
		ax.plot([x_m, x_M], [y]*2, color='white')
	ax.set_xlim(x_m, x_M)
	ax.set_ylim(y_m, y_M)

def draw_int_mat(ax, mat, colors):
	nrows = len(mat)
	ncols = len(mat[0])
	ax.set_xlim(0, ncols)
	ax.set_ylim(0, nrows)

	for i, row in enumerate(mat):
		for j, val in enumerate(row):
			ax.axvspan(xmin=j, xmax=j+1, ymin=1-i/nrows, ymax=1-(i+1)/nrows, color=colors[val])
	draw_grid(ax, nrows, ncols)

def get_train_task_ids() -> List[str]:
	"""
	return the list of the names of all training tasks
	"""
	return np.loadtxt("data/training.txt", dtype=str).tolist()

class Task:
	r"""
	pass
	
	Parameters
	----------
	task_id : str
		identifier of the task

	Attributes
	----------
	id_ : str
		identifier of the task
	nb_examples : int
		nb of examples available for the task
	data : dict
		data of the task
	type_ : {0, 1, 2, 3}
		Gives some hint about the nature of the task:
		- 0: the input and output are of same sizes
		- 1: the output is larger than the input in every dimension
		- 2: the output is smaller than the input in every dimension
		- 3: other
	"""
	
	COLORS = ['black', 'blue', 'red', 'green', 'yellow', 'gray', 'magenta', 'orange', 'cyan', 'brown']
	
	def __init__(self,
		task_id:str
	):
		self.id_ = task_id
		self.data = self._load()
		self.nb_examples, self.nb_questions, self.type_ = self._get_prop()

	def _load(self):
		r"""
		Return the data of the training task of id *self.id_*.
		"""
		with open('data/training/' + self.id_ + '.json') as json_data:
			data = load(json_data)
		return data

	def _get_prop(self):
		nb_examples = len(self.data['train'])
		nb_questions = len(self.data['test'])
		
		# list the sizes for each example
		in_sizes = []
		out_sizes = []
		for example in self.data['train']:
			in_sizes += [*np.shape(example['input'])]
			out_sizes += [*np.shape(example['output'])]

		in_sizes = np.array(in_sizes)
		out_sizes = np.array(out_sizes)
		task_type = 3
		if (in_sizes == out_sizes).all():
			task_type = 0
		elif (in_sizes <= out_sizes).all():
			task_type = 1
		elif (in_sizes >= out_sizes).all():
			task_type = 2
		return nb_examples, nb_questions, task_type

	def display(self):
		"""
		Displays the pairs of examples (input, output).
		The inputs are displayed at the top and the outputs at the bottom.
		"""
		fig, axs = plt.subplots(nrows=2, ncols=self.nb_examples, constrained_layout=True)
		fig.suptitle(self.id_)
		for ax in axs.flatten():
			plt.setp(ax.get_xticklabels(), visible=False)
			plt.setp(ax.get_yticklabels(), visible=False)
			ax.tick_params(axis='both', which='both', length=0)
			ax.set_aspect('equal')
		axs[0, 0].set_ylabel("input")
		axs[1, 0].set_ylabel("output")
		
		for col, pair in enumerate(self.data["train"]):
			for row, key in enumerate(["input", "output"]):
				draw_int_mat(
					axs[row, col],
					pair[key],
					Task.COLORS
				)

		plt.show()

class Histo(dict):
	"""
	pass
	"""
	def __init__(self, *args, **kwargs):
		dict.__init__(self, *args, **kwargs)
	
	def add_sample(self, value:int):
		if value in self:
			self[value] += 1
		else:
			self[value] = 1

strange_tasks = ['8abad3cf', 'd631b094', 'e6de6e8f', 'c803e39c', 'd5c634a2', '42f83767', '652646ff', '4852f2fa', 'b1986d4b']
task_id = 'b1986d4b' #'9344f635'
task = Task(task_id)
print(task.nb_examples)
print(task.nb_questions)
print(task.type_)
task.display()
exit()

if __name__ == "__main__":
	all_tasks = {task_id: Task(task_id) for task_id in get_train_task_ids()}
	attrs = ["nb_examples", "nb_questions", "type_"]
	stats = {attr: Histo() for attr in attrs}
	
	for task in all_tasks.values():
		for attr in attrs:
			stats[attr].add_sample(getattr(task, attr))

	print(stats)
	print()

	strange_task_ids = []
	for task_id, task in all_tasks.items():
		if task.type_ == 3:
			strange_task_ids.append(task_id)
	
	print(strange_task_ids)
	for task_id in strange_task_ids:
		all_tasks[task_id].display()
