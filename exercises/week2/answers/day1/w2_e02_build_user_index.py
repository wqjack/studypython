def build_user_index(users: list[dict]) -> dict[int, dict]:
    index: dict[int, dict] = {}
    for user in users:
        user_id = int(user["id"])
        index[user_id] = user
    return index


def main():
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    print(build_user_index(users))


if __name__ == "__main__":
    main()

