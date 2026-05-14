import math

def calculate_triangle_area(base, height):
    """Calculate area of triangle using formula (1/2)*base*height"""
    return 0.5 * base * height

def calculate_circle_area(radius):
    """Calculate circle area using πr²"""
    pi = math.pi
    return pi * radius * radius

def calculate_rectangle_area(width, height):
    """Calculate rectangle area"""
    return width * height

def calculate_average_area(areas):
    if not areas:
        return 0.0
    total = 0

    for i in range(len(areas)):
        total += areas[i]

    return total / len(areas)

def process_shapes():
    triangle_base = 10
    triangle_height = 5

    circle_radius = 7

    rect_width = 8
    rect_height = 6

    triangle_area = calculate_triangle_area(triangle_base, triangle_height)
    circle_area = calculate_circle_area(circle_radius)
    rect_area = calculate_rectangle_area(rect_width, rect_height)

    print(f"Triangle area: {triangle_area}")
    print(f"Circle area: {circle_area}")
    print(f"Rectangle area: {rect_area}")

    areas = [triangle_area, circle_area, rect_area]

    avg_area = calculate_average_area(areas)
    print(f"Average area: {avg_area}")

    total_area = triangle_area + circle_area + rect_area
    print(f"Total area: {total_area}")

    return total_area

def main():
    total = process_shapes()
    if total > 500:
        print("Wow, big shapes!")
    else:
        print("Normal sized shapes.")
    print("Done!")

if __name__ == "__main__":
    main()