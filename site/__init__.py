from site import controller
from site import fileReader

app.static_folder = 'static'

fr = fileReader.FileReader()
fr.file_loader()

controller.set_plot(fr.get_surv_rate(), fr.get_days())
