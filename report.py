"""Merakit laporan K-2 dari template jurusan dan hasil simulator."""
import json
import os
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Cm, Pt

sys.path.insert(0, "../tools")
from docx_kit import (baca_berkas, bersihkan, bullet, caption, gambar, h1, h2,
                      header_dokumen, kode, nomor_halaman, par, sampul, tabel)

TEMPLATE = "../template/Template Laporan Tugas Individu.docx"
OUT = "results/Laporan_K-2_Penjadwalan_Kebun.docx"
NAMA = "Dendy Zainal Mutaqien"
NIM = "250660121068"
KELAS = "IF-3C"
KODE = "K-2"
ANGGOTA = [
    ("Dendy Zainal Mutaqien", NIM,
     "Simulator penjadwalan, perhitungan manual, dan penyusunan laporan"),
    ("R.Sangga Buana", "250660121021",
     "Membuat Gantt chart keenam algoritma dan memeriksa angka Tabel 5.1"),
    ("M.Azkal Azkiya", "250660121107",
     "Memeriksa hitungan manual tiap algoritma dan format Daftar Pustaka"),
]


def baca_hasil():
    with open("results/jadwal.json", encoding="utf-8") as f:
        return json.load(f)


def sampul_k2(d):
    sampul(
        d,
        "LAPORAN TUGAS KELOMPOK",
        "Simulasi dan Evaluasi Algoritma Penjadwalan CPU\n"
        "pada Gateway Kebun Pintar",
        [
            ("Kode dan judul tugas", "K-2 Simulasi dan Evaluasi Algoritma Penjadwalan CPU"),
            ("Kelas / tema", f"{KELAS} — IoT dan Smart Farming"),
            ("Nama", NAMA),
            ("NIM", NIM),
            ("Anggota kelompok", "3 orang — Dendy Zainal Mutaqien, R.Sangga Buana, "
                                 "M.Azkal Azkiya (rincian di Lampiran D)"),
            ("Nama host", "INFINIX-ElementaryOS"),
            ("Minggu / tanggal kumpul", "Minggu ke-5 / 5 November 2026"),
            ("Kepingan puzzle", "Kepingan #5 → Level 3 Puzzle UTS"),
            ("Dosen pengampu", "Muhammad Agreindra Helmiawan, S.Kom., M.T"),
        ],
        "K-2",
    )


def pendahuluan(d):
    h1(d, "1. Pendahuluan")

    h2(d, "1.1 Latar belakang kasus")
    par(d, "Gateway kebun pintar menjalankan beberapa tugas sekaligus pada satu perangkat kecil: "
           "membaca sensor, mengendalikan pompa irigasi, dan mengirim data ke server. Semua tugas "
           "itu bersaing memperebutkan satu prosesor. Kalau penjadwalannya buruk, pembacaan sensor "
           "bisa tertunda beberapa detik, atau perintah menutup pompa baru dijalankan setelah air "
           "sudah meluap.")
    par(d, "Penjadwalan CPU menentukan urutan dan lama setiap tugas memakai prosesor. Algoritma "
           "yang berbeda menghasilkan rata-rata waktu tunggu, waktu penyelesaian, dan waktu "
           "respons yang berbeda pula. Pada perangkat yang tugasnya bercampur antara pekerjaan "
           "panjang dan pendek, pilihan algoritma bukan soal selera: ia menentukan apakah tugas "
           "mendesak benar-benar dilayani lebih dulu. Tugas ini membandingkan enam konfigurasi "
           "penjadwalan pada satu dataset kelas yang sama, memakai simulator yang hasilnya "
           "diverifikasi dengan perhitungan manual.")

    h2(d, "1.2 Tujuan tugas")
    par(d, "Capaian pembelajaran yang diukur adalah Sub-CPMK-5 (CPMK061, CPMK063, CPMK081, "
           "CPMK102, CPMK112). Tujuannya:")
    bullet(d, "membuat Gantt chart dan menghitung rata-rata waiting time, turnaround time, dan "
              "response time untuk FCFS, SJF, SRTF, Priority, serta Round Robin pada quantum 2 "
              "dan 3;", "Pertama, ")
    bullet(d, "membangun simulator penjadwalan sederhana, lalu memverifikasi keluarannya "
              "terhadap perhitungan manual;", "Kedua, ")
    bullet(d, "merekomendasikan algoritma yang paling sesuai untuk konteks gateway kebun "
              "pintar.", "Ketiga, ")

    h2(d, "1.3 Ruang lingkup")
    par(d, "Dataset kelas yang dipakai adalah P1(0,3,1), P2(0,6,3), P3(2,4,2), P4(3,8,4), dan "
           "P5(4,2,1) dengan format (arrival, burst, prioritas). Angka prioritas kecil berarti "
           "prioritas lebih tinggi. Simulator memakai satuan waktu satu tick dan mengasumsikan "
           "waktu konteks-switch nol. Algoritma preemptive yang diuji adalah SRTF dan Round "
           "Robin; algoritma non-preemptive yang diuji adalah FCFS, SJF, dan Priority.")
    par(d, "Yang tidak dikerjakan: pengukuran pada perangkat keras nyata, penjadwalan "
           "multiprosesor, dan analisis pengaruh waktu konteks-switch.")


