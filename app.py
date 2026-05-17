import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp

# --- SETUP LAYOUT PERANGKAT ---
st.set_page_config(page_title="Kalkulator Persamaan Non-Linier", layout="wide")

# --- STYLE CSS AGAR PAS DI LAYAR HP (ANTI-SCROLL) ---
st.markdown("""
<style>
    body { background-color: #FAFAFA; }
    .main-title { color: #1E3A8A; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .sub-title { color: #4B5563; text-align: center; margin-bottom: 25px; font-size: 1rem; }
    .card-calc { background-color: #FFFFFF; border: 1px solid #E5E7EB; padding: 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 20px; }
    
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: column !important;
            gap: 10px !important;
        }
        .stButton>button { width: 100% !important; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📈 Kalkulator Persamaan Non-Linier</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Mencari akar persamaan f(x) = 0 menggunakan Metode Numerik Biseksi & Newton-Raphson</p>", unsafe_allow_html=True)

# --- PANEL KONTROL SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan Metode")
    metode = st.selectbox("Pilih Metode Numerik:", ["Metode Biseksi (Bagi Dua)", "Metode Newton-Raphson"])
    st.write("---")
    st.markdown("""
    **Panduan Penulisan Fungsi:**
    * Pangkat menggunakan `**` (Contoh: $x^2$ ditulis `x**2`)
    * Perkalian menggunakan `*` (Contoh: $3x$ ditulis `3*x`)
    * Fungsi lain: `sin(x)`, `cos(x)`, `exp(x)`
    """)

# --- INPUT UTAMA USER ---
st.markdown("<div class='card-calc'>", unsafe_allow_html=True)
st.markdown("### 📥 Komponen Input Persamaan")

col1, col2 = st.columns(2)
with col1:
    fungsi_teks = st.text_input("Masukkan Fungsi f(x):", value="x**2 - 4", help="Contoh: x**2 - 4 atau x**3 - x - 2")
with col2:
    toleransi = st.number_input("Toleransi Error (ε):", min_value=1e-7, max_value=1e-1, value=1e-4, format="%.7f")

# Parsing string fungsi menjadi ekspresi matematika SymPy
x = sp.symbols('x')
try:
    f_expr = sp.parse_expr(fungsi_teks)
    f = sp.lambdify(x, f_expr, "numpy")
    
    # Hitung turunan otomatis untuk Newton-Raphson
    f_prime_expr = sp.diff(f_expr, x)
    f_prime = sp.lambdify(x, f_prime_expr, "numpy")
    valid_fungsi = True
except Exception as e:
    st.error(f"Format fungsi salah! Silakan periksa penulisan variabel. Error: {e}")
    valid_fungsi = False

# --- INPUT PARAMETER AWAL BERDASARKAN METODE ---
if valid_fungsi:
    col_param1, col_param2 = st.columns(2)
    if metode == "Metode Biseksi (Bagi Dua)":
        with col_param1:
            bawah = st.number_input("Batas Bawah (a):", value=0.0)
        with col_param2:
            atas = st.number_input("Batas Atas (b):", value=3.0)
    else:
        with col_param1:
            x0 = st.number_input("Tebakan Awal (x₀):", value=1.0)
st.markdown("</div>", unsafe_allow_html=True)

# --- TOMBOL EKSEKUSI PROSES KOMPUTASI ---
if valid_fungsi and st.button("PROSES PENCARIAN AKAR PERSAMAAN", type="primary", use_container_width=True):
    riwayat_iterasi = []
    konvergen = False
    max_iter = 100
    
    # ==========================================
    # 🟦 LOGIKA METODE BISEKSI
    # ==========================================
    if metode == "Metode Biseksi (Bagi Dua)":
        a = bawah
        b = atas
        
        if f(a) * f(b) >= 0:
            st.error("❌ Nilai f(a) dan f(b) harus memiliki tanda yang berbeda (f(a) × f(b) < 0). Akar tidak berada di dalam selang ini!")
        else:
            for i in range(1, max_iter + 1):
                c = (a + b) / 2.0
                fc = f(c)
                galat = abs(b - a)
                
                riwayat_iterasi.append({
                    "Iterasi": i, "Batas a": a, "Batas b": b, "Titik Tengah c": c,
                    "f(a)": f(a), "f(b)": f(b), "f(c)": fc, "Lebar Selang": galat
                })
                
                if galat < toleransi or abs(fc) < 1e-9:
                    akar_final = c
                    konvergen = True
                    break
                
                # Geser selang baru
                if f(a) * fc < 0:
                    b = c
                else:
                    a = c
                    
    # ==========================================
    # 🟩 LOGIKA METODE NEWTON-RAPHSON
    # ==========================================
    else:
        curr_x = x0
        st.write(f"**Fungsi Turunan f'(x) otomatis dideteksi:** `${sp.latex(f_prime_expr)}$`")
        
        for i in range(1, max_iter + 1):
            fx = f(curr_x)
            fdx = f_prime(curr_x)
            
            if abs(fdx) < 1e-12:
                st.error("❌ Turunan f'(x) bernilai 0 atau mendekati nol. Metode Newton-Raphson gagal (pembagian dengan nol).")
                break
                
            next_x = curr_x - (fx / fdx)
            galat = abs(next_x - curr_x)
            
            riwayat_iterasi.append({
                "Iterasi": i, "x_n": curr_x, "f(x_n)": fx, "f'(x_n)": fdx, "x_{n+1}": next_x, "Estimasi Error": galat
            })
            
            if galat < toleransi:
                akar_final = next_x
                konvergen = True
                break
            
            curr_x = next_x

    # ==========================================
    # 📊 MENAMPILKAN OUTPUT HASIL AKHIR
    # ==========================================
    if konvergen:
        st.write("---")
        st.success(f"🎉 **Sukses Konvergen!** Akar ditemukan pada **Iterasi ke-{len(riwayat_iterasi)}**")
        
        # Kartu Hasil Utama
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label="Nilai Akar x Terbaik", value=f"{akar_final:.6f}")
        with col_res2:
            st.metric(label="Nilai f(x) Terakhir", value=f"{f(akar_final):.2e}")
            
        # Tabel Langkah Iterasi Akademik (Bisa di-scroll di HP agar data angka presisi)
        st.markdown("### 📋 Tabel Riwayat Iterasi / Proses Konvergensi")
        df_hasil = pd.DataFrame(riwayat_iterasi)
        st.dataframe(df_hasil, use_container_width=True)
    else:
        st.warning("⚠️ Batas iterasi maksimum tercapai atau metode gagal menemukan akar dalam parameter input tersebut.")
