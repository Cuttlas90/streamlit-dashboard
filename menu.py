"""Creating a custom menu for application"""
import streamlit as st

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
