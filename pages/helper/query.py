"""handle creating all queries"""
# from datetime import datetime

class Queries():
    """
    create and return all queries
    inputs:
        name = name of stock
    """
    def __init__(self, name=None):
        self.name = name

    def get_stock_data(self):
        """return query to get stock data"""
        string = f"""select
                        stock_data.id, \"estimatedEPS\", \"sectorPE\", pe, all_holder_percent, all_holder_share
                    from
                        stock_data
                        INNER JOIN stocks ON stock_data.stock_id = stocks.id
                    where
                        stocks.name = '{self.name}'
                    order by 
                        stock_data.id desc
            """
        return string

    def get_daily_social(self, source):
        """return query to monthly sell value data"""
        string = f"""select
                        index,
                        number,
                        date
                    from
                        public.social_data
                        INNER JOIN stocks ON public.social_data.stock_id = stocks.id
                    where
                        stocks.name = '{self.name}'
                        and source = '{source}'
                    LIMIT
						30

        """
        return string
    def get_monthly_sell_value_data(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        sum(value) as value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        (public.all_data.column_title IN ('مبلغ فروش (میلیون ریال)' ,'درآمد شناسایی شده', 'درآمد محقق شده طی دوره یک ماهه - لیزینگ')
                            or public.all_data.column_title LIKE '%درآمد شناساسی شده طی دوره یک ماهه%')
                        and stocks.name = '{self.name}'
                        and public.report_list.\"letterCode\" IN ( 'ن-۳۰', 'ن-۳۱')
                        and public.all_data.deleted = false
                        and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                    group by
                        public.all_data.row_title,
                        public.all_data.end_to_period
        """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_production_value_data(self):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        sum(value) as value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        public.all_data.column_title = 'تعداد تولید'
                        and stocks.name = '{self.name}'
                        and public.report_list.\"letterCode\" IN ( 'ن-۳۰', 'ن-۳۱')
                        and public.all_data.deleted = false
                        and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                    group by
                        public.all_data.row_title,
                        public.all_data.end_to_period
        """
        return string

    def get_monthly_sell_no_data(self):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        sum(value) as value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        public.all_data.column_title = 'تعداد فروش'
                        and stocks.name = '{self.name}'
                        and public.report_list.\"letterCode\" IN ( 'ن-۳۰', 'ن-۳۱')
                        and public.all_data.deleted = false
                        and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                    group by
                        public.all_data.row_title,
                        public.all_data.end_to_period
        """
        return string

    def get_monthly_energy_consumption(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                    enery_type As row_title,
                    value,
                    end_to_period
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    public.all_data.enery_type is not null
                    and all_data.enery_type != ''
                    and all_data.column_title = 'مبلغ - میلیون ریال'
                    and stocks.name = '{self.name}'
                    and public.report_list.\"letterCode\" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
                    and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
        """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_construnction_income(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        stocks.name = '{self.name}'
                        and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                        and public.all_data.deleted = false
                        and public.all_data.column_title LIKE '%درآمد محقق شده طی دوره یک ماهه منتهی به%'
                        and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
    """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_banking_income(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        stocks.name = '{self.name}'
                        and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                        and public.all_data.deleted = false
                        and public.all_data.column_title like '%درآمد محقق شده طی دوره یک ماهه منتهی به%'
                        and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
    """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_banking_loan_income(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        stocks.name = '{self.name}'
                        and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                        and public.all_data.deleted = false
                        and public.all_data.column_title like '%درآمد تسهیلات اعطایی طی دوره یک ماهه منتهی%'
                        and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
    """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_banking_change_bond_invest(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        stocks.name = '{self.name}'
                        and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                        and public.all_data.deleted = false
                        and public.all_data.column_title like '%خالص افزایش(کاهش) در سرمایه گذاری در اوراق بدهی%'
                        and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
    """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_banking_change_stock_invest(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        stocks.name = '{self.name}'
                        and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                        and public.all_data.deleted = false
                        and public.all_data.column_title like '%افزایش(کاهش) سرمایه گذاری ها%'
                        and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
    """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_banking_cost(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        stocks.name = '{self.name}'
                        and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                        and public.all_data.table_id = 79
                        and public.all_data.deleted = false
                        and public.all_data.column_title like '%هزینه محقق شده طی دوره یک ماهه%'
                        and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                        and public.all_data.row_title not LIKE '%مامی اقلام هزینه های عملیاتی در صورت سود وزیان نمی باشد%'
    """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_banking_financial_cost(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        stocks.name = '{self.name}'
                        and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                        and public.all_data.table_id = 81
                        and public.all_data.deleted = false
                        and public.all_data.column_title like '%هزینه محقق شده طی دوره یک ماهه%'
                        and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                        and public.all_data.row_title not LIKE '%مامی اقلام هزینه های عملیاتی در صورت سود وزیان نمی باشد%'
    """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_banking_paid_interest(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        stocks.name = '{self.name}'
                        and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                        and public.all_data.deleted = false
                        and public.all_data.column_title like '%سود سپرده های سرمایه گذاری طی دوره%'
                        and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
    """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_insurance_recieve(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                    row_title,
                    value,
                    end_to_period
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    stocks.name = '{self.name}'
                    and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
                    and public.all_data.column_title = 'حق بیمه صادره (شامل قبولی اتکایی)مبلغ (میلیون ریال)'
                    and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_investment_income(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                    row_title,
                    value,
                    end_to_period
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    stocks.name = '{self.name}'
                    and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
                    and public.all_data.column_title like '%دوره یک ماهه منتهی به%'
                    and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_investment_sector(self):
        """return query to monthly sell value data"""
        string = f"""select
                    row_title,
                    value
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    stocks.name = '{self.name}'
					and public.all_data.table_id = 57
                    and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
					and public.all_data.end_to_period = (
																SELECT MAX(all_data.end_to_period)
																from
																	public.all_data
																	INNER JOIN stocks ON public.all_data.stock_id = stocks.id
																	INNER JOIN report_list ON public.all_data.report_id = report_list.id
																where
																	stocks.name = '{self.name}'
																	and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
															  )
					and public.all_data.column_title = 'کل سرمایه گذاری در سهامانتهای دورهبهای تمام شده'
                    and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                    """

        return string

    def get_monthly_investment_stocks(self):
        """return query to monthly sell value data"""
        string = f"""select
                    row_title,
                    value
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    stocks.name = '{self.name}'
                    and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
					and public.all_data.end_to_period = (
																SELECT MAX(all_data.end_to_period)
																from
																	public.all_data
																	INNER JOIN stocks ON public.all_data.stock_id = stocks.id
																	INNER JOIN report_list ON public.all_data.report_id = report_list.id
																where
																	stocks.name = '{self.name}'
																	and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
															  )
					and public.all_data.column_title = 'انتهای دورهارزش بازار'
                    and public.all_data.row_title NOT IN ('اوراق خزانه (پذیرفته نشده در بازار سرمایه)','اوراق مشارکت (پذیرفته نشده در بازار سرمایه)','سایر اوراق بهادار:','جمع سرمایه گذاری در املاک','پروژه در جریان ساخت','سرمایه  گذاری در املاک:','جمع سپرده هاى  سرمایه گذارى بانکی','سپرده هاى  سرمایه گذارى بانکی:','جمع اوراق مشتقه و تامین مالی پذیرفته شده در بورس و فرابورس','سرمایه گذاری در اوراق مشتقه و تامین مالی پذیرفته شده در بورس و فرابورس:','جمع  اوراق بهادار پذیرفته شده در بورس های کالایی و انرژی','سرمایه گذاری در اوراق بهادار پذیرفته شده در بورس های کالایی و انرژی:','جمع واحدهای صندوق های سرمایه  گذاری','سرمایه گذاری در واحدهای صندوق های سرمایه  گذاری:','جمع سهام پذیرفته شده در بورس و فرابورس','سهام درج شده در بازارهای پایه فرایورس','جمع سهام درج شده در بازارهای پایه فرایورس','سهام پذیرفته شده در بورس و فرابورس','برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                    """
        return string

    def get_monthly_insurance_payment(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                    row_title,
                    value,
                    end_to_period
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    stocks.name = '{self.name}'
                    and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
                    and public.all_data.column_title = 'خسارت پرداختیمبلغ (میلیون ریال)'
                    and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_leasing_income(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                    row_title,
                    value,
                    end_to_period
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    stocks.name = '{self.name}'
                    and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
                    and public.all_data.column_title LIKE '%درآمد محقق شده طی دوره یک ماهه منتهی به%'
                    and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_leasing_financial_cost(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                    row_title,
                    value,
                    end_to_period
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    stocks.name = '{self.name}'
                    and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
                    and public.all_data.column_title = 'هزینه محقق شده طی ماه'
                    and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_leasing_loan_out_no(self):
        """return query to monthly sell value data"""
        string = f"""select
                    row_title,
                    value,
                    end_to_period
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    stocks.name = '{self.name}'
                    and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
                    and public.all_data.column_title = 'تعداد تسهیلات ایجاد شده'
                    and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                    and public.all_data.row_title NOT LIKE '%نوع کالاهای واگذار شده در بخش اطلاعات پایه در سیستم وارد شود%'
                """
        return string


    def get_monthly_leasing_loan_in_no(self):
        """return query to monthly sell value data"""
        string = f"""select
                    row_title,
                    value,
                    end_to_period
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    stocks.name = '{self.name}'
                    and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
                    and public.all_data.column_title = 'تعداد تسهیلات تسویه شده'
                    and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                    and public.all_data.row_title NOT LIKE '%نوع کالاهای واگذار شده در بخش اطلاعات پایه در سیستم وارد شود%'
                """
        return string

    def get_monthly_leasing_loan_in_vol(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                    row_title,
                    value,
                    end_to_period
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    stocks.name = '{self.name}'
                    and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
                    and public.all_data.column_title = 'مبلغ اصل و فرع اقساط وصولی'
                    and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                    and public.all_data.row_title NOT LIKE '%نوع کالاهای واگذار شده در بخش اطلاعات پایه در سیستم وارد شود%'
                """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_leasing_loan_out_vol(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                    row_title,
                    value,
                    end_to_period
                from
                    public.all_data
                    INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                    INNER JOIN report_list ON public.all_data.report_id = report_list.id
                where
                    stocks.name = '{self.name}'
                    and public.report_list."letterCode" IN ( 'ن-۳۰', 'ن-۳۱')
                    and public.all_data.deleted = false
                    and public.all_data.column_title = 'مبلغ اصل و فرع تسهیلات اعطایی'
                    and public.all_data.row_title NOT IN ('برگشت از فروش:', 'جمع', 'جمع برگشت از فروش', 'جمع درآمد ارائه خدمات', 'جمع فروش داخلی', 'جمع فروش صادراتی', 'درآمد ارائه خدمات:', 'فروش داخلی:', 'فروش صادراتی:', '')
                    and public.all_data.row_title NOT LIKE '%نوع کالاهای واگذار شده در بخش اطلاعات پایه در سیستم وارد شود%'
                """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_quarterly_sell_and_profit(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                        INNER JOIN table_code ON public.all_data.table_id = table_code.id
                    where
                        public.all_data.row_title IN ('درآمدهای عملیاتی','سود(زیان) ناخالص','سود(زیان) خالص')
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
                        and public.all_data.deleted = false
                        and table_code.sheet_id = 1
        """
        if dollar:
            string = self._dollar_query(string)
        return string
    def get_quarterly_leasing_sell_and_profit(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                        INNER JOIN table_code ON public.all_data.table_id = table_code.id
                    where
                        public.all_data.row_title IN ('درآمدهای عملیاتی','سود(زیان) ناخالص','سود(زیان) خالص','درآمد حاصل از عملیات لیزینگ','سود (زیان) خالص پس از کسر مالیات')
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
                        and public.all_data.deleted = false
                        and table_code.sheet_id = 1
        """
        if dollar:
            string = self._dollar_query(string)
        return string
    
    def get_quarterly_investment_sell_and_profit(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                        INNER JOIN table_code ON public.all_data.table_id = table_code.id
                    where
                        public.all_data.row_title IN ('جمع درآمدهای عملیاتی','سود(زیان) ناخالص','سود(زیان) خالص')
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
                        and public.all_data.deleted = false
                        and table_code.sheet_id = 1
        """
        if dollar:
            string = self._dollar_query(string)
        return string
    
    def get_quarterly_banking_sell_and_profit(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                        INNER JOIN table_code ON public.all_data.table_id = table_code.id
                    where
                        public.all_data.row_title IN ('جمع درآمدهای عملیاتی','سود(زیان) ناخالص','سود(زیان) خالص')
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
                        and public.all_data.deleted = false
                        and table_code.sheet_id = 1
        """
        if dollar:
            string = self._dollar_query(string)
        return string
    
    def get_quarterly_insurance_sell_and_profit(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                        INNER JOIN table_code ON public.all_data.table_id = table_code.id
                    where
                        public.all_data.row_title IN ('سود (زیان) ناخالص فعالیتهای بیمه ای','درآمدهای بیمه ای','سود(زیان) خالص')
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
                        and public.all_data.deleted = false
                        and table_code.sheet_id = 1
        """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_quarterly_profit_ratio(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                        INNER JOIN table_code ON public.all_data.table_id = table_code.id
                    where
                        public.all_data.row_title IN ('درآمدهای عملیاتی','سود(زیان) ناخالص','سود(زیان) خالص')
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
                        and public.all_data.deleted = false
                        and table_code.sheet_id = 1
        """
        if dollar:
            string = self._dollar_query(string)
        return string
    def get_quarterly_leasing_profit_ratio(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                        INNER JOIN table_code ON public.all_data.table_id = table_code.id
                    where
                        public.all_data.row_title IN ('درآمدهای عملیاتی','سود(زیان) ناخالص','سود(زیان) خالص','درآمد حاصل از عملیات لیزینگ','سود (زیان) خالص پس از کسر مالیات')
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
                        and public.all_data.deleted = false
                        and table_code.sheet_id = 1
        """
        if dollar:
            string = self._dollar_query(string)
        return string
    
    def get_quarterly_investment_profit_ratio(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                        INNER JOIN table_code ON public.all_data.table_id = table_code.id
                    where
                        public.all_data.row_title IN ('جمع درآمدهای عملیاتی','سود(زیان) ناخالص','سود(زیان) خالص')
                        and public.all_data.sell_type IN ('درآمدهای عملیاتی','هزینه های عملیاتی')
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
                        and public.all_data.deleted = false
                        and table_code.sheet_id = 1
        """
        if dollar:
            string = self._dollar_query(string)
        return string
    def get_quarterly_banking_profit_ratio(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                        INNER JOIN table_code ON public.all_data.table_id = table_code.id
                    where
                        public.all_data.row_title IN ('جمع درآمدهای عملیاتی','سود(زیان) ناخالص','سود(زیان) خالص')
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
                        and public.all_data.deleted = false
                        and table_code.sheet_id = 1
        """
        if dollar:
            string = self._dollar_query(string)
        return string
   
    def get_quarterly_insurance_profit_ratio(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                        INNER JOIN table_code ON public.all_data.table_id = table_code.id
                    where
                        public.all_data.row_title IN ('سود (زیان) ناخالص فعالیتهای بیمه ای','درآمدهای بیمه ای','سود(زیان) خالص')
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
                        and public.all_data.deleted = false
                        and table_code.sheet_id = 1
        """
        if dollar:
            string = self._dollar_query(string)
        return string

    def _dollar_query(self, text):
        query_string = f"""WITH
        ranked_dates AS (
            {text}
        )
        select
            row_title,
            value::float / dollar.close As value,
            end_to_period
        from
            ranked_dates
            INNER JOIN dollar ON ranked_dates.end_to_period::varchar = dollar.\"Jalali\"
        """
        return query_string
    
    def price_query(self, dollar = False):
        """get stock price"""
        string = f"""select
                        date.miladi AS date,
                        \"openingPrice\" AS open,
                        \"maxPrice\" AS high,
                        \"minPrice\" AS low,
                        \"lastPrice\" AS close,
                        \"tradeVolume\" AS volume
                    from
                        public.stock_price
                        INNER JOIN stocks ON public.stock_price.stock_id = stocks.id
                        INNER JOIN date ON public.stock_price.\"tradeDate\" = date.jalali_3::TEXT
                    where
                        stocks.name = '{self.name}'
        """
        if dollar:
            string = self._dollar_query(string)
        return string

    QUERY_MONTHLY_COMPARE = """WITH
                        ranked_dates AS (
                            SELECT
                            stocks.name,
                            end_to_period,
                            SUM(value) as sum_value,
                            ROW_NUMBER() OVER (
                                PARTITION BY
                                stocks.name
                                ORDER BY
                                end_to_period DESC
                            ) AS rnk
                            FROM
                                public.all_data
                                INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                                INNER JOIN report_list ON public.all_data.report_id = report_list.id
                            where
                                stocks.\"stockType\" IN ('300','303','309')
                                AND public.all_data.column_title IN ('مبلغ فروش (میلیون ریال)','درآمد شناسایی شده')
                                and public.report_list.\"letterCode\" IN ( 'ن-۳۰', 'ن-۳۱')
                                and public.all_data.deleted = false
                            group by
                                stocks.name,
                                public.all_data.end_to_period
                        )
                        select
                        name,
                        (
                            MAX(
                            CASE
                                WHEN rnk = 1 THEN sum_value
                                ELSE 0
                            END
                            ) / NULLIF(MAX(
                            CASE
                                WHEN rnk = 2 THEN sum_value
                            END
                            ),0)
                        ) AS result,
                        (
                            SUM(
                            CASE
                                WHEN rnk IN (1, 2) THEN sum_value
                                ELSE 0
                            END
                            ) / NULLIF(SUM(
                            CASE
                                WHEN rnk in (3, 4) THEN sum_value
                            END
                            ),0)
                        ) AS result2,
                        (
                            SUM(
                            CASE
                                WHEN rnk IN (1, 2, 3) THEN sum_value
                                ELSE 0
                            END
                            ) / NULLIF(SUM(
                            CASE
                                WHEN rnk in (4, 5, 6) THEN sum_value
                            END
                            ),0)
                        ) AS result3,
                        max(end_to_period) as end_to_period
                        from
                        ranked_dates
                        group by
                        name"""
