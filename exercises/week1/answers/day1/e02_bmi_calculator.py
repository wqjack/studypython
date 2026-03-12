def calc_bmi(height_m: float, weight_kg: float) -> float:
    if height_m <= 0:
        raise ValueError("height_m must be greater than 0")
    return weight_kg / (height_m ** 2)


def main():
    height_m = 1.75
    weight_kg = 68
    bmi = calc_bmi(height_m, weight_kg)
    print(f"BMI: {bmi:.2f}")


if __name__ == "__main__":
    main()

