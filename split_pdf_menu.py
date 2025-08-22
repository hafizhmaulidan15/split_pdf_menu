#!/usr/bin/env python3
"""
Split PDF (Interactive Menu) v2
--------------------------------
Opsi:
  1) Ambil 1 halaman
  2) Ambil rentang halaman
  3) Ambil multi-seleksi (1,3,5-7,12)
  4) Ambil 1 halaman + sisanya (2 file)
  5) Pisah SEMUA halaman jadi file terpisah

Semua input halaman bersifat 1-indexed.

Dependencies:
    pip install PyPDF2
Usage:
    python split_pdf_menu_v2.py
"""

import sys
import re
from pathlib import Path

# Prefer PyPDF2, fallback to pypdf
try:
    from PyPDF2 import PdfReader, PdfWriter
except Exception:  # pragma: no cover
    from pypdf import PdfReader, PdfWriter  # type: ignore


def parse_multi_selection(s: str) -> list[int]:
    s = s.replace(" ", "")
    if not s:
        raise ValueError("Input kosong.")
    result: set[int] = set()
    for part in s.split(","):
        if not part:
            continue
        if "-" in part:
            m = re.fullmatch(r"(\d+)-(\d+)", part)
            if not m:
                raise ValueError(f"Rentang tidak valid: {part}")
            start, end = int(m.group(1)), int(m.group(2))
            if start <= 0 or end <= 0 or end < start:
                raise ValueError(f"Rentang tidak valid: {part}")
            for p in range(start, end + 1):
                result.add(p)
        else:
            if not part.isdigit():
                raise ValueError(f"Nomor halaman tidak valid: {part}")
            page = int(part)
            if page <= 0:
                raise ValueError(f"Nomor halaman tidak valid: {part}")
            result.add(page)
    return sorted(result)


def clamp_pages(pages: list[int], total_pages: int) -> list[int]:
    return [p for p in pages if 1 <= p <= total_pages]


def ensure_writer_contains(writer: PdfWriter, filename: str) -> None:
    if len(writer.pages) == 0:
        raise RuntimeError(f"Tidak ada halaman yang ditulis untuk {filename}.")


