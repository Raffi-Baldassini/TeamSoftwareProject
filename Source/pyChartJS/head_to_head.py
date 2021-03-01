from flask import Flask, render_template
from pychartjs import BaseChart, ChartType, Color, Options                             

application = Flask(__name__)

"""
This a dummy example of what the results of a head-to-head match could look like
"""

class wpmChart(BaseChart):
    type = ChartType.Bar
    
    class data:
        class wpm:
            label = "WPM"
            data = [120, 74]
            backgroundColor = Color.Palette(Color.Purple, 7, 'lightness')

        class acc:
            label = "Acc"
            data = [78, 95]
            backgroundColor = Color.Palette(Color.Cyan, 7, 'lightness')

    class labels:
        grouped = ["user7456", "user874"]

    class options:
        title   = Options.Title(text="Head to Head", fontSize=18)
        scales = {
            "yAxes": [
                {"id": "WPM",
                 "ticks": {
                     "beginAtZero": True,
                     "max": 250
                     }
                },
                {"id": "Acc",
                 "position": "right",
                 "ticks": {"beginAtZero": True,
                     "max": 100
                    }
                }
            ]
        }
        _labels = Options.Legend_Labels(fonColor=Color.Gray, fullwidth=True)
        legend = Options.Legend(position='bottom', labels=_labels)
        
@application.route("/")
def index():
    wpm = wpmChart()
    wpmChartJSON = wpm.get()
    return render_template("index.html", wpmChartJSON = wpmChartJSON)
    
if __name__ == "__main__":
    application.run(debug = False)
