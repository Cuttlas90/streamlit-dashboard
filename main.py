"""Plot Some main monthly and quarterly charts"""
from pathlib import Path
import shutil

import streamlit as st
import pandas as pd
import altair as alt

from login import check_local_token
from pages.helper.monthly_chart import add_monthly_charts
from pages.helper.query import Queries
from request import vasahm_query
from menu import add_menu
from text_constant import MAIN_PAGE


st.set_page_config(layout='wide',
                    page_title="وسهم",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')
st.session_state.ver = '0.1.8'

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
df = pd.read_csv("data.csv").dropna()
list_of_name = df['name'].to_list()
if "stock" in st.query_params:
    STOCK_INDEX = list_of_name.index(st.query_params.stock)
else:
    STOCK_INDEX = 0
name = st.sidebar.selectbox("لیست سهام", options = list_of_name, index=STOCK_INDEX)
selected_stock = df.iloc[df.loc[df['name'] == name].index[0]]
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
            col4.metric(
                "درصد سهامداران عمده",
                f"{format(stock_data[0]['all_holder_percent'], '.2f')}"
                )
        # pylint: disable=bare-except
        except:
            pass


    add_monthly_charts(selected_stock, dollar_toggle)


    st.header('درآمدهای عملیاتی و سود', divider='rainbow')

    error, stock_data = vasahm_query(queries.get_quarterly_sell_and_profit(dollar=dollar_toggle))
    if error:
        st.error(stock_data, icon="🚨")
    else:
        stock_data_history = pd.DataFrame(stock_data, columns=["row_title",
        "value",
        "end_to_period"])

        stock_data_history["end_to_period"] = stock_data_history["end_to_period"].astype(str)
        # specify the type of selection, here single selection is used
        chart2 = alt.Chart(stock_data_history).mark_area(opacity=0.3).encode(
            alt.Color('row_title:N', title="سرفصلها"),
            alt.Y('value:Q', title="مبلغ (میلیون)").stack(None),
            alt.X('end_to_period:N',title="تاریخ")
        )

        st.altair_chart(chart2, use_container_width=True)

    st.header('حاشیه سود خالص', divider='rainbow')

    error, stock_data = vasahm_query(queries.get_quarterly_profit_ratio())
    if error:
        st.error(stock_data, icon="🚨")
    else:
        stock_data_history = pd.DataFrame(stock_data, columns=["row_title",
        "value",
        "end_to_period"])
        stock_data_history["end_to_period"] = stock_data_history["end_to_period"].astype(str)
        pivot_df = stock_data_history.pivot_table(index='end_to_period',
                                                columns='row_title',
                                                values='value',
                                                aggfunc='sum').reset_index()
        pivot_df["profit_ratio"] = (pivot_df["سود(زیان) خالص"].astype(float)
                                    /pivot_df["درآمدهای عملیاتی"].astype(float))

        chart_product = alt.Chart(pivot_df,
                                height=600).mark_line().encode(
                        alt.X('end_to_period:N', title='تاریخ'),
                        alt.Y('profit_ratio:Q', title="میزان عمکرد").axis(format='%'),
                        # alt.Color('column_name:N', title='دسته ها'),
                    )
        chart_product.configure_title(
                    fontSize=20,
                    font='Vazirmatn',
                )

        chart_product.configure(
            font='Vazirmatn'
        )
        st.altair_chart(chart_product, use_container_width=True)
