"""help to plot and add quartely chart for all type of reports"""
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from request import vasahm_query

from pages.helper.query import Queries


def add_quartely_charts(selected_stock, dollar_toggle):
    """get data and add monthly charts"""
    queries = Queries(selected_stock["name"])
    if selected_stock["cSecValReal"] in [39, 56, 90]:

        error, stock_data = vasahm_query(queries.get_quarterly_investment_sell_and_profit(dollar=dollar_toggle))
        if error:
            st.error(stock_data, icon="🚨")
        else:
            if len(stock_data) > 0:
                st.header('درآمدهای عملیاتی و سود', divider='rainbow')
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


        error, stock_data = vasahm_query(queries.get_quarterly_investment_profit_ratio())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            if len(stock_data) > 0:
                st.header('حاشیه سود خالص', divider='rainbow')
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
                pivot_df["profit_ratio"] = pivot_df["profit_ratio"].replace([np.inf, -np.inf], 0)
                chart_product = alt.Chart(pivot_df).mark_line().encode(
                                    alt.X('end_to_period:N', title='تاریخ'),
                                    alt.Y('profit_ratio:Q', title="میزان عمکرد").axis(format='%'),
                                    # alt.Color('column_name:N', title='دسته ها'),
                            )
                st.altair_chart(chart_product, use_container_width=True)

    elif selected_stock["cSecValReal"] in [57]:

        error, stock_data = vasahm_query(queries.get_quarterly_banking_sell_and_profit(dollar=dollar_toggle))
        if error:
            st.error(stock_data, icon="🚨")
        else:
            if len(stock_data) > 0:
                st.header('درآمدهای عملیاتی و سود', divider='rainbow')
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


        error, stock_data = vasahm_query(queries.get_quarterly_banking_profit_ratio())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            if len(stock_data) > 0:
                st.header('حاشیه سود خالص', divider='rainbow')
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
                pivot_df["profit_ratio"] = pivot_df["profit_ratio"].replace([np.inf, -np.inf], 0)
                chart_product = alt.Chart(pivot_df).mark_line().encode(
                                    alt.X('end_to_period:N', title='تاریخ'),
                                    alt.Y('profit_ratio:Q', title="میزان عمکرد").axis(format='%'),
                                    # alt.Color('column_name:N', title='دسته ها'),
                            )
                st.altair_chart(chart_product, use_container_width=True)

    elif selected_stock["cSecValReal"] in [58]:
        error, stock_data = vasahm_query(queries.get_quarterly_leasing_sell_and_profit(dollar=dollar_toggle))
        if error:
            st.error(stock_data, icon="🚨")
        else:
            if len(stock_data) > 0:
                st.header('درآمدهای عملیاتی و سود', divider='rainbow')
                stock_data_history = pd.DataFrame(stock_data, columns=["row_title",
                "value",
                "end_to_period"])

                stock_data_history["end_to_period"] = stock_data_history["end_to_period"].astype(str)

                filtered_df_1 = stock_data_history[~stock_data_history['row_title'].isin(['سود(زیان) خالص', 'سود (زیان) خالص پس از کسر مالیات'])]
                sum_key1_key2 = stock_data_history[stock_data_history['row_title'].isin(['سود(زیان) خالص', 'سود (زیان) خالص پس از کسر مالیات'])].groupby('end_to_period')['value'].sum().reset_index()
                sum_key1_key2['row_title'] = 'سود خالص'
                sum_key1_key2 = sum_key1_key2[['row_title', 'value', 'end_to_period']]
                new_df2 = pd.concat([filtered_df_1, sum_key1_key2], ignore_index=True)

                filtered_df = new_df2[~new_df2['row_title'].isin(['درآمد حاصل از عملیات لیزینگ', 'درآمدهای عملیاتی'])]
                sum_key1_key2 = new_df2[new_df2['row_title'].isin(['درآمد حاصل از عملیات لیزینگ', 'درآمدهای عملیاتی'])].groupby('end_to_period')['value'].sum().reset_index()
                sum_key1_key2['row_title'] = 'درآمد'
                sum_key1_key2 = sum_key1_key2[['row_title', 'value', 'end_to_period']]
                new_df = pd.concat([filtered_df, sum_key1_key2], ignore_index=True)

                # specify the type of selection, here single selection is used
                chart2 = alt.Chart(new_df).mark_area(opacity=0.3).encode(
                        alt.Color('row_title:N', title="سرفصلها"),
                        alt.Y('value:Q', title="مبلغ (میلیون)").stack(None),
                        alt.X('end_to_period:N',title="تاریخ")
                )

                st.altair_chart(chart2, use_container_width=True)


        error, stock_data = vasahm_query(queries.get_quarterly_leasing_profit_ratio())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            if len(stock_data) > 0:
                st.header('حاشیه سود خالص', divider='rainbow')
                stock_data_history = pd.DataFrame(stock_data, columns=["row_title",
                "value",
                "end_to_period"])
                stock_data_history["end_to_period"] = stock_data_history["end_to_period"].astype(str)
                
                filtered_df_1 = stock_data_history[~stock_data_history['row_title'].isin(['سود(زیان) خالص', 'سود (زیان) خالص پس از کسر مالیات'])]
                sum_key1_key2 = stock_data_history[stock_data_history['row_title'].isin(['سود(زیان) خالص', 'سود (زیان) خالص پس از کسر مالیات'])].groupby('end_to_period')['value'].sum().reset_index()
                sum_key1_key2['row_title'] = 'سود خالص'
                sum_key1_key2 = sum_key1_key2[['row_title', 'value', 'end_to_period']]
                new_df2 = pd.concat([filtered_df_1, sum_key1_key2], ignore_index=True)

                filtered_df = new_df2[~new_df2['row_title'].isin(['درآمد حاصل از عملیات لیزینگ', 'درآمدهای عملیاتی'])]
                sum_key1_key2 = new_df2[new_df2['row_title'].isin(['درآمد حاصل از عملیات لیزینگ', 'درآمدهای عملیاتی'])].groupby('end_to_period')['value'].sum().reset_index()
                sum_key1_key2['row_title'] = 'درآمد'
                sum_key1_key2 = sum_key1_key2[['row_title', 'value', 'end_to_period']]
                new_df = pd.concat([filtered_df, sum_key1_key2], ignore_index=True)

                
                pivot_df = new_df.pivot_table(index='end_to_period',
                                                            columns='row_title',
                                                            values='value',
                                                            aggfunc='sum').reset_index()
                pivot_df["profit_ratio"] = (pivot_df['سود خالص'].astype(float)
                                                /pivot_df['درآمد'].astype(float))
                pivot_df["profit_ratio"] = pivot_df["profit_ratio"].replace([np.inf, -np.inf], 0)
                chart_product = alt.Chart(pivot_df).mark_line().encode(
                                    alt.X('end_to_period:N', title='تاریخ'),
                                    alt.Y('profit_ratio:Q', title="میزان عمکرد").axis(format='%'),
                                    # alt.Color('column_name:N', title='دسته ها'),
                            )
                st.altair_chart(chart_product, use_container_width=True)

    elif selected_stock["cSecValReal"] in [66]:
        error, stock_data = vasahm_query(queries.get_quarterly_insurance_sell_and_profit(dollar=dollar_toggle))
        if error:
            st.error(stock_data, icon="🚨")
        else:
            if len(stock_data) > 0:
                st.header('درآمدهای عملیاتی و سود', divider='rainbow')
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


        error, stock_data = vasahm_query(queries.get_quarterly_insurance_profit_ratio())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            if len(stock_data) > 0:
                st.header('حاشیه سود خالص', divider='rainbow')
                stock_data_history = pd.DataFrame(stock_data, columns=["row_title",
                "value",
                "end_to_period"])
                stock_data_history["end_to_period"] = stock_data_history["end_to_period"].astype(str)
                pivot_df = stock_data_history.pivot_table(index='end_to_period',
                                                            columns='row_title',
                                                            values='value',
                                                            aggfunc='sum').reset_index()
                pivot_df["profit_ratio"] = (pivot_df["سود(زیان) خالص"].astype(float)
                                                /pivot_df["درآمدهای بیمه ای"].astype(float))
                pivot_df["profit_ratio"] = pivot_df["profit_ratio"].replace([np.inf, -np.inf], 0)
                chart_product = alt.Chart(pivot_df).mark_line().encode(
                                    alt.X('end_to_period:N', title='تاریخ'),
                                    alt.Y('profit_ratio:Q', title="میزان عمکرد").axis(format='%'),
                                    # alt.Color('column_name:N', title='دسته ها'),
                            )
                st.altair_chart(chart_product, use_container_width=True)

    # elif selected_stock["cSecValReal"] in [67]:
    #     pass
    # for current report support by normal
    # elif selected_stock["cSecValReal"] in [70]:
    #     pass
    # for current report support by normal

    # elif selected_stock["cSecValReal"] in [90]:
    #     pass
    else:

        error, stock_data = vasahm_query(queries.get_quarterly_sell_and_profit(dollar=dollar_toggle))
        if error:
            st.error(stock_data, icon="🚨")
        else:
            if len(stock_data) > 0:
                st.header('درآمدهای عملیاتی و سود', divider='rainbow')
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


        error, stock_data = vasahm_query(queries.get_quarterly_profit_ratio())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            if len(stock_data) > 0:
                st.header('حاشیه سود خالص', divider='rainbow')
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
                pivot_df["profit_ratio"] = pivot_df["profit_ratio"].replace([np.inf, -np.inf], 0)
                chart_product = alt.Chart(pivot_df).mark_line().encode(
                                    alt.X('end_to_period:N', title='تاریخ'),
                                    alt.Y('profit_ratio:Q', title="میزان عمکرد").axis(format='%'),
                                    # alt.Color('column_name:N', title='دسته ها'),
                            )
                st.altair_chart(chart_product, use_container_width=True)
