import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.today().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        today = dt.datetime.today().date()
        return sum([record.amount for record in self.records
                    if record.date == today])

    def get_week_stats(self):
        week_period = dt.datetime.today().date() - dt.timedelta(days=7)
        today = dt.datetime.today().date()
        return sum([record.amount for record in self.records
                    if today >= record.date > week_period])

    def calc_difference(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        difference = self.calc_difference()
        if difference > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {difference} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 74.14
    EURO_RATE = 87.61

    def get_today_cash_remained(self, currency):
        difference = self.calc_difference()
        currency_dict = {'rub': ['руб', 1.0],
                         'eur': ['Euro', self.EURO_RATE],
                         'usd': ['USD', self.USD_RATE]}

        if currency not in currency_dict.keys():
            return 'Неправильный формат валюты'

        if difference == 0:
            return 'Денег нет, держись'

        cash = round((abs(difference) / currency_dict[currency][1]), 2)
        message = f'{cash} {currency_dict[currency][0]}'

        if difference > 0:
            return f'На сегодня осталось {message}'
        else:
            return f'Денег нет, держись: твой долг - {message}'
