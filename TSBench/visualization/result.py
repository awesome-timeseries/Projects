from flask import Blueprint
from tsbench.scoring import addTogether
result = Blueprint('result', __name__)

@result.route('/<algo_name>/<scor_name>/')
def index(algo_name, scor_name):
    data_dict = addTogether('./results/{0}/score_{1}.json'.format(algo_name, scor_name))
    message = """
    </br>
    <table align="center" border="1" width="600" frame="hsides" rules="groups" >
        <colgroup span="1" width="200"></colgroup>
        <colgroup span="6" width="600"></colgroup>
        <thead>
            <tr>
            <td></td>
            <td>TP</td>
            <td>FP</td>
            <td>FN</td>
            <td>Precision</td>
            <td>Recall</td>
            <td>F-Score</td>
            </tr>
        </thead>
        <tbody>
    """
    message += """<tr><td>total</td>"""
    for j in [0, 2, 3, 4, 5, 6]:
        message += """<td>""" + str(data_dict['total'][j]) + """</td>"""
    message += """</tr>"""

    for k in data_dict:
        if(k != 'total'):
            message += """<tr>"""
            message += """<td>""" + k + """</td>"""
            for j in [0, 2, 3, 4, 5, 6]:
                message += """<td>""" + str(data_dict[k][j]) + """</td>"""
            message += """</tr>"""
    message += """
        </tbody>
    </table>
    """
    return message
