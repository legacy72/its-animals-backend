from decimal import Decimal


def price_to_text(price):
    price = Decimal(price)
    rub = int(price)
    cop = int(100 * (price - rub))

    if 11 <= rub % 100 <= 19:
        text = f'{rub} рублей'
    elif rub % 10 == 1:
        text = f'{rub} рубль'
    elif 2 <= rub % 10 <= 4:
        text = f'{rub} рубля'
    else:
        text = f'{rub} рублей'

    if cop:
        if cop % 10 == 1:
            text += f' {cop} копейка'
        elif 2 <= cop % 10 <= 4:
            text += f' {cop} копейки'
        else:
            text += f' {cop} копеек'

    return text
