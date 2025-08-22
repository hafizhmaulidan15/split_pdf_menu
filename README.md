# PDF Menu Splitter 🔪

<p align="center">
  <img style="margin-right: 8px;" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img style="margin-right: 8px;" src="https://img.shields.io/badge/PyPDF2-FFD43B?style=for-the-badge&logo=adobeacrobatreader&logoColor=black" alt="PyPDF2">
</p>

**PDF Menu Splitter** adalah aplikasi berbasis Python sederhana yang memanfaatkan pustaka **PyPDF2** untuk memisahkan file PDF dengan cepat.  
Cocok digunakan untuk laporan panjang, dokumen akademik, e-book, atau PDF lain yang perlu dipecah menjadi bagian lebih kecil.  

---

## ✨ Fitur Utama

*   **Ambil Satu Halaman 📄**: Ekstrak 1 halaman tertentu dari PDF.  
*   **Ambil Rentang Halaman 📑**: Pisahkan beberapa halaman berurutan (misal `10-15`).  
*   **Multi Seleksi 🗂**: Kombinasi halaman/rentang (misal `1,3,5-7,12`).  
*   **Halaman + Sisanya ➗**: Simpan halaman tertentu di satu file, sisanya ke file lain.  
*   **Split Semua 📚**: Pecah seluruh PDF sehingga setiap halaman jadi file PDF terpisah.  

---

## 🛠️ Tech Stack

*   Python 3.8+  
*   PyPDF2  

---

## 🚀 Instalasi & Menjalankan

1. Clone repositori:  
   ```bash
   git clone https://github.com/hafizhmaulidan15/split_pdf_menu
   cd split_pdf_menu

2. Install dependensi:

   ```bash
   pip install PyPDF2
   ```

3. Jalankan aplikasi:

   ```bash
   python split_pdf_menu.py
   ```

4. Ikuti instruksi pada terminal:

   * Masukkan path file PDF (contoh: `"D:\Dokumen\laporan.pdf"`)
   * Pilih opsi (1–5)
   * Masukkan nomor/rentang halaman sesuai kebutuhan

---

## 📖 Contoh Penggunaan

**Ekstrak halaman 6**

```
=== Split PDF (Menu) ===
Path PDF sumber: "D:\Dokumen\laporan.pdf"
Prefix nama file output (default: 'hasil'): output
📄 Total halaman: 60

=== Opsi ===
1) Ambil 1 halaman
2) Ambil rentang halaman
3) Ambil multi seleksi
4) Ambil 1 halaman + sisanya
5) Split semua halaman ke file terpisah
Pilih opsi (1-5): 1
Nomor halaman: 6
➡️  Akan mengekstrak halaman 6.
Lanjut eksekusi? [y/N]: y
✅ Berhasil: output_hal_06.pdf
```

**Split semua halaman →** output:

```
output_hal_01.pdf, output_hal_02.pdf, ... output_hal_60.pdf
```

---

## 🤝 Kontribusi

Kontribusi sangat terbuka!

1. Fork repo ini
2. Buat branch fitur baru:

   ```bash
   git checkout -b feature/nama-fitur
   ```
3. Commit perubahan Anda:

   ```bash
   git commit -m "feat: tambahkan fitur baru"
   ```
4. Push ke branch:

   ```bash
   git push origin feature/nama-fitur
   ```
5. Buat Pull Request

