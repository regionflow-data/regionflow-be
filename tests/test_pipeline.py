from regionflow.pipeline import RegionSignal, build_region_snapshot


def test_high_stockout_region_is_flagged():
    snapshots = build_region_snapshot([RegionSignal("gangnam", 100, 12, 20)])

    assert snapshots[0].action == "rebalance-inventory"
