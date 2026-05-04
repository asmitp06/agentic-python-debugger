try:
    a, b = map(int, input().split())
except (EOFError, ValueError):
    a, b = 0, 0
print(a + b)