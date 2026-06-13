from tfuga import Runner, StateBook, TextPublisher, TextSection


def test_runner():
    assert Runner().run("x", lambda: 2 + 2).output == 4


def test_statebook():
    assert StateBook().sequence("abc")[0].state == "ready"


def test_writer():
    text = TextPublisher().render("T", [TextSection("A", "B")])
    assert text.startswith("# T")
