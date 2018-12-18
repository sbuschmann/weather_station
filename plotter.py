#!/usr/bin/env python
# encoding: utf-8

import matplotlib
matplotlib.use('Agg')

import glob
import os
import pandas as pd
import numpy as np
import datetime as dt
import time
import matplotlib.pyplot as plt

#from IPython.core.interactiveshell import InteractiveShell
#InteractiveShell.ast_node_interactivity = "all"


def remove_outliers(df, overwrite = False, q_upper = 0.99, q_lower = 0.01):
    for col in df.columns:
        col_derivative = "d%s" %col
        df[col_derivative] = df[col].shift(-1)/df[col].shift(0)-1
        lower = df[col_derivative].quantile(q_lower)
        upper = df[col_derivative].quantile(q_upper)
        f_lower = df[col_derivative]<lower
        f_upper = df[col_derivative]>upper
        f = f_lower | f_upper
        df.loc[:, col]  = df.loc[:, col].copy(deep = True)
        df.loc[f, col] = np.nan
        df.loc[f, col].fillna(method = "pad", inplace = True)
        df.drop(col_derivative, axis = 1, inplace = True)
    return df



#path = r"/Users/stephan/prog/weather_station"
path = r"."

frames = []

print("Generating weather plots....")
while True:
    start = dt.datetime.now()
    time.sleep(60)
    for file in glob.glob(os.path.join(path, "*.csv")):
        frames.append(pd.read_csv(file, header = None, names = ["time", "Temp", "Hum"]))
    df = pd.concat(frames)

    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time")
    df = df.sort_index()

    df = remove_outliers(df)

    last = "1D"
    freq = "10T"

    fig, axs = plt.subplots(2, 1)


    temp = df["Temp"]
    hum = df["Hum"]

    tmp = temp.last(last)
    tmp = tmp.last(last).groupby(pd.Grouper(freq=freq)).mean()

    temp_last_val = temp[-1]
    hum_last_val = hum[-1]

    axs[0].annotate("%s\n%.2f°\n%.2f%%" %(dt.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), temp_last_val, hum_last_val)
                    , xy = (0.5, 0.6)
                    , xycoords = "axes fraction"
                    , style="normal"
                    , bbox=dict(boxstyle="square", fc="w", ec="k")
                   )

    axs[0].plot(tmp.index, tmp.values, "-", lw=2, color="orange")
    axs[0].grid(True)
    axs[0].set_ylabel("Temperature")
    axs[0].get_xaxis().set_ticklabels([])

    tmp = hum.last(last)
    tmp = tmp.last(last).groupby(pd.Grouper(freq=freq)).mean()
    #hum_last_val = tmp[-1]
    #axs[1].annotate("Aktuelle Luftfeuchtigkeit \n%.2f%%" %hum_last_val, xy = (1.1, 0.8), xycoords = "axes fraction")
    axs[1].grid(True)
    axs[1].set_ylim(45, 60)
    axs[1].set_ylabel("Humidity")
    axs[1].set_xlabel("Zeit")
    axs[1].plot(tmp.index, tmp.values, "-", lw=2)

    #fig.tight_layout()
    fig.autofmt_xdate()

    fig.savefig(os.path.join(path, "weather_info.png"), dpi = 200)

    end = dt.datetime.now()
    print("runtime %s" %(end-start))
