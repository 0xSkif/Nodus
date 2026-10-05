import platform
from pathlib import Path
from rich.console import Console
from typing import Any
from nodus.inputs import (
    get_boolean,
    get_number,
    get_single_option,
    get_text
)
from nodus.tree import build_tree, find_paths


console = Console()


def select_directory(root: Path) -> Path:
    expanded_paths: set[Path] = find_paths(root)

    while True:
        options = build_tree(
            directory=root,
            root=root,
            expanded_paths=expanded_paths)

        alternative: Any = get_single_option(
            prompt="\nNavigate to the desired directory:", options=options)

        if isinstance(alternative, Path):
            return alternative


class DirectoryManager:
    """Class that manages directory creation, navigation, and structure."""

    def __init__(self, root: Path | None = None) -> None:
        """Function that initializes the manager and sets the root directory."""

        self.root: Path = root or self.default_root()

    def default_root(self) -> Path:
        """Function that returns the operating system's default folder; otherwise, uses a folder chosen/created by the user."""

        default_directory: Path = Path.home()

        if platform.system() == "Windows":
            onedrive: Path = default_directory / "OneDrive"

            if onedrive.exists():
                return onedrive

        return default_directory

    def configure_root(self) -> Path:
        """Function that prompts for root directory configuration and folder management."""

        options: list[dict[str, Any]] = [
            {"name": "    1. Select a root directory.", "value": "1"},
            {"name": "    2. Create a new root directory.", "value": "2"},
            {"name": "    3. Create a quick path.", "value": "3"},
        ]

        alternative = get_single_option(
            prompt="Select an option:", options=options)

        if alternative == "1":
            self.root = select_directory(self.root)
        elif alternative == "2":
            self.root = self.single_directory(self.root)
        else:
            path_text: str = get_text(prompt="\nEnter the new path:")
            new_path: Path = self.root / path_text

            try:
                new_path.mkdir(parents=True, exist_ok=True)
                console.print(
                    "\n[green][+] Path created successfully![/green]")
                self.root = new_path
            except PermissionError as e:
                console.print(f"\n[red][-] Permission Error:[/red] {e}")
            except OSError as e:
                console.print(
                    f"\n[red][-] Operating System Error:[/red] {e}")
            except Exception as e:
                console.print(
                    f"\n[red][-] An unexpected error occurred:[/red] {e}")

        return self.root

    def configure_directory(self, root: Path | None = None) -> list[Path]:
        """
        Function that prompts the user for the number of directories to be created 
        in the root directory.
        """

        target: Path = root or self.root

        if not target.exists():
            console.print(
                "\n[red][-] Directory does not exist or was not found.[/red]")
            return []

        number: int = get_number(
            prompt="\nEnter the number of folders to be created:")

        if number <= 0:
            return []

        if number == 1:
            return [self.single_directory(target)]
        else:
            return self.multiple_directories(target, number)

    def single_directory(self, root: Path) -> Path:
        """Function that creates only one directory per session in the root directory."""

        while True:
            name: str = get_text(
                prompt="\nEnter the name of the new directory:")
            sanitized_name = Path(name).name

            if not sanitized_name:
                console.print(
                    "\n[yellow][!] Invalid directory name![/yellow]")
                continue

            directory = root / sanitized_name

            try:
                directory.mkdir(parents=False, exist_ok=True)
                console.print(
                    "\n[green][+] Directory created successfully![/green]")
                return directory
            except PermissionError as e:
                console.print(f"\n[red][-] Permission Error:[/red] {e}")
                continue
            except OSError as e:
                console.print(
                    f"\n[red][-] Operating System Error:[/red] {e}")
                continue
            except Exception as e:
                console.print(
                    f"\n[red][-] An unexpected error occurred:[/red] {e}")
                continue

    def multiple_directories(self, directory: Path, counter: int) -> list[Path]:
        """
        Function that creates several directories per session in
        the root directory with default or custom names.
        """

        options: list[Any] = [
            {"name": "Use default naming.", "value": "1"},
            {"name": "Create custom names.", "value": "2"}]

        alternative: str = get_single_option(
            prompt="\nSelect an option:", options=options)
        directory_list: list[Path] = []

        if alternative == "1":
            while True:
                try:
                    for i in range(1, counter + 1):
                        target = directory / f"Untitled {i}"
                        target.mkdir(exist_ok=True)
                        directory_list.append(target)

                    console.print(
                        "\n[green][+] Directories were created successfully![/green]")
                    break
                except PermissionError as e:
                    console.print(
                        f"\n[red][-] Permission Error:[/red] {e}")
                    continue
                except OSError as e:
                    console.print(
                        f"\n[red][-] Operating System Error:[/red] {e}")
                    continue
                except Exception as e:
                    console.print(
                        f"\n[red][-] An unexpected error occurred:[/red] {e}")
                    continue
        else:
            while True:
                try:
                    names: str = get_text(
                        prompt=f"\nEnter the names of {counter} directories separated by commas:")
                    names_list = [
                        name.strip() for name in names.split(",") if name.strip()]

                    if len(names_list) != counter:
                        console.print(
                            f"\n[yellow][!] You provided {len(names_list)}, but {counter} were expected. Try again. [/yellow]")
                        continue

                    for folder in names_list:
                        target = directory / Path(folder).name
                        target.mkdir(exist_ok=True)
                        directory_list.append(target)

                    console.print(
                        "\n[green][+] Directories were created successfully![/green]")
                    break
                except PermissionError as e:
                    console.print(
                        f"\n[red][-] Permission Error:[/red] {e}")
                    continue
                except OSError as e:
                    console.print(
                        f"\n[red][-] Operating System Error:[/red] {e}")
                    continue
                except Exception as e:
                    console.print(
                        f"\n[red][-] An unexpected error occurred:[/red] {e}")
                    continue

        return directory_list

    def configure_subdirectory(self) -> None:
        """
        Function that prompts the user for the number of subdirectories to be created
        in the root directory or in other directories.
        """

        while True:
            console.print(
                "\nNavigate to the directory where you want to create subdirectories:")
            
            selected: Path = select_directory(self.root)

            if not selected:
                console.print(
                    "\n[yellow][!] No directory selected![/yellow]")
            else:
                console.print(
                    f"\n[green][+] Configuring directory: {selected.name}[/green]")

                counter: int = get_number(
                    prompt=f"\nEnter the number of subdirectories to be created in {selected.name}:")

                if counter == 1:
                    self.single_subdirectory(selected)
                elif counter > 1:
                    self.multiple_subfolders(selected, counter)

            choice: bool = get_boolean(
                prompt="\nDo you want to select more directories?")

            if not choice:
                break

    def single_subdirectory(self, root: Path) -> Path:
        """
        Function that creates only one subdirectory per session in the
        root directory or other directories.
        """

        while True:
            name: str = get_text(
                prompt="\nEnter the name of the new subdirectory:")
            sanitized_name = Path(name).name

            if not sanitized_name:
                console.print(
                    "\n[yellow][!] Invalid subdirectory name![/yellow]")
                continue

            directory = root / sanitized_name

            try:
                directory.mkdir(parents=False, exist_ok=True)
                console.print(
                    "\n[green][+] Subdirectory created successfully![/green]")
                return directory
            except PermissionError as e:
                console.print(f"\n[red][-] Permission Error:[/red] {e}")
                continue
            except OSError as e:
                console.print(
                    f"\n[red][-] Operating System Error:[/red] {e}")
                continue
            except Exception as e:
                console.print(
                    f"\n[red][-] An unexpected error occurred:[/red] {e}")
                continue

    def multiple_subfolders(self, directory: Path, counter: int) -> list[Path]:
        """
        Function that creates several subdirectories per session in the root directory or
        other directories with default or custom names.
        """

        options: list[Any] = [
            {"name": "Use default naming.", "value": "1"},
            {"name": "Create custom names.", "value": "2"}]

        alternative: str = get_single_option(
            prompt="\nSelect an option:", options=options)
        subdirectory_list: list[Path] = []

        if alternative == "1":
            while True:
                try:
                    for i in range(1, counter + 1):
                        target = directory / f"Untitled {i}"
                        target.mkdir(exist_ok=True)
                        subdirectory_list.append(target)

                    console.print(
                        "\n[green][+] Subdirectories were created successfully![/green]")
                    break
                except PermissionError as e:
                    console.print(
                        f"\n[red][-] Permission Error:[/red] {e}")
                    continue
                except OSError as e:
                    console.print(
                        f"\n[red][-] Operating System Error:[/red] {e}")
                    continue
                except Exception as e:
                    console.print(
                        f"\n[red][-] An unexpected error occurred:[/red] {e}")
                    continue
        else:
            while True:
                try:
                    names: str = get_text(
                        prompt=f"\nEnter the names of {counter} subdirectories separated by commas:")
                    names_list = [
                        name.strip() for name in names.split(",") if name.strip()]

                    if len(names_list) != counter:
                        console.print(
                            f"\n[yellow][!] You provided {len(names_list)}, but {counter} were expected. Try again. [/yellow]")
                        continue

                    for subdirectory in names_list:
                        target = directory / Path(subdirectory).name
                        target.mkdir(exist_ok=True)
                        subdirectory_list.append(target)

                    console.print(
                        "\n[green][+] Subdirectories were created successfully![/green]")
                    break
                except PermissionError as e:
                    console.print(
                        f"\n[red][-] Permission Error:[/red] {e}")
                    continue
                except OSError as e:
                    console.print(
                        f"\n[red][-] Operating System Error:[/red] {e}")
                    continue
                except Exception as e:
                    console.print(
                        f"\n[red][-] An unexpected error occurred:[/red] {e}")
                    continue

        return subdirectory_list


