from agent import SearchAgent


def test_astar_logical_reasoning():

    agent = SearchAgent()

    # -------------------------------------------------
    # TEST 1: Unsafe tile
    # -------------------------------------------------

    start = (0, 0)
    goal = (2, 0)

    grid_size = (3, 1)
    walls = set()

    tile_facts = {
        (1, 0): [
            'TargetVisible',
            'HasDust',
            'BloodseekerMissing'
        ]
    }

    path = agent.astar_search(
        start,
        goal,
        grid_size,
        walls,
        tile_facts
    )

    print("Test 1 - Unsafe tile")
    print("Calculated path:", path)

    assert path == [], \
        "FAILED: A* entered an infeasible tile!"

    print("PASS: Unsafe tile was rejected.\n")

    # -------------------------------------------------
    # TEST 2: Safe tile
    # -------------------------------------------------

    agent = SearchAgent()

    tile_facts = {
        (1, 0): [
            'TargetVisible',
            'HasDust'
        ]
    }

    path = agent.astar_search(
        start,
        goal,
        grid_size,
        walls,
        tile_facts
    )

    print("Test 2 - Safe tile")
    print("Calculated path:", path)

    assert path == ['Right', 'Right'], \
        "FAILED: Safe tile should be allowed!"

    print("PASS: Safe tile was allowed.\n")

    print("All A* Logical Reasoning Tests Passed!")


if __name__ == "__main__":
    test_astar_logical_reasoning()