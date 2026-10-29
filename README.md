# K-2 — Simulasi dan Evaluasi Algoritma Penjadwalan CPU

Tugas kelompok Sistem Operasi (USA-WP2260110), IF-3C, tema **IoT dan Smart Farming**.
Konteks: pembacaan sensor, kontrol pompa irigasi, dan pengiriman data pada gateway IoT.

Laporan: [`results/IF-3C_K-2_250660121068_Dendy Zainal Mutaqien.pdf`](results/IF-3C_K-2_250660121068_Dendy%20Zainal%20Mutaqien.pdf)

## Dataset kelas

`P1(0,3,1) P2(0,6,3) P3(2,4,2) P4(3,8,4) P5(4,2,1)` — format (arrival, burst, prioritas),
angka prioritas kecil = prioritas tinggi. Quantum RR = 2 dan 3.

## Hasil

| Algoritma | Rata-rata Waiting | Turnaround | Response |
|---|---|---|---|
| FCFS | 7.40 | 12.00 | 7.40 |
| SJF | 5.00 | 9.60 | 5.00 |
| SRTF | **4.80** | **9.40** | 4.40 |
| Priority | 5.00 | 9.60 | 5.00 |
| RR q=2 | 8.60 | 13.20 | **2.60** |
| RR q=3 | 8.60 | 13.20 | 4.20 |

Keenam konfigurasi cocok dengan perhitungan manual (dua desimal), diverifikasi lewat
`sched.py --verifikasi`.

## Menjalankan

```bash
python3 sched.py --verifikasi        # hitung + cocokkan dengan manual
python3 sched.py                     # tulis results/jadwal.json
../ipc-kebun/.venv/bin/python figures.py    # Gantt chart + grafik metrik
../ipc-kebun/.venv/bin/python report.py     # rakit laporan docx
../ipc-kebun/.venv/bin/python ../toc.py \
  "results/IF-3C_K-2_250660121068_Dendy Zainal Mutaqien.docx" \
  "results/IF-3C_K-2_250660121068_Dendy Zainal Mutaqien.pdf"
```

## Catatan analisis

- **Efek konvoi** FCFS: P5 hanya butuh 2 tick tapi menunggu 17 tick di belakang P4.
- **Priority = SJF** pada dataset ini karena urutan prioritas kebetulan sama dengan urutan
  burst terpendek. Pada dataset lain hasilnya akan berbeda.
- **RR q=2 dan q=3** memberi waiting/turnaround identik, tetapi q=2 unggul di response
  time (2.60 vs 4.20).

Rekomendasi: Priority preemptive untuk tugas kendali pompa, Round Robin quantum kecil
untuk pembacaan sensor periodik.
