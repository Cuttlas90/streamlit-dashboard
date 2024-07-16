"""help to plot and add monthly hart for all type of reports"""
import streamlit as st
import pandas as pd
import altair as alt

from request import vasahm_query

from pages.helper.query import Queries


def chart_adder(err, data, title, y_label, chart_type = 'bar'):
    """helper function for plotting charts"""
    if chart_type == 'bar':
        if err:
            st.error(data, icon="🚨")
        else:
            if len(data) > 0:
                st.header(title, divider='rainbow')
                stock_data_history = pd.DataFrame(data, columns=["row_title",
                "value",
                "end_to_period"])
                stock_data_history["end_to_period"] = stock_data_history[
                    "end_to_period"].astype(str)

                chart = alt.Chart(stock_data_history).mark_bar().encode(
                    alt.Color('row_title:N', title="سرفصلها"),
                    alt.Y('sum(value):Q', title=y_label),
                    alt.X('end_to_period:N',title="تاریخ")
                )
                st.altair_chart(chart, use_container_width=True)
    elif chart_type == 'pie':
        if err:
            st.error(data, icon="🚨")
        else:
            if len(data) > 0:
                st.header(title, divider='rainbow')
                stock_data_history_temp = pd.DataFrame(data, columns=["row_title",
                "value"])
                stock_data_history = stock_data_history_temp[stock_data_history_temp['value'] != 0]
                chart = alt.Chart(stock_data_history).mark_arc().encode(
                    alt.Theta(field="value", type="quantitative"),
                    alt.Color(field="row_title", type="nominal", title="سرفصلها")
                )
                st.altair_chart(chart, use_container_width=True)


def add_monthly_charts(selected_stock, dollar_toggle):
    """get data and add monthly charts"""
    queries = Queries(selected_stock["name"])
    if selected_stock["cSecValReal"] in [39, 56]:
        error, stock_data = vasahm_query(
              queries.get_monthly_investment_income(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'درآمدهای ماهانه شرکت', "مبلغ (میلیون)")
        error, stock_data = vasahm_query(
              queries.get_monthly_investment_sector())
        chart_adder(error, stock_data, 'توزیع سرمایه گذاری بر اساس صنعت', None, "pie")
        error, stock_data = vasahm_query(
              queries.get_monthly_investment_stocks())
        chart_adder(error, stock_data, 'توزیع سرمایه گذاری بر اساس شرکت و اوراق', None, "pie")
    elif selected_stock["cSecValReal"] in [57]:
        error, stock_data = vasahm_query(
              queries.get_monthly_banking_income(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'درآمدهای ماهانه بانک', "مبلغ (میلیون)")
        error, stock_data = vasahm_query(
              queries.get_monthly_banking_loan_income(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'درآمدهای ماهانه حاصل از وام بانک', "مبلغ (میلیون)")
        error, stock_data = vasahm_query(
              queries.get_monthly_banking_change_bond_invest(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'تغییرات ماهانه سرمایه گذاری در اوراق', "مبلغ (میلیون)")
        error, stock_data = vasahm_query(
              queries.get_monthly_banking_change_stock_invest(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'تغییرات ماهانه سرمایه گذاری در سهام', "مبلغ (میلیون)")
        error, stock_data = vasahm_query(
              queries.get_monthly_banking_cost(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'هزینه های ماهانه بانک', "مبلغ (میلیون)")
        error, stock_data = vasahm_query(
              queries.get_monthly_banking_financial_cost(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'هزینه های مالی ماهانه بانک', "مبلغ (میلیون)")
        error, stock_data = vasahm_query(
              queries.get_monthly_banking_paid_interest(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'بهره هزینه های مالی ماهانه بانک', "مبلغ (میلیون)")

    elif selected_stock["cSecValReal"] in [58]:
        error, stock_data = vasahm_query(
              queries.get_monthly_leasing_income(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'درآمدهای ماهانه شرکت', "مبلغ (میلیون)")

        error, stock_data = vasahm_query(
              queries.get_monthly_leasing_financial_cost(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'هزینه ماهانه تامین شرکت', "مبلغ (میلیون)")

        error, stock_data = vasahm_query(
              queries.get_monthly_leasing_loan_out_no())
        chart_adder(error, stock_data, 'تعداد وام های اعطایی ماهانه', "تعداد")

        error, stock_data = vasahm_query(
              queries.get_monthly_leasing_loan_in_no())
        chart_adder(error, stock_data, 'تعداد وام های دریافتی ماهانه', "تعداد")

        error, stock_data = vasahm_query(
              queries.get_monthly_leasing_loan_in_vol(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'مبلغ وام های اعطایی ماهانه', "مبلغ (میلیون)")

        error, stock_data = vasahm_query(
              queries.get_monthly_leasing_loan_out_vol(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'مبلغ وام های دریافتی ماهانه', "مبلغ (میلیون)")

    elif selected_stock["cSecValReal"] in [66]:
        error, stock_data = vasahm_query(
              queries.get_monthly_insurance_recieve(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'گزارش ماهانه صدور حق بیمه', "مبلغ (میلیون)")

        error, stock_data = vasahm_query(
              queries.get_monthly_insurance_payment(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'گزارش ماهانه پرداخت خسارت', "مبلغ (میلیون)")


    elif selected_stock["cSecValReal"] in [67]:
        pass
    elif selected_stock["cSecValReal"] in [70]:
        error, stock_data = vasahm_query(
              queries.get_monthly_construnction_income(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'گزارش ماهانه درآمد شرکت ساختمانی', "مبلغ (میلیون)")

    elif selected_stock["cSecValReal"] in [90]:
        pass
    else:

        error, stock_data = vasahm_query(queries.get_monthly_sell_value_data(dollar=dollar_toggle))
        chart_adder(error, stock_data, 'گزارش ماهانه فروش', "مبلغ (میلیون)")

        error, stock_data = vasahm_query(queries.get_monthly_production_value_data())
        chart_adder(error, stock_data, 'گزارش تعداد تولید', "تعداد")

        error, stock_data = vasahm_query(queries.get_monthly_sell_no_data())
        chart_adder(error, stock_data, 'گزارش تعداد فروش', "تعداد")

        error, stock_data = vasahm_query(queries.get_monthly_energy_consumption())
        chart_adder(error, stock_data, 'گزارش مصرف انرژی ماهانه', "تعداد")
