"""Query Workbench."""

import streamlit as st
import pandas as pd
import altair as alt

from login import check_local_token
from pages.helper.query import Queries
from request import vasahm_query
from menu import add_menu



st.set_page_config(layout='wide',
                   page_title="وسهم - میزکار، دسترسی آزاد اطلاعات",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

with open( "style.css", encoding="UTF-8") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


add_menu()

df = pd.read_csv("data.csv").dropna()
list_of_name = df['name'].to_list()
if "stock" in st.query_params:
    STOCK_INDEX = list_of_name.index(st.query_params.stock)
else:
    STOCK_INDEX = 0
name = st.sidebar.selectbox("لیست سهام", options = list_of_name, index=STOCK_INDEX)
selected_stock = df.iloc[df.loc[df['name'] == name].index[0]]

if "ver" in st.session_state:
    st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

check_local_token()
if "token" in st.session_state:

    queries = Queries(name)

    error, stock_data = vasahm_query(queries.get_daily_social())
    if error:
        st.error(stock_data, icon="🚨")
    else:
        if len(stock_data) > 0:
            st.header("اقبال به سهم", divider='rainbow')
            stock_data_history = pd.DataFrame(stock_data, columns=[
            "number",
            "date"])
            # stock_data_history["date"] = stock_data_history[
            #     "date"].astype(str)

            chart = alt.Chart(stock_data_history).mark_bar().encode(
                # alt.Color('row_title:N', title="سرفصلها"),
                alt.Y('number:Q', title="تعداد کامنت"),
                alt.X('date:N',title="تاریخ")
            )
            st.altair_chart(chart, use_container_width=True)
