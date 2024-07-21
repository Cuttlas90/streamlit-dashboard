"""help to plot and add quartely chart for all type of reports"""
import streamlit as st
import pandas as pd
import altair as alt

from request import vasahm_query

from pages.helper.query import Queries


def add_quartely_charts(selected_stock, dollar_toggle):
    """get data and add monthly charts"""
    queries = Queries(selected_stock["name"])
    if selected_stock["cSecValReal"] in [39, 56, 90]:
        st.header('درآمدهای عملیاتی و سود', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_quarterly_investment_sell_and_profit(dollar=dollar_toggle))
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

        error, stock_data = vasahm_query(queries.get_quarterly_investment_profit_ratio())
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
                                            /pivot_df["جمع درآمدهای عملیاتی"].astype(float))

            chart_product = alt.Chart(pivot_df,
                                    height=600).mark_line().encode(
                                alt.X('end_to_period:N', title='تاریخ'),
                                alt.Y('profit_ratio:Q', title="میزان عمکرد").axis(format='%'),
                                # alt.Color('column_name:N', title='دسته ها'),
                        )
            st.altair_chart(chart_product, use_container_width=True)

    elif selected_stock["cSecValReal"] in [57]:
        st.header('درآمدهای عملیاتی و سود', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_quarterly_banking_sell_and_profit(dollar=dollar_toggle))
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

        error, stock_data = vasahm_query(queries.get_quarterly_banking_profit_ratio())
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
                                            /pivot_df["جمع درآمدهای عملیاتی"].astype(float))

            chart_product = alt.Chart(pivot_df,
                                    height=600).mark_line().encode(
                                alt.X('end_to_period:N', title='تاریخ'),
                                alt.Y('profit_ratio:Q', title="میزان عمکرد").axis(format='%'),
                                # alt.Color('column_name:N', title='دسته ها'),
                        )
            st.altair_chart(chart_product, use_container_width=True)

    # elif selected_stock["cSecValReal"] in [58]:
    #     pass

    # elif selected_stock["cSecValReal"] in [66]:
    #     pass
    # elif selected_stock["cSecValReal"] in [67]:
    #     pass
    # for current report support by normal
    # elif selected_stock["cSecValReal"] in [70]:
    #     pass
    # for current report support by normal

    # elif selected_stock["cSecValReal"] in [90]:
    #     pass
    else:

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
            st.altair_chart(chart_product, use_container_width=True)
