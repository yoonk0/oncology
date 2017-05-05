from flask import Flask, flash, redirect, render_template, request, session, abort
from app import app
from app import plot

"""
	This is the controller for the program
"""

def set_plot(surv_rate_arg, days_arg):
	"""
	Sets up the data for drawing a desired graph
	"""
	global plot
	plot = plot.Plot()
	plot.set_matrix(surv_rate_arg, days_arg)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/form")
def input():
	return render_template('form.html')

@app.route("/result", methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		result = request.form
		calc = plot.plot_graph(result.get('age'), result.get('ctStage'), 0, result.get('comoScore'))
		return render_template('result.html', result = result, calc = calc)
	return render_template('index.html')

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
