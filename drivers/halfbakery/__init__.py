def harvest():
    test_items = [{'-': 'https://someplace.com/something1', 'a': 1},
                  {'-': 'https://someplace.com/something2', 'b': 2},
                  {'-': 'https://someplace.com/something3', 'c': 3}]

    for item in test_items:
        yield item
