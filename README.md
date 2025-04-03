------------
v1.0
------------
Create a basic funcional chart (class) basing on PyCharm module. Chart takes a data from user and plot it in time domain. It dynamically changes Y-axe to fit to the data range. most important instructions:
- Chart.__init__() - to initialize the object you have to add parameters:
	- pos: (int, int) - position of left-top corner of the plot
	- axis: (int, int) - lengths of axis X and Y.
	- title: str - plot's title,
	- screen - surface to draw a plot.
- Chart.feed(data) - adds a new time-value point to the plot. Time is calculated automatically by the function.
- Chart.draw() - draws the plot on self.screen.