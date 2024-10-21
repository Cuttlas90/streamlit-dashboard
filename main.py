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

name, selected_stock = add_list_selector()
dollar_toggle = st.sidebar.toggle(
    "نمایش به دلار",
    help="با فعال کردن این گزینه تمامی مبالغ بر اساس دلار بازمحاسبه می گردد."
    )
st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

check_local_token()
if "token" in st.session_state:
    queries = Queries(name)

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
            source = pd.DataFrame({
                "category": ["سهامدار عمده", "سهامدار خرد"],
                "value": [stock_data[0]['all_holder_percent'], 100- stock_data[0]['all_holder_percent']]
            })

            chart = alt.Chart(source, height=90).mark_arc(innerRadius=10, outerRadius=30).encode(
                # theta="value",
                theta=alt.Theta("value", title="درصد"),
                color=alt.Color('category:N', title="سهامدار"),
                # autoSize=alt.AutoSizeParams(contains='content', type='fit')
            )
            col4.altair_chart(chart, use_container_width=True)
            # col4.metric(
            #     "درصد سهامداران عمده",
            #     f"{format(stock_data[0]['all_holder_percent'], '.2f')}"
            #     )
        # pylint: disable=bare-except
        except:
            pass


    add_monthly_charts(selected_stock, dollar_toggle)
    add_quartely_charts(selected_stock, dollar_toggle)
