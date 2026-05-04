# samples/broken_syntax.py
def add(a, b):
    """Adds two numbers together.

    Args:
        a (int | float): The first number.
        b (int | float): The second number.

    Returns:
        int | float: The sum of a and b.
    """
    return a + b

if __name__ == "__main__":
    print(add(1, 2))