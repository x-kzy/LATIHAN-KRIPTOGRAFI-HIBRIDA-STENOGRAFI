# LATIHAN-KRIPTOGRAFI-HIBRIDA-STENOGRAFI

Repository ini dikembangkan oleh **Havidz ANDRIAN** (NIM: 231118899), IF-C Pagi, Universitas Mikroskil. Project ini berisi implementasi sistem keamanan data menggunakan pendekatan **Kriptografi Hibrida** yang diintegrasikan dengan **Steganografi**.

# Tentang Program
Program `hybridcript.py` adalah sebuah antarmuka *Command Line* (CLI) interaktif yang menggabungkan berbagai algoritma kriptografi menjadi satu alur keamanan berlapis.

Tujuan utama dari program ini adalah:
* **Keamanan Hibrida:** Menggabungkan efisiensi enkripsi simetris (AES-GCM) dengan keamanan distribusi kunci asimetris (RSA & Diffie-Hellman).
* **Integritas & Autentikasi Data:** Memastikan data tidak diubah selama proses transmisi menggunakan fungsi *hash* (SHA-256) dan Tanda Tangan Digital (DSA).
* **Steganografi (Penyembunyian Data):** Menyamarkan paket data yang sudah dienkripsi ke dalam media file gambar (BMP) menggunakan teknik *Least Significant Bit* (LSB), sehingga informasi rahasia tidak memancing kecurigaan pihak ketiga.

# Fitur Utama
* **Manajemen Kunci:** Pembuatan pasangan kunci RSA dan DSA, serta simulasi pertukaran kunci terautentikasi (Diffie-Hellman + RSA Auth).
* **Enkripsi & Dekripsi:** Menggunakan standar AES-256 mode GCM.
* **Digital Signature:** Pembuatan dan verifikasi tanda tangan digital secara presisi.
* **Steganografi Terintegrasi:** Fitur untuk menyembunyikan dan mengekstrak pesan rahasia secara aman dari dalam gambar *cover*.
* **Sistem Log:** Mencatat dan menampilkan seluruh riwayat aksi eksperimen selama program berjalan.

# Cara Menjalankan Program
Pastikan device anda sudah menginstal Python. Berikut adalah langkah-langkah untuk menjalankan program ini menggunakan Visual Studio Code:
1. **Unduh** file `hybridcript.py`
2. Buka aplikasi **Visual Studio Code**.
3. Buka terminal bawaan VS Code dengan mengklik menu **Terminal > New Terminal** di bagian atas.
4. Program ini membutuhkan *library* eksternal `pycryptodome`. Lakukan instalasi dengan menjalankan perintah berikut di terminal:
```bash
pip install pycryptodome

```
5. Setelah instalasi berhasil, tekan tombol **F5** atau **CTRL+F5** untuk menjalankan program pada terminal anda.
6. Program akan langsung beroperasi di terminal dan siap digunakan.
7. Selesai.

# Contoh Penggunaan Singkat
Berikut adalah skenario dasar jika anda ingin mengenkripsi dan menyembunyikan pesan rahasia ke dalam sebuah gambar:
1. Jalankan program dan pilih **Menu 1** untuk *Generate* Kunci RSA + DSA (tekan *Enter* untuk menggunakan ukuran *default*).
2. Pilih **Menu 8** (Steganografi - Sembunyikan Pesan Aman ke Gambar).
3. Program akan meminta *cover* gambar. Pilih opsi **1** untuk melakukan *generate demo BMP*. Program akan membuat file dasar secara otomatis.
4. Masukkan pesan rahasia yang ingin dilindungi (contoh: `Ini adalah pesan sangat rahasia`).
5. Tentukan nama file *output* (contoh: `gambar_rahasia.bmp`).
6. Selesai! Pesan Anda kini telah dienkripsi, ditandatangani, dan disembunyikan dengan aman di dalam gambar `gambar_rahasia.bmp`.

**Contoh Output di Terminal:**

```text
STATUS SISTEM SAAT INI:
+-----------------------------------+------------+
| Komponen                          | Status     |
+-----------------------------------+------------+
| Diffie-Hellman + RSA Auth         | NONAKTIF   |
| AES Session Key                   | NONAKTIF   |
| RSA Keys                          | AKTIF      |
| DSA Keys                          | AKTIF      |
...

Pesan berhasil disembunyikan!
 Cover: demo_cover.bmp
 Output: gambar_rahasia.bmp
 Bits disisipkan: 13456
 Ukuran pesan: 33 bytes
 Pipeline: SHA256 -> DSA Sign -> AES-GCM Encrypt -> RSA Encrypt AES Key -> LSB Stego
 Scheme : HYBRID-STEGO-INTEGRATED-V2

```

*(Untuk membaca dan mengekstrak kembali pesan tersebut, Anda cukup menggunakan **Menu 9** dan memasukkan nama file gambar yang telah diproses).*
Untuk hasil lebih lanjut disarankan melakukan percobaan secara mandiri dan bisa menonton video yang telah saya buat terkait pembahasan programnya.
