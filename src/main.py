from constants import CONTENT, HTML_TEMPLATE, PUBLIC, STATIC
from gen_content import copy_from_dir_to_dir, generate_pages


def main() -> None:
    copy_from_dir_to_dir(STATIC, PUBLIC)
    generate_pages(CONTENT, HTML_TEMPLATE, PUBLIC)


if __name__ == "__main__":
    main()
