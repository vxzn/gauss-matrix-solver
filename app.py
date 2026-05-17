import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp

# --- SETUP LAYOUT PERANGKAT ---
st.set_page_config(page_title="Kalkulator Non-Linier Pintar Pro", layout="wide")

# --- STYLE CSS MODERN (NYAMAN DI HP & LAPTOP) ---
st.markdown("""
<style>
    body { background-color: #FAFAFA; }
    .main-title { color: #1E3A8A; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .sub-title { color: #4B5563; text-align: center; margin-bottom: 25px; font-size: 1rem; }
    .card-calc { background-color: #FFFFFF; border: 1px solid #E5E7EB; padding: 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 20px; }
    .hint-box { background-color: #F0FDF4; border: 1px solid #BBF7D0; color: #166534; padding: 12px; border-radius: 8px; margin-bottom: 15px; font-size: 0.9rem; }
    .metric-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 15px; border-radius: 10px; text-align: center; }
    
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: column !important;
            gap: 10px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🌱 Kalkulator Persamaan Non-Linier</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Analisis Pencarian Akar Komputasi Numerik Interaktif — Bebas Eror & Ramah Pemula</p>", unsafe_allow_html=True)

# --- PANEL KONTROL SIDEBAR ---
with st.sidebar:
    st.markdown("### 🧠 Metode Komputasi")
    metode = st.selectbox("Pilih Cara Kerja Mesin:", ["Metode Biseksi (Bagi Dua Selang)", "Metode Newton-Raphson (Garis Singgung)"])
    
    st.write("---")
    st.markdown("### 🎯 Tingkat Keakuratan Hasil")
    keakuratan = st.select_slider(
        "Pilih tingkat ketelitian:",
        options=["Standar (Cepat)", "Akurat (Rekomendasi)", "Super Detail"],
        value="Akurat (Rekomendasi)"
    )
    
    # Konversi bahasa santai ke nilai matematika epsilon toleransi error
    if keakuratan == "Standar (Cepat)": 
        toleransi = 1e-3
    elif keakuratan == "Akurat (Rekomendasi)": 
        toleransi = 1e-5
    else: 
        toleransi = 1e-7

    st.write("---")
    st.markdown("### 📚 Preset Soal Eksperimen")
    preset = st.selectbox("Pilih Contoh Soal:", [
        "Kustom (Ketik Sendiri)", 
        "Polinomial: x**3 - x - 2", 
        "Trigonometri: x - cos(x)", 
        "Eksponensial: exp(-x) - x"
    ])

# Definisikan nilai input fungsi bawaan berdasarkan preset yang dipilih
default_fungsi = "x**2 - 4"
if "Polinomial" in preset: 
    default_fungsi = "x**3 - x - 2"
elif "Trigonometri" in preset: 
    default_fungsi = "x - cos(x)"
elif "Eksponensial" in preset: 
    default_fungsi = "exp(-x) - x"

# --- INPUT UTAMA USER ---
st.markdown("<div class='card-calc'>", unsafe_allow_html=True)
st.markdown("### 📥 1. Tulis Persamaan Matematika Anda")

fungsi_teks = st.text_input("Ketik fungsi di sini (Gunakan variabel x):", value=default_fungsi, help="Gunakan ** untuk pangkat dan * untuk perkalian. Contoh: x**2 - 4")

# --- PARSING FUNGSI MATEMATIKA (VERSI AMAN & ANTI-TYPEROR) ---
x = sp.symbols('x')
valid_fungsi = True

try:
    f_expr = sp.parse_expr(fungsi_teks)
    
    # Fungsi pembantu menggunakan evaluasi numerik float murni (.evalf()) agar bebas eror tipe data
    def hitung_f(nilai_x):
        return float(f_expr.subs(x, nilai_x).evalf())
        
    # Otomatis menghitung turunan kalkulus untuk metode Newton-Raphson
    f_prime_expr = sp.diff(f_expr, x)
    def hitung_f_prime(nilai_x):
        return float(f_prime_expr.subs(x, nilai_x).evalf())

except Exception as e:
    st.error(f"Format penulisan salah! Pastikan perkalian ditulis eksplisit menggunakan bintang (*). Contoh: 3*x")
    valid_fungsi = False

# --- ASISTEN PINTAR: SCANNING AKAR OTOMATIS ---
if valid_fungsi:
    st.write("---")
    st.markdown("### 💡 2. Panduan Angka Input (Asisten Pintar)")
    
    # Memindai tanda fungsi dari koordinat x = -10 sampai 10 untuk mendeteksi letak akar asli
    scan_x = np.linspace(-10, 10, 100)
    saran_a, saran_b = None, None
    try:
        for idx in range(len(scan_x) - 1):
            if hitung_f(scan_x[idx]) * hitung_f(scan_x[idx+1]) < 0:
                saran_a = float(round(scan_x[idx], 1))
                saran_b = float(round(scan_x[idx+1], 1))
                break
    except:
        pass

    # Menampilkan notifikasi bantuan bagi pengguna awam
    if saran_a is not None and saran_b is not None:
        st.markdown(f"""
        <div class='hint-box'>
            <b>✨ Asisten Pintar Mendeteksi:</b> Grafik fungsi Anda terdeteksi memotong garis nol di antara angka <b>{saran_a}</b> dan <b>{saran_b}</b>.<br>
            Gunakan angka saran ini pada kolom input di bawah agar kalkulator Anda dijamin sukses melakukan perhitungan!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='hint-box' style='background-color:#FFFBEB; border-color:#FEF3C7; color:#92400E;'>
            <b>💡 Tips Pemula:</b> Jika asisten gagal mendeteksi, cobalah memasukkan angka rentang 0 sampai 3 terlebih dahulu untuk melihat analisis kurvanya.
        </div>
        """, unsafe_allow_html=True)

    # Menampilkan kolom parameter input dinamis berdasarkan metode yang aktif
    col_param1, col_param2 = st.columns(2)
    if "Biseksi" in metode:
        with col_param1: 
            val_a = saran_a if saran_a is not None else 0.0
            bawah = st.number_input("Masukkan Batas Kiri (a):", value=val_a, step=0.1)
        with col_param2: 
            val_b = saran_b if saran_b is not None else 3.0
            atas = st.number_input
