import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp

# --- SETUP LAYOUT PERANGKAT ---
st.set_page_config(page_title="Kalkulator Non-Linier Pintar", layout="wide")

# --- STYLE CSS MODERN ---
st.markdown("""
<style>
    body { background-color: #FAFAFA; }
    .main-title { color: #1E3A8A; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .sub-title { color: #4B5563; text-align: center; margin-bottom: 25px; font-size: 1rem; }
    .card-calc { background-color: #FFFFFF; border: 1px solid #E5E7EB; padding: 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 20px; }
    .hint-box { background-color: #F0FDF4; border: 1px solid #BBF7D0; color: #166534; padding: 12px; border-radius: 8px; margin-bottom: 15px; font-size: 0.9rem; }
    .metric-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 15px; border-radius: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🌱 Kalkulator Non-Linier Pintar</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Cara mudah dan interaktif memahami pencarian akar persamaan matematika f(x) = 0</p>", unsafe_allow_html=True)

# --- PANEL KONTROL SIDEBAR ---
with st.sidebar:
    st.markdown("### 🧠 Pilih Gaya Belajar")
    metode = st.selectbox("Pilih Cara Kerja Mesin:", ["Metode Biseksi (Bagi Dua Selang)", "Metode Newton-Raphson (Garis Singgung)"])
    
    st.write("---")
    st.markdown("### 🎯 Tingkat Keakuratan Hasil")
    keakuratan = st.select_slider(
        "Pilih tingkat ketelitian:",
        options=["Standar (Cepat)", "Akurat (Rekomendasi)", "Super Detail"],
        value="Akurat (Rekomendasi)"
    )
    
    # Konversi bahasa santai ke nilai matematika epsilon
    if keakuratan == "Standar (Cepat)": toleransi = 1e-3
    elif keakuratan == "Akurat (Rekomendasi)": toleransi = 1e-5
    else: toleransi = 1e-7

# --- INPUT UTAMA USER ---
st.markdown("<div class='card-calc'>", unsafe_allow_html=True)
st.markdown("### 📥 1. Tulis Persamaan Matematika Anda")

fungsi_teks = st.text_input("Ketik fungsi di sini (Gunakan x sebagai variabel):", value="x**2 - 4", help="Contoh: x**2 - 4 atau x**3 - x - 2")

# Parsing string fungsi menjadi ekspresi matematika SymPy
x = sp.symbols('x')
valid_fungsi = True
try:
    f_expr = sp.parse_expr(fungsi_teks)
    f = sp.lambdify(x, f_expr, "numpy")
    f_prime_expr = sp.diff(f_expr, x)
    f_prime = sp.lambdify(x, f_prime_expr, "numpy")
except Exception as e:
    st.error(f"Format penulisan salah. Pastikan perkalian ditulis pakai bintang *, contoh: 3*x")
    valid_fungsi = False

# --- FITUR PINTAR: SCANNING AKAR OTOMATIS UNTUK PEMULA ---
if valid_fungsi:
    st.write("---")
    st.markdown("### 💡 2. Panduan Angka Input (Asisten Pintar)")
    
    # Scan tanda fungsi dari x = -10 sampai 10 untuk mencari perubahan tanda (lokasi akar)
    scan_x = np.linspace(-10, 10, 50)
    saran_a, saran_b = None, None
    try:
        scan_y = f(scan_x)
        for idx in range(len(scan_x) - 1):
            if scan_y[idx] * scan_y[idx+1] < 0: # Ada perubahan tanda positif/negatif (berarti ada akar!)
                saran_a = float(round(scan_x[idx], 1))
                saran_b = float(round(scan_x[idx+1], 1))
                break
    except:
        pass

    # Berikan rekomendasi teks yang sangat manusiawi
    if saran_a is not None and saran_b is not None:
        st.markdown(f"""
        <div class='hint-box'>
            <b>✨ Asisten Pintar Mendeteksi:</b> Grafik fungsi Anda memotong garis nol di antara angka <b>{saran_a}</b> dan <b>{saran_b}</b>.<br>
            Gunakan angka saran ini pada kolom input di bawah agar kalkulator bekerja dengan sukses!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='hint-box' style='background-color:#FFFBEB; border-color:#FEF3C7; color:#92400E;'>
            <b>💡 Tips Pemula:</b> Cobalah memasukkan angka rentang kecil seperti 0 sampai 3 terlebih dahulu untuk melihat bentuk kurva fungsinya.
        </div>
        """, unsafe_allow_html=True)

    # Tampilkan kolom parameter input berdasarkan saran otomatis
    col_param1, col_param2 = st.columns(2)
    if "Biseksi" in metode:
        with col_param1: 
            val_a = saran_a if saran_a is not None else 0.0
            bawah = st.number_input("Masukkan Batas Kiri (a):", value=val_a)
        with col_param2: 
            val_b = saran_b if saran_b is not None else 3.0
            atas = st.number_input("Masukkan Batas Kanan (b):", value=val_b)
    else:
        with col_param1: 
            val_x0 = saran_a if saran_a is not None else 1.0
            x0 = st.number_input("Masukkan Titik Tebakan Awal (x₀):", value=val_x0)
st.markdown("</div>", unsafe_allow_html=True)

# --- PROSES KOMPUTASI ---
if valid_fungsi and st.button("🚀 MULAI CARI JAWABAN PERSAMAAN", type="primary", use_container_width=True):
    riwayat_iterasi = []
    konvergen = False
    max_iter = 100
    
    if "Biseksi" in metode:
        a, b = bawah, atas
        if f(a) * f(b) >= 0:
            st.error("❌ Waduh, kalkulator gagal memproses! Angka Batas Kiri dan Batas Kanan yang Anda masukkan tidak mengurung akar. Silakan ikuti kotak hijau panduan asisten di atas.")
            valid_fungsi = False
        else:
            for i in range(1, max_iter + 1):
                c = (a + b) / 2.0
                fc = f(c)
                galat = abs(b - a)
                riwayat_iterasi.append({"Langkah ke-": i, "Batas Kiri (a)": a, "Batas Kanan (b)": b, "Titik Tengah (c)": c, "Nilai Fungsi f(c)": fc, "Sisa Error": galat})
                if galat < toleransi or abs(fc) < 1e-12:
                    akar_final = c
                    konvergen = True
                    break
                if f(a) * fc < 0: b = c
                else: a = c
    else:
        curr_x = x0
        for i in range(1, max_iter + 1):
            fx = f(curr_x)
            fdx = f_prime(curr_x)
            if abs(fdx) < 1e-12:
                st.error("❌ Tebakan awal Anda membuat grafik mendatar (turunan = 0). Silakan ganti angka tebakan awal Anda dengan angka lain.")
                break
            next_x = curr_x - (fx / fdx)
            galat = abs(next_x - curr_x)
            riwayat_iterasi.append({"Langkah ke-": i, "Titik Tebakan": curr_x, "Nilai Fungsi f(x)": fx, "Sisa Error": galat})
            if galat < toleransi:
                akar_final = next_x
                konvergen = True
                break
            curr_x = next_x

    # ==========================================
    # 📊 SEKSI KESIMPULAN BAHASA MANUSIA
    # ==========================================
    if konvergen:
        st.write("---")
        st.balloons()
        
        # Kartu Hasil Utama Bahasa Sederhana
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"<div class='metric-box'><p style='color:#6B7280;margin:0;font-size:0.85rem;'>🔑 TITIK POTONG (AKAR X)</p><h2 style='color:#1E3A8A;margin:5px 0 0 0;'>{akar_final:.5f}</h2></div>", unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"<div class='metric-box'><p style='color:#6B7280;margin:0;font-size:0.85rem;'>📉 AKURASI ERROR AKHIR</p><h2 style='color:#10B981;margin:5px 0 0 0;'>{galat:.2e}</h2></div>", unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"<div class='metric-box'><p style='color:#6B7280;margin:0;font-size:0.85rem;'>⏱️ TOTAL PERCOBAAN MESIN</p><h2 style='color:#F59E0B;margin:5px 0 0 0;'>{len(riwayat_iterasi)} Kali</h2></div>", unsafe_allow_html=True)
            
        st.write("")
        
        # Penjelasan Edukatif Kesimpulan
        st.markdown(f"""
        ### 📖 Kesimpulan Analisis (Cara Membaca Hasil):
        Kalkulator telah melakukan percobaan pengulangan sebanyak **{len(riwayat_iterasi)} kali**. Kesimpulannya, jika Anda memasukkan angka **{akar_final:.5f}** ke dalam variabel $x$ pada fungsi `${sp.latex(f_expr)}$,$` maka hasil persamaannya akan menjadi **0** (atau mendekati nol dengan tingkat eror yang sangat kecil sebesar `{galat:.2e}`).
        """)
        
        # Visualisasi Grafik
        col_graph1, col_graph2 = st.columns(2)
        with col_graph1:
            st.markdown("#### 📈 Di mana letak akarnya pada grafik?")
            x_vals = np.linspace(akar_final - 4, akar_final + 4, 200)
            try:
                y_vals = f(x_vals)
                df_chart = pd.DataFrame({"Sumbu X": x_vals, "Kurva Fungsi": y_vals})
                st.line_chart(df_chart, x="Sumbu X", y="Kurva Fungsi")
                st.caption("Akar persamaan adalah titik tempat kurva memotong garis horizontal tengah (Sumbu X=0).")
            except:
                st.warning("Grafik tidak mendukung format fungsi kompleks.")

        with col_graph2:
            st.markdown("#### 📉 Bagaimana mesin memperkecil kesalahan?")
            df_iter = pd.DataFrame(riwayat_iterasi)
            st.line_chart(df_iter, x="Langkah ke-", y="Sisa Error")
            st.caption("Grafik menunjukkan bagaimana eror/kesalahan tebakan menyusut drastis menuju nol seiring bertambahnya langkah percobaan.")
            
        # Tabel Detail Langkah
        with st.expander("📋 Lihat tabel detail langkah demi langkah matematika (Untuk Tugas Kuliah)"):
            st.dataframe(df_iter, use_container_width=True)
