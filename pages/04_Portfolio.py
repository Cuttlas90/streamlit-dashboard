import streamlit as st
import pandas as pd
import plotly.express as px
import plost
from request import vasahm_query
from slider import create_slider
from request import get_nonce
from request import get_key
import altair as alt

st.session_state.ver = '0.1.2'

st.set_page_config(layout='wide',
                   page_title="Vasahm Dashboard",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

df = pd.read_csv("data.csv").dropna()
list_of_name = df['name'].to_list()
# st.sidebar.image(image="./assets/logo.png")
def del_porto_submition_variable():
    del st.session_state.porto_submition 
st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')
 
def add_submit_state():
    st.session_state["porto_submition"] = True

def create_form():
    if "portfolio_analyzer" in locals():
        del portfolio_analyzer
    portfolio_analyzer = st.form("portfolio_analyzer")

    cols2 = portfolio_analyzer.columns(2, gap="small")
    cols2[0].text_input('تاریخ شروع', placeholder='14010130', key=f"portfolio_month_start")
    cols2[1].text_input('تاریخ شروع', placeholder='14010130', key=f"portfolio_month_finish")
    cols = portfolio_analyzer.columns(3, gap="small")
    for i in range(st.session_state.portfo_number):
      cols[0].selectbox("لیست سهام", options = list_of_name, key=f"stock_name_{i}")
      cols[1].text_input('قیمت خرید', placeholder='12345', key=f"stock_number_{i}")
      cols[2].text_input('سهم از کل پورتفو (درصد)', placeholder='20', key=f"stock_percent_{i}")
    # Every form must have a submit button.
    options = portfolio_analyzer.multiselect(
    'شاخصهای مورد نظر خود برای مقایسه را انتخاب کنید',
    ['شاخص کل', 'شاخص همزون', 'طلا', 'زعفران (نهال)'],
    ['شاخص کل'], key="indexes")
    portfolio_analyzer.form_submit_button("بررسی عملکرد سبد", on_click=add_submit_state)

def get_email_callback():
    hasError, message = get_nonce(st.session_state.email)
    if hasError:
        st.error(message, icon="🚨")
    else:
        submit_nonce = st.form("submit_nonce")
        nonce = submit_nonce.text_input('کد تایید خود را وارد کنید', placeholder='XXXX', key="nonce")
        submitted = submit_nonce.form_submit_button("ارسال", on_click = get_nonce_callback )

def get_nonce_callback():
    hasError, message = get_key(st.session_state.email, st.session_state.nonce)
    if hasError:
        st.error(message, icon="🚨")
        del st.session_state["nonce"]
    else:
        st.session_state["token"] = message


if "token" not in st .session_state:
    get_email = st.form("get_email")
    email = get_email.text_input('ایمیل خود را وارد کنید', placeholder='example@mail.com', key="email")
    # Every form must have a submit button.
    submitted = get_email.form_submit_button("دریافت کد", on_click = get_email_callback )
else:

    if "porto_submition" not in st.session_state:
        st.number_input('تعداد سهام موجود در سبد خود را وارد کنید',
                        min_value=1,
                        max_value=10,
                        on_change=create_form,
                        value=1,
                        key="portfo_number")
    else:
        st.button("ثبت مجدد سبد سرمایه گذاری",
                  key="resubmmition_portfo",
                  help=None,
                  on_click=del_porto_submition_variable,
                  args=None,
                  kwargs=None,
                  type="secondary",
                  disabled=False,
                  use_container_width=True)
        st.write("you are here")


