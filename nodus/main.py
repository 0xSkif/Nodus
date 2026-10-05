from nodus.inputs import get_boolean
from nodus.managers import DirectoryManager, FileManager


def menu() -> None:
    directory_manager = DirectoryManager()
    directory_manager.configure_root()

    create_directories: bool = get_boolean(
        prompt="Do you want to create directories for the root?")

    if create_directories:
        directory_manager.configure_directory()

        create_subdirectories: bool = get_boolean(
            prompt="Do you want to create subdirectories for the root directories?")

        if create_subdirectories:
            directory_manager.configure_subdirectory()

    create_files: bool = get_boolean(prompt="\nDo you want to create files for the root?")

    if create_files:
        file_manager = FileManager(root=directory_manager.root)
        file_manager.configure_files()


if __name__ == "__main__":
    menu()