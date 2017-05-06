import rpy2.robjects as robjects
import numpy as np

class FileReader:
	"""
	This class is for reading a R file
	"""
	def __init__(self):
		self.filename = 'application/data/model.rdata'
		self.survRate = None
		self.days = None

	def file_loader(self):
		""" Converst R object file to numpy object """
		# load your file
		robjects.r['load'](self.filename) 

		# retrieve the matrix that was loaded from the file
		lookuptableSurv = robjects.r['lookuptable.surv']
		daysR = robjects.r['days']

		# turn the R matrix into a numpy array
		self.survRate  = np.array(lookuptableSurv)
		self.days = np.array(daysR)

	def get_surv_rate(self):
		""" Get survival rate """
		return self.survRate

	def get_days(self):
		""" Get the range of time """
		return self.days
