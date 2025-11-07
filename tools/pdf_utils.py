"""Utilities for working with PDF and XSD evidence files without external deps."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zlib
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass
class PdfPage:
    number: int
    text: str


@dataclass
class PdfDocument:
    path: Path
    sha256: str
    size: int
    modified: float
    pages: List[PdfPage]


def _decode_pdf_string(data: bytes) -> str:
    result: List[str] = []
    i = 0
    length = len(data)
    while i < length:
        byte = data[i]
        if byte == 0x5C:  # '\\'
            i += 1
            if i >= length:
                break
            byte = data[i]
            if byte in b"nrtbf":
                result.append({
                    ord("n"): "\n",
                    ord("r"): "\r",
                    ord("t"): "\t",
                    ord("b"): "\b",
                    ord("f"): "\f",
                }[byte])
            elif byte in b"()\\":
                result.append(chr(byte))
            elif 0x30 <= byte <= 0x37:  # octal escape
                digits = [chr(byte)]
                for _ in range(2):
                    if i + 1 < length and 0x30 <= data[i + 1] <= 0x37:
                        i += 1
                        digits.append(chr(data[i]))
                    else:
                        break
                try:
                    result.append(chr(int("".join(digits), 8)))
                except ValueError:
                    pass
            else:
                result.append(chr(byte))
        else:
            result.append(chr(byte))
        i += 1
    return "".join(result)


def _decode_pdf_hex(data: str) -> str:
    try:
        raw = bytes.fromhex(re.sub(r"\s+", "", data))
    except ValueError:
        return ""
    for encoding in ("utf-16-be", "latin1", "utf-8"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin1", errors="ignore")


def _extract_pdf_objects(raw: bytes) -> Dict[int, Dict[str, Optional[bytes]]]:
    objects: Dict[int, Dict[str, Optional[bytes]]] = {}
    pattern = re.compile(rb"(\d+)\s+0\s+obj\s*(.*?)\s*endobj", re.S)
    for match in pattern.finditer(raw):
        obj_id = int(match.group(1))
        content = match.group(2)
        dict_part = content
        stream_data: Optional[bytes] = None
        if b"stream" in content:
            before_stream, after_stream = content.split(b"stream", 1)
            dict_part = before_stream
            if b"endstream" in after_stream:
                stream_data = after_stream.split(b"endstream", 1)[0]
                for prefix in (b"\r\n", b"\n", b"\r"):
                    if stream_data.startswith(prefix):
                        stream_data = stream_data[len(prefix) :]
                        break
                for suffix in (b"\r\n", b"\n", b"\r"):
                    if stream_data.endswith(suffix):
                        stream_data = stream_data[: -len(suffix)]
                        break
        objects[obj_id] = {"dict": dict_part, "stream": stream_data}
    return objects


def extract_text_by_page(pdf_path: Path) -> List[PdfPage]:
    raw = pdf_path.read_bytes()
    objects = _extract_pdf_objects(raw)
    pages: List[PdfPage] = []
    page_objs: List[int] = [
        obj_id
        for obj_id, data in objects.items()
        if data["dict"] and (b"/Type/Page" in data["dict"] or b"/Type /Page" in data["dict"])
    ]
    page_objs.sort()

    for index, page_id in enumerate(page_objs, start=1):
        data = objects[page_id]
        dict_part = data["dict"] or b""
        contents_refs: List[int] = []
        arr_match = re.search(rb"/Contents\s*\[(.*?)\]", dict_part, re.S)
        if arr_match:
            contents_refs = [int(num) for num in re.findall(rb"(\d+)\s+0\s+R", arr_match.group(1))]
        else:
            ref_match = re.search(rb"/Contents\s+(\d+)\s+0\s+R", dict_part)
            if ref_match:
                contents_refs = [int(ref_match.group(1))]
        collected: List[str] = []
        for ref in contents_refs:
            stream_info = objects.get(ref)
            if not stream_info:
                continue
            stream = stream_info.get("stream")
            if stream is None:
                continue
            dict_bytes = stream_info.get("dict") or b""
            if b"FlateDecode" in dict_bytes:
                try:
                    stream = zlib.decompress(stream)
                except zlib.error:
                    continue
            try:
                stream_text = stream.decode("latin1")
            except Exception:
                stream_text = stream.decode("latin1", errors="ignore")
            parts: List[str] = []
            for match in re.finditer(r"\(([^()]*)\)\s*Tj", stream_text):
                parts.append(_decode_pdf_string(match.group(1).encode("latin1")).strip())
            for match in re.finditer(r"\[(.*?)\]\s*TJ", stream_text, re.S):
                segments = re.findall(r"\(([^()]*)\)", match.group(1))
                if segments:
                    decoded = [
                        _decode_pdf_string(segment.encode("latin1")).strip()
                        for segment in segments
                    ]
                    parts.append("".join(decoded))
            for match in re.finditer(r"<([0-9A-Fa-f\s]+)>\s*Tj", stream_text):
                decoded = _decode_pdf_hex(match.group(1)).strip()
                if decoded:
                    parts.append(decoded)
            for match in re.finditer(r"\[(.*?)\]\s*TJ", stream_text, re.S):
                hex_segments = re.findall(r"<([0-9A-Fa-f\s]+)>", match.group(1))
                if hex_segments:
                    decoded = "".join(_decode_pdf_hex(seg).strip() for seg in hex_segments)
                    if decoded:
                        parts.append(decoded)
            text = " ".join(filter(None, parts))
            if text:
                collected.append(text)
        pages.append(PdfPage(number=index, text="\n".join(collected)))
    return pages


def load_pdf_document(path: Path) -> PdfDocument:
    pages = extract_text_by_page(path)
    sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
    stat = path.stat()
    return PdfDocument(
        path=path,
        sha256=sha256,
        size=stat.st_size,
        modified=stat.st_mtime,
        pages=pages,
    )


def build_pdf_index(base_path: Path) -> List[PdfDocument]:
    return [load_pdf_document(path) for path in sorted(base_path.glob("*.pdf"))]


def build_xsd_inventory(base_path: Path) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    for path in sorted(base_path.glob("*.xsd")):
        sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
        entries.append(
            {
                "filename": path.name,
                "sha256": sha256,
                "size": path.stat().st_size,
            }
        )
    return entries


def write_pdf_index_json(documents: Iterable[PdfDocument], output_path: Path) -> None:
    payload = []
    for doc in documents:
        payload.append(
            {
                "filename": doc.path.name,
                "sha256": doc.sha256,
                "size": doc.size,
                "modified": datetime.fromtimestamp(doc.modified, tz=timezone.utc).isoformat(),
                "pages": len(doc.pages),
            }
        )
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def write_xsd_inventory_json(entries: Iterable[Dict[str, str]], output_path: Path) -> None:
    output_path.write_text(json.dumps(list(entries), indent=2, ensure_ascii=False))


def dump_pages(documents: Iterable[PdfDocument], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for doc in documents:
        doc_dir = output_dir / doc.path.stem
        doc_dir.mkdir(exist_ok=True)
        for page in doc.pages:
            (doc_dir / f"page_{page.number:03d}.txt").write_text(page.text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate DGII PDF evidence artifacts")
    parser.add_argument("base", type=Path, help="Directory containing official PDF/XSD files")
    parser.add_argument(
        "--dump-pages",
        dest="dump_pages",
        action="store_true",
        help="Dump extracted page text",
    )
    parser.add_argument(
        "--index-json",
        dest="index_json",
        type=Path,
        help="Path to write pdf_index.json",
    )
    parser.add_argument(
        "--xsd-json",
        dest="xsd_json",
        type=Path,
        help="Path to write xsd_inventory.json",
    )
    parser.add_argument(
        "--pages-dir",
        dest="pages_dir",
        type=Path,
        default=Path("_pages"),
        help="Output directory for page dumps",
    )
    args = parser.parse_args()

    base_path = args.base
    pdf_docs = build_pdf_index(base_path)
    xsd_entries = build_xsd_inventory(base_path)

    if args.dump_pages:
        dump_pages(pdf_docs, args.pages_dir)
    if args.index_json:
        write_pdf_index_json(pdf_docs, args.index_json)
    if args.xsd_json:
        write_xsd_inventory_json(xsd_entries, args.xsd_json)


if __name__ == "__main__":
    main()
