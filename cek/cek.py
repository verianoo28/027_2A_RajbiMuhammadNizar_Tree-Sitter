import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")

def cari_error(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        hasil = cari_error(child)
        if hasil is not None:
            return hasil
    return None

def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME (sudah jadi)
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        print(f"{path}:{node.start_point[0] + 1}: {node.text.decode().strip()}")

        # Fitur 2: fungsi yang lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        fungsi = cap["fungsi"][0]
        jumlah = cap["fungsi"][0].end_point[0] - cap["fungsi"][0].start_point[0] + 1
        if jumlah > 30:
            nama = cap["nama"][0].text.decode()
            print(f"{path}:{fungsi.start_point[0] + 1}: fungsi {nama} terlalu panjang ({jumlah} baris)")
        # Fitur 3: file yang pohonnya mengandung error
    if tree.root_node.has_error:
        err = cari_error(tree.root_node)
        print(f"{path}:{err.start_point[0] + 1}: sintaks error")

SKIP = {".git", "venv", ".venv", "node_modules", "__pycache__"}

for path in Path(sys.argv[1]).rglob("*.py"):
    if SKIP & set(path.parts):
        continue
    cek_file(path)