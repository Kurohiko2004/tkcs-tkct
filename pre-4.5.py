"""Trích xuất thông tin chức năng PL 4.5 từ Markdown sang CSV."""

import argparse
import csv
import re
from pathlib import Path

delimiter = ";"
delimiter = "\t"

COLUMNS = [
    "STT",
    "Tên yêu cầu chức năng",
    "Mô tả yêu cầu chức năng",
    "Đối tượng sử dụng",
]
FUNCTION_HEADING = re.compile(
    r"^\s*#{2,6}\s+(?:\*\*)?(\d+)\\?\.\s+(.+?)(?:\*\*)?\s*$",
    re.MULTILINE,
)


def clean_text(value: str) -> str:
    value = value.replace("**", "")
    value = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|>&])", r"\1", value)
    return re.sub(r"\s+", " ", value).strip()


def extract_field(block: str, label: str) -> str:
    # Bỏ dấu ** nếu có trong nhãn để tìm kiếm linh hoạt
    pattern = re.compile(
        rf"\|\s*(?:\*\*)?{re.escape(label)}(?:\*\*)?\s*:\s*([^|]+)", re.IGNORECASE
    )
    match = pattern.search(block)
    if match:
        return clean_text(match.group(1))
    return ""

def convert_md_to_csv(input_file: Path) -> Path:
    content = input_file.read_text(encoding="utf-8-sig")
    headings = list(FUNCTION_HEADING.finditer(content))
    if not headings:
        raise ValueError("Không tìm thấy tiêu đề chức năng đánh số trong file.")

    rows = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(content)
        block = content[heading.end():end]
        function_description = extract_field(block, "Mô tả chức năng nghiệp vụ")
        actor = extract_field(block, "Tác nhân chính")
        if not function_description or not actor:
            raise ValueError(
                f"Chức năng {heading.group(1)} thiếu mô tả chức năng nghiệp vụ "
                "hoặc tác nhân chính."
            )
        rows.append([
            heading.group(1),
            clean_text(heading.group(2)),
            function_description,
            actor,
        ])

    output_file = input_file.with_suffix(".csv")
    with output_file.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.writer(output, delimiter=delimiter)
        writer.writerow(COLUMNS)
        writer.writerows(rows)
    print(f"Exported {len(rows)} rows: {ascii(str(output_file))}")
    return output_file


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", type=Path, help="Đường dẫn file Markdown.")
    input_file = parser.parse_args().input_file
    if not input_file.is_file():
        parser.error(f"Không tìm thấy file: {input_file}")
    try:
        convert_md_to_csv(input_file)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