def dasar_teori(d):
    h1(d, "2. Dasar Teori Singkat")
    par(d, "Penjadwal CPU memilih proses mana yang berjalan saat prosesor bebas. Silberschatz "
           "dkk. (2018) mengelompokkan kriteria penilaiannya menjadi waktu tunggu (waiting "
           "time), waktu penyelesaian (turnaround time), dan waktu respons (response time). "
           "Waiting time adalah total waktu proses berada di antrean siap; turnaround time "
           "adalah selisih antara waktu selesai dan waktu kedatangan; response time adalah "
           "selisih antara waktu pertama kali mendapat prosesor dan waktu kedatangan.")
    par(d, "FCFS (First Come First Served) melayani proses sesuai urutan kedatangan. Algoritma "
           "ini sederhana dan tidak preemptive, tetapi terkenal dengan efek konvoi: satu proses "
           "panjang di depan menahan semua proses di belakangnya. SJF (Shortest Job First) "
           "memilih proses dengan burst time terkecil. SJF terbukti memberi rata-rata waiting "
           "time minimum untuk himpunan proses yang sudah tersedia, tetapi versi "
           "non-preemptive-nya merugikan proses yang datang lebih dulu. SRTF (Shortest Remaining "
           "Time First) adalah versi preemptive dari SJF: setiap kali ada proses baru datang, "
           "sisa waktu proses yang sedang berjalan dibandingkan, dan prosesor berpindah ke yang "
           "sisanya lebih pendek.")
    par(d, "Priority scheduling memilih proses dengan prioritas tertinggi. Tanpa aging, "
           "algoritma ini dapat membuat proses berprioritas rendah tidak pernah dilayani "
           "(starvation). Round Robin menghapus kelemahan itu dengan memberi setiap proses jatah "
           "waktu tetap (quantum) secara bergiliran. Quantum kecil membuat response time rendah "
           "tetapi menambah jumlah pergantian konteks; quantum besar mendekati perilaku FCFS. "
           "Pada Round Robin, besarnya quantum menjadi parameter yang harus dipilih, bukan "
           "sesuatu yang datang sendiri.")


def lingkungan(d):
    h1(d, "3. Lingkungan Praktik")
    tabel(d, ["Komponen", "Keterangan"], [
        ("Laptop (host)", "elementary OS 8, AMD Ryzen 7 7735HS, RAM 16 GiB, kernel "
                          "7.0.0-34-generic"),
        ("Hypervisor", "Tidak dipakai — simulasi dijalankan langsung pada host"),
        ("VM / host", "INFINIX-ElementaryOS, 16 vCPU"),
        ("Perangkat lain", "Tidak berlaku — dataset kelas dipakai sebagai beban simulasi"),
        ("Bahasa dan alat", "Python 3.12.3; matplotlib untuk Gantt chart dan grafik; "
                            "python-docx untuk laporan"),
        ("Satuan waktu", "1 tick; asumsi waktu konteks-switch nol"),
    ], lebar=[4.0, 11.2])


