import csv
from pathlib import Path


def safe_amount(raw: str) -> float:
    try:
        return float(raw)
    except (TypeError, ValueError):
        return 0.0


def load_orders(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_report(orders: list[dict]) -> list[dict]:
    agg: dict[str, dict] = {}
    for order in orders:
        user_id = order["user_id"]
        amount = safe_amount(order["amount"])
        row = agg.setdefault(user_id, {"user_id": user_id, "total": 0.0, "count": 0})
        row["total"] += amount
        row["count"] += 1

    result = []
    for row in agg.values():
        avg = row["total"] / row["count"] if row["count"] else 0.0
        result.append(
            {
                "user_id": row["user_id"],
                "total_amount": f"{row['total']:.2f}",
                "order_count": str(row["count"]),
                "avg_amount": f"{avg:.2f}",
            }
        )
    return result


def main():
    base = Path(__file__).parent
    orders = load_orders(base / "orders.csv")
    report = build_report(orders)
    print(report)


if __name__ == "__main__":
    main()

