"""
Scatter Plot With Tooltips
==========================
A scatter-plot with tooltip labels on hover.  Hover over the points to see
the point labels.
Use the toolbar buttons at the bottom-right of the plot to enable zooming
and panning, and to reset the view.
"""
import matplotlib.pyplot as plt
import numpy as np
import mpld3

fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
N = 100

scatter = ax.scatter(np.random.normal(size=N),
                     np.random.normal(size=N),
                     c=np.random.random(size=N),
                     s=1000 * np.random.random(size=N),
                     alpha=0.3,
                     cmap=plt.cm.jet)
ax.grid(color='white', linestyle='solid')

ax.set_title("Scatter Plot (with tooltips!)", size=20)

labels = ['point {0}'.format(i + 1) for i in range(N)]
tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
mpld3.plugins.connect(fig, tooltip)

plt.savefig("E:/IPython2/141007 Sphinx and ShapelyChipDesigns/try4/docs/pyplots/img/scatter_plot.png")
plt.savefig("scatter_plot.png")
mpld3.save_html(fig, "E:/IPython2/141007 Sphinx and ShapelyChipDesigns/try4/docs/pyplots/img/scatter_plot.html")
#mpld3.save_html(fig, "E:/IPython2/141007 Sphinx and ShapelyChipDesigns/try4/docs/_build/html/_images/scatter_plot.html")
mpld3.save_html(fig, "E:/IPython2/141007 Sphinx and ShapelyChipDesigns/try4/docs/pyplots/scatter_plot.html")
mpld3.save_html(fig, "scatter_plot.html")
mpld3.save_html(fig, "_img/scatter_plot.html")