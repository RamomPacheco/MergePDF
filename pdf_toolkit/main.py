"""Interactive CLI for PDF manipulation."""

from __future__ import annotations

from docx_bridge.pdf_to_docx import edit_via_docx
from operations.edit_text import edit_text
from operations.extract import extract_tables, extract_text
from operations.merge import merge_pdfs
from operations.protect import decrypt_pdf, encrypt_pdf
from operations.rotate import rotate_pdf
from operations.split import split_pdf
from operations.watermark import add_watermark

MENU = """
=== PDF Toolkit ===
[1]  Mesclar PDFs
[2]  Dividir PDF
[3]  Rotacionar páginas
[4]  Adicionar watermark
[5]  Extrair texto
[6]  Extrair tabelas
[7]  Proteger com senha
[8]  Remover senha
[9]  Editar texto (direto - pymupdf)
[10] Editar texto (via DOCX - edição rica)
[0]  Sair
"""


def _prompt(message: str) -> str:
    return input(message).strip()


def _parse_paths(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def _parse_page_numbers(raw: str, all_pages: bool) -> list[int] | None:
    if all_pages or not raw:
        return None
    pages: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        page_num = int(part)
        if page_num < 1:
            raise ValueError("Page numbers must be >= 1")
        pages.append(page_num - 1)
    return pages


def handle_merge() -> None:
    raw = _prompt("Caminhos dos PDFs (separados por vírgula): ")
    output = _prompt("Arquivo de saída: ")
    merge_pdfs(_parse_paths(raw), output)
    print(f"Operação concluída: {output}")


def handle_split() -> None:
    input_file = _prompt("Arquivo PDF: ")
    output_dir = _prompt("Pasta de saída: ")
    split_pdf(input_file, output_dir)
    print(f"Operação concluída: páginas salvas em {output_dir}")


def handle_rotate() -> None:
    input_file = _prompt("Arquivo PDF: ")
    output_file = _prompt("Arquivo de saída: ")
    degrees = int(_prompt("Graus (90, 180, 270): "))
    pages_raw = _prompt("Páginas (1,2,3 ou vazio para todas): ")
    rotate_pdf(
        input_file,
        output_file,
        degrees,
        _parse_page_numbers(pages_raw, all_pages=not pages_raw),
    )
    print(f"Operação concluída: {output_file}")


def handle_watermark() -> None:
    input_file = _prompt("Arquivo PDF: ")
    watermark_file = _prompt("Arquivo watermark PDF: ")
    output_file = _prompt("Arquivo de saída: ")
    add_watermark(input_file, watermark_file, output_file)
    print(f"Operação concluída: {output_file}")


def handle_extract_text() -> None:
    input_file = _prompt("Arquivo PDF: ")
    text = extract_text(input_file)
    print("--- Texto extraído ---")
    print(text)
    print("Operação concluída.")


def handle_extract_tables() -> None:
    input_file = _prompt("Arquivo PDF: ")
    tables = extract_tables(input_file)
    print(f"Tabelas encontradas: {len(tables)}")
    for index, table in enumerate(tables, start=1):
        print(f"\n--- Tabela {index} ---")
        for row in table:
            print(row)
    print("Operação concluída.")


def handle_encrypt() -> None:
    input_file = _prompt("Arquivo PDF: ")
    output_file = _prompt("Arquivo de saída: ")
    password = _prompt("Senha: ")
    encrypt_pdf(input_file, output_file, password)
    print(f"Operação concluída: {output_file}")


def handle_decrypt() -> None:
    input_file = _prompt("Arquivo PDF: ")
    output_file = _prompt("Arquivo de saída: ")
    password = _prompt("Senha: ")
    decrypt_pdf(input_file, output_file, password)
    print(f"Operação concluída: {output_file}")


def handle_edit_direct() -> None:
    input_file = _prompt("Arquivo PDF: ")
    output_file = _prompt("Arquivo de saída: ")
    old_text = _prompt("Texto a substituir: ")
    new_text = _prompt("Novo texto: ")
    count = edit_text(input_file, output_file, old_text, new_text)
    print(f"Operação concluída: {count} substituição(ões) em {output_file}")


def handle_edit_docx() -> None:
    input_file = _prompt("Arquivo PDF: ")
    output_file = _prompt("Arquivo de saída (.pdf): ")
    old_text = _prompt("Texto a substituir: ")
    new_text = _prompt("Novo texto: ")
    edit_via_docx(input_file, output_file, old_text, new_text)
    print(f"Operação concluída: {output_file}")


HANDLERS = {
    "1": handle_merge,
    "2": handle_split,
    "3": handle_rotate,
    "4": handle_watermark,
    "5": handle_extract_text,
    "6": handle_extract_tables,
    "7": handle_encrypt,
    "8": handle_decrypt,
    "9": handle_edit_direct,
    "10": handle_edit_docx,
}


def main() -> None:
    """Run the interactive menu loop."""
    while True:
        print(MENU)
        choice = _prompt("Escolha uma opção: ")

        if choice == "0":
            print("Encerrando.")
            break

        handler = HANDLERS.get(choice)
        if handler is None:
            print("Opção inválida.")
            continue

        try:
            handler()
        except Exception as exc:
            cause = exc.__cause__
            if cause is not None:
                print(f"Erro: {exc}")
                print(f"Detalhe: {cause}")
            else:
                print(f"Erro: {exc}")


if __name__ == "__main__":
    main()
