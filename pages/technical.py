"""Comapre monthly data in a customized way"""

import streamlit as st
import pandas as pd
import altair as alt
from login import check_local_token
import numpy as np

from pages.helper.gauge_chart import plot_gauge
from pages.helper.query import Queries
from pages.helper.ta_metrics import add_ta_metrics
from request import get_stock_monthly
# from slider import create_range_slider
from menu import add_menu
from finta import TA
from request import vasahm_query
import plotly.graph_objs as go
import streamlit.components.v1 as components



st.set_page_config(layout='wide',
                   page_title="وسهم - داده های تکنیکال",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='collapsed')


with open( "style.css", encoding='UTF-8') as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
add_menu()
if "ver" in st.session_state:
    st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

df = pd.read_csv("data.csv").dropna()
list_of_name = df['name'].to_list()
if "stock" in st.query_params:
    STOCK_INDEX = list_of_name.index(st.query_params.stock)
else:
    STOCK_INDEX = 0

name = st.sidebar.selectbox("لیست سهام", options = list_of_name, index=STOCK_INDEX)
dollar_toggle = st.sidebar.toggle(
    "نمایش به دلار",
    help="با فعال کردن این گزینه تمامی مبالغ بر اساس دلار بازمحاسبه می گردد."
    )



check_local_token()
if "token" in st.session_state:
    queries = Queries(name)

    error, stock_data = vasahm_query(queries.price_query(dollar=dollar_toggle))
    if error:
        st.error(stock_data, icon="🚨")
    else:
        components.iframe(f"https://chart.vasahm.com/?name={name}", height=500)
        stock_data_history = pd.DataFrame(stock_data, columns=["date","open","high","low","close", "volume"])
        stock_data_history['date'] = pd.to_datetime(stock_data_history['date'])
        stock_data_history['open'] = stock_data_history['open'].astype(int)
        stock_data_history['high'] = stock_data_history['high'].astype(int)
        stock_data_history['low'] = stock_data_history['low'].astype(int)
        stock_data_history['close'] = stock_data_history['close'].astype(int)
        stock_data_history['volume'] = stock_data_history['volume'].astype(int)

        data_to_plot = stock_data_history
        data_to_plot.drop(["volume"], axis=1)
        stock_data_history.set_index("date", inplace=True)

        col1, col2 = st.columns(2)
        
        move_gauge = col1.empty()
        osi_gauge = col2.empty()

        current_value_moving = 0
        current_value_indicator = 0


        col1, col2 = st.columns(2)

        col11, col12, col13 = col1.columns(3)

        current_value_moving = add_ta_metrics(stock_data_history, [10],"EMA (10)", "10 period EMA", col11, current_value_moving, "EMA")
        current_value_moving = add_ta_metrics(stock_data_history, [20], "EMA (20)", "20 period EMA", col12, current_value_moving, "EMA")
        current_value_moving = add_ta_metrics(stock_data_history, [30], "EMA (30)", "30 period EMA", col13, current_value_moving, "EMA")
        current_value_moving = add_ta_metrics(stock_data_history, [50], "EMA (50)", "50 period EMA", col11, current_value_moving, "EMA")
        current_value_moving = add_ta_metrics(stock_data_history, [100], "EMA (100)", "100 period EMA", col12, current_value_moving, "EMA")
        current_value_moving = add_ta_metrics(stock_data_history, [200], "EMA (200)", "200 period EMA", col13, current_value_moving, "EMA")
        
        current_value_moving = add_ta_metrics(stock_data_history, [10],"SMA (10)", "10 period SMA", col11, current_value_moving, "SMA")
        current_value_moving = add_ta_metrics(stock_data_history, [20], "SMA (20)", "20 period SMA", col12, current_value_moving, "SMA")
        current_value_moving = add_ta_metrics(stock_data_history, [30], "SMA (30)", "30 period SMA", col13, current_value_moving, "SMA")
        current_value_moving = add_ta_metrics(stock_data_history, [50], "SMA (50)", "50 period SMA", col11, current_value_moving, "SMA")
        current_value_moving = add_ta_metrics(stock_data_history, [100], "SMA (100)", "100 period SMA", col12, current_value_moving, "SMA")
        current_value_moving = add_ta_metrics(stock_data_history, [200], "SMA (200)", "200 period SMA", col13, current_value_moving, "SMA")
        
        current_value_moving = add_ta_metrics(stock_data_history, [20], "VAMA (20)", "20 period VAMA", col11, current_value_moving, "VAMA")
        current_value_moving = add_ta_metrics(stock_data_history, [9], "HMA (9)", "9 period HMA.", col12, current_value_moving, "HMA")

        col21, col22, col23 = col2.columns(3)

        current_value_indicator = add_ta_metrics(stock_data_history, [14], "RSI (14)", "14 period RSI", col21, current_value_indicator, "RSI")
        current_value_indicator = add_ta_metrics(stock_data_history, [14], "STOCH (14)", "14 period STOCH %K", col22, current_value_indicator, "STOCH")
        current_value_indicator = add_ta_metrics(stock_data_history, [14], "CCI (14)", "14 period CCI", col23, current_value_indicator, "CCI")
        current_value_indicator = add_ta_metrics(stock_data_history, [14], "ADX (14)", "14 period ADX.", col21, current_value_indicator, "ADX")
        current_value_indicator = add_ta_metrics(stock_data_history, [14], "AO (14)", "AO", col22, current_value_indicator, "AO")
        current_value_indicator = add_ta_metrics(stock_data_history, [10], "MOM", "MOM", col23, current_value_indicator, "MOM")
        current_value_indicator = add_ta_metrics(stock_data_history, [10,26], "MACD", "SIGNAL", col21, current_value_indicator, "MACD")
        current_value_indicator = add_ta_metrics(stock_data_history, [14,14], "STOCHRSI", "14 period stochastic RSI.", col22, current_value_indicator, "STOCHRSI")
        current_value_indicator = add_ta_metrics(stock_data_history, [14], "WILLIAMS", "14 Williams %R", col23, current_value_indicator, "WILLIAMS")
        current_value_indicator = add_ta_metrics(stock_data_history, [], "EBBP BULL", "Bull.", col21, current_value_indicator, "EBBP")
        current_value_indicator = add_ta_metrics(stock_data_history, [], "EBBP BEAR", "Bear.", col22, current_value_indicator, "EBBP")
        current_value_indicator = add_ta_metrics(stock_data_history, [], "UO", 0, col23, current_value_indicator, "UO")

        
        plot_gauge(current_value_moving, -15, 15, "Moving Averages Gauge", move_gauge)
        plot_gauge(current_value_indicator, -9, 9, "Oscillators Gauge", osi_gauge)