def count_ones(n):
    """Подсчитывает количество единиц в двоичном представлении числа"""
    count = 0
    while n > 0:
        count += n & 1
        n >>= 1
    return count


assert count_ones(5) == 2
assert count_ones(7) == 3
assert count_ones(247923789) == 13
assert count_ones(2147483647) == 31