from flask import Flask, render_template, Markup, make_response
import numpy as np
from numpy.linalg import inv
import matplotlib
import matplotlib.pyplot as plt
import io, base64, os

app = Flask(__name__)

## Funcion de minimos cuadrados
def mc(x,y):
	#Parametros Iniciales
	n = len(x); sg = 1; ajuste = 1; xn = x; yn = y;
	#Determina el grado del polinomio
	m = 3
	# Obtencion Matriz sx
	sx = np.empty((m+2,m+2))
	for i in range(1,m+2):
		for j in range(1,m+2):
			sx[i][j] = sum(pow(xn,(i+j-2)))
	sx = np.delete(sx,(0), axis=0); sx = np.delete(sx,(0), axis=1)
	# Obtencion Vector sy
	sy = np.empty((m+2,1))
	for i in range(1,m+2):
		ml = pow(xn,i-1)
		sy[i] = sum(yn*ml)
	sy = np.delete(sy,(0), axis=0);
	isx = inv(sx)
	### Ecuacion ###
	c = isx.dot(sy)
	num = np.ones((m+1,1))
	for w in range(0,m+1):
		num[w] = (c[w])
	#Valores para graficar
	xx = np.linspace(min(x), max(x),100)
	cn = np.flipud(c)
	ya = np.polyval(cn,x)
	yy = np.polyval(cn,xx)

	return xx,yy,num.T
##
x = np.array([1,98,126,294,345,456,785,976,985])
y = np.array([568,158,546,345,814,98,346,542,257])
xx,yy,num = mc(x,y)
## Grafica
def ima_cod(x,y,xx,yy):
    #Grafica
    plt.plot(x,y,linestyle='none', marker='.')
    plt.plot(xx,yy)
    plt.grid()
    #Codificacion
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return(plot_url)
##
graph = ''
plot_url = ima_cod(x,y,xx,yy)
graph = Markup('<img src="data:image/png;base64,{}" width: 360; height: 200>'.format(plot_url))
##
@app.route("/")
@app.route("/index.html")

def index():
    return render_template("index.html",
    graph = graph)