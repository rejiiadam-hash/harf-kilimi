#!/usr/bin/env python3
"""Build dist/index.html by inlining a word list into src.html.

Usage: python3 build.py [words.json]
Default words file: ../words.json, falling back to sample_words.json.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLACEHOLDER = "/*WORDS_JSON*/null"
WORD_RE = re.compile(r"^[ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ]{3,7}$")


def pick_words_path(argv):
    if len(argv) > 1:
        return os.path.abspath(argv[1])
    default = os.path.join(HERE, "..", "words.json")
    if os.path.isfile(default):
        return os.path.abspath(default)
    print("note: ../words.json not found, using sample_words.json", file=sys.stderr)
    return os.path.join(HERE, "sample_words.json")


def main():
    wpath = pick_words_path(sys.argv)
    with open(wpath, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not isinstance(data.get("targets"), list):
        sys.exit(f"error: {wpath} has no 'targets' array")
    targets = [w for w in data.get("targets", []) if isinstance(w, str)]
    extra = [w for w in data.get("extra", []) if isinstance(w, str)]
    bad = [w for w in targets + extra if not WORD_RE.match(w)]
    if bad:
        print(f"warning: {len(bad)} words do not match the pattern and will be ignored, e.g. {bad[:5]}", file=sys.stderr)
    payload = {"lang": data.get("lang", "tr"), "version": data.get("version", 1),
               "targets": targets, "extra": extra}
    js = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    js = js.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")

    with open(os.path.join(HERE, "src.html"), encoding="utf-8") as f:
        src = f.read()
    if src.count(PLACEHOLDER) != 1:
        sys.exit("error: placeholder /*WORDS_JSON*/null must appear exactly once in src.html")
    out = src.replace(PLACEHOLDER, js)
    os.makedirs(os.path.join(HERE, "dist"), exist_ok=True)
    dst = os.path.join(HERE, "dist", "index.html")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"built {dst} from {wpath}: {len(targets)} targets, {len(extra)} extra, {len(out.encode('utf-8'))//1024} KB")


if __name__ == "__main__":
    main()
