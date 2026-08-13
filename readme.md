# LaTeX to PDF Converter

A simple Python script that converts a `.tex` LaTeX file into a `.pdf` by calling `pdflatex`.

## Requirements

You need:

* Python 3.10+
* A LaTeX distribution that provides `pdflatex`
* Any LaTeX packages required by your `.tex` document

The Python script uses the standard library `subprocess` module, so no additional Python packages are required.

> Do **not** use `pip install pdflatex` for this project. That installs a Python package with the same name, not the actual `pdflatex` compiler.

---

## Project Structure

```text
latex-to-pdf/
├── tex_to_pdf.py
├── resume.tex
└── README.md
```

---

# Windows Setup

## 1. Install Python

Install Python from the official Python distribution or through your preferred package manager.

Verify the installation:

```powershell
python --version
```

or:

```powershell
py --version
```

---

## 2. Install MiKTeX

On Windows, the recommended LaTeX distribution is **MiKTeX**.

After installation, verify that `pdflatex` is available:

```powershell
pdflatex --version
```

You should see output similar to:

```text
MiKTeX-pdfTeX ...
```

---

## 3. Fix the PATH if `pdflatex` is not recognized

If you see:

```text
pdflatex: The term 'pdflatex' is not recognized...
```

find the MiKTeX installation directory.

A typical location is:

```text
C:\Users\<USERNAME>\AppData\Local\Programs\MiKTeX\miktex\bin\x64
```

For example:

```text
C:\Users\Rayma\AppData\Local\Programs\MiKTeX\miktex\bin\x64
```

Temporarily add it to the current PowerShell session:

```powershell
$env:Path += ";C:\Users\<USERNAME>\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
```

Then test:

```powershell
pdflatex --version
```

You can also check whether PowerShell can locate it:

```powershell
Get-Command pdflatex
```

### Important

Add the **directory containing `pdflatex.exe`**, not the executable itself.

Correct:

```text
C:\Users\<USERNAME>\AppData\Local\Programs\MiKTeX\miktex\bin\x64
```

Incorrect:

```text
C:\Users\<USERNAME>\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe
```

If you installed MiKTeX while VS Code was already open, completely restart VS Code so its integrated terminal receives the updated environment variables.

---

## 4. Configure automatic LaTeX package installation

LaTeX documents often depend on additional packages.

For example, a document may contain:

```latex
\usepackage{marvosym}
```

If MiKTeX reports:

```text
The required file could not be found: marvosym.sty
```

open **MiKTeX Console**, search for:

```text
marvosym
```

and install the package.

Alternatively, enable automatic package installation in MiKTeX Console under the package installation settings.

You can also install some packages from PowerShell:

```powershell
mpm --install=marvosym
```

---

# Linux Setup

The exact installation command depends on your Linux distribution.

## Ubuntu / Debian

Update the package list:

```bash
sudo apt update
```

Install a basic LaTeX environment:

```bash
sudo apt install texlive-latex-base
```

For documents that use a wider range of packages, install:

```bash
sudo apt install texlive-latex-extra
```

A more complete installation is:

```bash
sudo apt install texlive-full
```

`texlive-full` is very large, so it is usually unnecessary unless you regularly work with many different LaTeX templates.

Verify the installation:

```bash
pdflatex --version
```

---

## Fedora

Install LaTeX with:

```bash
sudo dnf install texlive-scheme-basic
```

For a broader collection of packages, you may need additional TeX Live packages depending on your document.

Verify:

```bash
pdflatex --version
```

---

## Arch Linux

Install TeX Live:

```bash
sudo pacman -S texlive-basic
```

Additional LaTeX package groups may be required depending on the document.

Verify:

```bash
pdflatex --version
```

---

# Running the Converter

Given:

```text
latex-to-pdf/
├── tex_to_pdf.py
└── resume.tex
```

run:

## Windows

```powershell
python .\tex_to_pdf.py .\resume.tex
```

## Linux

```bash
python3 tex_to_pdf.py resume.tex
```

The resulting PDF will normally be created beside the `.tex` file:

```text
latex-to-pdf/
├── tex_to_pdf.py
├── resume.tex
├── resume.pdf
├── resume.aux
└── resume.log
```

LaTeX generates several helper files during compilation, including `.aux` and `.log` files. These are normal.

---

# Custom Output Directory

