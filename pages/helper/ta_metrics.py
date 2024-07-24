
import streamlit as st
import pandas as pd
import altair as alt
from login import check_local_token
import numpy as np

from pages.helper.gauge_chart import plot_gauge
from pages.helper.query import Queries
from request import get_stock_monthly
# from slider import create_range_slider
from menu import add_menu
from finta import TA
from request import vasahm_query
import plotly.graph_objs as go
import streamlit.components.v1 as components


def _update_guage(a, b, c, condition):
    if condition in ["EMA","SMA","VAMA", "HMA"]:
        if b >= c:
            a = a +1
        else:
            a=a-1
        return a
    elif condition in ["RSI","STOCH"]:
        if b >= 70.0:
            a = a +1
        elif b <= 30.0:
            a=a-1
        return a
    elif condition in ["ADX"]:
        if b >= 50.0:
            a = a +1
        elif b <= 50.0:
            a=a-1
        return a
    elif condition == "CCI":
        if b >= 100.0:
            a = a -1
        elif b <= -100.0:
            a=a+1
        return a
    elif condition in ["AO","MOM", "MACD"]:
        
        if b >= 0.0:
            a = a +1
        elif b <= 0.0:
            a=a-1
        return a
    elif condition in ["STOCHRSI"]:
        if b >= 0.5:
            a = a +1
        elif b <= 0.5:
            a=a-1
        return a
    elif condition in ["WILLIAMS"]:
        if b >= -20.0:
            a = a +1
        elif b <= -80.0:
            a=a-1
        return a

def add_ta_metrics(stock_data_history, data,metric_label, col, place, num, ind):
    if ind == "EMA":
        smas = TA.EMA(stock_data_history, data[0])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'],ind)
        return num
    elif ind == "SMA":
        smas = TA.SMA(stock_data_history, data[0])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "VAMA":
        smas = TA.VAMA(stock_data_history, data[0])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "HMA":
        smas = TA.HMA(stock_data_history, data[0])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "RSI":
        smas = TA.RSI(stock_data_history, data[0])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "STOCH":
        smas = TA.STOCH(stock_data_history, data[0])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "CCI":
        smas = TA.CCI(stock_data_history, data[0])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "ADX":
        smas = TA.ADX(stock_data_history, data[0])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "AO":
        smas = TA.AO(stock_data_history, data[0])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "MOM":
        smas = TA.MOM(stock_data_history, data[0])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "MACD":
        smas = TA.MACD(stock_data_history, data[0], data[1])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "STOCHRSI":
        smas = TA.STOCHRSI(stock_data_history, data[0], data[1])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "WILLIAMS":
        smas = TA.WILLIAMS(stock_data_history, data[0])
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        num=_update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "UO":
        smas = TA.UO(stock_data_history)
        sma_df = pd.DataFrame(smas)
        st.write(sma_df.iloc[-1][col])
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        _update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
    elif ind == "EBBP":
        smas = TA.EBBP(stock_data_history)
        sma_df = pd.DataFrame(smas)
        place.metric(label=metric_label, value = int(sma_df.iloc[-1][col]), delta = int(sma_df.iloc[-1][col]-sma_df.iloc[-2][col]))
        _update_guage(num, sma_df.iloc[-1][col], stock_data_history.iloc[-1]['close'], ind)
        return num
        