"""LanguageTool (en-GB) check of every spoken line and every on-screen text of an episode.
Usage: python scripts/lt_check.py <lines.json> <out.md> <scene.py> [<scene.py> ...]
lines.json = [{"id": ..., "text": ...}]. On-screen texts = string literals in the scene files (docstrings skipped).
Note (23 Nov 2026): language_tool_python 3.x renamed Match.errorLength/ruleId to error_length/rule_id;
the old names raise AttributeError. Needs Java 17 on the runner (actions/setup-java)."""
import ast, json, re, sys
import language_tool_python
lines_path, out_path, scene_files = sys.argv[1], sys.argv[2], sys.argv[3:]
items = [(f"voice {x['id']}", x["text"]) for x in json.load(open(lines_path))]
import os
for f in scene_files:
    if not os.path.exists(f) or f in ('-', 'none'):
        continue
    tree = ast.parse(open(f).read())
    docs = {id(n.body[0].value) for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.Module, ast.ClassDef)) and n.body
            and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
    seen = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs:
            s = n.value.strip()
            if s in seen or len(s) < 3 or not re.search(r"[A-Za-z]{3}", s): continue
            if re.fullmatch(r"[a-z0-9_./\-]+", s) or s.startswith(("#", "%", "[S")): continue
            seen.add(s); items.append((f"screen {f.split('/')[-1]}:{n.lineno}", s))
tool = language_tool_python.LanguageTool("en-GB")
IGNORE = {"MORFOLOGIK_RULE_EN_GB"}   # spelling: unknown words are listed separately (names, tickers)
rows, spell = [], {}
for where, text in items:
    for m in tool.check(text):
        L = m.error_length if hasattr(m, "error_length") else m.errorLength
        rid = m.rule_id if hasattr(m, "rule_id") else m.ruleId
        bad = text[m.offset:m.offset + L]
        if rid in IGNORE:
            spell.setdefault(bad, []).append(where); continue
        rows.append(f"| {where} | {rid} | `{bad}` → {', '.join(m.replacements[:3]) or '—'} | {m.message} | {text} |")
out = f"# LanguageTool en-GB · {len(items)} texts\n\n## Grammar / style ({len(rows)})\n\n| where | rule | text → suggestion | message | full text |\n|---|---|---|---|---|\n"
out += "\n".join(rows) + f"\n\n## Unknown words ({len(spell)})\n\n" + "\n".join(f"- `{w}` ({len(v)}×): {', '.join(v[:4])}" for w, v in sorted(spell.items()))
open(out_path, "w").write(out + "\n"); print(out)
