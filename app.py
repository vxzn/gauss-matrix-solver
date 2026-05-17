import streamlit as st
import numpy as np
from fractions import Fraction

# --- SETTING LAYOUT ---
st.set_page_config(page_title="Kalkulator Eliminasi Gauss", layout="wide")

# --- STYLE CSS SEDERHANA & MINIMALIS (FOKUS PADA DATA) ---
st.markdown("""
<style>
    body { background-color: #FAFAFA; }
    .title { color: #1E3A8A; font-weight: bold; text-align: center; }
    .step-card { background-color: #FFFFFF; border: 1px solid #E5E7EB; border-left: 5px solid #3B82F6; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .matrix-box { font-family: monospace; font-size: 1.1rem; background-color: #F8FAFC; padding: 10px; border-radius: 6px; border: 1px solid #E2E8F0; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>Kalkulator Eliminasi Gauss murni</h1>", unsafe_allow_html=True)
st.write("Aplikasi ini menyelesaikan Sistem Persamaan Linear (SPL) menggunakan metode **Eliminasi Gauss** (mengubah matriks menjadi Segitiga Atas) disertai penjelasan langkah OBE dan Substitusi Balik.")

# --- INPUT CONFIGURATION ---
st.write("---")
n = st.number_input("Masukkan Ordo Matriks (N x N):", min_value=2, max_value=5, value=3, step=1)

# --- FUNGSI HELPER FORMAT ANGKA ---
def to_fraction_str(val):
    if abs(val) < 1e-9:
        return "0"
    frac = Fraction(str(val)).limit_denominator()
    return str(frac)

# --- GENERATE GRID INPUT MINIMALIS (PAS DI HP & LAPTOP) ---
st.markdown("### 📥 Input Matriks Augmented $[A | b]$")
cols_input = st.columns(n + 1)

A_input = []
b_input = []

# Membuat grid input tanpa tumpuk
for i in range(n):
    row_inputs = []
    cols = st.columns(n + 1)
    for j in range(n):
        with cols[j]:
            val = st.text_input(f"A[{i+1}][{j+1}]", value="0", key=f"A_{i}_{j}", label_visibility="visible")
            try:
                row_inputs.append(float(Fraction(val)))
            except:
                row_inputs.append(0.0)
    with cols[n]:
        val_b = st.text_input(f"b[{i+1}]", value="0", key=f"b_{i}", label_visibility="visible")
        try:
            b_input.append(float(Fraction(val_b)))
        except:
            b_input.append(0.0)
    A_input.append(row_inputs)

# --- TOMBOL EKSEKUSI ---
st.write("---")
if st.button("HITUNG MENGGUNAKAN ELIMINASI GAUSS", type="primary", use_container_width=True):
    
    # Konversi ke NumPy Array untuk komputasi linear algebra
    A = np.array(A_input, dtype=float)
    b = np.array(b_input, dtype=float)
    
    # Gabungkan menjadi matriks augmented [A|b]
    augmented = np.hstack([A, b.reshape(-1, 1)])
    
    st.markdown("### 🎬 Langkah-Langkah Operasi Baris Elementer (OBE)")
    
    # Tampilkan Matriks Awal
    st.markdown("<div class='step-card'>", unsafe_allow_html=True)
    st.write("**Matriks Augmented Awal $[A|b]$:**")
    matrix_str = ""
    for r in range(n):
        matrix_str += " | ".join([to_fraction_str(augmented[r, c]) for c in range(n)]) + f"  ==>  [ {to_fraction_str(augmented[r, n])} ]\n"
    st.text(matrix_str)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # --- PROSES ELIMINASI MAJU (FORWARDS ELIMINATION) ---
    bisa_diselesaikan = True
    for i in range(n):
        # 1. Pivoting parsial jika pivot berharga 0
        if abs(augmented[i, i]) < 1e-9:
            tukar_baris = -1
            for k in range(i + 1, n):
                if abs(augmented[k, i]) > 1e-9:
                    tukar_baris = k
                    break
            if tukar_baris != -1:
                augmented[[i, tukar_baris]] = augmented[[tukar_baris, i]]
                st.markdown("<div class='step-card'>", unsafe_allow_html=True)
                st.write(f"🔄 **OBE: Tukar Baris {i+1} dengan Baris {tukar_baris+1}** karena elemen pivot bernilai 0.")
                matrix_str = ""
                for r in range(n):
                    matrix_str += " | ".join([to_fraction_str(augmented[r, c]) for c in range(n)]) + f"  ==>  [ {to_fraction_str(augmented[r, n])} ]\n"
                st.text(matrix_str)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                bisa_diselesaikan = False
                break
        
        # 2. Eliminasi elemen di bawah pivot
        for k in range(i + 1, n):
            factor = augmented[k, i] / augmented[i, i]
            if abs(factor) > 1e-9:
                augmented[k, i:] -= factor * augmented[i, i:]
                st.markdown("<div class='step-card'>", unsafe_allow_html=True)
                st.write(f"🔢 **OBE: Baris {k+1} = Baris {k+1} - ({to_fraction_str(factor)}) $\\times$ Baris {i+1}**")
                matrix_str = ""
                for r in range(n):
                    matrix_str += " | ".join([to_fraction_str(augmented[r, c]) for c in range(n)]) + f"  ==>  [ {to_fraction_str(augmented[r, n])} ]\n"
                st.text(matrix_str)
                st.markdown("</div>", unsafe_allow_html=True)

    # --- VALIDASI HASIL MATRIKS SEGITIGA ATAS ---
    if not bisa_diselesaikan or abs(augmented[n-1, n-1]) < 1e-9:
        if abs(augmented[n-1, n]) > 1e-9:
            st.error("❌ Sistem Persamaan Linear TIDAK MEMILIKI SOLUSI (Matriks Singular Singular).")
        else:
            st.warning("⚠️ Sistem Persamaan Linear MEMILIKI SOLUSI TAK BERHINGGA.")
    else:
        # --- PROSES SUBSTITUSI BALIK (BACK SUBSTITUTION) ---
        st.markdown("### 🔄 Substitusi Balik (Back Substitution)")
        x = np.zeros(n)
        
        for i in range(n - 1, -1, -1):
            suku_diketahui = 0.0
            langkah_teks = f"Persamaan dari Baris {i+1}: "
            
            # Membangun teks penjelasan subtitusi matematika
            fitur_teks = []
            for j in range(i + 1, n):
                suku_diketahui += augmented[i, j] * x[j]
                fitur_teks.append(f"({to_fraction_str(augmented[i, j])} \\times {to_fraction_str(x[j])})")
            
            x[i] = (augmented[i, n] - suku_diketahui) / augmented[i, i]
            
            st.markdown("<div class='step-card'>", unsafe_allow_html=True)
            if fitur_teks:
                st.write(f"Mencari $X_{i+1}$:")
                st.latex(f"X_{{{i+1}}} = \\frac{{{to_fraction_str(augmented[i, n])} - {' - '.join(fitur_teks)}}}{{{to_fraction_str(augmented[i, i])}}} = {to_fraction_str(x[i])}")
            else:
                st.write(f"Mencari $X_{i+1}$ langsung dari baris terakhir:")
                st.latex(f"X_{{{i+1}}} = \\frac{{{to_fraction_str(augmented[i, n])}}}{{{to_fraction_str(augmented[i, i])}}} = {to_fraction_str(x[i])}")
            st.markdown("</div>", unsafe_allow_html=True)

        # --- TAMPILKAN HASIL AKHIR ---
        st.write("---")
        st.markdown("### 📊 Vektor Hasil Akhir (Solusi SPL):")
        cols_hasil = st.columns(n)
        for i in range(n):
            with cols_hasil[i]:
                st.metric(label=f"Nilai X_{i+1}", value=to_fraction_str(x[i]))
