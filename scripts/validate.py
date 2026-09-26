#!/usr/bin/env python3
"""Validate the skills: structure, metadata and every cubecli command they cite.

Checks
- manifest.json lists exactly the skill directories, and its version matches
  plugin.json.
- Each SKILL.md has frontmatter with `name` (= directory name, kebab-case, max
  64 chars) and `description` (max 1024 chars), and stays under 500 lines.
- Relative links resolve.
- Every `cubecli ...` invocation in a SKILL.md (code blocks and inline code) is
  a real command in the generated reference, and every `--flag` it uses exists
  on that command. This is what keeps the skills from inventing flags.

Usage: scripts/validate.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "cubepath"
SKILLS = PLUGIN / "skills"

errors: list[str] = []


def err(where: Path | str, msg: str) -> None:
    errors.append(f"{Path(where).relative_to(ROOT) if isinstance(where, Path) else where}: {msg}")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def load_reference() -> tuple[dict[str, set[str]], set[str]]:
    """Command path -> flags, from every skill's reference/ plus the index."""
    commands: dict[str, set[str]] = {}
    global_flags: set[str] = {"--help", "-h"}
    heading = re.compile(r"^## `(cubecli [^`]+)`$")
    flag = re.compile(r"^- `(?:-(\w), )?--([\w-]+)")
    for ref in SKILLS.glob("*/reference/*.md"):
        current = None
        in_globals = False
        for line in ref.read_text().splitlines():
            if line == "## Global flags":
                in_globals, current = True, None
                continue
            m = heading.match(line)
            if m:
                current, in_globals = m.group(1), False
                commands.setdefault(current, set())
                continue
            if line.startswith("## "):
                current, in_globals = None, False
                continue
            f = flag.match(line)
            if f:
                names = {"--" + f.group(2)} | ({"-" + f.group(1)} if f.group(1) else set())
                if in_globals:
                    global_flags |= names
                elif current:
                    commands[current] |= names
    return commands, global_flags


def invocations(text: str) -> list[str]:
    """cubecli command lines from fenced blocks and inline code."""
    found = []
    for block in re.findall(r"```[a-z]*\n(.*?)```", text, re.S):
        joined = re.sub(r"\\\n\s*", " ", block)
        for line in joined.splitlines():
            line = line.split("#", 1)[0] if " #" in line else line
            for part in re.split(r"\||&&|;|\$\(", line):
                part = part.strip()
                if part.startswith("cubecli ") or re.search(r"(^|\s)cubecli\s", part):
                    found.append(part[part.index("cubecli"):])
    prose = re.sub(r"```.*?```", "", text, flags=re.S)
    for code in re.findall(r"`([^`\n]+)`", prose):
        if code.startswith("cubecli "):
            found.append(code.split("|")[0].strip())
    return found


def check_invocation(skill: Path, line: str, commands: dict[str, set[str]], global_flags: set[str]) -> None:
    tokens = line.split()
    # Global flags may come before the command: `cubecli --profile work vps list`.
    rest = tokens[1:]
    while rest and rest[0].startswith("-"):
        flag_name = rest[0].split("=", 1)[0]
        if flag_name not in global_flags:
            err(skill, f"unknown global flag {flag_name}: {line}")
        rest = rest[2:] if flag_name == "--profile" and "=" not in rest[0] else rest[1:]
    words = []
    for t in rest:
        if not re.fullmatch(r"[a-z][a-z0-9-]*", t):
            break
        words.append(t)
    # Longest prefix that is a known command.
    if not words:
        return  # placeholder such as `cubecli <group> --help`
    cmd = None
    for n in range(len(words), 0, -1):
        candidate = "cubecli " + " ".join(words[:n])
        if candidate in commands:
            cmd = candidate
            break
    if cmd is None:
        # A group without a subcommand ("cubecli vps") is fine in prose.
        prefix = "cubecli " + " ".join(words)
        if words and any(c.startswith(prefix + " ") for c in commands):
            return
        err(skill, f"unknown command: {line}")
        return
    allowed = commands[cmd] | global_flags
    for t in tokens:
        if t.startswith("-") and not re.fullmatch(r"-+\d.*", t):
            name = t.split("=", 1)[0].rstrip(",.)")
            if name in ("-", "--"):
                continue
            if name not in allowed:
                err(skill, f"`{cmd}` has no flag {name}: {line}")


def main() -> int:
    manifest = json.loads((ROOT / "manifest.json").read_text())
    plugin = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
    json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())

    if manifest.get("version") != plugin.get("version"):
        err("manifest.json", f"version {manifest.get('version')} != plugin.json {plugin.get('version')}")

    dirs = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
    if sorted(manifest.get("skills", [])) != dirs:
        err("manifest.json", f"skills {sorted(manifest.get('skills', []))} != directories {dirs}")

    commands, global_flags = load_reference()
    if not commands:
        err("reference", "no commands found: run scripts/generate-reference.sh")

    for name in dirs:
        skill = SKILLS / name / "SKILL.md"
        if not skill.exists():
            err(SKILLS / name, "missing SKILL.md")
            continue
        text = skill.read_text()
        fm = parse_frontmatter(text)
        if fm.get("name") != name:
            err(skill, f"frontmatter name {fm.get('name')!r} must equal the directory name")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
            err(skill, "name must be kebab-case, max 64 characters")
        desc = fm.get("description", "")
        if not desc or len(desc) > 1024:
            err(skill, f"description must be 1-1024 characters (has {len(desc)})")
        if text.count("\n") > 500:
            err(skill, "SKILL.md over 500 lines: move detail into separate files")
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
            if "://" in target:
                continue
            if not (skill.parent / target).exists():
                err(skill, f"broken link: {target}")
        for line in invocations(text):
            check_invocation(skill, line, commands, global_flags)

    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s)")
        return 1
    print(f"OK: {len(dirs)} skills, {len(commands)} cubecli commands in the reference")
    return 0


if __name__ == "__main__":
    sys.exit(main())
