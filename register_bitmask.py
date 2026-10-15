"""
Лабораторна робота № 2. Модуль 2.
Побітове упакування, модифікація та розпакування апаратного 16-бітного регістра.
Освітній компонент: Програмування на Python.
"""

import sys

# Бітові маски та позиційні зсуви для 16-бітного регістра
INT_SOURCE_SHIFT = 13
INT_SOURCE_MASK = 0x7  # 3 біти (0b111)

MASKED_SHIFT = 12
MASKED_MASK = 0x1  # 1 біт (0b1)

VECTOR_ADDR_SHIFT = 5
VECTOR_ADDR_MASK = 0x7F  # 7 бітів (0b1111111)

PRIO_SHIFT = 0
PRIO_MASK = 0x1F  # 5 бітів (0b11111)

def pack_register(int_source: int, masked: bool, vector_addr: int, prio: int) -> int:
    """
    Упаковує параметри у єдиний 16-бітний цілочисельний регістр за допомогою
    операцій бітового зсуву (<<) та побітового логічного АБО (|).
    """
    # Валідація допустимих діапазонів значень бітових полів
    if not (0 <= int_source <= 7):
        raise ValueError(f"INT_SOURCE виходить за межі 3 бітів (0..7): {int_source}")
    if not (0 <= vector_addr <= 127):
        raise ValueError(f"VECTOR_ADDR виходить за межі 7 бітів (0..127): {vector_addr}")
    if not (0 <= prio <= 31):
        raise ValueError(f"PRIO виходить за межі 5 бітів (0..31): {prio}")

    masked_bit = 1 if masked else 0

    # Побітове складання зміщених полів у єдине 16-бітне ціле
    register_val = (
        (int_source << INT_SOURCE_SHIFT)
        | (masked_bit << MASKED_SHIFT)
        | (vector_addr << VECTOR_ADDR_SHIFT)
        | (prio << PRIO_SHIFT)
    )
    return register_val


def unpack_register(register_val: int) -> dict:
    """
    Розпаковує 16-бітне число у словник значень окремих бітових полів
    за допомогою бітових зсувів праворуч (>>) та бітових масок І (&).
    """
    int_source = (register_val >> INT_SOURCE_SHIFT) & INT_SOURCE_MASK
    masked = bool((register_val >> MASKED_SHIFT) & MASKED_MASK)
    vector_addr = (register_val >> VECTOR_ADDR_SHIFT) & VECTOR_ADDR_MASK
    prio = (register_val >> PRIO_SHIFT) & PRIO_MASK

    return {
        "int_source": int_source,
        "masked": masked,
        "vector_addr": vector_addr,
        "prio": prio
    }


def clear_masked_flag(register_val: int) -> int:
    """Скидає маску переривання (біт 12) у 0 за допомогою операторів & та ~ (цільовий артефакт)."""
    mask = ~(1 << MASKED_SHIFT)
    return (register_val & mask) & 0xFFFF


def main() -> None:
    """Головна точка входу для демонстрації бітових операцій над апаратним регістром."""
    print("=" * 80)
    print(f"{'ЕRegister: ПОБІТОВЕ УПАКУВАННЯ ТА МАНІПУЛЯЦІЯ РЕГІСТРАМИ':^80}")
    print("=" * 80)

    # Початкові інженерні параметри датчика
    initial_int_source = 5      # від 0 до 7 (3 біти)
    initial_masked = True       # від 0 до 1 (1 біт)
    initial_vector_addr = 100    # від 0 до 127 (7 бітів)
    initial_prio = 15           # від 0 до 31 (5 бітів)

   # 1. Упакування регістра
    reg_word = pack_register(initial_int_source, initial_masked, initial_vector_addr, initial_prio)

    print(f"Початкові поля: INT_SOURCE={initial_int_source}, MASKED={initial_masked}, VECTOR_ADDR={initial_vector_addr}, PRIO={initial_prio}")
    print(f"Упакований 16-бітний регістр:")
    print(f"  Десятковий формат (DEC): {reg_word:d}")
    print(f"  Шістнадцятковий (HEX):   0x{reg_word:04X}")
    print(f"  Двійковий формат (BIN):  0b{reg_word:016b}")
    print(f"  Вісімковий формат (OCT): 0o{reg_word:06o}")
    print("-" * 80)

    # 2. Розпакування та верифікація полів
    unpacked = unpack_register(reg_word)
    print(f"{'РЕЗУЛЬТАТ РОЗПАКУВАННЯ ТА ВЕРИФІКАЦІЇ':^80}")
    print(f"  INT_SOURCE : {unpacked['int_source']} (очікувалося {initial_int_source})")
    print(f"  MASKED     : {unpacked['masked']} (очікувалося {initial_masked})")
    print(f"  VECTOR_ADDR: {unpacked['vector_addr']} (очікувалося {initial_vector_addr})")
    print(f"  PRIO       : {unpacked['prio']} (очікувалося {initial_prio})")
    print("-" * 80)

    # 3. Маніпуляція окремими бітовими прапорцями
    print(f"{'МАНІПУЛЯЦІЯ БІТОМ 12 (MASKED)':^80}")

    reg_masked_cleared = clear_masked_flag(reg_word)
    print(f"  Після CLEAR_MASKED: 0b{reg_masked_cleared:016b} (HEX: 0x{reg_masked_cleared:04X}, MASKED={unpack_register(reg_masked_cleared)['masked']})")
    print("=" * 80)


if __name__ == "__main__":
    main()