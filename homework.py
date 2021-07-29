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

    def add_record(self, rc):
        self.records.append(rc)

    def get_today_stats(self):
        today_amount = 0
        for record in self.records:
            if record.date == dt.datetime.today().date():
                today_amount += record.amount
        return round(today_amount, 2)

    def get_week_stats(self):
        week_period = dt.datetime.today().date() - dt.timedelta(days=7)
        total_amount = 0
        for record in self.records:
            if week_period < record.date <= dt.datetime.today().date():
                total_amount += record.amount
        return total_amount


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        difference = self.limit - self.get_today_stats()
        if difference > 0:
            msg = (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                   f'калорийностью не более {difference} кКал')
        else:
            msg = 'Хватит есть!'
        return msg


class CashCalculator(Calculator):
    USD_RATE = 74.17
    EURO_RATE = 87.44

    def get_today_cash_remained(self, currency):
        dif = self.limit - self.get_today_stats()

        if currency == 'eur':
            msg_02 = (f'{round((abs(dif) / self.EURO_RATE), 2)} Euro')
        elif currency == 'usd':
            msg_02 = (f'{round((abs(dif) / self.USD_RATE), 2)} USD')
        elif currency == 'rub':
            msg_02 = f'{abs(dif)} руб'

        if dif > 0:
            msg = f'На сегодня осталось {msg_02}'
        elif dif == 0:
            msg = 'Денег нет, держись'
        else:
            msg = f'Денег нет, держись: твой долг - {msg_02}'
        return msg
