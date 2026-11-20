# cek.py

CLI kecil untuk memeriksa file Python di sebuah folder memakai Tree-sitter. Ia melaporkan tiga hal:

1. Komentar yang mengandung `TODO` atau `FIXME`
2. Fungsi yang lebih dari 30 baris
3. File yang sintaksnya mengandung error

## Memasang dependensi

Butuh Python 3.10 atau lebih baru.

```
pip install tree-sitter tree-sitter-python
```

## Menjalankan

```
python cek/cek.py <folder>
```

Contoh, memeriksa folder uji bawaan:

```
python cek/cek.py cek/uji/
```

Skrip menelusuri semua file `*.py` di dalam folder, termasuk subfolder.

## Contoh output

```
cek\uji\ada_todo.py:2: # TODO: perbaiki ini
cek\uji\ada_todo.py:3: # FIXME: salah
cek\uji\fungsi_panjang.py:1: fungsi panjang terlalu panjang (32 baris)
cek\uji\rusak.py:1: sintaks error
```

Formatnya `file:baris: pesan`. Urutan file bisa berbeda tergantung sistem.

## Cara kerja singkat

- **TODO/FIXME:** query `((comment) @c (#match? @c "TODO|FIXME"))`. Karena yang dicari node `comment`, teks `TODO` di dalam string biasa tidak ikut terlapor.
- **Fungsi panjang:** query `(function_definition name: (identifier) @nama) @fungsi`, lalu jumlah baris dihitung dari `end_point[0] - start_point[0] + 1`.
- **Sintaks error:** dicek dengan `tree.root_node.has_error`. Baris pertama yang bermasalah dicari dengan fungsi rekursif `cari_error` yang mencari node `ERROR` atau `MISSING` pertama.

## Catatan

- Semua fungsi dihitung, termasuk method di dalam kelas dan fungsi bersarang.
- Batas fungsi panjang adalah lebih dari 30 baris.

## Pengujian

- Folder `cek/uji/` berisi tiga file uji buatan sendiri: satu dengan TODO/FIXME, satu dengan fungsi 32 baris, dan satu dengan sintaks rusak.
- Diuji juga pada repositori [psf/requests](https://github.com/psf/requests). Hasilnya ada di `cek/hasil_repo.txt`. Dua temuan dicocokkan manual dengan kode aslinya:
  - Komentar TODO di `src/requests/hooks.py`, baris 29: cocok.
  - Fungsi `request` di `src/requests/api.py`, baris 24, 48 baris: cocok.
