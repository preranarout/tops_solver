import matplotlib.pyplot as plt

def simplePlot(x, y, fig_title, x_axis_label, y_axis_label, legend_text):
	y_max = max(y)
	y_min = min(y)

	x_max = max(x)
	x_min = min(x)

	fig = plt.figure(fig_title)
	ax = plt.axes(xlim=(x_min - (x_max - x_min)*0.3, x_max + (x_max - x_min)*0.3), ylim=(y_min - (y_max - y_min)*0.3, y_max + (y_max - y_min)*0.3))

	for i in range(0, len(x)):
		ax.plot([x[i]], [y[i]], 'o', ms=5, color='black')

	lines, = ax.plot(x, y, '-', linewidth=1, color='black', label=legend_text)

	fig.set_size_inches(14, 6)

	legend = plt.legend(loc=2)

	plt.ylabel(y_axis_label, fontsize=12)
	plt.xlabel(x_axis_label, fontsize=12)
	plt.xticks(fontsize=10)
	plt.yticks(fontsize=10)
	ax.yaxis.grid(True)

	plt.show()