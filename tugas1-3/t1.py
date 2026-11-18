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
    
print("--- anak langsung function_definition ---")
tree = parser.parse(kode1)
fungsi = tree.root_node.children[0]
for c in fungsi.children:
    print(c.type, "|", "bernama" if c.is_named else "anonim")

print("--- jumlah ---")
print(len(fungsi.children), len(fungsi.named_children))

print("--- anak dari parameters ---")
param = fungsi.children[2]
for c in param.children:
    print(c.type, "|", "bernama" if c.is_named else "anonim")