# -*- coding: utf-8 -*- 

import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt

import glob
import pandas as pd
import numpy as np
import datetime as dt
import time
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
plt.style.use('default')

#from IPython.core.interactiveshell import InteractiveShell
#InteractiveShell.ast_node_interactivity = "all"


def remove_outliers(df, overwrite = False, q_upper = 0.99, q_lower = 0.01):   
    sensors = df.sensor.unique()
    for sensor in sensors:
        f_sensor = df["sensor"] == sensor 
        for col in df.columns:
            col_derivative = "d%s" %col
            df.loc[f_sensor, col_derivative] = df.loc[f_sensor, col].shift(-1)/df.loc[f_sensor, col].shift(0)-1
            lower = df.loc[f_sensor, col_derivative].quantile(q_lower)
            upper = df.loc[f_sensor, col_derivative].quantile(q_upper)
            f_lower = df.loc[f_sensor, col_derivative]<lower
            f_upper = df.loc[f_sensor, col_derivative]>upper
            f = f_lower | f_upper
            df.loc[f_sensor, col]  = df.loc[f_sensor, col].copy(deep = True)
            df.loc[f_sensor & f, col] = np.nan
            df.loc[f_sensor & f, col].fillna(method = "pad", inplace = True)
            df.drop(col_derivative, axis = 1, inplace = True)
    #return df

def load_data(path = r"/Volumes/pi/prog/weather_station"):
    frames = []
    files = glob.glob(os.path.join(path, "data", "weather_data_*.csv"))
    print("Loading files... in total %s files available" %len(files))
    for file in files[:]:
        print(file)
        frames.append(pd.read_csv(file))
    data = pd.concat(frames)
    df = data.copy(deep = True)

    df["time"] = pd.to_datetime(df["time"])
    f = df["time"].isnull()
    df = df[~f]
    df = df.set_index("time")
    df = df.sort_index()
    #df = df.loc[df.index.notnull()]

    return df

def plot_weather_data():
    #remove_outliers(df)

    fig, axs = plt.subplots(2,1
                           # , figsize=(10, 10)
                           )
    #fig.suptitle("hhuhu")


    last = "1D"
    freq = "10T"

    lineWidth = 2

    n=0

    sensor_in = 4
    sensor_out = 17

    last_temp_in = df.loc[df.sensor==sensor_in, "temp"][-1]
    last_temp_out = df.loc[df.sensor==sensor_out, "temp"][-1]
    last_hum_in = df.loc[df.sensor==sensor_in, "hum"][-1]
    last_hum_out = df.loc[df.sensor==sensor_out, "hum"][-1]
    last_time = df.index[-1].strftime("%H:%M:%S")


    legend_elements = [Line2D([0], [0], color='r', lw=0, label='Temp In %s' %last_temp_in),
                       Line2D([0], [0], color='w', lw=0, label='Temp Out %s' %last_temp_out)]

    now = dt.datetime.now()
    annotation = ""

    what_to_plot = "temp"
    f = df["sensor"]==sensor_in
    tmp = df.loc[f].last(last)
    tmp = tmp.groupby(pd.Grouper(freq=freq)).mean()
    axs[n].plot(tmp.index, tmp[what_to_plot], "-", lw=lineWidth)

    f = df["sensor"]==sensor_out
    tmp = df.loc[f].last(last)
    tmp = tmp.groupby(pd.Grouper(freq=freq)).mean()
    axs[n].plot(tmp.index, tmp[what_to_plot], "-", lw=lineWidth)

    axs[n].grid(True)
    axs[n].set_ylabel("Temperature [°C]")
    axs[n].get_xaxis().set_ticklabels([])
    axs[n].set_ylim(-5,25)
    #axs[n].text(last_time, 10, "huhu")
    #axs[n].legend(handles=legend_elements, loc='right')
    lgd1 = axs[n].legend(["In \nAktuell %s°" %last_temp_in, "Out\nAktuell %s°" %last_temp_out], 
                  loc = "upper center", bbox_to_anchor=(1.17, 1))

    n=1
    what_to_plot = "hum"
    f = df["sensor"]==sensor_in
    tmp = df.loc[f].last(last)
    tmp = tmp.groupby(pd.Grouper(freq=freq)).mean()
    axs[n].plot(tmp.index, tmp[what_to_plot], "-", lw=lineWidth)

    f = df["sensor"]==sensor_out
    tmp = df.loc[f].last(last)
    tmp = tmp.groupby(pd.Grouper(freq=freq)).mean()
    axs[n].plot(tmp.index, tmp[what_to_plot], "-", lw=lineWidth)

    axs[n].grid(True)
    axs[n].set_ylabel("Humidity [%]")
    axs[n].set_xlabel("Uhrzeit")
    axs[n].xaxis.set_major_formatter(DateFormatter('%H:%M'))
    #axs[n].yaxis.set_major_formatter(DateFormatter('%d%%'))
    #axs[n].xaxis.set_major_locator(HourLocator(np.arange(0,25,1)))

    lgd2 = axs[n].legend(["In \nAktuell %s%%" %last_hum_in, "Out\nAktuell %s%%" %last_hum_out],
                  loc = "upper center", bbox_to_anchor=(1.17, 1))

    fig.autofmt_xdate()
    fig.savefig(os.path.join(path, "weather_info.png"), bbox_extra_artists = (lgd1,lgd2), dpi=200, bbox_inches='tight')

path = r"/Volumes/pi/prog/weather_station"
path = r"."

while True:
    df = load_data(path)
    plot_weather_data()
    time.sleep(60)