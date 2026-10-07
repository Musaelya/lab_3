"""
Модуль «Калькулятор комиссий».
Рассчитывает комиссию за денежный перевод в зависимости от суммы.
"""

# Границы тарифных диапазонов
MIN_AMOUNT = 100
MAX_AMOUNT = 50000

# Порог для фиксированной комиссии (новое правило из Части 4)
FIXED_COMMISSION_THRESHOLD = 40000
FIXED_COMMISSION = 500.0


def calculate_commission(amount: int) -> float:
    """
    Рассчитывает комиссию для денежного перевода.

    Тарифная сетка:
        * 100..1000      -> 50 руб.
        * 1001..20000    -> 100 руб.
        * 20001..40000   -> 200 руб. + 1% от суммы
        * 40001..50000   -> 500 руб. (фиксированная)

    Args:
        amount (int): Сумма перевода (от 100 до 50 000 руб.)

    Returns:
        float: Размер комиссии в рублях.

    Raises:
        ValueError: Если сумма не входит в допустимый диапазон.
        TypeError: Если передано нечисловое значение.
    """
    # Проверка типа (защита от "abc", None, list и т.п.)
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise TypeError("Сумма перевода должна быть числом")

    # Проверка диапазона
    if amount < MIN_AMOUNT or amount > MAX_AMOUNT:
        raise ValueError(
            f"Сумма перевода должна быть от {MIN_AMOUNT} до {MAX_AMOUNT} руб."
        )

    # Тарифные диапазоны (сверху вниз — от большего к меньшему)
    if amount > FIXED_COMMISSION_THRESHOLD:
        return FIXED_COMMISSION
    if amount > 20000:
        return 200.0 + amount * 0.01
    if amount > 1000:
        return 100.0
    return 50.0