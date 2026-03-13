def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def main():
    print(safe_int("10"), safe_int("x"))
    print(safe_float("2.5"), safe_float(None))


if __name__ == "__main__":
    main()

