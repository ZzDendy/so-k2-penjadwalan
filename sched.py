"""Simulator penjadwalan CPU untuk dataset kelas K-2.

Dataset: P(arrival, burst, prioritas). Angka prioritas kecil = prioritas tinggi.
Simulasi memakai satuan waktu 1 tick supaya algoritma preemptive (SRTF, RR)
dapat dibandingkan dengan aturan yang sama.
"""
import argparse
import json

# name, arrival, burst, priority
DATASET = [
    ("P1", 0, 3, 1),
    ("P2", 0, 6, 3),
    ("P3", 2, 4, 2),
    ("P4", 3, 8, 4),
    ("P5", 4, 2, 1),
]


def simulasi(kind, quantum=None, data=DATASET):
    """Kembalikan (segmen, metrik). segmen = [(nama, mulai, selesai), ...]."""
    arr = {n: a for n, a, b, p in data}
    burst = {n: b for n, a, b, p in data}
    prio = {n: p for n, a, b, p in data}
    sisa = dict(burst)
    urut = [n for n, *_ in data]

    menunggu = []
    selesai = set()
    mulai_pertama = {}
    waktu_selesai = {}
    segmen = []

    def catat(nama, t):
        if segmen and segmen[-1][0] == nama and segmen[-1][2] == t:
            segmen[-1] = (nama, segmen[-1][1], t + 1)
        else:
            segmen.append((nama, t, t + 1))

    def pilih(kandidat, aturan):
        if aturan == "fcfs":
            return min(kandidat, key=lambda n: (arr[n], urut.index(n)))
        if aturan == "sjf":
            return min(kandidat, key=lambda n: (burst[n], arr[n], urut.index(n)))
        if aturan == "srtf":
            return min(kandidat, key=lambda n: (sisa[n], arr[n], urut.index(n)))
        if aturan == "priority":
            return min(kandidat, key=lambda n: (prio[n], arr[n], urut.index(n)))
        raise ValueError(aturan)

    preemptive = kind in ("srtf", "rr")
    aturan = "fcfs" if kind == "rr" else kind

    t = 0
    sekarang = None
    terpakai = 0

    while len(selesai) < len(data):
        for n in urut:
            if arr[n] == t:
                menunggu.append(n)

        if sekarang is None:
            if not menunggu:
                t += 1
                continue
            sekarang = pilih(menunggu, aturan) if kind != "rr" else menunggu.pop(0)
            if kind != "rr":
                menunggu.remove(sekarang)
            terpakai = 0
        elif kind == "srtf":
            kandidat = pilih(menunggu, "srtf") if menunggu else None
            if kandidat and sisa[kandidat] < sisa[sekarang]:
                menunggu.remove(kandidat)
                menunggu.append(sekarang)
                sekarang = kandidat
                terpakai = 0
        elif kind == "rr" and terpakai == quantum:
            menunggu.append(sekarang)
            sekarang = menunggu.pop(0)
            terpakai = 0

        mulai_pertama.setdefault(sekarang, t)
        catat(sekarang, t)
        sisa[sekarang] -= 1
        terpakai += 1
        t += 1

        if sisa[sekarang] == 0:
            waktu_selesai[sekarang] = t
            selesai.add(sekarang)
            sekarang = None
            terpakai = 0

    metrik = {}
    for n in urut:
        tat = waktu_selesai[n] - arr[n]
        metrik[n] = {
            "arrival": arr[n],
            "burst": burst[n],
            "prio": prio[n],
            "mulai": mulai_pertama[n],
            "selesai": waktu_selesai[n],
            "waiting": tat - burst[n],
            "turnaround": tat,
            "response": mulai_pertama[n] - arr[n],
        }
    return segmen, metrik


def rata(metrik):
    k = ("waiting", "turnaround", "response")
    return {x: sum(m[x] for m in metrik.values()) / len(metrik) for x in k}


ALGORITMA = [
    ("FCFS", "fcfs", None),
    ("SJF", "sjf", None),
    ("SRTF", "srtf", None),
    ("Priority", "priority", None),
    ("RR q=2", "rr", 2),
    ("RR q=3", "rr", 3),
]

# Hasil hitung manual di atas kertas, tanpa memakai simulator. Kalau angka
# simulator berbeda dari tabel ini, berarti simulatornya yang salah.
HITUNG_MANUAL = {
    "FCFS": {"waiting": 7.40, "turnaround": 12.00, "response": 7.40},
    "SJF": {"waiting": 5.00, "turnaround": 9.60, "response": 5.00},
    "SRTF": {"waiting": 4.80, "turnaround": 9.40, "response": 4.40},
    "Priority": {"waiting": 5.00, "turnaround": 9.60, "response": 5.00},
    "RR q=2": {"waiting": 8.60, "turnaround": 13.20, "response": 2.60},
    "RR q=3": {"waiting": 8.60, "turnaround": 13.20, "response": 4.20},
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--verifikasi", action="store_true")
    p.add_argument("--json", default="results/jadwal.json")
    a = p.parse_args()

    hasil = {}
    for label, kind, q in ALGORITMA:
        segmen, metrik = simulasi(kind, q)
        hasil[label] = {"segmen": segmen, "metrik": metrik, "rata": rata(metrik)}

    if a.json:
        import os
        os.makedirs("results", exist_ok=True)
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(hasil, f, indent=2)

    print("| Algoritma | Rata-rata Waiting | Rata-rata Turnaround | Rata-rata Response |")
    print("|---|---|---|---|")
    for label, _, _ in ALGORITMA:
        r = hasil[label]["rata"]
        print(f"| {label} | {r['waiting']:.2f} | {r['turnaround']:.2f} | {r['response']:.2f} |")

    print("\nUrutan eksekusi:")
    for label, _, _ in ALGORITMA:
        s = hasil[label]["segmen"]
        print(f"  {label:10s} " + " ".join(f"{n}[{m}-{e}]" for n, m, e in s))

    if a.verifikasi:
        print("\nVerifikasi terhadap hitung manual:")
        gagal = 0
        for label, manual in HITUNG_MANUAL.items():
            if manual is None:
                print(f"  {label:10s} (tanpa pembanding manual)")
                continue
            r = hasil[label]["rata"]
            beda = max(abs(r[k] - manual[k]) for k in manual)
            tandai = "cocok" if beda < 0.005 else f"BEDA {beda:.3f}"
            if beda >= 0.005:
                gagal += 1
            print(f"  {label:10s} {tandai}")
        print("semua cocok" if gagal == 0 else f"{gagal} algoritma tidak cocok")


if __name__ == "__main__":
    main()
