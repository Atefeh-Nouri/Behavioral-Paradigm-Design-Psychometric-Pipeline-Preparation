# reports/make_combined_svg.py
"""
Render one or more text test reports into a single colorized SVG.
Sanitizes input to prevent XML parsing errors (e.g., U+0000 NULL bytes).
"""
import re
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.rule import Rule
from rich.text import Text

# (pattern, style) — first match wins
RULES = [
    (re.compile(r"\bFAILED\b|\bFAIL\b|\bERROR\b"), "bold red"),
    (re.compile(r"\bPASSED\b|\bPASS\b|ALL TESTS PASSED|EQUIVALENT"), "bold green"),
    (re.compile(r"\b\d+ passed\b"), "bold green"),
    (re.compile(r"\b\d+ failed\b"), "bold red"),
    (re.compile(r"^=====.*=====$"), "cyan"),
    (re.compile(r"^\[[^\]]+\]$"), "bold cyan"),
    (re.compile(r"^Result:"), "bold green"),
]

# Regex to match characters that are strictly illegal in XML 1.0 / SVG
# Includes \x00-\x08, \x0b, \x0c, \x0e-\x1f
ILLEGAL_XML_CHARS_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')

def sanitize_for_xml(text: str) -> str:
    """Removes NULL bytes and control characters that break SVG rendering."""
    # Remove standard illegal XML chars
    text = ILLEGAL_XML_CHARS_RE.sub('', text)
    # Remove surrogate pairs that might have been mangled during file read
    text = text.encode('utf-8', 'replace').decode('utf-8', 'ignore')
    return text

def style_line(line: str) -> Text:
    for pattern, style in RULES:
        if pattern.search(line):
            return Text(line, style=style)
    return Text(line)

def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2

    *input_paths, output_path = argv[1:]
    inputs = [Path(p) for p in input_paths]
    output = Path(output_path)

    missing = [p for p in inputs if not p.exists()]
    if missing:
        for p in missing:
            print(f"ERROR: missing input file: {p}", file=sys.stderr)
        return 1

    console = Console(
        record=True,
        width=160,
        force_terminal=True,
        color_system="truecolor",
    )

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    console.print(Rule(
        f"[bold magenta]CPT Project Verification — {stamp}[/]",
        style="magenta",
    ))
    console.print()

    for idx, path in enumerate(inputs):
        if idx > 0:
            console.print()
            console.print(Rule(style="cyan"))
            console.print()

        # Read and sanitize the file content to prevent U+0000 XML crashes
        raw_text = path.read_text(encoding="utf-8", errors="replace")
        
        for raw in raw_text.splitlines():
            clean_line = sanitize_for_xml(raw)
            
            if "\x1b[" in clean_line:
                console.print(Text.from_ansi(clean_line))
            else:
                console.print(style_line(clean_line))

    console.print()
    console.print(Rule(style="magenta"))

    output.parent.mkdir(parents=True, exist_ok=True)
    console.save_svg(str(output), title="CPT Project — Verification")
    size_kb = output.stat().st_size / 1024
    print(f"Wrote {output}  ({size_kb:.1f} KB)")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))