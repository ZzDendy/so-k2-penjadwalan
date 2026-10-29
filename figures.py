"""Membuat Gantt chart semua algoritma untuk laporan K-2."""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

FONT = "DejaVu Sans"
WARNA = ["#3B5B8C", "#B7791F", "#2F6B3C", "#A03B2C", "#5B3B8C"]
OUT = "results"


def gantt(hasil, path):
    urutan = [n for n, *_ in json.load(open("results/jadwal.json"))["FCFS"]["metrik"].items()]
    peta = {n: WARNA[i % len(WARNA)] for i, n in enumerate(urutan)}

    label = list(hasil)
    fig, ax = plt.subplots(figsize=(9.0, 0.62 * len(label) + 1.0))
    for baris, nama in enumerate(label):
        y = len(label) - baris - 1
        for p, mulai, selesai in hasil[nama]["segmen"]:
            ax.add_patch(plt.Rectangle((mulai, y + 0.12), selesai - mulai, 0.62,
                                       facecolor=peta[p], edgecolor="white", linewidth=1.1))
            if selesai - mulai >= 1.4:
                ax.text((mulai + selesai) / 2, y + 0.43, p, ha="center", va="center",
                        color="white", fontsize=7.5, fontfamily=FONT, fontweight="bold")

    ax.set_yticks(range(len(label)))
    ax.set_yticklabels(label[::-1], fontfamily=FONT, fontsize=8.5)
    ax.set_xlim(0, max(s for v in hasil.values() for _, _, s in v["segmen"]) + 0.4)
    ax.set_ylim(0, len(label))
    ax.set_xlabel("Waktu (tick)", fontfamily=FONT, fontsize=8.5)
    ax.tick_params(axis="x", labelsize=7.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", color="#DDDDDD", linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_title("Gantt chart perbandingan algoritma penjadwalan",
                 fontsize=10, fontfamily=FONT, fontweight="bold")
    ax.legend(handles=[Patch(facecolor=c, label=n) for n, c in peta.items()],
              ncol=len(peta), frameon=False, fontsize=7.5,
              loc="upper center", bbox_to_anchor=(0.5, -0.11))
    fig.tight_layout()
    fig.savefig(path, dpi=220, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def grafik_metrik(hasil, path):
    label = list(hasil)
    kunci = [("waiting", "Waiting"), ("turnaround", "Turnaround"), ("response", "Response")]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    lebar = 0.26
    for i, (k, judul) in enumerate(kunci):
        nilai = [hasil[n]["rata"][k] for n in label]
        pos = [x + (i - 1) * lebar for x in range(len(label))]
        b = ax.bar(pos, nilai, lebar, label=judul,
                   color=["#3B5B8C", "#B7791F", "#2F6B3C"][i], edgecolor="white", linewidth=0.5)
        for r in b:
            ax.annotate(f"{r.get_height():.2f}",
                        (r.get_x() + r.get_width() / 2, r.get_height()),
                        textcoords="offset points", xytext=(0, 2), ha="center",
                        fontsize=6.5, fontfamily=FONT)

    ax.set_xticks(range(len(label)))
    ax.set_xticklabels(label, fontfamily=FONT, fontsize=8.5)
    ax.set_ylabel("Rata-rata (tick)", fontfamily=FONT, fontsize=8.5)
    ax.tick_params(labelsize=7.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.5)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper left")
    ax.set_ylim(0, max(v["rata"][k] for v in hasil.values() for k, _ in kunci) * 1.28)
    ax.set_title("Perbandingan metrik penjadwalan", fontsize=10,
                 fontfamily=FONT, fontweight="bold")
    fig.tight_layout()
    fig.savefig(path, dpi=220, facecolor="white")
    plt.close(fig)


def main():
    os.makedirs(OUT, exist_ok=True)
    with open("results/jadwal.json", encoding="utf-8") as f:
        hasil = json.load(f)
    gantt(hasil, f"{OUT}/gambar-gantt.png")
    grafik_metrik(hasil, f"{OUT}/gambar-metrik.png")
    print("gambar:", [f for f in sorted(os.listdir(OUT)) if f.endswith(".png")])


if __name__ == "__main__":
    main()
