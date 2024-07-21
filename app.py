from flask import Flask, render_template
import pickle
from map_box import create_plot, avg_global_temp, hottest_countries, coldest_countries, choro_map

app = Flask(__name__)

# Load the model and scaler
# model = pickle.load(open('weather_model.pkl', 'rb'))
# scaler = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/forecast')
# def forecast():
#     return render_template('forecast.html')

# @app.route('/predictions')
# def predictions():
#     return render_template('predictions.html')

@app.route('/interactive')
def interactive():
    plot = create_plot()
    return render_template('interactive.html', plot=plot)

@app.route('/temperature-analysis')
def temp_analysis():
    return render_template('temp_analysis.html')

@app.route('/gauge-plot')
def gauge_plot():
    plot = avg_global_temp()
    return render_template('plot.html', plot=plot)

@app.route('/bar-plot')
def bar_plot():
    plot = hottest_countries()
    return render_template('plot.html', plot=plot)

@app.route('/bar-plot2')
def bar_plot2():
    plot = coldest_countries()
    return render_template('plot.html', plot=plot)

@app.route('/map')
def map():
    plot = choro_map()
    return render_template('plot.html', plot=plot)
    

if __name__ == '__main__':
    app.run(debug=True)
