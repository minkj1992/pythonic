import itertools


class TimeZone:
    pass

class Account:
    transaction_counter = itertools.count(100)
    _interest_rate = 0.5

    _transaction_codes = {
        'deposit': 'D',
        'withdraw': 'W',
        'interest': 'I',
        'rejected': 'X'
    }


if __name__ == '__main__':
    import os
    os.system("pytest")