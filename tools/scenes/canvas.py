"""Builder canvas geometry after scene 05b (zoom 0.7986, panned)."""
K, OX, OY = 0.7986, 620.7, 540.2
PALETTE = {"Trigger": 228, "Hermes": 262, "Files": 304, "Filter": 337, "Search": 371, "Append": 404, "Read": 446,
           "Map": 479, "Collate": 513, "Index": 547, "Prompt": 580, "Output": 614, "Run command": 655,
           "Run Python": 689, "Write file": 722}


def S(wx, wy):
    """Screen point of a world point on the canvas."""
    return round(OX + K * wx), round(OY + K * wy)


def drop_point(x, y):
    """Where to drop a palette item so the new node's top-left lands on world (x, y)."""
    return S(x + 120, y + 36)


def palette(name):
    return 1800, PALETTE[name]
