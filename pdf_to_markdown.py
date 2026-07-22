import argparse
from pathlib import Path
from markitdown import MarkItDown


def convert_pdf(input_file, output_file=None):
    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_file}")

    converter = MarkItDown()
    result = converter.convert(str(input_path))

    output_path = (
        Path(output_file)
        if output_file
        else input_path.with_suffix(".md")
    )

    output_path.write_text(
        result.text_content,
        encoding="utf-8"
    )

    print(f"Converted: {input_path.name} → {output_path}")


def convert_folder(input_folder, output_folder):
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    if not input_path.exists():
        raise FileNotFoundError(f"Folder not found: {input_folder}")

    output_path.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_path.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    converter = MarkItDown()

    for pdf_file in pdf_files:
        result = converter.convert(str(pdf_file))

        markdown_file = output_path / f"{pdf_file.stem}.md"

        markdown_file.write_text(
            result.text_content,
            encoding="utf-8"
        )

        print(f"Converted: {pdf_file.name} → {markdown_file.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert PDF files to Markdown"
    )

    parser.add_argument(
        "input",
        help="Path to a PDF file or folder containing PDF files"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output Markdown file for single PDF conversion"
    )

    parser.add_argument(
        "--output-dir",
        help="Output folder for batch conversion"
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    try:
        if input_path.is_dir():
            if not args.output_dir:
                print("Please provide --output-dir for batch conversion.")
            else:
                convert_folder(
                    args.input,
                    args.output_dir
                )
        else:
            convert_pdf(
                args.input,
                args.output
            )

    except Exception as error:
        print(f"Error: {error}")