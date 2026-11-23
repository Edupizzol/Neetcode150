#!/usr/bin/env python3
"""Gera o card de progresso (SVG) e a seção de questões do README.

Uma questão conta como resolvida quando existe no repositório algum arquivo
ou pasta cujo nome contém o nome da questão (maiúsculas, hífens e _ são
ignorados), ex.:

    0217-contains-duplicate.cpp
    arrays/contains-duplicate.py
    1-TwoSum.py
    1-two-sum/            (pasta)

Uso: python3 scripts/update_progress.py
"""

import json
import os
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = json.loads((ROOT / "scripts" / "problems.json").read_text(encoding="utf-8"))
IGNORED_DIRS = {".git", ".github", "scripts", "assets", "node_modules"}
IGNORED_FILES = {"README.md", "LICENSE"}

START = "<!-- PROGRESS:START -->"
END = "<!-- PROGRESS:END -->"

THEMES = {
    "dark": {
        "bg": "#0d1117", "border": "#30363d", "text": "#e6edf3", "muted": "#8b949e",
        "empty": "#21262d", "track": "#21262d",
        "Easy": "#2ec4a6", "Medium": "#f5b82e", "Hard": "#f4516c",
    },
    "light": {
        "bg": "#ffffff", "border": "#d0d7de", "text": "#1f2328", "muted": "#656d76",
        "empty": "#ebedf0", "track": "#ebedf0",
        "Easy": "#00a38c", "Medium": "#d49500", "Hard": "#e0284f",
    },
}
DIFF_PT = {"Easy": "Fácil", "Medium": "Média", "Hard": "Difícil"}
DIFF_EMOJI = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"


def find_solutions():
    """Mapeia slug -> caminho relativo da solução encontrada."""
    def squash(s):
        # ignora maiúsculas, hífens, _ e pontuação: "1-TwoSum" -> "1twosum"
        return re.sub(r"[^a-z0-9]", "", s.lower())

    slugs = sorted((p["slug"] for p in PROBLEMS), key=lambda s: len(squash(s)), reverse=True)
    keys = [(s, squash(s)) for s in slugs]
    found = {}

    def match(name):
        stem = squash(name)
        # o slug mais longo vence (TwoSumII não conta como TwoSum)
        for slug, key in keys:
            if key in stem:
                return slug
        return None

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS and not d.startswith("."))
        rel_dir = Path(dirpath).relative_to(ROOT)
        for d in dirnames:
            slug = match(d)
            if slug and slug not in found:
                found[slug] = (rel_dir / d).as_posix()
        for f in sorted(filenames):
            if f in IGNORED_FILES or f.startswith("."):
                continue
            slug = match(Path(f).stem)
            if slug and slug not in found:
                found[slug] = (rel_dir / f).as_posix()
    return found


