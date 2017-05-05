For this project, the Client wanted us to create a website that will help patients make a decision about whether to choose surgery(RC)
or chemo-radiation therapy (CRT) for their treatment.
Therefore, this project involves 3 major parts:
1. Creating a website using Flask.
2. Creating a visualization for the graph to show on the website using Plotly.
3. Converting the R data into Python object and analyzing the data in Python for drawing the graph.

For this project, we used the Model View Controller framework:
- Everything in our templates folder is the View.
- controller.py file is the Controller.
- fileReader.py and plot.py are the Model.

Once the User puts in all the information and clicks "Submit", Plotly will generate an html file called patientGraph.html
and replace the existing html file with the new one to update the image on the website.

Regarding the requirements for this project, we have included:
- 1 UML Class Diagram
- Design Pattern: MVC
- 3 Data Structures in Python: list, dictionary, numpy array
- Advanced Topics: Flask, jQuery, Python, Plotly, R
