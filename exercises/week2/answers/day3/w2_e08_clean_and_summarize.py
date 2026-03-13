import json
from pathlib import Path


def clean_user(raw: dict) -> dict:
    return {
        "id": int(raw.get("id", 0)),
        "name": raw.get("name") or "unknown",
        "department": raw.get("department") or "unknown",
        "role": raw.get("role") or "unknown",
        "age": int(raw.get("age") or 0),
    }


def summarize(users: list[dict]) -> dict:
    dep: dict[str, int] = {}
    role: dict[str, int] = {}
    for user in users:
        dep[user["department"]] = dep.get(user["department"], 0) + 1
        role[user["role"]] = role.get(user["role"], 0) + 1
    return {"by_department": dep, "by_role": role}


def main():
    base = Path(__file__).parent
    rows = json.loads((base / "users_dirty.json").read_text(encoding="utf-8"))
    cleaned = [clean_user(row) for row in rows]
    result = summarize(cleaned)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

