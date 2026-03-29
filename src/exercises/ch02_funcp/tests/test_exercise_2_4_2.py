from exercises.ch02_funcp.exercise_2_4_2 import capitalise_names


def test_capitalise_names():

    names = ["alice", "bob", "charlie", "diana"]

    # lazy returned collection
    lazy = capitalise_names(names)

    # list will force lazy collection to evaluate
    assert list(lazy) == ["ALICE", "BOB", "CHARLIE", "DIANA"]