The script can optionally accept an output directory.

## Windows

```powershell
python .\tex_to_pdf.py .\resume.tex .\output
```

## Linux

```bash
python3 tex_to_pdf.py resume.tex output
```

This will create:

```text
output/
└── resume.pdf
```

> The second argument is an **output directory**, not a PDF filename.

For example, this is incorrect:

```powershell
python .\tex_to_pdf.py .\resume.tex resume.pdf
```

because the script will interpret `resume.pdf` as a directory.

Use:

```powershell
python .\tex_to_pdf.py .\resume.tex
```

if you simply want `resume.pdf`.

---

# Python Script

`tex_to_pdf.py`:

```python
import subprocess
from pathlib import Path
import sys


def tex_to_pdf(tex_file: str, output_dir: str | None = None) -> Path:
    """
    Compile a .tex file into a PDF using pdflatex.

    Args:
        tex_file: Path to the input .tex file.
        output_dir: Optional directory where the PDF should be created.

    Returns:
        Path to the generated PDF.
    """

    tex_path = Path(tex_file).resolve()

    if not tex_path.exists():
        raise FileNotFoundError(f"TeX file not found: {tex_path}")

    if tex_path.suffix.lower() != ".tex":
        raise ValueError("Input file must have a .tex extension.")

    if output_dir is None:
        output_path = tex_path.parent
    else:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)

    command = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-output-directory={output_path}",
        str(tex_path),
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

    except FileNotFoundError:
        raise FileNotFoundError(
            "pdflatex was not found. Install MiKTeX or TeX Live "
            "and make sure pdflatex is available in PATH."
        )

    if result.returncode != 0:
        raise RuntimeError(
            "LaTeX compilation failed.\n\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )

    pdf_path = output_path / f"{tex_path.stem}.pdf"

    if not pdf_path.exists():
        raise RuntimeError("pdflatex completed but no PDF was created.")

    return pdf_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tex_to_pdf.py input.tex")
        print("  python tex_to_pdf.py input.tex output_directory")
        sys.exit(1)

    tex_file = sys.argv[1]

    output_dir = None
    if len(sys.argv) >= 3:
        output_dir = sys.argv[2]

    try:
        pdf = tex_to_pdf(tex_file, output_dir)
        print(f"PDF successfully created: {pdf}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
```

---

# Troubleshooting

## `pdflatex` is not recognized

Windows:

```powershell
pdflatex --version
```

If it fails, make sure the MiKTeX `bin\x64` directory is in your `PATH`.

Linux:

```bash
which pdflatex
```

If no path is returned, install TeX Live.

---

## Missing `.sty` file

Example:

```text
LaTeX Error: File `marvosym.sty' not found.
```

This means your document depends on a LaTeX package that is not installed.

On MiKTeX, install the corresponding package through **MiKTeX Console**.

On Ubuntu/Debian, many commonly used packages are included with:

```bash
sudo apt install texlive-latex-extra
```

---

## Check where `pdflatex` is installed

### Windows Command Prompt

```cmd
where pdflatex
```

### Windows PowerShell

```powershell
Get-Command pdflatex
```

### Linux

```bash
which pdflatex
```

---

## Virtual environments

Python virtual environments do not contain `pdflatex`.

For example:

```text
(.venv) PS C:\project>
```

only indicates that a particular Python environment is active.

`pdflatex` is a separate system executable and must still be installed through MiKTeX, TeX Live, or another LaTeX distribution.

---

# How It Works

The Python script executes a command equivalent to:

```bash
pdflatex resume.tex
```

using Python's `subprocess` module.

Internally:

```python
subprocess.run([
    "pdflatex",
    "-interaction=nonstopmode",
    "-halt-on-error",
    "resume.tex",
])
```

The operating system searches its `PATH` for the `pdflatex` executable.

The options mean:

```text
-interaction=nonstopmode
```

Continue compilation without waiting for interactive input.

```text
-halt-on-error
```

Stop compilation when a serious LaTeX error occurs.

The Python script checks the process return code and reports an error if compilation fails.

---

# Notes

Some LaTeX documents need to be compiled more than once to correctly generate:

* Cross-references
* Table of contents entries
* Page references
* Bibliographies
* Citation references

For simple documents such as resumes, one compilation is often enough. More complex documents may require multiple `pdflatex` passes or tools such as `bibtex` or `biber`.
