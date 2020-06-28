from flask import Flask, render_template, request, redirect, send_from_directory
import pandas as pd
from bokeh.plotting import figure, output_file, show, save
from pandas.io.json import json_normalize
import requests
import io
import csv
from flask import make_response
import os


app = Flask(__name__)

app.vars={}

@app.route('/getInput' ,methods=['GET','POST'])
def getInput():
  if request.method == 'GET':
      return render_template('Input.html')
  else:
      # request was a POST
      app.vars['ticker'] = request.form['ticker']

      return redirect('/submit_stockdata')

@app.route('/submit_stockdata')
def submit_stockdata():
    tik = app.vars['ticker']
    req = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+tik+'&outputsize=compact&apikey=YLPW4B9AHAN1DML5&datatype=csv')
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+tik+'&outputsize=compact&apikey=YLPW4B9AHAN1DML5&datatype=csv'
    df = pd.read_csv(url)
    #print(df)
    x = pd.to_datetime(df['timestamp'])
    y = df['close']
    #print(x)

    # create a new plot with a title and axis labels
    p = figure(title="Stock Price", x_axis_label='DateTime', y_axis_label='Price', plot_width=800, plot_height=250, x_axis_type="datetime")

    # add a line renderer with  line thickness
    p.line(x, y, line_width=2)

    output = output_file("output.html")

    #show(p)
    save(p)

    return send_from_directory( '.' ,'output.html')


if __name__ == "__main__":
    app.run()
