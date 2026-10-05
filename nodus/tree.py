from pathlib import Path
from rich.console import Console
from typing import TypedDict


console = Console()


class NodeTree(TypedDict):
    """Class that structures individual tree items displayed in the command-line interface (CLI)."""

    name: str
    value: Path | str | None


def find_paths(root: Path, filter_files: bool = True) -> set[Path]:
    """
    Global function that maps root directories to expand the structure on 
    the command line and allows filtering for directories only or including files.
    """

    found: set[Path] = {root.resolve()}

    try:
        for item in root.iterdir():
            if item.name.startswith((".", "$")):
                continue

            if item.is_dir():
                found.update(find_paths(item, filter_files))
            elif not filter_files and item.is_file():
                found.add(item.resolve())
    except PermissionError:
        pass
    except OSError as e:
        console.print(
            f"\n[red][-] Operating System Error:[/red] {e}")
    except Exception as e:
        console.print(
            f"\n[red][-] An Unexpected Error Occurred:[/red] {e}")

    return found


def build_tree(
        directory: Path,
        root: Path,
        expanded_paths: set[Path],
        prefix: str = "",
        last: bool = True,
        top: bool = True,
        filter_file: bool = True) -> list[NodeTree]:
    """
    Global function that renders the user directory as a tree structure
    in the command-line interface (CLI) in an interactive manner.
    """

    alternative: list[NodeTree] = []
    expanded = directory.resolve() in expanded_paths
    top = directory.resolve() == root.resolve()

    icon = "○" if expanded else "●"

    if top:
        label = f"{icon} {directory.name or directory}"
    else:
        branch = "└── " if last else "├── "
        label = f"{prefix}{branch}{icon} {directory.name}"

    alternative.append({"name": label, "value": directory})

    if expanded and directory.is_dir():
        try:

            # Filters items, ignoring hidden folders and files, and applies a filter for directories only when enabled:
            itens = [
                item
                for item in directory.iterdir()
                if not item.name.startswith((".", "$"))
                and (not filter_file or item.is_dir())]

            # Sorts the directories, organizing folders first and files afterwards:
            internal_itens = sorted(
                itens,
                key=lambda tipo: (not tipo.is_dir(), tipo.name.lower()))

            new_prefix = "" if top else prefix + \
                ("    " if last else "│   ")

            for i, item in enumerate(internal_itens):
                recente = i == len(internal_itens) - 1

                if item.is_dir():
                    alternative.extend(
                        build_tree(
                            directory=item,
                            root=root,
                            expanded_paths=expanded_paths,
                            prefix=new_prefix,
                            last=recente,
                            top=False,
                            filter_file=filter_file,))
                else:
                    bough = "└── " if recente else "├── "
                    file_label = f"{new_prefix}{bough}📄 {item.name}"
                    alternative.append({"name": file_label, "value": item})
        except PermissionError:
            alternative.append(
                {"name": f"{prefix}    Administrator permission required.", "value": None})
        except OSError as e:
            console.print(
                f"\n[red][-] Operating System Error:[/red] {e}")
        except Exception as e:
            console.print(
                f"\n[red][-] An Unexpected Error Occurred:[/red] {e}")

    return alternative
