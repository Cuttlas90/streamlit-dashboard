"""Creating a custom menu for application"""
import streamlit as st
import pandas as pd

def add_menu():
    """adding a custom menu to app"""
    st.sidebar.page_link("main.py", label="بنیادی", icon="📰")
    st.sidebar.page_link("pages/monthly_compare.py", label="دیده بان ماهانه", icon="📋")
    st.sidebar.page_link("pages/workbench.py", label="میزکار", icon="🗃️")
    st.sidebar.page_link("pages/portfolio.py", label="تحلیل پورتفو", icon="📊")
    st.sidebar.page_link("pages/monte_carlo.py", label="مونته کارلو", icon="🧮")
    st.sidebar.page_link("pages/leveraged_funds.py", label="صندوقهای اهرمی", icon="🧮")
    st.sidebar.page_link("pages/technical.py", label="اطلاعات تکنیکال", icon="📈")
    st.sidebar.page_link("pages/social_page.py", label="اطلاعات رفتاری", icon="🌐")
    # st.sidebar.page_link("pages/simple_chart.py", label="نمودار ساده ماهانه", icon="📋")
    st.sidebar.page_link("pages/changelog.py", label="تازه ها", icon="💬")


def add_list_selector():
    """create and init list selector"""
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
    return selected_stock