def langkah(d, hasil):
    h1(d, "4. Langkah Pengerjaan")
    par(d, "Pekerjaan dibagi menjadi tiga tahap: menulis simulator, menghitung manual sebagai "
           "pembanding, lalu membuat Gantt chart. Folder kerja berisi sched.py (simulator), "
           "figures.py (gambar), dan results/ (keluaran JSON dan PNG).")

    h2(d, "4.1 Langkah 1: Menulis simulator dengan satu mesin waktu")
    par(d, "Agar FCFS, SJF, Priority, SRTF, dan Round Robin bisa dibandingkan dengan aturan yang "
           "sama, simulator tidak ditulis sebagai lima fungsi terpisah. Semua algoritma memakai "
           "satu loop waktu yang naik satu tick, dan perbedaannya hanya pada fungsi pemilih "
           "proses. Round Robin ditangani dengan menghitung tick yang sudah dipakai proses "
           "berjalan; SRTF dengan membandingkan sisa waktu setiap kali ada proses baru datang.")
    kode(d, baca_berkas("sched.py"))

    h2(d, "4.2 Langkah 2: Menghitung manual sebagai pembanding")
    par(d, "Sebelum mempercayai simulator, keenam hasilnya dihitung manual di atas kertas. "
           "Contoh FCFS: proses dijalankan berurutan P1(0-3), P2(3-9), P3(9-13), P4(13-21), "
           "P5(21-23). Waiting time tiap proses adalah waktu mulai dikurangi waktu kedatangan; "
           "nilai rata-ratanya (0+3+7+10+17)/5 = 7,40. Angka inilah yang dibandingkan dengan "
           "keluaran simulator, bukan sebaliknya.")
    kode(d, "$ python3 sched.py --verifikasi\n"
            "Verifikasi terhadap hitung manual:\n"
            "  FCFS       cocok\n"
            "  SJF        cocok\n"
            "  SRTF       cocok\n"
            "  Priority   cocok\n"
            "  RR q=2     cocok\n"
            "  RR q=3     cocok\n"
            "semua cocok")

    h2(d, "4.3 Langkah 3: Membuat Gantt chart")
    par(d, "Simulator menyimpan setiap segmen eksekusi sebagai (proses, waktu mulai, waktu "
           "selesai). figures.py mengubah segmen itu menjadi batang horizontal, satu baris per "
           "algoritma, sehingga pola preemption pada SRTF dan Round Robin terlihat langsung "
           "dibandingkan dengan FCFS yang berupa satu batang utuh.")
    kode(d, baca_berkas("figures.py"))


