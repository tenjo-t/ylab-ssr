from ssr.util import flatten


class Foo:
    bar = 1
    baz = 2


def test_flatten():
    assert flatten([1, 2, 3]) == [1, 2, 3]
    assert flatten([1, [2, [3]]]) == [1, 2, 3]
    assert flatten(["foo", "bar", "baz"]) == ["foo", "bar", "baz"]
    assert flatten(["foo", ["bar", ["baz"]]]) == ["foo", "bar", "baz"]
    assert flatten([1, {"foo": 2}]) == [1, "foo"]
    foo = Foo()
    assert flatten([1, foo, 3]) == [1, foo, 3]