def topics():
    order = []
    grouped = {}
    for p in PROBLEMS:
        if p["topic"] not in grouped:
            order.append(p["topic"])
            grouped[p["topic"]] = []
        grouped[p["topic"]].append(p)
    return [(t, grouped[t]) for t in order]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_svg(solved, theme):
    c = THEMES[theme]
    W = 860
    pad = 28
    header_h = 150
    row_h = 30
    rows = topics()
    H = header_h + len(rows) * row_h + 64
    total = len(PROBLEMS)
    done = sum(1 for p in PROBLEMS if p["slug"] in solved)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="{FONT}" role="img" aria-label="NeetCode 150: {done} de {total} resolvidas">',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>',
    ]

    # Cabeçalho: total
    out.append(f'<text x="{pad}" y="44" fill="{c["muted"]}" font-size="13" font-weight="600" letter-spacing="1.5">NEETCODE 150</text>')
    out.append(
        f'<text x="{pad}" y="98" fill="{c["text"]}" font-family="{MONO}" font-size="52" font-weight="700">{done}'
        f'<tspan fill="{c["muted"]}" font-size="24" font-weight="500"> / {total}</tspan></text>'
    )
    out.append(f'<text x="{pad}" y="122" fill="{c["muted"]}" font-size="13">{done / total * 100:.1f}% da trilha concluída</text>')

    # Cabeçalho: por dificuldade
    col_w = 150
    x0 = W - pad - 3 * col_w + 20
    for i, diff in enumerate(("Easy", "Medium", "Hard")):
        x = x0 + i * col_w
        tot = sum(1 for p in PROBLEMS if p["difficulty"] == diff)
        d = sum(1 for p in PROBLEMS if p["difficulty"] == diff and p["slug"] in solved)
        bw = col_w - 30
        out.append(f'<text x="{x}" y="66" fill="{c[diff]}" font-size="13" font-weight="600">{DIFF_PT[diff]}</text>')
        out.append(
            f'<text x="{x}" y="94" fill="{c["text"]}" font-family="{MONO}" font-size="22" font-weight="700">{d}'
            f'<tspan fill="{c["muted"]}" font-size="14" font-weight="500"> / {tot}</tspan></text>'
        )
        out.append(f'<rect x="{x}" y="108" width="{bw}" height="6" rx="3" fill="{c["track"]}"/>')
        if d:
            out.append(f'<rect x="{x}" y="108" width="{max(6, bw * d / tot):.1f}" height="6" rx="3" fill="{c[diff]}"/>')

    out.append(f'<line x1="{pad}" y1="{header_h - 8}" x2="{W - pad}" y2="{header_h - 8}" stroke="{c["border"]}"/>')

    # Linhas por tópico
    label_w = 200
    sq = 18
    gap = 5
    bar_x = 610
    bar_w = 150
    for r, (topic, probs) in enumerate(rows):
        y = header_h + 10 + r * row_h
        d = sum(1 for p in probs if p["slug"] in solved)
        complete = d == len(probs)
        out.append(
            f'<text x="{pad}" y="{y + 13}" fill="{c["text"] if d else c["muted"]}" font-size="13"'
            f'{" font-weight=\"600\"" if complete else ""}>{esc(topic)}</text>'
        )
        for i, p in enumerate(probs):
            x = pad + label_w + i * (sq + gap)
            fill = c[p["difficulty"]] if p["slug"] in solved else c["empty"]
            out.append(f'<rect x="{x}" y="{y}" width="{sq}" height="{sq}" rx="4" fill="{fill}"/>')
        out.append(f'<rect x="{bar_x}" y="{y + 6}" width="{bar_w}" height="6" rx="3" fill="{c["track"]}"/>')
        if d:
            out.append(f'<rect x="{bar_x}" y="{y + 6}" width="{max(6, bar_w * d / len(probs)):.1f}" height="6" rx="3" fill="{c["text"]}"/>')
        out.append(
            f'<text x="{W - pad}" y="{y + 13}" text-anchor="end" fill="{c["text"] if complete else c["muted"]}" '
            f'font-family="{MONO}" font-size="12">{d}/{len(probs)}</text>'
        )

    # Legenda
    ly = H - 30
    x = pad
    for key, label in (("Easy", "Fácil"), ("Medium", "Média"), ("Hard", "Difícil"), ("empty", "Não resolvida")):
        out.append(f'<rect x="{x}" y="{ly - 10}" width="12" height="12" rx="3" fill="{c[key]}"/>')
        out.append(f'<text x="{x + 18}" y="{ly}" fill="{c["muted"]}" font-size="12">{label}</text>')
        x += 40 + len(label) * 7
    out.append(f'<text x="{W - pad}" y="{ly}" text-anchor="end" fill="{c["muted"]}" font-size="12">cada quadrado é uma questão, na ordem da trilha</text>')

    out.append("</svg>")
    return "\n".join(out) + "\n"


def render_readme_section(solved):
    lines = [START, ""]
    for topic, probs in topics():
        d = sum(1 for p in probs if p["slug"] in solved)
        mark = " ✅" if d == len(probs) else ""
        lines.append(f"<details>\n<summary><b>{topic}</b> — {d}/{len(probs)}{mark}</summary>\n")
        lines.append("| # | Questão | Dificuldade | Solução |")
        lines.append("|--:|---------|-------------|---------|")
        for p in probs:
            link = f"[{p['title']}](https://leetcode.com/problems/{p['slug']}/)"
            sol = f"✅ [código]({quote(solved[p['slug']])})" if p["slug"] in solved else ""
            lines.append(f"| {p['n']} | {link} | {DIFF_EMOJI[p['difficulty']]} {DIFF_PT[p['difficulty']]} | {sol} |")
        lines.append("\n</details>\n")
    lines.append(END)
    return "\n".join(lines)


def main():
    solved = find_solutions()
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    for theme in THEMES:
        (assets / f"progress-{theme}.svg").write_text(render_svg(solved, theme), encoding="utf-8")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    if START not in readme or END not in readme:
        raise SystemExit(f"README.md precisa conter {START} e {END}")
    before, rest = readme.split(START, 1)
    _, after = rest.split(END, 1)
    readme_path.write_text(before + render_readme_section(solved) + after, encoding="utf-8")
    print(f"{len(solved)}/{len(PROBLEMS)} resolvidas")


if __name__ == "__main__":
    main()
