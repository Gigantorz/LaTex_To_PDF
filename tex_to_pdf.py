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

    Raises:
        FileNotFoundError: If the .tex file or pdflatex cannot be found.
        RuntimeError: If pdflatex compilation fails.
    """

    tex_path = Path(tex_file).resolve()

    if not tex_path.exists():
        raise FileNotFoundError(f"TeX file not found: {tex_path}")

    if tex_path.suffix.lower() != ".tex":
        raise ValueError("Input file must have a .tex extension.")

    # By default, place the PDF beside the .tex file.
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
            "pdflatex was not found. Make sure a LaTeX distribution "
            "such as MiKTeX or TeX Live is installed and pdflatex is in PATH."
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