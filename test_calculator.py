"""
Модульные тесты для модуля calculator.
Запуск: pytest --cov=calculator --cov-report=html
"""
import pytest
from calculator import calculate_commission


class TestCalculateCommission:
    """Позитивные тесты — корректный расчёт комиссии."""

    @pytest.mark.parametrize(
        "amount, expected",
        [
            # Тариф 1: 100..1000 -> 50 руб.
            (100, 50.0),      # нижняя граница диапазона
            (500, 50.0),
            (1000, 50.0),     # верхняя граница диапазона
            # Тариф 2: 1001..20000 -> 100 руб.
            (1001, 100.0),    # нижняя граница
            (10000, 100.0),
            (20000, 100.0),   # верхняя граница
            # Тариф 3: 20001..40000 -> 200 + 1%
            (20001, 400.01),  # нижняя граница
            (30000, 500.0),
            (40000, 600.0),   # верхняя граница третьего тарифа
            # Тариф 4: 40001..50000 -> фиксированная 500 руб.
            (40001, 500.0),   # нижняя граница нового правила
            (50000, 500.0),   # верхняя граница
        ],
    )
    def test_commission_calculation(self, amount, expected):
        assert calculate_commission(amount) == pytest.approx(expected)


class TestCalculateCommissionErrors:
    """Негативные тесты — обработка невалидных данных."""

    @pytest.mark.parametrize("invalid_amount", [99, 0, -1, -100, 50001, 100000])
    def test_invalid_amount_raises_value_error(self, invalid_amount):
        with pytest.raises(ValueError):
            calculate_commission(invalid_amount)

    @pytest.mark.parametrize("invalid_type", ["abc", None, [100], {"a": 1}, 100.5])
    def test_invalid_type_raises_type_error(self, invalid_type):
        with pytest.raises(TypeError):
            calculate_commission(invalid_type)

    def test_bool_raises_type_error(self):
        # bool — подкласс int, но для суммы не подходит
        with pytest.raises(TypeError):
            calculate_commission(True)


class TestBoundaryValues:
    """Отдельный класс для явной проверки границ диапазонов."""

    @pytest.mark.parametrize(
        "amount, expected",
        [
            (100, 50.0),      # граница MIN
            (1000, 50.0),     # граница 1-го тарифа
            (1001, 100.0),    # переход во 2-й тариф
            (20000, 100.0),   # граница 2-го тарифа
            (20001, 400.01),  # переход в 3-й тариф
            (40000, 600.0),   # граница 3-го тарифа
            (40001, 500.0),   # переход в 4-й тариф
            (50000, 500.0),   # граница MAX
        ],
    )
    def test_boundaries(self, amount, expected):
        assert calculate_commission(amount) == pytest.approx(expected, rel=1e-9)