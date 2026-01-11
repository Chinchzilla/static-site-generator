from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parents[1].resolve()
STATIC = ROOT_DIR.joinpath("static").resolve()
PUBLIC = ROOT_DIR.joinpath("public").resolve()
CONTENT = ROOT_DIR.joinpath("content").resolve()
PUB_INDEX_HTML = PUBLIC.joinpath("index.html").resolve()
HTML_TEMPLATE = ROOT_DIR.joinpath("template.html").resolve()
