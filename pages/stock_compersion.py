"""Plot Some main monthly and quarterly charts"""
from pathlib import Path
import shutil

import pandas as pd
import streamlit as st
import altair as alt

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

    df = pd.read_csv("data.csv").dropna()
    list_of_name = df['name'].to_list()
    names = st.sidebar.multiselect(
        "لیست سهام",
        options = list_of_name,
        max_selections=5)
    stocks_index = []
    for name in names:
        stocks_index.append(int((df.loc[df['name'] == name].index[0]).astype(str)))
    name_string = ",".join(names)
    name_string="'"+name_string+"'"
    name_string.replace(",","','")
    string = f"""select
                stocks.name AS name , all_data.row_title AS row_title, value
            from
                all_data
                INNER JOIN stocks ON all_data.stock_id = stocks.id
                INNER JOIN table_code ON all_data.table_id = table_code.id
            where
                stocks.name IN ({name_string})
                and table_code.sheet_id=9
            order by 
                all_data.id desc
    """


    # selected_stock = df.iloc[df.loc[df['name'] == name].index[0]]
    # queries = Queries(name)

    error, stock_data = vasahm_query(string)
    if error:
        st.error(stock_data, icon="🚨")
    else:
        if len(stock_data) > 0:
            st.header('درآمدهای عملیاتی و سود', divider='rainbow')
            stock_data_history = pd.DataFrame(stock_data, columns=["name",
            "row_title",
            "value"])

            # stock_data_history["end_to_period"] = stock_data_history[
            #     "end_to_period"].astype(str)
            # specify the type of selection, here single selection is used
            selection = alt.selection_multi(fields=['name'], bind='legend', nearest=True)
            chart2 = alt.Chart(stock_data_history).mark_area(opacity=0.3).encode(
                    alt.Color('name:N', title="نام"),
                    alt.Y('value:Q', title="مبلغ (میلیون)").stack(None),
                    alt.X('row_title:N',title="شرح"),
            tooltip=[
                        alt.Tooltip("name:N", title='نام'),
                        alt.Tooltip("value:Q",  title='میزان'),
                        ],
                    opacity=alt.condition(selection, alt.value(1), alt.value(0))
            ).add_selection(
                selection
            )

            points = chart2.mark_point(shape="circle", filled=True, size=80).encode(
                opacity=alt.condition(selection, alt.value(1), alt.value(0))
            )
            com_chart = chart2 + points
            st.altair_chart(com_chart, use_container_width=True)
