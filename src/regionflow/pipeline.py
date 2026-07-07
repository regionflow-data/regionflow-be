from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class RegionSignal:
    region: str
    orders: int
    stockouts: int
    delivery_minutes: int


@dataclass(frozen=True)
class RegionSnapshot:
    region: str
    demand_index: float
    stockout_rate: float
    avg_delivery_minutes: float
    action: str


def build_region_snapshot(signals: list[RegionSignal]) -> list[RegionSnapshot]:
    grouped: dict[str, list[RegionSignal]] = {}
    for signal in signals:
        grouped.setdefault(signal.region, []).append(signal)

    snapshots: list[RegionSnapshot] = []
    for region, rows in grouped.items():
        orders = sum(row.orders for row in rows)
        stockouts = sum(row.stockouts for row in rows)
        delivery = mean(row.delivery_minutes for row in rows)
        stockout_rate = stockouts / orders if orders else 0
        action = "rebalance-inventory" if stockout_rate > 0.08 else "normal"
        snapshots.append(
            RegionSnapshot(
                region=region,
                demand_index=round(orders / max(len(rows), 1), 2),
                stockout_rate=round(stockout_rate, 4),
                avg_delivery_minutes=round(delivery, 2),
                action=action,
            )
        )

    return sorted(snapshots, key=lambda item: item.demand_index, reverse=True)
