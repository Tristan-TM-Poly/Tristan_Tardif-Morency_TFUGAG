from tfuga.ait_code_analyser_writer import AITCodeAnalyserWriter


def test_analyser_scores_python_file():
    source = '"""demo"""\n\nimport math\n\ndef f(x):\n    return math.sqrt(x)\n'
    signal = AITCodeAnalyserWriter().analyse_python("demo.py", source)
    assert signal.oak_score >= 7.0
    assert signal.functions == 1


def test_analyser_generates_markdown_report():
    files = [("a.py", "def f():\n    return 1\n"), ("b.txt", "ignored")]
    repo = AITCodeAnalyserWriter().analyse_many(files)
    report = AITCodeAnalyserWriter().markdown_report(repo)
    assert "AIT Code Analysis" in report
    assert "a.py" in report


def test_analyser_generates_proposal():
    repo = AITCodeAnalyserWriter().analyse_many([("a.py", "# TODO: improve\ndef f():\n    return 1\n")])
    proposal = AITCodeAnalyserWriter().proposal_markdown(repo)
    assert "AIT Improvement Proposal" in proposal
    assert "[ ]" in proposal