def hasil(d, hasil_json):
    h1(d, "5. Hasil dan Analisis")

    h2(d, "5.1 Hasil")
    par(d, "Tabel 5.1 memuat rata-rata ketiga metrik untuk enam konfigurasi. Seluruh angka "
           "berasal dari simulator yang sudah diverifikasi dengan hitungan manual.")
    baris = []
    for label in ("FCFS", "SJF", "SRTF", "Priority", "RR q=2", "RR q=3"):
        r = hasil_json[label]["rata"]
        baris.append((label, f"{r['waiting']:.2f}", f"{r['turnaround']:.2f}",
                      f"{r['response']:.2f}"))
    tabel(d, ["Algoritma", "Rata-rata Waiting", "Rata-rata Turnaround",
              "Rata-rata Response"], baris, lebar=[3.4, 3.9, 4.0, 3.9])
    caption(d, "Tabel 5.1 Rata-rata metrik per algoritma (satuan tick)")

    par(d, "Gambar 5.1 memperlihatkan urutan eksekusi masing-masing algoritma pada satu garis "
           "waktu yang sama.")
    gambar(d, "results/gambar-gantt.png", 15.5,
           "Gambar 5.1 Gantt chart keenam konfigurasi penjadwalan")
    par(d, "Gambar 5.2 menyandingkan ketiga metrik dalam satu grafik agar trade-off antar "
           "algoritma terlihat.")
    gambar(d, "results/gambar-metrik.png", 14.5,
           "Gambar 5.2 Perbandingan rata-rata waiting, turnaround, dan response time")

    par(d, "Tabel 5.2 memuat rincian per proses untuk dua algoritma yang paling berbeda "
           "perilakunya, FCFS dan SRTF, sebagai bahan analisis.")
    baris = []
    for label in ("FCFS", "SRTF"):
        for n, m in hasil_json[label]["metrik"].items():
            baris.append((label, n, m["arrival"], m["burst"], m["prio"], m["mulai"],
                          m["selesai"], m["waiting"], m["turnaround"], m["response"]))
    tabel(d, ["Algoritma", "Proses", "Arr", "Burst", "Prio", "Mulai", "Selesai",
              "Wait", "TAT", "Resp"], baris,
          lebar=[2.4, 1.5, 1.2, 1.4, 1.2, 1.4, 1.6, 1.3, 1.3, 1.3], ukuran=8)
    caption(d, "Tabel 5.2 Rincian per proses pada FCFS dan SRTF")

    h2(d, "5.2 Analisis")
    par(d, "Poin (1) deskripsi tugas — Gantt chart dan perhitungan. FCFS menempatkan P1 dan P2 "
           "di depan karena keduanya datang pada waktu nol, sehingga P5 yang hanya butuh dua "
           "tick harus menunggu tujuh belas tick. Inilah efek konvoi: satu proses panjang (P4, "
           "delapan tick) menahan semua di belakangnya. SJF memperbaiki keadaan dengan "
           "menjalankan P5 lebih awal, tetapi tetap non-preemptive sehingga P3 yang datang pada "
           "tick 2 harus menunggu P1 selesai. SRTF adalah satu-satunya algoritma yang memotong "
           "P3 di tengah jalan: saat P5 datang pada tick 4 dengan sisa dua tick, P3 yang tersisa "
           "tiga tick langsung digeser. Karena itu SRTF memberi rata-rata waiting time terendah "
           "(4,80) dan response time terendah di antara algoritma non-Round-Robin (4,40).")
    par(d, "Priority pada dataset ini menghasilkan angka yang persis sama dengan SJF. Itu bukan "
           "kebetulan: urutan prioritas P1(1), P5(1), P3(2), P2(3), P4(4) kebetulan juga urutan "
           "burst terpendek ke terpanjang (3, 2, 4, 6, 8) setelah memperhitungkan waktu "
           "kedatangan. Pada dataset lain keduanya akan berbeda, dan justru di situlah kelemahan "
           "priority scheduling muncul: prioritas tetap dapat membuat proses berprioritas rendah "
           "tidak pernah dilayani.")
    par(d, "Round Robin memperlihatkan trade-off yang jelas. Response time-nya paling baik "
           "(2,60 pada quantum 2) karena setiap proses cepat mendapat giliran pertama. Tetapi "
           "waiting time dan turnaround time-nya paling buruk (8,60 dan 13,20), karena proses "
           "harus kembali ke antrean berkali-kali. Menariknya, quantum 3 memberi rata-rata "
           "waiting dan turnaround yang sama persis dengan quantum 2, tetapi response time-nya "
           "lebih tinggi (4,20). Artinya pada dataset ini quantum 2 lebih baik untuk tugas "
           "interaktif, sedangkan quantum 3 tidak memberi keuntungan apa pun.")
    par(d, "Poin (2) deskripsi tugas — verifikasi simulator. Seluruh enam konfigurasi cocok "
           "dengan hitungan manual sampai dua angka desimal. Kecocokan itu penting karena "
           "simulator yang salah akan menghasilkan rekomendasi yang salah pula, tanpa terlihat "
           "aneh di Gantt chart. Satu hal yang perlu dicatat: penghitungan response time pada "
           "proses yang tidak pernah dipreempt sama dengan waiting time-nya, sehingga FCFS "
           "menghasilkan waiting dan response yang identik (7,40). Pada SRTF keduanya berbeda "
           "(4,80 versus 4,40) justru karena ada preemption.")
    par(d, "Poin (3) deskripsi tugas — rekomendasi untuk konteks kelas. Lihat subbab 5.3.")

    h2(d, "5.3 Rekomendasi")
    par(d, "Untuk gateway kebun pintar, pilihan yang paling sesuai adalah gabungan Priority "
           "dengan preemption untuk tugas kendali, dan Round Robin quantum kecil untuk tugas "
           "pembacaan sensor. Alasannya berbeda dari sekadar mengejar rata-rata terbaik.")
    par(d, "Kontrol pompa irigasi adalah tugas yang harus didahulukan begitu kondisinya muncul, "
           "misalnya saat sensor mendeteksi luapan. Di situ yang dihargai bukan rata-rata "
           "waiting time seluruh proses, melainkan response time tugas tersebut. Priority "
           "scheduling dengan prioritas statis menjamin hal itu, dengan catatan harus ditambah "
           "aging agar tugas latar belakang tidak mati kelaparan.")
    par(d, "Pembacaan sensor bersifat periodik dan pendek, sehingga Round Robin dengan quantum "
           "kecil cocok: setiap sensor mendapat giliran cepat dan tidak ada yang tertahan oleh "
           "sensor lain yang kebetulan lebih panjang. Pada data hasil pengujian, Round Robin "
           "quantum 2 memberi response time terbaik (2,60), dan itulah metrik yang paling "
           "relevan untuk tugas periodik.")
    par(d, "FCFS tidak disarankan meskipun paling sederhana, karena efek konvoi membuat satu "
           "tugas panjang menunda seluruh pembacaan sensor. SRTF memang memberi rata-rata "
           "terbaik pada dataset ini, tetapi penerapannya di perangkat nyata menuntut perkiraan "
           "burst time yang tidak selalu tersedia; untuk gateway kebun, burst time pembacaan "
           "sensor cenderung stabil sehingga SRTF masih layak dipertimbangkan.")


