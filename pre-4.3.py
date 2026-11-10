import argparse
import io
from pathlib import Path

import pandas as pd


def convert_md_table_to_csv(input_file: Path) -> Path:
    content = input_file.read_text(encoding="utf-8-sig")
    table_lines = [
        line for line in content.splitlines()
        if line.strip().startswith("|")
    ]
    if not table_lines:
        raise ValueError("Không tìm thấy bảng Markdown trong file.")

    df = pd.read_csv(
        io.StringIO("\n".join(table_lines)),
        sep="|",
        engine="python",
        skipinitialspace=True,
    )
    df = df.dropna(how="all", axis=1).iloc[:, :2]
    if len(df.columns) != 2:
        raise ValueError("Bảng PL 4.3 cần có ít nhất hai cột.")
    df.columns = ["STT", "Tên yêu cầu chức năng"]

    for column in df.columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.replace(r"\*\*(.*?)\*\*", r"\1", regex=True)
            .str.replace(r"\\-", "-", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    df = df[
        df["STT"].str.fullmatch(r"\d+", na=False)
        & df["Tên yêu cầu chức năng"].ne("")
    ]
    output_file = input_file.with_suffix(".csv")
    df.to_csv(output_file, sep=";", index=False, encoding="utf-8-sig")
    print(f"Exported CSV: {ascii(str(output_file))}")
    return output_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chuyển bảng yêu cầu chức năng PL 4.3 từ Markdown sang CSV."
    )
    parser.add_argument("input_file", type=Path, help="Đường dẫn file Markdown.")
    input_file = parser.parse_args().input_file
    if not input_file.is_file():
        parser.error(f"Không tìm thấy file: {input_file}")
    try:
        convert_md_table_to_csv(input_file)
    except (OSError, ValueError, pd.errors.ParserError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
