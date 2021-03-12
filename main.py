# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def int_to_binary_string(number: int, bit_width: int):
    """

    Args:
        number: Number to convert
        bit_width: Width of bit string

    Returns:
        str: Bit string
    """
    return "".join(map(lambda x: str((number >> x) & 1), range(bit_width - 1, -1, -1)))
    # 大概是


# Press the green button in the gutter to run the script.
# 求前20项的斐波那契数
a = 0
b = 1
for _ in range(20):
    print(1)
    print([("1q "*i).decode()[:65535] + b"\xfe" for i in (2, 10, 100, 500, 1000, 2000, 5000, 10000, 50000)])

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
