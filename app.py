from flask import Flask, render_template
from pandas_datareader import data
from datetime import datetime, timedelta
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.resources import CDN

app = Flask(__name__)


@app.route('/plot/')
def plot():
    start = datetime.now() - timedelta(days=45)
    end = datetime.now()
    df = data.DataReader(name="GOOG", data_source="yahoo", start=start, end=end)

    def inc_dec(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df['Status'] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
    df['middle'] = (df.Open + df.Close) / 2
    df['Height'] = abs(df.Close - df.Open)

    p = figure(title="Candlestick Chart", x_axis_type='datetime',
               width=1000, height=300, sizing_mode='scale_width')
    p.grid.grid_line_alpha = 0.3

    hours_12 = 12 * 60 * 60 * 1000

    p.segment(df.index, df.High, df.index, df.Low, line_color='black')

    p.rect(df.index[df.Status == 'Increase'], df.middle[df.Status == 'Increase'],
           hours_12, df.Height[df.Status == 'Increase'], fill_color='green', line_color='black')

    p.rect(df.index[df.Status == 'Decrease'], df.middle[df.Status == 'Decrease'],
           hours_12, df.Height[df.Status == 'Decrease'], fill_color='red', line_color='black')

    # another graph of line

    q = figure(title="Line Graph", x_axis_type='datetime',
               width=1000, height=300, sizing_mode='scale_width')

    q.line(df.index, df.Open, color='red', legend_label='Opning value')
    q.circle(df.index, df.Open, size=5, fill_color='black', color='black')

    q.line(df.index, df.Close, color='green', legend_label='Closing value')
    q.circle(df.index, df.Close, size=5, fill_color='black', color='black')

    s = gridplot([[p], [q]])
    script1, div1 = components(s)

    cdn_js = CDN.js_files[0]
    # cdn_css = CDN.css_files
    return render_template("plot.html",
                           script1=script1,
                           div1=div1,
                           cdn_js=cdn_js)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about/')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
