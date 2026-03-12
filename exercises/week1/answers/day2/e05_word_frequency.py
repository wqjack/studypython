def word_frequency(words: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for word in words:
        result[word] = result.get(word, 0) + 1
    return result


def main():
    words = ["python", "swift", "python", "js", "python", "js"]
    print(word_frequency(words))


if __name__ == "__main__":
    main()

