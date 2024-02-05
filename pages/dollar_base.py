"""Plot Some main monthly and quarterly charts in dollar"""

import streamlit as st
import pandas as pd
import altair as alt

from request import vasahm_query, get_nonce, get_key


st.set_page_config(layout='wide',
                   page_title="Vasahm Dashboard",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

# st.markdown(
#     """
#     <style>
#     #MainMenu {visibility: hidden;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <style>
#     .stDeployButton {
#             visibility: hidden;
#         }
#     </style>
#     """, unsafe_allow_html=True
# )
with open("style.css", encoding='UTF-8') as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


# st.sidebar.image(image="./assets/logo.png")
st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')


def get_email_callback():
    """Send nonce to entered email."""
    has_error, message = get_nonce(st.session_state.email)
    if has_error:
        st.error(message, icon="🚨")
    else:
        submit_nonce = st.form("submit_nonce")
        submit_nonce.text_input('کد تایید خود را وارد کنید',
                                        placeholder='XXXX',
                                        key="nonce")
        submit_nonce.form_submit_button("ارسال", on_click = get_nonce_callback )

def get_nonce_callback():
    """Confirm nonce for login."""
    has_error, message = get_key(st.session_state.email, st.session_state.nonce)
    if has_error:
        st.error(message, icon="🚨")
        del st.session_state["nonce"]
    else:
        st.session_state["token"] = message


if "token" not in st .session_state:
    get_email = st.form("get_email")
    email = get_email.text_input('ایمیل خود را وارد کنید',
                                 placeholder='example@mail.com',
                                 key="email")
    # Every form must have a submit button.
    submitted = get_email.form_submit_button("دریافت کد", on_click = get_email_callback )
else:

    df = pd.read_csv("data.csv").dropna()
    list_of_name = df['name'].to_list()

    name = st.sidebar.selectbox("لیست سهام", options = list_of_name)

    st.header('گزارش ماهانه فروش - دلاری', divider='rainbow')

    query_string = f"""WITH
    ranked_dates AS (
        select
        \"rowTitle\",
        sum(value) as value,
        \"endToPeriod\"
        from
        \"MonthlyData\"
        INNER JOIN stocks ON \"MonthlyData\".stock_id = stocks.id
        where
        (
        \"MonthlyData\".\"columnTitle\" = 'مبلغ فروش (میلیون ریال)'
        or \"MonthlyData\".\"columnTitle\" = 'درآمد شناسایی شده'
        or \"MonthlyData\".\"columnTitle\" = 'درآمد محقق شده طی دوره یک ماهه - لیزینگ'
        )
        and stocks.name = '{name}'
        group by
        \"MonthlyData\".\"rowTitle\",
        \"MonthlyData\".\"endToPeriod\"
    )
    select
    \"rowTitle\",
    value / dollar.rate * 1000000 As dollar_value,
    \"endToPeriod\"
    from
    ranked_dates
    INNER JOIN dollar ON ranked_dates.\"endToPeriod\"::varchar = dollar.\"Jalali\"
    """

    error, stock_data = vasahm_query(query_string)
    if error:
        st.error(stock_data, icon="🚨")
    else:
        stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
        "dollar_value",
        "endToPeriod"])
        stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
        # specify the type of selection, here single selection is used
        selector = alt.selection_single(encodings=['x', 'color'])

        chart = alt.Chart(stock_data_history).mark_bar().encode(
            color='rowTitle:N',
            y='sum(dollar_value):Q',
            x='endToPeriod:N'
        )
        st.altair_chart(chart, use_container_width=True)


    st.header('گزارش تعداد تولید', divider='rainbow')
    query_string = f"""select
        \"rowTitle\",
        sum(value) as value,
        \"endToPeriod\"
    from
        \"MonthlyData\"
        INNER JOIN stocks ON \"MonthlyData\".stock_id = stocks.id
    where
        (
        \"MonthlyData\".\"columnTitle\" = 'تعداد تولید'
        )
        and stocks.name = '{name}'
    group by
        \"MonthlyData\".\"rowTitle\",
        \"MonthlyData\".\"endToPeriod\"
    """
    error, stock_data = vasahm_query(query_string)
    if error:
        st.error(stock_data, icon="🚨")
    else:
        stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
        "value",
        "endToPeriod"])
        stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
        # specify the type of selection, here single selection is used
        selector = alt.selection_single(encodings=['x', 'color'])

        chart_product = alt.Chart(stock_data_history).mark_bar().encode(
            color='rowTitle:N',
            y='sum(value):Q',
            x='endToPeriod:N'
        )
        st.altair_chart(chart_product, use_container_width=True)

    st.header('گزارش تعداد فروش', divider='rainbow')
    query_string = f"""select
        \"rowTitle\",
        sum(value) as value,
        \"endToPeriod\"
    from
        \"MonthlyData\"
        INNER JOIN stocks ON \"MonthlyData\".stock_id = stocks.id
    where
        (
        \"MonthlyData\".\"columnTitle\" = 'تعداد فروش'
        )
        and stocks.name = '{name}'
    group by
        \"MonthlyData\".\"rowTitle\",
        \"MonthlyData\".\"endToPeriod\"
    """
    error, stock_data = vasahm_query(query_string)
    if error:
        st.error(stock_data, icon="🚨")
    else:
        stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
        "value",
        "endToPeriod"])
        stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
        # specify the type of selection, here single selection is used
        selector = alt.selection_single(encodings=['x', 'color'])

        chart_product = alt.Chart(stock_data_history).mark_bar().encode(
            color='rowTitle:N',
            y='sum(value):Q',
            x='endToPeriod:N'
        )
        st.altair_chart(chart_product, use_container_width=True)


    st.header('درآمدهای عملیاتی و سود - دلاری', divider='rainbow')
    query_string = f"""WITH
    ranked_dates AS (
        select
        \"rowTitle\",
        value,
        \"endToPeriod\"
        from
        \"QuarterlyData\"
        INNER JOIN stocks ON \"QuarterlyData\".stock_id = stocks.id
        where
        (
            \"QuarterlyData\".\"rowTitle\" = 'درآمدهای عملیاتی'
            or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) ناخالص'
            or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) خالص'
        )
        and stocks.name = '{name}'
    )
    select
    \"rowTitle\",
    value::float / dollar.rate * 1000000 As dollar_value,
    \"endToPeriod\"
    from
    ranked_dates
    INNER JOIN dollar ON ranked_dates.\"endToPeriod\"::varchar = dollar.\"Jalali\"
    """
    error, stock_data = vasahm_query(query_string)
    if error:
        st.error(stock_data, icon="🚨")
    else:
        stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
        "dollar_value",
        "endToPeriod"])

        stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
        # specify the type of selection, here single selection is used
        chart2 = alt.Chart(stock_data_history).mark_area(opacity=0.3).encode(
            color='rowTitle:N',
            y=alt.Y('dollar_value:Q').stack(None),
            x='endToPeriod:N'
        )

        st.altair_chart(chart2, use_container_width=True)

    st.header('حاشیه سود خالص - دلاری', divider='rainbow')
    query_string = f"""WITH
    ranked_dates AS (
        select
        \"rowTitle\",
        value,
        \"endToPeriod\"
        from
        \"QuarterlyData\"
        INNER JOIN stocks ON \"QuarterlyData\".stock_id = stocks.id
        where
        (
            \"QuarterlyData\".\"rowTitle\" = 'درآمدهای عملیاتی'
            or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) ناخالص'
            or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) خالص'
        )
        and stocks.name = '{name}'
    )
    select
    \"rowTitle\",
    value::float / dollar.rate * 1000000 As dollar_value,
    \"endToPeriod\"
    from
    ranked_dates
    INNER JOIN dollar ON ranked_dates.\"endToPeriod\"::varchar = dollar.\"Jalali\"
    """
    error, stock_data = vasahm_query(query_string)
    if error:
        st.error(stock_data, icon="🚨")
    else:
        stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
        "dollar_value",
        "endToPeriod"])
        stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
        pivot_df = stock_data_history.pivot_table(index='endToPeriod',
                                                columns='rowTitle',
                                                values='dollar_value',
                                                aggfunc='sum').reset_index()
        pivot_df["profit_ratio"] = (pivot_df["سود(زیان) خالص"].astype(float)
                                    /pivot_df["درآمدهای عملیاتی"].astype(float))

        chart_product = alt.Chart(pivot_df,
                                height=600).mark_line().encode(
                        alt.X('endToPeriod:N', title='تاریخ'),
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
