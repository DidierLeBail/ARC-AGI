import numpy as np

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

if __name__ == "__main__":
	pass
