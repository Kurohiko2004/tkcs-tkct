"""Kiểm tra yêu cầu của file CSV thứ nhất có trong file thứ hai bằng set."""

import argparse
import csv
import unicodedata
from pathlib import Path


def normalize(value):
    return unicodedata.normalize('NFC', value).strip().casefold()


def read_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as source:
        reader = csv.DictReader(source, delimiter=';')
        if not reader.fieldnames:
            raise ValueError(f'{path}: file không có tiêu đề cột.')
        keys = [normalize(name) for name in reader.fieldnames]
        if len(keys) != len(set(keys)):
            raise ValueError(f'{path}: tên cột bị trùng sau khi chuẩn hóa.')
        if 'yêu cầu người sử dụng' not in keys:
            raise ValueError(f'{path}: thiếu cột Yêu cầu người sử dụng.')
        rows = []
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'{path}: dòng CSV {reader.line_num} sai số cột.')
            record = {normalize(name): value for name, value in row.items()}
            value = record['yêu cầu người sử dụng']
            if not normalize(value):
                raise ValueError(f'{path}: yêu cầu trống tại dòng CSV {reader.line_num}.')
            rows.append((reader.line_num, value, row))
        return reader.fieldnames, rows


def compare_files(file1, file2):
    fieldnames1, rows1 = read_csv(file1)
    _, rows2 = read_csv(file2)
    values2 = {normalize(value) for _, value, _ in rows2}
    missing = 0
    output_file = Path(file1).with_name(f'{Path(file1).stem}_differences.txt')
    with output_file.open('w', encoding='utf-8-sig', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames1, delimiter=';')
        for line_number, value, row in rows1:
            exists = normalize(value) in values2
            status = 'CÓ TRONG FILE 2' if exists else 'KHÔNG CÓ TRONG FILE 2'
            print(f'Dòng CSV {line_number}: {status} | {value}')
            if not exists:
                writer.writerow(row)
                missing += 1

    print(f'\nSố dòng file 1: {len(rows1)}; file 2: {len(rows2)}')
    print(f'Số yêu cầu file 1 đã kiểm tra: {len(rows1)}')
    print(f'Có trong file 2: {len(rows1) - missing}; không có: {missing}')
    print(f'File chứa các dòng khác biệt: {output_file}')
    return len(rows1), missing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file1', type=Path, help='File CSV thứ nhất (phân tách bằng dấu ;).')
    parser.add_argument('file2', type=Path, help='File CSV thứ hai (phân tách bằng dấu ;).')
    args = parser.parse_args()
    try:
        compare_files(args.file1, args.file2)
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
