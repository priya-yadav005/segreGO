

from pathlib import Path
import tokenize
import io
import re
import sys

ROOT = Path(r"e:/projects/segrego")
EXTS = {'.py', '.html', '.htm', '.css', '.js'}

html_comment_re = re.compile(r"<!--.*?-->", re.DOTALL)
django_tag_re = re.compile(r"\{
block_comment_re = re.compile(r"/\*.*?\*/", re.DOTALL)

changed_files = []

def strip_python_comments(text: str) -> str:
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))

        filtered = [t for t in tokens if t.type != tokenize.COMMENT]
        return tokenize.untokenize(filtered)
    except Exception:
        return text

def strip_html_comments(text: str) -> str:
    text = django_tag_re.sub('', text)
    text = html_comment_re.sub('', text)
    return text

def strip_css_js_comments(text: str) -> str:

    text = block_comment_re.sub('', text)

    text = re.sub(r'(^|\s)//.*$', lambda m: m.group(1), text, flags=re.MULTILINE)
    return text

for path in ROOT.rglob('*'):
    if path.suffix.lower() in EXTS and path.is_file():
        try:
            text = path.read_text(encoding='utf-8')
        except Exception:
            try:
                text = path.read_text(encoding='latin-1')
            except Exception:
                print(f"Skipping binary or unreadable file: {path}")
                continue

        new_text = text
        if path.suffix.lower() == '.py':
            new_text = strip_python_comments(text)
        elif path.suffix.lower() in ('.html', '.htm'):
            new_text = strip_html_comments(text)
        elif path.suffix.lower() in ('.css', '.js'):
            new_text = strip_css_js_comments(text)

        if new_text != text:
            bak = path.with_suffix(path.suffix + '.bak')
            bak.write_text(text, encoding='utf-8')
            path.write_text(new_text, encoding='utf-8')
            changed_files.append(str(path.relative_to(ROOT)))

if changed_files:
    print('Modified files:')
    for f in changed_files:
        print(' -', f)
else:
    print('No changes made.')

print('\nBackups saved as filename + .bak in same folders.')
