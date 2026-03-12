def to_grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def main():
    for score in [95, 82, 76, 61, 40]:
        print(score, "=>", to_grade(score))


if __name__ == "__main__":
    main()

