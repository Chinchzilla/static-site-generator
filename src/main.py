import sys

from constants import CONTENT, DOCS, HTML_TEMPLATE, STATIC
from gen_content import copy_from_dir_to_dir, generate_pages_recursive


def main() -> None:
    basepath: str = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_from_dir_to_dir(from_dir=STATIC, to_dir=DOCS)
    generate_pages_recursive(
        from_dir=CONTENT, template_path=HTML_TEMPLATE, to_dir=DOCS, basepath=basepath
    )


if __name__ == "__main__":
    main()
