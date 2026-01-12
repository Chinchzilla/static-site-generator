from pathlib import Path
from shutil import copy, rmtree

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html,
)


def copy_from_dir_to_dir(from_dir: Path, to_dir: Path) -> None:
    print("Copying files from", from_dir, "to", to_dir)
    if not from_dir.is_dir():
        raise ValueError(f"{from_dir.name}/ is not a directory")

    if to_dir.is_dir():
        print(f"Removing dir {to_dir.name}/")
        rmtree(to_dir)

    if not to_dir.exists():
        print(f"Creating dir {to_dir.name}/")
        to_dir.mkdir()

    for file in from_dir.iterdir():
        if file.is_file():
            print(f"Copying file {file.name} to {to_dir.name}/")
            _: Path | str = copy(file, to_dir)
        elif file.is_dir():
            print(f"Advancing to subdirectory {file.name}/")
            copy_from_dir_to_dir(file, to_dir.joinpath(file.name).resolve())


def generate_page(
    from_path: Path, template_path: Path, to_path: Path, basepath: str
) -> None:
    print(
        f"Generating page from {from_path.name} to {to_path.name} using {template_path.name}"
    )
    if not from_path.is_file():
        raise ValueError(f"{from_path.name} is not a file")

    with from_path.open("r") as from_file:
        from_content: str = from_file.read()

    with template_path.open("r") as template_file:
        template_content: str = template_file.read()

    page_title: str = extract_title(from_content).strip()
    page_content: str = markdown_to_html(from_content.strip()).to_html()

    html_from_template: str = (
        template_content.replace("{{ Title }}", page_title)
        .replace("{{ Content }}", page_content)
        .replace('href="/', f'href="{basepath}"')
        .replace('src="/', f'src="{basepath}"')
    )

    if not to_path.parent.is_dir():
        print(f"Creating dir {to_path.parent}")
        to_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Writing file {to_path.name}")
    with to_path.open("w") as to_file:
        _: int = to_file.write(html_from_template)


def generate_pages_recursive(
    from_dir: Path, template_path: Path, to_dir: Path, basepath: str
) -> None:
    print("Generating pages from", from_dir.name, "to", to_dir.name)
    for file in from_dir.iterdir():
        if file.suffix == ".md":
            print("Found '.md' file to be converted", file.name)
            generate_page(
                file, template_path, to_dir.joinpath(file.stem + ".html"), basepath
            )
        elif file.is_dir():
            print("Found directory, recursing into it", file.name)
            generate_pages_recursive(
                file, template_path, to_dir.joinpath(file.name), basepath
            )


def extract_title(markdown: str) -> str:
    for block in markdown_to_blocks(markdown):
        if block_to_block_type(block) == BlockType.HEADING and block.strip().startswith(
            "# "
        ):
            return block[2:].strip()
    raise ValueError("No title found")
