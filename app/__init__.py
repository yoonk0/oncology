from flask import Flask

app = Flask(__name__)
import controller
import fileReader

app.static_folder = 'static'

fr = fileReader.FileReader()
fr.file_loader()

controller.set_plot(fr.get_surv_rate(), fr.get_days())
