import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode1 = b"""def sapa(nama):
    return nama
"""

kode2 = b"""if x > 1:
    y = 2
else:
    y = 3
"""

kode3 = b"""class Kucing:
    def suara(self):
        return 1
"""

for kode in [kode1, kode2, kode3]:
    tree = parser.parse(kode)
    print(kode.decode())
    print(tree.root_node)
    print()