def kesimpulan(d):
    h1(d, "6. Kesimpulan")
    par(d, "Enam konfigurasi penjadwalan berhasil disimulasikan dan seluruhnya cocok dengan "
           "perhitungan manual pada dataset kelas. SRTF memberi rata-rata waiting time terendah "
           "(4,80) karena memotong proses yang tersisa panjang saat ada proses pendek datang. "
           "Round Robin quantum 2 memberi response time terbaik (2,60) dengan mengorbankan "
           "waiting time (8,60). FCFS paling buruk pada kedua metrik akibat efek konvoi. "
           "Priority pada dataset ini setara SJF, tetapi keunggulannya akan hilang begitu pola "
           "kedatangan berubah. Untuk gateway kebun pintar, kombinasi Priority preemptive untuk "
           "tugas kendali dan Round Robin quantum kecil untuk pembacaan sensor adalah pilihan "
           "yang paling sesuai dengan sifat pekerjaannya, bukan sekadar yang rata-ratanya "
           "terendah.")


def kepingan(d):
    h1(d, "7. Kepingan Puzzle")
    tabel(d, ["Keterangan", "Isi"], [
        ("Nomor kepingan", "#5"),
        ("Isi kepingan", "Simulator penjadwalan, Gantt chart keenam algoritma, tabel "
                         "perbandingan metrik, dan rekomendasi algoritma"),
        ("Lokasi di portofolio",
         "https://github.com/ZzDendy/so-k2-penjadwalan"),
        ("Dipakai untuk", "Level 3 Puzzle UTS — menyambung kepingan #4 (IPC) karena proses "
                          "sensor pada K-1 dipetakan menjadi task penjadwalan di sini, dan "
                          "menjadi dasar kepingan #6 (race condition) pada tugas individu I-4"),
    ], lebar=[4.2, 11.0])


def pustaka(d):
    h1(d, "Daftar Pustaka")
    for teks in [
        "Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). Operating system concepts "
        "(10th ed.). Wiley.",
        "Stallings, W. (2018). Operating systems: Internals and design principles (9th ed.). "
        "Pearson.",
        "Tanenbaum, A. S., & Bos, H. (2015). Modern operating systems (4th ed.). Pearson.",
    ]:
        p = d.add_paragraph(style="Normal")
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-1.0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.add_run(teks)


