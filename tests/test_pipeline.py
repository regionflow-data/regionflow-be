from regionflow.pipeline import RegionSignal, build_region_snapshot


def test_high_stockout_region_is_flagged():
    snapshots = build_region_snapshot([RegionSignal("gangnam", 100, 12, 20)])

    assert snapshots[0].action == "rebalance-inventory"


def test_region_snapshots_are_grouped_and_sorted_by_demand():
    snapshots = build_region_snapshot([
        RegionSignal("mapo", 10, 0, 15),
        RegionSignal("gangnam", 40, 1, 20),
        RegionSignal("mapo", 15, 0, 25),
    ])

    assert [snapshot.region for snapshot in snapshots] == ["gangnam", "mapo"]
    assert snapshots[1].demand_index == 12.5
    assert snapshots[1].avg_delivery_minutes == 20
    assert snapshots[1].action == "normal"
