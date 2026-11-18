"""Contoh layanan sederhana untuk menguji jelajah.py.

Isinya sengaja beragam: kelas, method, fungsi biasa, async def,
dekorator, type hint, dan fungsi bersarang.
"""
import json
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pengguna:
    id: int
    nama: str
    email: str
    aktif: bool = True
    peran: list = field(default_factory=list)

    def ringkas(self) -> str:
        status = "aktif" if self.aktif else "nonaktif"
        return f"{self.nama} <{self.email}> ({status})"

    def punya_peran(self, peran: str) -> bool:
        return peran in self.peran


class RepositoriPengguna:
    def __init__(self, path_data: str):
        self.path_data = path_data
        self._cache = {}

    def muat(self) -> None:
        if not os.path.exists(self.path_data):
            self._cache = {}
            return
        with open(self.path_data, "r", encoding="utf-8") as f:
            mentah = json.load(f)
        for item in mentah:
            pengguna = Pengguna(**item)
            self._cache[pengguna.id] = pengguna

    def simpan(self) -> None:
        data = [vars(p) for p in self._cache.values()]
        with open(self.path_data, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def cari(self, id: int) -> Optional[Pengguna]:
        return self._cache.get(id)

    def tambah(self, pengguna: Pengguna) -> None:
        if pengguna.id in self._cache:
            raise ValueError("ID sudah dipakai")
        self._cache[pengguna.id] = pengguna

    def hapus(self, id: int) -> bool:
        if id in self._cache:
            del self._cache[id]
            return True
        return False

    def semua_aktif(self) -> list:
        return [p for p in self._cache.values() if p.aktif]


class LayananPengguna:
    def __init__(self, repo: RepositoriPengguna):
        self.repo = repo

    def daftar(self, nama: str, email: str) -> Pengguna:
        if "@" not in email:
            raise ValueError("Email tidak valid")
        id_baru = len(self.repo._cache) + 1
        pengguna = Pengguna(id=id_baru, nama=nama, email=email)
        self.repo.tambah(pengguna)
        self.repo.simpan()
        return pengguna

    async def ambil_async(self, id: int) -> Optional[Pengguna]:
        return self.repo.cari(id)

    def nonaktifkan(self, id: int) -> bool:
        pengguna = self.repo.cari(id)
        if pengguna is None:
            return False
        pengguna.aktif = False
        self.repo.simpan()
        return True

    def laporan(self) -> str:
        def format_baris(p):
            return f"- {p.ringkas()}"

        baris = [format_baris(p) for p in self.repo.semua_aktif()]
        return "\n".join(baris)


def buat_layanan(path: str = "data.json") -> LayananPengguna:
    repo = RepositoriPengguna(path)
    repo.muat()
    return LayananPengguna(repo)


def validasi_email(email: str) -> bool:
    # def palsu_di_komentar(x): pass
    return "@" in email and "." in email.split("@")[-1]


def main():
    layanan = buat_layanan()
    layanan.daftar("Budi", "budi@contoh.com")
    layanan.daftar("Sari", "sari@contoh.com")
    print(layanan.laporan())


if __name__ == "__main__":
    main()