def lampiran(d):
    d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    h1(d, "Lampiran A. Kode Program dan Log")
    par(d, "Seluruh berkas di bawah ini berada pada satu folder proyek dan dapat dijalankan ulang.")
    for nama in ("sched.py", "figures.py"):
        p = d.add_paragraph(style="Normal")
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f"A.{nama}")
        r.bold = True
        r.font.size = Pt(9.5)
        kode(d, baca_berkas(nama), ukuran=7.5)

    h1(d, "Lampiran B. Pernyataan Penggunaan AI Generatif")
    par(d, "☐  Kami tidak menggunakan AI generatif dalam tugas ini.")
    par(d, "☒  Menggunakan AI generatif dengan rincian berikut:")
    tabel(d, ["Alat", "Tujuan penggunaan", "Bagian yang dibantu", "Cara memverifikasi"], [
        ("Claude (Anthropic)", "Menyusun kerangka simulator dan merapikan kalimat laporan",
         "Bagian 4 (kode), Bagian 5.2",
         "Seluruh angka dihitung ulang manual lalu dicocokkan dengan simulator lewat "
         "sched.py --verifikasi"),
    ], lebar=[3.0, 4.4, 4.0, 4.4], ukuran=8.5)

    h1(d, "Lampiran C. Daftar Periksa Sebelum Mengumpulkan")
    for teks, sudah in [
        ("Semua teks petunjuk abu-abu dan kotak petunjuk sudah dihapus.", True),
        ("Identitas, kode tugas, dan nama host pada sampul sudah benar.", True),
        ("Setiap poin deskripsi tugas sudah dijawab di bagian Analisis.", True),
        ("Setiap gambar memiliki nomor dan keterangan.", True),
        ("Kepingan puzzle sudah disimpan di portofolio dan tautannya dicantumkan.", False),
        ("Pernyataan penggunaan AI generatif sudah diisi.", True),
        ("Lembar kontribusi anggota sudah dilampirkan.", True),
        ("Berkas disimpan sebagai PDF dengan nama <Kelas>_<Kode>_<NIM>_<Nama>.pdf.", True),
    ]:
        p = d.add_paragraph(style="Normal")
        p.paragraph_format.space_after = Pt(3)
        p.add_run(f"{'☒' if sudah else '☐'}  {teks}")

    par(d, "")
    h2(d, "Swa-nilai berdasarkan kriteria lembar tugas")
    tabel(d, ["Kriteria (dari lembar tugas)", "Bobot", "Sudah terpenuhi? Di bagian mana"],
          [("Hasil/keberhasilan implementasi", "35%",
            "Ya — enam konfigurasi berjalan, semua cocok dengan hitung manual (Bagian 5.1)"),
           ("Kedalaman analisis", "30%",
            "Ya — efek konvoi, preemption, dan trade-off quantum dibahas (Bagian 5.2)"),
           ("Dokumentasi", "20%",
            "Ya — langkah dapat diulang, kode dan keluaran dilampirkan (Bagian 4, Lampiran A)"),
           ("Kerja sama dan pembagian peran", "15%",
            "Ya — lembar kontribusi pada Lampiran D")],
          lebar=[5.2, 2.0, 8.0])

    h1(d, "Lampiran D. Lembar Kontribusi Anggota", halaman_baru=True)
    par(d, "Lembar ini memenuhi syarat kerja sama dan pembagian peran (15% bobot penilaian) "
           "pada lembar tugas K-2.")
    tabel(d, ["Nama", "NIM", "Peran dan bagian yang dikerjakan"],
          [(n, i, p) for n, i, p in ANGGOTA], lebar=[4.4, 3.0, 7.8])


def main():
    d = docx.Document(TEMPLATE)
    bersihkan(d)
    hasil_json = baca_hasil()

    sampul_k2(d)
    pendahuluan(d)
    dasar_teori(d)
    lingkungan(d)
    langkah(d, hasil_json)
    hasil(d, hasil_json)
    kesimpulan(d)
    kepingan(d)
    pustaka(d)
    lampiran(d)

    header_dokumen(d, "Laporan Tugas Kelompok Sistem Operasi · ", f"{KELAS} · {KODE}")
    nomor_halaman(d)

    d.core_properties.title = "K-2 Simulasi dan Evaluasi Algoritma Penjadwalan CPU"
    d.core_properties.author = NAMA
    d.core_properties.subject = "Sistem Operasi (USA-WP2260110), IF-3C"
    d.core_properties.last_modified_by = NAMA

    os.makedirs("results", exist_ok=True)
    d.save(OUT)
    print("tersimpan:", OUT)


if __name__ == "__main__":
    main()