def safe_write(writer: PdfWriter, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as f:
        writer.write(f)


def extract_single(reader: PdfReader, page: int, out_prefix: str) -> Path:
    writer = PdfWriter()
    writer.add_page(reader.pages[page - 1])
    out = Path(f"{out_prefix}_hal_{page:02d}.pdf")
    ensure_writer_contains(writer, str(out))
    safe_write(writer, out)
    return out


def extract_range(reader: PdfReader, start: int, end: int, out_prefix: str) -> Path:
    writer = PdfWriter()
    for p in range(start, end + 1):
        writer.add_page(reader.pages[p - 1])
    out = Path(f"{out_prefix}_hal_{start:02d}-{end:02d}.pdf")
    ensure_writer_contains(writer, str(out))
    safe_write(writer, out)
    return out


def extract_multi(reader: PdfReader, pages: list[int], out_prefix: str) -> Path:
    writer = PdfWriter()
    for p in pages:
        writer.add_page(reader.pages[p - 1])
    out = Path(f"{out_prefix}_multi_{len(pages)}hal.pdf")
    ensure_writer_contains(writer, str(out))
    safe_write(writer, out)
    return out


def extract_single_and_rest(reader: PdfReader, pick: int, out_prefix: str) -> tuple[Path, Path]:
    total = len(reader.pages)
    picked = extract_single(reader, pick, out_prefix)
    rest_writer = PdfWriter()
    for i in range(1, total + 1):
        if i != pick:
            rest_writer.add_page(reader.pages[i - 1])
    rest_path = Path(f"{out_prefix}_sisa_tanpa_{pick:02d}.pdf")
    ensure_writer_contains(rest_writer, str(rest_path))
    safe_write(rest_writer, rest_path)
    return picked, rest_path


def split_all_pages(reader: PdfReader, out_prefix: str) -> list[Path]:
    paths: list[Path] = []
    total = len(reader.pages)
    for i in range(1, total + 1):
        paths.append(extract_single(reader, i, out_prefix))
    return paths


def confirm(prompt: str) -> bool:
    ans = input(f"{prompt} [y/N]: ").strip().lower()
    return ans in ("y", "yes")


def main() -> int:
    print("=== Split PDF (Menu) v2 ===")
    pdf_path = input("Path PDF sumber: ").strip().strip('"').strip("'")
    if not pdf_path:
        print("❌ Path PDF kosong.")
        return 1

    src = Path(pdf_path)
    if not src.exists():
        print(f"❌ File tidak ditemukan: {src}")
        return 1

    out_prefix = input("Prefix nama file output (default: 'hasil'): ").strip() or "hasil"

    try:
        reader = PdfReader(str(src))
    except Exception as e:
        print(f"❌ Gagal membuka PDF: {e}")
        return 1

    total = len(reader.pages)
    print(f"📄 Total halaman: {total}")

    print("\n=== Opsi ===")
    print("1) Ambil 1 halaman")
    print("2) Ambil rentang halaman")
    print("3) Ambil multi seleksi")
    print("4) Ambil 1 halaman + sisanya")
    print("5) Split semua halaman ke file terpisah")
    try:
        opt = int(input("Pilih opsi (1-5): ").strip())
    except ValueError:
        print("❌ Opsi harus angka 1-5.")
        return 1

    try:
        if opt == 1:
            page = int(input("Nomor halaman: ").strip())
            if not (1 <= page <= total):
                print("❌ Nomor halaman di luar jangkauan.")
                return 1
            print(f"➡️  Akan mengekstrak halaman {page}.")
            if not confirm("Lanjut eksekusi?"):
                print("🚫 Dibatalkan.")
                return 0
            out = extract_single(reader, page, out_prefix)
            print(f"✅ Berhasil: {out}")

        elif opt == 2:
            raw = input("Rentang (mis. 10-15): ").strip()
            m = re.fullmatch(r"(\d+)-(\d+)", raw)
            if not m:
                print("❌ Format rentang tidak valid.")
                return 1
            start, end = int(m.group(1)), int(m.group(2))
            if start < 1 or end < 1 or end < start or end > total:
                print("❌ Rentang di luar jangkauan.")
                return 1
            print(f"➡️  Akan mengekstrak halaman {start}-{end}.")
            if not confirm("Lanjut eksekusi?"):
                print("🚫 Dibatalkan.")
                return 0
            out = extract_range(reader, start, end, out_prefix)
            print(f"✅ Berhasil: {out}")

        elif opt == 3:
            raw = input("Halaman/rentang (mis. 1,3,5-7,12): ").strip()
            pages = parse_multi_selection(raw)
            pages = clamp_pages(pages, total)
            if not pages:
                print("❌ Tidak ada halaman valid.")
                return 1
            print(f"➡️  Akan mengekstrak {len(pages)} halaman: {pages[:10]}{'...' if len(pages) > 10 else ''}")
            if not confirm("Lanjut eksekusi?"):
                print("🚫 Dibatalkan.")
                return 0
            out = extract_multi(reader, pages, out_prefix)
            print(f"✅ Berhasil: {out}")

        elif opt == 4:
            page = int(input("Halaman yang dipisah (mis. 6): ").strip())
            if not (1 <= page <= total):
                print("❌ Nomor halaman di luar jangkauan.")
                return 1
            print(f"➡️  Akan membuat 2 file: satu berisi halaman {page}, satu lagi tanpa halaman {page}.")
            if not confirm("Lanjut eksekusi?"):
                print("🚫 Dibatalkan.")
                return 0
            p_single, p_rest = extract_single_and_rest(reader, page, out_prefix)
            print(f"✅ Berhasil: {p_single}  &  {p_rest}")

        elif opt == 5:
            print(f"➡️  Akan memisah semua {total} halaman ke file terpisah.")
            if not confirm("Lanjut eksekusi?"):
                print("🚫 Dibatalkan.")
                return 0
            outs = split_all_pages(reader, out_prefix)
            print(f"✅ Berhasil bikin {len(outs)} file. Contoh: {outs[:3]}{'...' if len(outs)>3 else ''}")

        else:
            print("❌ Opsi tidak dikenal.")
            return 1

    except Exception as e:
        print(f"❌ Terjadi error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
