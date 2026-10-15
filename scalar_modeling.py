"""
Лабораторна робота № 2. Модуль 1.
Аналітичне моделювання нелінійного сигналу та розрахунок комплексного імпедансу.
Освітній компонент: Програмування на Python.
"""

import math
import cmath
import sys


def compute_main(x: float, y: float) -> float:
    """
    f(x, y) = (cos(x * y) + ln(x^4 + 1)) / (exp(y / 3) + sqrt(x + 1))
    """
    if x < -1.0:
        raise ValueError("Параметр x не може бути від'ємним для фізичної системи.")

    result = (math.cos(x * y) + math.log(x**4.0 + 1.0))/(math.exp(y / 3.0) + math.sqrt(x + 1.0))
    return result


def compute_rlc_impedance(r_resistance: float, l_inductance: float, c_capacitance: float, frequency_hz: float) -> complex:
    """
    Обчислює комплексний опір (імпеданс) послідовного RLC-контуру:
    Z = R + j * (omega * L - 1 / (omega * C)), де omega = 2 * pi * f
    """
    if frequency_hz <= 0.0 or c_capacitance <= 0.0 or l_inductance <= 0.0:
        raise ValueError("Фізичні параметри L, C та частота f повинні бути строго більшими за нуль.")

    omega = 2.0 * math.pi * frequency_hz
    reactance_l = omega * l_inductance
    reactance_c = 1.0 / (omega * c_capacitance)
    total_reactance = reactance_l - reactance_c

    # Формування комплексного числа типу complex
    impedance = complex(r_resistance, total_reactance)
    return impedance


def main() -> None:
    """Головна точка входу для демонстрації аналітичних скалярних обчислень."""
    print("=" * 80)
    print(f"{'АНАЛІТИЧНЕ МОДЕЛЮВАННЯ ТА ОБЧИСЛЕННЯ СКАЛЯРНИХ ДАНИХ':^80}")
    print("=" * 80)

    # 1. Розрахунок аналітичного сигналу
    x_2 = 2.5  # секунди
    y_2 = 4.0  # рад/с
    signal_val = compute_main(x_2, y_2)

    # Еталонне значення для перевірки точності
    reference_val =(math.cos(2.5 * 4.0) + math.log(2.5**4.0 + 1.0)) / (math.exp(4.0 / 3.0) + math.sqrt(2.5 + 1.0))
    is_accurate = math.isclose(signal_val, reference_val, rel_tol=1e-9, abs_tol=1e-12)

    print(f"X{x_2:8.3f}")
    print(f"Y{y_2:8.3f}")
    print(f"Розраховане значення сигналу:  {signal_val:12.8f}")
    print(f"Еталонне значення перевірки:   {reference_val:12.8f}")
    print(f"Точність IEEE 754 (isclose):   {str(is_accurate).upper()} (rel_tol=1e-9)")
    print("-" * 80)

    # 2. Розрахунок комплексного імпедансу RLC кола
    r_val = 100.0        # Ом
    l_val = 0.05         # Генрі (50 мГн)
    c_val = 10.0e-6      # Фарад (10 мкФ)
    freq_val = 200.0     # Герц

    z_complex = compute_rlc_impedance(r_val, l_val, c_val, freq_val)
    z_magnitude, z_phase_rad = cmath.polar(z_complex)
    z_phase_deg = math.degrees(z_phase_rad)

    print(f"{'РОЗРАХУНОК КОМПЛЕКСНОГО ІМПЕДАНСУ RLC-КОНТУРУ':^80}")
    print("-" * 80)
    print(f"Параметри кола: R = {r_val:.1f} Ом, L = {l_val * 1e3:.1f} мГн, C = {c_val * 1e6:.1f} мкФ, f = {freq_val:.1f} Гц")
    print(f"Комплексний імпеданс Z:        {z_complex.real:8.3f} + {z_complex.imag:8.3f}j Ом")
    print(f"Активний опір Re(Z):           {z_complex.real:8.3f} Ом")
    print(f"Реактивний опір Im(Z):         {z_complex.imag:8.3f} Ом")
    print(f"Повний модуль імпедансу |Z|:   {z_magnitude:8.3f} Ом")
    print(f"Фазовий кут зсуву (Arg Z):     {z_phase_deg:8.3f} град ({z_phase_rad:8.4f} рад)")
    print("=" * 80)


if __name__ == "__main__":
    main()