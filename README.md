# TASKSCAPE — Maze Deadline Dodger

TASKSCAPE merupakan permainan maze chase game yang dibangun menggunakan **Python dan Pygame**, tema yang diakses berhubungan dengan kehidupan asli mahasiswa yang dikejar oleh deadline tugas. Mengumpulkan **tugas** berupa dots yang tersebar sepanjang maze yang telah digenerate sambil menghindar agen **Dosen**, yang masing-masing memiliki AI yang berbeda mencakup Informed Search dan bahkan Reinforcement Learning.

Setiap progress melalui tiap semester dirancang dengan kesulitan yang bertahap, survive endless Skripsi Mode, dan mengejar posisi pertama dalam local leaderboard.

---

## Kelompok Machine Learning for Intelligence System:
1. Felycia Edelyne Irwan
2. George Ananda
3. Rosselle Amelia Christy
4. Adrian Lemuel Iskandar
5. Ni Gusti Agung Ayu Evangelina Budidarma
---

## Fitur

- **Procedurally generated mazes** menggunakan recursive backtracking dengan layout yang bisa berubah secara dinamis
- **Four ghost AI types** dengan algoritma ML yang berbeda:
  - *Dosen Killer* — Breadth First Search yang akan menemukan rute terpendek menuju pemain
  - *Dosen Galak* — greedy dan pergerakan random untuk mengecoh pemain
  - *Dosen AI* — Q-Learning yang bisa dengan adaptif mengubah strategi pengejaran pemain
  - *Dosen Skripsi* — pergerakan berbasis heatmap yang bisa mengincar area yang paling sering dilewati pemain
- **5 difficulty tiers** mulai dari Semester 1 hingga Semester 7, yang dilengkapi dengan mode Trial dan Skipsi Mode dengan scaling infinite
- **Power-ups**: extra nyawa, ghost melambat, ghost beku, perisai, dan magnet dots
- **Maze reshuffling** berdasarkan timer countdown yang terus berjalan
- **Lives, scoring, and combo bonuses** setiap berhasil menyelesaikan level
- **Player login screen** dengan avatar yang bebas dipilih oleh pemain (Mahasiswi, Mahasiswa, Lumba-lumba, Si Ngantuk, Kucing Kopi, dan Zombie SKS)
- **Local JSON leaderboard** untuk melacak top scores, jumlah dots yang sudah dikumpulkan, level yang berhasil diraih, dan tanggal
- **Sound effects** untuk mengumpulkan dots, level up, dan game over
- Tambahan splash screen, menu pause, countdown, dan layar konfirmasi setiap menyelesaikan level
---

## Mode Permainan

| Level | Label | Maze Size | Ghosts | Timer |
|---|---|---|---|---|
| Trial | TRIAL | 9×9 | 1 | Off |
| 1 | Semester 1 | 13×13 | 2 | 30s |
| 2 | Semester 3 | 15×15 | 3 | 25s |
| 3 | Semester 5 | 17×17 | 3 | 22s |
| 4 | Semester 7 | 19×19 | 4 | 20s |
| ∞ | SKRIPSI MODE | dynamic, scaling | 4 | 20s |

Setiap menyelesaikan level akan memperoleh bonus points dan extra nyawa.\

---

## Kontrol

| Action | Keys |
|---|---|
| Move | Arrow keys or `W` `A` `S` `D` |
| Pause / Resume | `P` |
| Confirm / Retry | `Enter` or `Space` |
| Back / Cancel | `Esc` |
| Menus, avatars, buttons | Mouse click |
---

## Power-ups

| Power-up | Effect |
|---|---|
| ❤️ Extra Life | Menambah nyawa +1 secara instan (maksimal 9) |
| 🐢 Dosen Lambat | Memperlambat semua ghost dalam 9 detik |
| ❄️ Dosen Beku | Membekukan semua ghost dalam 8 detik |
| 🛡️ Perisai | Memblocking 1 ghost |
| 🧲 Tugas Magnet | Menarik dots yang terdekat dalam 13 detik |

Power ups akan muncul dalam periode tertentu dalam maze dan akan menghilang apabila tidak diambil dalam jangka waktu tertentu.

---

## Struktur Project

```
taskscape/
├── taskscape_sound.py        # Permainan utama dengan sound effect (paling direkomendasikan)
├── taskscape_fix.py          # Permainan yang sama, namun tanpa suara
├── taskscape_leaderboard.json # Leaderboard local untuk menyimpan file (autocreated)
├── assets/                    # UI icon, logo, dan aset lain yang dibutuhkan dalam game
└── sfx/                       # Sound effects (MP3): gameover, levelup, tugasbits
```
> Kedua file `.py` memiliki versi yang hampir sama, `taskscape_sound.py` dibangun menggunakan layout `taskscape_fix.py` yang diberi sound effect sehingga file ini bisa digunakan jika ingin dimainkan tanpa suara.
---

## Requirements

- Python 3.9+
- [Pygame](https://www.pygame.org/) (`pip install pygame`)
- [NumPy](https://numpy.org/) (`pip install numpy`)

```bash
pip install pygame numpy
```

## Menjalankan permainan

```bash
python taskscape_sound.py
```

Pastikan folder `assets/` (dan `sfx/` untuk versi suara) terdapat di samping script - semua path asset berhubungan dengan lokasi file utama. Icon atau file sound yang hilang telah diatasi dengan baik dan tidak akan crash dalam permainan.

---

## Leaderboard
Skor otomatis tersimpan dalam `taskscape_leaderboard.json` di directory yang sama dengan script. Setiap records score yang masuk, level yang tercapai, jumlah dots yang diperoleh, dan nama pemain akan disimpan dalam leaderboard (top 20 pemain).

---

## Dokumentasi Kontribusi
1. Felycia Edelyne Irwan: melakukan generate maze (dinamis dan struktur maze bisa dijangkau oleh pemain), merancang avatar dan splash screen, merubah tema permainan, melatih ghost dengan AI yang beragam, dan melakukan testing
2. George Ananda: merancang power ups, membuat login dan escape button, melatih ghost dengan AI yang beragam, dan sistem lives yang bertambah setelah menyelesaikan level, dan melakukan testing
3. Rosselle Amelia Christy: mendesain UI games dan mencari icon yang sesuai dengan penggunaan dalam game, desain logo games, dan melakukan testing
4. Adrian Lemuel Iskandar: memasukkan hasil dari permainan kedalam leaderboard dan melakukan testing
5. Ni Gusti Agung Ayu Evangelina Budidarma: menambahkan sound effect pada permainan games dan melakukan testing