class FileManager:
    """Class that manages file creation and manipulation."""

    def __init__(self, root: Path | None = None) -> None:
        """Function that initializes the manager with a linked or default root."""

        self.root: Path = root or Path.home()

    def configure_files(self) -> None:
        """Function that prompts the user for the number of files to be created in the
        root directory or other directories."""

        while True:
            console.print(
                "\nNavigate to the directory where you want to create files:")
            target: Path = select_directory(self.root)

            if not target or not target.exists():
                console.print(
                    "\n[yellow][!] Invalid or non-existent directory![/yellow]")
            else:
                counter: int = get_number(
                    prompt=f"\nEnter the amount of files to be created in {target.name}:")

                if counter == 1:
                    self.single_file(target)
                elif counter > 1:
                    self.multiple_files(target, counter)

            choice: bool = get_boolean(
                prompt="\nDo you want to create files in other directories?")

            if not choice:
                break

    def single_file(self, directory: Path) -> Path | None:
        """Function that creates only one file per session in the root directory or other directories."""

        while True:
            name: str = get_text(
                prompt="\nEnter the file name (include extension):")
            sanitized_name = Path(name).name

            if not sanitized_name:
                console.print(
                    "\n[yellow][!] Invalid file name![/yellow]")
                continue

            target = directory / sanitized_name

            try:
                target.touch(exist_ok=True)
                console.print(
                    "\n[green][+] File created successfully![/green]")

                return target
            except PermissionError as e:
                console.print(f"\n[red][-] Permission Error:[/red] {e}")
                continue
            except OSError as e:
                console.print(
                    f"\n[red][-] Operating System Error:[/red] {e}")
                continue
            except Exception as e:
                console.print(
                    f"\n[red][-] An unexpected error occurred:[/red] {e}")
                continue

    def multiple_files(self, target: Path, counter: int) -> list[Path]:
        """
        Function that creates several files per session in the
        root directory with default or custom names.
        """

        options: list[Any] = [
            {"name": "Use default naming.", "value": "1"},
            {"name": "Create custom names.", "value": "2"}]

        alternative: str = get_single_option(
            prompt="\nSelect an option:", options=options)
        file_list: list[Path] = []

        if alternative == "1":
            while True:
                try:
                    extension: str = get_text(
                        prompt="\nEnter the file extension:").lstrip(".")

                    formatted_extension = f".{extension}" if extension else ".txt"

                    for i in range(1, counter + 1):
                        file_path = target / \
                            f"Untitled {i}{formatted_extension}"
                        file_path.touch(exist_ok=True)
                        file_list.append(file_path)

                    console.print(
                        "\n[green][+] Files created successfully![/green]")
                    break
                except PermissionError as e:
                    console.print(
                        f"\n[red][-] Permission Error:[/red] {e}")
                    continue
                except OSError as e:
                    console.print(
                        f"\n[red][-] Operating System Error:[/red] {e}")
                    continue
                except Exception as e:
                    console.print(
                        f"\n[red][-] An unexpected error occurred:[/red] {e}")
                    continue
        else:
            while True:
                try:
                    names: str = get_text(
                        prompt=f"\nEnter the names of {counter} files (with extension) separated by commas:")
                    names_list = [
                        name.strip() for name in names.split(",") if name.strip()]

                    if len(names_list) != counter:
                        console.print(
                            f"\n[yellow][!] You provided {len(names_list)} names, but {counter} were expected. Try again.[/yellow]")
                        continue

                    for item in names_list:
                        file_path = target / Path(item).name
                        file_path.touch(exist_ok=True)
                        file_list.append(file_path)

                    console.print(
                        "\n[green][+] Files created successfully![/green]")
                    break
                except PermissionError as e:
                    console.print(
                        f"\n[red][-] Permission Error:[/red] {e}")
                    continue
                except OSError as e:
                    console.print(
                        f"\n[red][-] Operating System Error:[/red] {e}")
                    continue
                except Exception as e:
                    console.print(
                        f"\n[red][-] An unexpected error occurred:[/red] {e}")
                    continue

        return file_list