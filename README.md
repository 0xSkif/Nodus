![Nodus Logo](<docs/Nodus Logo - ENG.jpeg>)

**Brazilian Version:** [README em Português](<docs/README PT-BR.md>)

## 1. About

Nodus is a lightweight, interactive Command Line Interface (CLI) tool developed in Python to automate the bulk creation, navigation, and management of directories and files.

With native support for **Windows, Linux, and macOS**, Nodus was designed to speed up the setup of development environments, study directory structures, and project organization with minimal commands.

### 1.1 Features

- **Interactive Navigation:** Dynamic tree view of your directory structure.
- **Bulk Operations:** Create multiple files and folders using standard or custom naming patterns in a single session
- **Cross-Platform:** Native and automatic support for Windows, Linux, and macOS without requiring system tweaks.
- **Portable & Efficient:** Lightweight execution with minimal system resource consumption.

## 2. Architecture & How It Works

Nodus is built on a modular architecture guided by the **Single Responsibility Principle (SRP)**, divided into three main pillars: User Interface (CLI), recursive navigation, and File System Input/Output (I/O) management.

### 2.1 Technologies & Dependencies

- **[Python 3.10+](https://www.python.org/):** Core programming language.
- **[Rich](https://github.com/Textualize/rich):** Terminal formatting, panels, and tree structure rendering.
- **`InquirerPy:`** Interactive CLI menus and prompt selection.
- **Native Modules:**
    - **`pathlib`:** Robust, cross-platform file path manipulation.
    - **`platform`:** Operating system detection.
    - **`typing`:** Static typing support for source code logic.

## 3. Installation & Usage

**Nodus** can be executed in two ways:

- Installing the **portable executable** (does not require Python).
- Running from the **source code** manually (requires Python installed).

### 3.1 Portable Executable

1. Go to the [Releases](https://github.com/0xSkif/nodus/releases) tab in this repository.
2. Download the `nodus.exe` file or the executable binary for your operating system.
3. Open your terminal in the download folder and run:

    ```powershell
    .\nodus.exe
    ```

### 3.2 Source Code

1. Clone the repository:

    ```bash
    git clone https://github.com/0xSkif/nodus.git
    cd nodus
    ```
2. Install the dependencies and editable package:
    ```bash
    pip install -e .
    ```
3. Run the global command:
    ```bash
    nodus
    ```
