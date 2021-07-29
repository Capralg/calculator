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
        difference = self.limit - self.get_today_stats()

        if currency == 'eur':
            msg_02 = f'{round((abs(difference) / CashCalculator.EURO_RATE), 2)} Euro'
        elif currency == 'usd':
            msg_02 = f'{round((abs(difference) / CashCalculator.USD_RATE), 2)} USD'
        elif currency == 'rub':
            msg_02 = f'{abs(difference)} руб'

        if difference > 0:
            msg = f'На сегодня осталось {msg_02}'
        elif difference == 0:
            msg = 'Денег нет, держись'
        else:
            msg = f'Денег нет, держись: твой долг - {msg_02}'
        return msg


# для CashCalculator
r1 = Record(amount=100, comment='Безудержный шопинг', date='22.07.2021')
r2 = Record(amount=1568,
            comment='Наполнение потребительской корзины',
            date='19.07.2021')
r3 = Record(amount=600, comment='Катание на такси', date='25.07.2021')

# для CaloriesCalculator
r4 = Record(amount=1186,
            comment='Кусок тортика. И ещё один.',
            date='27.07.2021')
r5 = Record(amount=840, comment='Йогурт.', date='29.07.2021')
r6 = Record(amount=1140, comment='Баночка чипсов.', date='24.07.2021')


cash_calculator = CashCalculator(2500)
calories_calculator = CaloriesCalculator(1000)

cash_calculator.add_record(r1)
cash_calculator.add_record(r2)
cash_calculator.add_record(r3)
calories_calculator.add_record(r4)
calories_calculator.add_record(r5)
calories_calculator.add_record(r6)
cash_calculator.add_record(Record(amount=100, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=300, comment='Васе за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='26.07.2021'))

print(cash_calculator.get_today_cash_remained('usd'))
print(calories_calculator.get_calories_remained())

print(f'Недельная статистика: {cash_calculator.get_week_stats()}')
