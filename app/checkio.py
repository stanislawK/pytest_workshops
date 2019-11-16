from math import ceil, floor

"""
You should write a function for converting a number to string using several
rules. First of all, you will need to cut the number with a given base
(base argument; default 1000). The value is a float number with decimal after
the point (decimals argument; default 0). For the value, use the rounding
towards zero rule (5.6⇒5, -5.6⇒-5) if the decimal = 0, otherwise use the
standard rounding procedure. If the number of decimals is greater than the
current number of digits after dot, trail value with zeroes. The number should
be a value with letters designating the power. You will be given a list of
power designations (powers argument;
default ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']). If you are given suffix
(suffix argument; default ‘’) , then you must append it. If you don’t have
enough powers - stay at the maximum. And zero is always zero without powers,
but with suffix.
"""


def friendly_number(number, base=1000, decimals=0, suffix='',
                    powers=['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']):
    powers_dict = {power: base**i for i, power in enumerate(powers)}
    if not decimals:
        number = floor(number) if number >= 0 else ceil(number)
    power_arg = ""
    for i, values in enumerate(powers_dict.items()):
        key, value = values
        if number and abs(number) / value < 1:
            power_arg = powers[i-1]
            number = number / powers_dict[power_arg]
            number = round(number, decimals) if decimals else int(number)
            break
        elif number and i == len(powers_dict.items())-1:
            power_arg = powers[i]
            number = number / powers_dict[power_arg]
            number = round(number, decimals) if decimals else int(number)

    return f"{number:.{decimals}f}{power_arg}{suffix}"
