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

import matplotlib.pyplot as plt

def draw_grid(ax, nrows, ncols):
	x_m, x_M = ax.get_xlim()
	y_m, y_M = ax.get_ylim()
	xs = np.linspace(x_m, x_M, ncols + 1)
	ys = np.linspace(y_m, y_M, nrows + 1)
	for x in xs:
		ax.plot([x]*2, [y_m, y_M], color='gray')
	for y in ys:
		ax.plot([x_m, x_M], [y]*2, color='gray')
	ax.set_xlim(x_m, x_M)
	ax.set_ylim(y_m, y_M)

def get_train_tasks():
	"""
	return the list of the name of all training tasks
	"""
	return np.loadtxt("data/training.txt", dtype=str).tolist()

class Task:
	"""
	pass
	
	Parameters
	----------
	task_id : int
		identifier of the task

	Attributes
	----------
	id_ : int
		identifier of the task
	nb_examples : int
		nb of examples available for the task
	data: dict
		data of the task
	type_ : int
		Gives some hint about the nature of the task.
	"""
	def __init__(self,
		task_id
	):
		self.id_ = task_id
		self.data = self._load()
		self.nb_examples, self.nb_questions, self.type_ = self._get_prop()

	def _load(self):
		r"""
		Return the data of the training task of id *self.id_*.
		"""
		with open('data/training/' + task_id + '.json') as json_data:
			data = load(json_data)
		return data
	
	def _get_prop(self):
		nb_examples = len(self.data['train'])
		nb_questions = len(self.data['test'])
		task_type = 0

	def display(self):
		"""
		Displays the annotated data of the task.
		"""
		pass

task_id = '9344f635'
task = Task(task_id)

if __name__ == "__main__":
	pass
