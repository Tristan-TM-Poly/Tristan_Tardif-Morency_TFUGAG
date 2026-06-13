# AIT-CodeAnalyserWriter

`AITCodeAnalyserWriter` analyzes Python source snapshots and writes OAK-oriented reports.

## It produces

- per-file signals;
- repository OAK score;
- top improvement actions;
- Markdown documentation report;
- Markdown proposal checklist.

## Use

```python
from tfuga.ait_code_analyser_writer import AITCodeAnalyserWriter

ait = AITCodeAnalyserWriter()
repo = ait.analyse_many([("module.py", "def f():\n    return 1\n")])
print(ait.markdown_report(repo))
```

This is designed for assistant-side analysis of Tristan's GitHub code and creation pipeline.
