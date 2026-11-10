import argparse
import csv
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Trích xuất yêu cầu người sử dụng từ file Markdown."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        type=Path,
        help="Đường dẫn file Markdown (bỏ trống để nhập sau khi chạy).",
    )
    args = parser.parse_args()

    input_md_file = args.input_file
    if input_md_file is None:
        input_md_file = Path(input("Nhập đường dẫn file Markdown: ").strip().strip('"'))
    if not input_md_file.is_file():
        parser.error(f"Không tìm thấy file: {input_md_file}")

    output_csv_file = "danh_sach_yeu_cau_nguoi_su_dung.csv"

    # 1. Đọc nội dung file Markdown
    content = input_md_file.read_text(encoding="utf-8-sig")

    # 2. Định vị khu vực bảng "Danh sách các yêu cầu của người sử dụng"
    start_pos = content.find("2. ## **Danh sách các yêu cầu của người sử dụng**")
    if start_pos != -1:
        content = content[start_pos:]

    # 3. Regex trích xuất từng dòng trong bảng Markdown
    line_pattern = re.compile(
        r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|$",
        re.MULTILINE,
    )
    matches = line_pattern.findall(content)

    # Dòng tiêu đề cột CSV theo đúng tutorial.md
    headers = [
        "STT",
        "Tên yêu cầu chức năng",
        "Mô tả yêu cầu chức năng",
        "Đối tượng sử dụng",
        "Ghi chú",
    ]
    valid_rows = []

    for match in matches:
        stt, req_name, req_desc, users, note = [column.strip() for column in match]

        # Bỏ qua dòng tiêu đề bảng và dòng phân cách | :---: | ----- |
        if stt.upper() in ["STT", ":---:", "---", ":---"] or "YÊU CẦU NGƯỜI SỬ DỤNG" in req_name:
            continue
        if set(stt).issubset({"-", ":", " "}):
            continue

        # Làm sạch ký tự Markdown (loại bỏ **in đậm**, gạch chéo escape, v.v.)
        req_name_clean = re.sub(r"\*\*(.*?)\*\*", r"\1", req_name)
        req_desc_clean = (
            re.sub(r"\*\*(.*?)\*\*", r"\1", req_desc)
            .replace("\\-", "-")
            .replace("\\+", "+")
        )
        users_clean = re.sub(r"\*\*(.*?)\*\*", r"\1", users).replace("\\-", "-")
        note_clean = re.sub(r"\*\*(.*?)\*\*", r"\1", note)

        valid_rows.append(
            [stt, req_name_clean, req_desc_clean, users_clean, note_clean]
        )

    # 4. Ghi dữ liệu ra file CSV/TSV
    # Dùng tab để tránh xung đột với dấu phẩy hoặc chấm phẩy trong mô tả.
    with open(output_csv_file, "w", encoding="utf-8-sig", newline="") as output:
        writer = csv.writer(output, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        writer.writerows(valid_rows)

    print(f"Đã trích xuất thành công {len(valid_rows)} dòng vào '{output_csv_file}'.")


if __name__ == "__main__":
    main()