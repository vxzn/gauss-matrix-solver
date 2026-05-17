import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp

# --- SETUP LAYOUT PERANGKAT ---
st.set_page_config(page_title="Kalkulator Persamaan Non-Linier Pro", layout="wide")

# --- STYLE CSS MODERN ---
st.markdown("""
<style>
    body { background-color: #FAFAFA; }
    .main-title { color: #1E3A8A; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .sub-title { color: #4B5563; text-align: center; margin-bottom: 25px; font-size: 1rem; }
    .card-calc { background-color: #FFFFFF; border: 1px solid #E5E7EB; padding: 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 20px; }
    .metric-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 15px; border-radius: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>⚡ Gauss-NonLinier Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Platform Analisis Persamaan Non-Linier Interaktif — Kurva Fungsi & Laju Galat Real-Time</p>", unsafe_allow_html=True)

# --- PANEL KONTROL SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan Metode")
    metode = st.selectbox("Pilih Metode Numerik:", ["Metode Biseksi (Bagi Dua)", "Metode Newton-Raphson"])
    st.write("---")
    
    st.markdown("### 📚 Preset Soal Ujian")
    preset = st.selectbox("Pilih Contoh Soal Eksperimen:", [
        "Kustom (Ketik Sendiri)", 
        "Polinomial: x**3 - x - 2", 
        "Trigonometri: x - cos(x)", 
        "Eksponensial: exp(-x) - x"
    ])

# Define default value berdasarkan pilihan preset
default_fungsi = "x**2 - 4"
if "Polinomial" in preset: default_fungsi = "x**3 - x - 2"
elif "Trigonometri" in preset: default_fungsi = "x - cos(x)"
elif "Eksponensial" in preset: default_fungsi = "exp(-x) - x"

# --- INPUT UTAMA USER ---
st.markdown("<div class='card-calc'>", unsafe_allow_html=True)
st.markdown("### 📥 Komponen Input Persamaan")

col1, col2 = st.columns(2)
with col1:
    fungsi_teks = st.text_input("Masukkan Fungsi f(x):", value=default_fungsi)
with col2:
    toleransi = st.number_input("Toleransi Error Maksimum (ε):", min_value=1e-7, max_value=1e-1, value=1e-5, format="%.7f")

# Parsing string fungsi menjadi ekspresi matematika SymPy
x = sp.symbols('x')
valid_fungsi = True
try:
    f_expr = sp.parse_expr(fungsi_teks)
    f = sp.lambdify(x, f_expr, "numpy")
    f_prime_expr = sp.diff(f_expr, x)
    f_prime = sp.lambdify(x, f_prime_expr, "numpy")
except Exception as e:
    st.error(f"Format penulisan fungsi matematika salah! Error: {e}")
    valid_fungsi = False

if valid_fungsi:
    col_param1, col_param2 = st.columns(2)
    if metode == "Metode Biseksi (Bagi Dua)":
        with col_param1: bawah = st.number_input("Batas Bawah Selang (a):", value=0.0)
        with col_param2: atas = st.number_input("Batas Atas Selang (b):", value=3.0)
    else:
        with col_param1: x0 = st.number_input("Nilai Tebakan Awal (x₀):", value=1.0)
st.markdown("</div>", unsafe_allow_html=True)

# --- PROSES KOMPUTASI ---
if valid_fungsi and st.button("PROSES ANALISIS AKAR PERSAMAAN", type="primary", use_container_width=True):
    riwayat_iterasi = []
    konvergen = False
    max_iter = 100
    
    if metode == "Metode Biseksi (Bagi Dua)":
        a, b = bawah, atas
        if f(a) * f(b) >= 0:
            st.error("❌ Syarat Metode Biseksi gagal: f(a) dan f(b) harus berlawanan tanda! Coba lebarkan selang batas bawah/atas Anda.")
            valid_fungsi = False
        else:
            for i in range(1, max_iter + 1):
                c = (a + b) / 2.0
                fc = f(c)
                galat = abs(b - a)
                riwayat_iterasi.append({"Iterasi": i, "Titik Tengah (c)": c, "f(c)": fc, "Error": galat})
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
                st.error("❌ Turunan f'(x) bernilai nol. Perhitungan Newton-Raphson macet.")
                break
            next_x = curr_x - (fx / fdx)
            galat = abs(next_x - curr_x)
            riwayat_iterasi.append({"Iterasi": i, "Titik x_n": curr_x, "f(x_n)": fx, "Error": galat})
            if galat < toleransi:
                akar_final = next_x
                konvergen = True
                break
            curr_x = next_x

    # ==========================================
    # 📊 SEKSI OUTPUT VISUALISASI MODERN
    # ==========================================
    if konvergen:
        st.write("---")
        st.success(f"🎯 **Sistem Berhasil Konvergen!** Akar ditemukan pada tingkat iterasi ke-{len(riwayat_iterasi)}.")
        
        # Kartu Skor Metrik
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"<div class='metric-box'><p style='color:#6B7280;margin:0;'>AKAR PERSAMAAN (x)</p><h2 style='color:#1E3A8A;margin:5px 0 0 0;'>{akar_final:.6f}</h2></div>", unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"<div class='metric-box'><p style='color:#6B7280;margin:0;'>NILAI AKHIR f(x)</p><h2 style='color:#10B981;margin:5px 0 0 0;'>{f(akar_final):.2e}</h2></div>", unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"<div class='metric-box'><p style='color:#6B7280;margin:0;'>TOTAL ITERASI</p><h2 style='color:#F59E0B;margin:5px 0 0 0;'>{len(riwayat_iterasi)}</h2></div>", unsafe_allow_html=True)
            
        st.write("")
        
        # FITUR BARU: VISUALISASI 2 GRAFIK SEKALIGUS (KURVA FUNGSI VS LAJU GALAT)
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            st.markdown("#### 📉 Visualisasi Kurva Geometri $f(x)$")
            # Membuat koordinat plot di sekitar lokasi akar
            x_vals = np.linspace(akar_final - 3, akar_final + 3, 200)
            try:
                y_vals = f(x_vals)
                df_chart = pd.DataFrame({"Sumbu X": x_vals, "Fungsi f(x)": y_vals})
                st.line_chart(df_chart, x="Sumbu X", y="Fungsi f(x)")
                st.caption("Grafik di atas mendeteksi letak lengkungan fungsi Anda melintasi garis nol (sumbu-X).")
            except:
                st.warning("Gagal memuat grafik kurva untuk fungsi ini.")

        with col_graph2:
            st.markdown("#### 📉 Laju Penurunan Tingkat Galat (Error)")
            df_iter = pd.DataFrame(riwayat_iterasi)
            st.line_chart(df_iter, x="Iterasi", y="Error")
            st.caption("Aplikasi menunjukkan grafik nilai galat yang turun drastis mendekati batas toleransi Anda.")
            
        # Tabel Riwayat
        st.write("")
        st.markdown("### 📋 Log Tabel Riwayat Langkah Iterasi")
        st.dataframe(df_iter, use_container_width=True)
