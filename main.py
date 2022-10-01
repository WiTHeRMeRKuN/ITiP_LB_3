import datetime as dt


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

class Calculator:

    def __init__(self, limit):
        self.limit = limit #Лимит трат и калорий на день
        self.records = [] #Хранение записей
        self.current_date = dt.date.today()
        self.days_ago = self.current_date - dt.timedelta(7)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        day_stats = []
        for record in self.records:
            if record.date == self.current_date:
                day_stats.append(record.amount)
        return sum(day_stats)

    def get_week_stats(self):
        week_stats = []
        for record in self.records:
            if self.days_ago <= record.date <= self.current_date:
                week_stats.append(record.amount)
        return sum(week_stats)

class CashCalculator(Calculator):

    rouble = 1
    dollar = 55.30
    euro = 52.74

    def get_today_cash_remained(self, currency):
        currencies = {'usd': ('dollars', self.dollar), 'euro': ('euros', self.euro),
                       'rub': ('рублей', self.rouble)}
        delta_cash = self.limit - self.get_today_stats()
        if delta_cash == 0:
            message = f'Денег нет, но Вы держитесь'
        name, rate = currencies.get(currency)
        delta_cash = delta_cash / rate
        if delta_cash > 0:
            message = f'Ты можешь потратить ещё {delta_cash} {name}'
        else:
            delta_cash = abs(delta_cash)
            message = f'Денег нет, но Вы держитесь! Твой долг {delta_cash} {name}'
        return message

class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        delta_calories = self.limit-self.get_today_stats()
        if delta_calories > 0:
            message = f'Ты можешь потребить ещё {delta_calories} калорий'
        else:
            message = f'Хватит есть!'
        return message

cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=160, comment='Чай Чёрный'))
cash_calculator.add_record(Record(amount=345, comment='Обед в столовой'))
cash_calculator.add_record(Record(amount=2000, comment='Поход в ночной клуб', date='01.10.2022'))
print(cash_calculator.get_today_cash_remained(currency='rub'))

calories_calculator = CaloriesCalculator(1000)
calories_calculator.add_record(Record(amount=200, comment='Хлеб'))
calories_calculator.add_record(Record(amount=500, comment='Обед', date='01.10.2022'))
print(calories_calculator.get_calories_remained())