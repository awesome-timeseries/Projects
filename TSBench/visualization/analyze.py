import StringIO
from flask import Flask, Blueprint, render_template, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from tsbench.scoring import addTogether
from tsbench.helper import getSingleData
try:
  import simplejson as json
except ImportError:
  import json

analyze = Blueprint('analyze', __name__, template_folder='./templates')

@analyze.route('/<algo_name>/<scor_name>/data/<dir_name>/<file_name>/')
def plotFile(algo_name, scor_name, dir_name, file_name):
    return render_template('details.html', 
                            text='/text/'+algo_name+'/'+scor_name+'/'+dir_name+'/'+file_name+'/', 
                            png_true='/png_true/'+dir_name+'/'+file_name+'/',
                            png_detected='/png_detected/'+algo_name+'/'+dir_name+'/'+file_name+'/')

@analyze.route('/text/<algo_name>/<scor_name>/<dir_name>/<file_name>/')
def text(algo_name, scor_name, dir_name, file_name):
    with open('./results/{0}/score_{1}.json'.format(algo_name, scor_name)) as f:
        scores = json.load(f)['./data/{0}/{1}'.format(dir_name, file_name)]
    message = "TP: {0}  TN: {1}  FP: {2}  FN: {3}  <p>Precision: {4}</p><p>Recall: {5}</p><p>FScore: {6}</p>".format(
            scores[0], scores[1], scores[2], scores[3], scores[4], scores[5], scores[6])
    return message

@analyze.route('/png_true/<dir_name>/<file_name>/')
def png_true(dir_name, file_name):
    file_path = './data/' + dir_name + '/' + file_name

    fig = Figure(figsize=(13, 4), dpi=100)

    axis = fig.add_subplot(1, 1, 1)
    ys = getSingleData(file_path)
    xs = range(ys.__len__())
    axis.plot(xs, ys)

    ab = fig.add_subplot(1, 1, 1)
    with open('./data/labels.json') as f:
        xn = json.load(f)['./data/{0}/{1}'.format(dir_name, file_name)] # a list
    yn = []
    for i in xn:
        yn.append(ys[i])
    ab.scatter(xn, yn, marker='o', color='r', s=15)

    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    #fig.savefig(file_path[:-4]+'.png')
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@analyze.route('/png_detected/<algo_name>/<dir_name>/<file_name>/')
def png_detected(algo_name, dir_name, file_name):
    file_path = './data/' + dir_name + '/' + file_name
    fig = Figure(figsize=(13, 4), dpi=100)
    
    axis = fig.add_subplot(1, 1, 1)
    ys = getSingleData(file_path)
    xs = range(ys.__len__())
    axis.plot(xs, ys)

    cut = fig.add_subplot(1, 1, 1)
    ymin = min(ys)
    ymax = max(ys)
    len = 0.1 * (ymax - ymin)
    ymin -= len
    ymax += len
    with open('./results/{0}/proportion.txt'.format(algo_name), 'r') as f:
        pro = float(f.readline())
        train_length = int(ys.__len__()* pro)
    cut.vlines(train_length, ymin, ymax, colors = "r", linewidth=5)

    ab = fig.add_subplot(1, 1, 1)
    with open('./results/{0}/anomaly_points.json'.format(algo_name)) as f:
        xn = json.load(f)['./data/{0}/{1}'.format(dir_name, file_name)] # a list
    yn = []
    for i in xn:
        yn.append(ys[i])
    ab.scatter(xn, yn, marker='o', color='r', s=15)

    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
