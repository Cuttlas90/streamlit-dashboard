"""Plot Some main monthly and quarterly charts"""
from pathlib import Path
import shutil

import streamlit as st
import altair as alt
import pandas as pd

from login import check_local_token
from pages.helper.monthly_chart import add_monthly_charts
from pages.helper.quarterly_chart import add_quartely_charts
from pages.helper.query import Queries
from request import vasahm_query
from menu import add_list_selector, add_menu
from text_constant import MAIN_PAGE


st.set_page_config(layout='wide',
                    page_title="وسهم",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')
st.session_state.ver = '0.1.9'

STREAMLIT_STATIC_PATH = Path(st.__path__[0]) / "static/static"
CSS_PATH = STREAMLIT_STATIC_PATH / "media/"
if not CSS_PATH.is_dir():
    CSS_PATH.mkdir()

css_file = CSS_PATH / "IRANSansWeb.ttf"
if not css_file.exists():
    shutil.copy("assets/font/IRANSansWeb.ttf", css_file)

with open( "style.css", encoding="utf-8") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

def sfmono():
    """alrair chart theme"""
    font = "iransans"
    return {
        "config" : {
            "font": font
        }
    }

alt.themes.register('sfmono', sfmono)
alt.themes.enable('sfmono')

add_menu()
st.components.v1.html(MAIN_PAGE, height=60, scrolling=False)
if "stock_index" not in st.session_state:
        st.session_state.stock_index = 0
df = pd.read_csv("data.csv").dropna()
list_of_name = df['name'].to_list()
if "stock" in st.query_params:
    st.session_state.stock_index = list_of_name.index(st.query_params.stock)
name = st.sidebar.selectbox(
    "لیست سهام",
    options = list_of_name,
    index=st.session_state.stock_index,
    key="stock_slector",
    disabled=True)
st.session_state.stock_index = int((df.loc[df['name'] == name].index[0]).astype(str))
selected_stock = df.iloc[df.loc[df['name'] == name].index[0]]
dollar_toggle = st.sidebar.toggle(
    "نمایش به دلار",
    help="با فعال کردن این گزینه تمامی مبالغ بر اساس دلار بازمحاسبه می گردد."
    )
st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

check_local_token()
if "token" in st.session_state:
    queries = Queries(st.session_state.stock_index)

    error, stock_data = vasahm_query(queries.get_stock_data())
    if error:
        st.error(stock_data, icon="🚨")
    else:
        col1, col2, col3, col4 = st.columns(4)
        try:
            col1.metric(
                "سود سهم",
                f"{stock_data[0]['estimatedEPS']}"
                )
            col2.metric(
                "P/E سهم",
                f"{format(float(stock_data[0]['pe']), '.2f')}"
                )
            col3.metric(
                "P/E صنعت",
                f"{format(float(stock_data[0]['sectorPE']), '.2f')}"
                )
            col4.metric(
                "درصد سهامداران عمده",
                f"{format(stock_data[0]['all_holder_percent'], '.2f')}"
                )
        # pylint: disable=bare-except
        except:
            pass


    add_monthly_charts(selected_stock, dollar_toggle)
    add_quartely_charts(selected_stock, dollar_toggle)
