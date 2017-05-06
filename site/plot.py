import numpy as np

import plotly
import plotly.graph_objs as go

from plotly.offline import plot
from plotly.graph_objs import Scatter, Figure, Layout

class Plot:
	"""
	This class is responsible for drawing a graph catered to the user input including age, stage, facility, and CDCC.
	"""

	def __init__(self):
		self.surv_rate = None;
		self.days = None;

	def set_matrix(self, surv_rate_arg, days_arg):
		""" Constructor.

		Set surv_rate_arg as surv_rate, and days_arg as days

		Args:
			self: this class object
			surv_rate_arg: an array of survival rate
			days_arg: an array of days

		"""

		self.surv_rate = surv_rate_arg
		self.days = days_arg

	def change_graph_range(self, age_input):

		""" Changes the age range.

		Given the age range, cut out the range beyond the certain point

		Args:
			self: this class object
			age_input: age input

		Returns:
			limit: the end index of the range

		"""

		input1 = 70
		input2 = 80

		range1 = 9
		range2 = 8
		range3 = 7

		limit = 0
		if (age_input < input1):
			limit = range1*365
		elif (age_input < input2):
			limit = range2*365
		else:
			limit = range3*365

		return limit

	def compute_median(self, surv_rate):
		""" Computes median.

		Given the age range, cut out the range beyond the certain point

		Args:
			self: this class object
			surv_rate: an array of survival rate

		Returns:
			median

		"""

		median = 0
		for i in range(0, surv_rate.size):
			if (surv_rate[i] <= 0.5):
				median = self.days[i]/365
				break
		return median

	def plot_graph(self, age, stage, facility, CDCC):
		""" Draws a scatter graph

		Retrieves the data according to age, stage, facility, and CDCC variables.
		Draws a graph with the corresponding data.
		X-axis is time (in year) and y-axis: difference in survival rate between CRT and RT.

		Args:
			self: this class object
			age: age variable
			stage: stage variable
			facility: facility variable
			CDCC: CDCC variable

		Returns:
			{'breakeven':breakeven, 'median': median1}: return value. break even point and median survival time

		"""
		stage_input = int(stage)-2
		CDCCInt = int(CDCC)-1
		age_input = int(age)

		limit = self.change_graph_range(age_input)

		index = 0
		while (self.days[index] < limit):
			index += 1

		if (age_input > 90):
			age_input = 26
		else:
			age_input = age_input - 65

		chemo = self.surv_rate[0:index,0,age_input,stage_input,0,CDCCInt]
		time = self.days[0:index]/365
		surgery = self.surv_rate[0:index,1,age_input,stage_input,0,CDCCInt]

		median1 = self.compute_median(chemo)
		median2 = self.compute_median(surgery)

		zero_breakeven = 0
		for i in range(0, chemo.size):
			if (chemo[i] - surgery[i] <= 0) and (i != 0):
				zero_breakeven = i
				print i
				break

		diffsum = np.empty(len(time))
		for i in range (0, len(diffsum)):
			diffsum[i] = 0
			for j in range (0, i):
				diffsum[i] += (chemo[j] - surgery[j])

		breakeven = limit/365
		for j in range(0, len(diffsum)):
			if (diffsum[j] <= 0) and (j >= zero_breakeven):
				breakeven = self.days[j]/365
				break

		trace = go.Scatter(
			x = time,
			y = diffsum,
			name = 'Difference',
			marker = dict(
				size = 20,
				color = 'rgba(152, 0. 0. .8)',
				line = dict(
					width = 2,
					color = 'rgb(0,0,0)'
				)
			)
		)

		# color area before the break even point
		color_area1 = dict(
			type = 'rect',
			xref = 'x',
			yref = 'paper',
			x0 = 0,
			y0 = 0,
			x1 = breakeven,
			y1 = 1,
			fillcolor = '#66cdaa',
			opacity = 0.1
		)

		# color area after the break even point
		endpoint = limit/365
		color_area2 = dict(
			type = 'rect',
			xref = 'x',
			yref = 'paper',
			x0 = breakeven,
			y0 = 0,
			x1 = endpoint,
			y1 = 1,
			fillcolor = '#feffa3',
			opacity = 0.2
		)

		# draw the median survival time for CRT group
		line_median1 = dict(
			type = 'line',
			xref = 'x',
			yref = 'paper',
			x0 = median1,
			y0 = 0,
			x1 = median1,
			y1 = 1,
			line = dict(
				width = 2,
				color ='#eb6841'
			)
		)

		# draw the median survival time for RT group
		line_median2 = dict(
			type = 'line',
			xref = 'x',
			yref = 'paper',
			x0 = median2,
			y0 = 0,
			x1 = median2,
			y1 = 1,
			line = dict(
				width = 2,
				color ='#eb6841'
			)
		)

		# draw the break even point line
		line_breakeven = dict(
			type = 'line',
			xref = 'x',
			yref = 'paper',
			x0 = breakeven,
			y0 = 0,
			x1 = breakeven,
			y1 = 1,
			line = dict(
				width = 2,
				color ='#ffbe4f'
			)
		)

		max_y = (chemo-surgery).max(axis = 0)
		text_median1 = dict(
            x= median1,
            y= max_y,
            xref= 'x',
            yref= 'y',
            text='median(CRT)',
            showarrow=True,
            font=dict(
                size=12,
                color='#ffffff'
            ),
            align='center',
			arrowhead=2,
            ax= -40,
            ay= 30,
            arrowsize=1,
            arrowwidth=2,
            bordercolor='#c7c7c7',
            borderwidth=1,
            borderpad=4,
            bgcolor='#042c62',
            opacity=0.8,
		)


		text_median2 = dict(
            x= median2,
            y= max_y,
            xref= 'x',
            yref= 'y',
            text='median(RC)',
            showarrow=True,
            font=dict(
                size=12,
                color='#ffffff'
            ),
            align='center',
			arrowhead=2,
            ax= -40,
            ay= -30,
            arrowsize=1,
            arrowwidth=2,
            bordercolor='#c7c7c7',
            borderwidth=1,
            borderpad=4,
            bgcolor='#042c62',
            opacity=0.8,
		)

		text_breakeven = dict(
            x= breakeven,
            y= max_y,
            xref= 'x',
            yref= 'y',
            text='breakeven point',
            showarrow=True,
            font=dict(
                size=12,
                color='#ffffff'
            ),
            align='center',
			arrowhead=2,
            ax= -70,
            ay=  70,
            arrowsize=1,
            arrowwidth=2,
            bordercolor='#c7c7c7',
            borderwidth=1,
            borderpad=4,
            bgcolor='#042c62',
            opacity=0.8,
		)

		layout3 = go.Layout(
		    yaxis=dict(
				zeroline = True,
		   		# title='Difference',
		        autorange=True,
       			showgrid=False,
        		showline=False,
        		autotick=True,
        		ticks='',
		        showticklabels=False
		    ),
		    xaxis=dict(
			 	title = 'Time',
				autotick = True,
			    tickmode = "linear",
			    ticks = 'outside',
			    tick0 = 0,
			    tickangle = 30,
			    ticksuffix = " year",
			    tickcolor='#000',
			  	    hoverformat = '.2f'
		    ),
			shapes = [color_area1, color_area2, line_median1, line_median2, line_breakeven],
			annotations = [text_median1, text_median2, text_breakeven]
		)

		data = [trace]

		layout = go.Layout(
		    yaxis=dict(
				zeroline = True,
		        title='Difference',
		    ),
		    xaxis=dict(
			 	title = 'Time',
				autotick = True,
			    tickmode = "linear",
			    ticks = 'outside',
			    tick0 = 0,
			    tickangle = 30,
			    ticksuffix = " year",
			    tickcolor='#000',
			  	    hoverformat = '.2f'
		    )
		)

		fig = dict(data=data, layout=layout3)

		plot(fig, filename='app/static/patientGraph.html', auto_open=False)

		return {'breakeven':breakeven, 'median': median1}
