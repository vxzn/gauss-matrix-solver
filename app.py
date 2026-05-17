import streamlit as st
import time
from fractions import Fraction
from matrix_logic import eliminasi_gauss_ultimate, format_angka

# --- INITIAL SETUP ---
st.set_page_config(
    page_title="Matrix Solver",
    page_icon="🟦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PANEL KONTROL SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0;">
            <p style="margin: 0; font-size: 0.75rem; color: #3B82F6; font-weight: 700; letter-spacing: 1px;">KONTROL UTAMA</p>
            <h3 style="margin: 3px 0 0 0; font-size: 1.25rem; font-weight:700; color: #1F2937;">Pengaturan Aplikasi</h3>
        </div>
    """, unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("##### 📥 Format Bilangan")
    format_output = st.selectbox(
        "Format angka hasil akhir:", 
        ["Pecahan / Fraction (1/3)", "Desimal (0.3333)"], 
        label_visibility="collapsed"
    )
    
    st.write("")
    
    st.markdown("##### ⏱️ Kecepatan Baris")
    kecepatan_simulasi = st.select_slider(
        "Durasi animasi langkah:", options=[1, 2, 3, 4, 5], value=2,
        format_func=lambda x: f"{x} Detik"
    )
    
    st.write("---")
    
    # KARTU IDENTITAS MAHASISWA MINIMALIS PUTIH
    st.markdown("""
        <div style="border: 1px solid #E5E7EB; padding: 16px; border-radius: 12px; background-color: #F9FAFB;">
            <p style="margin: 0; font-size: 0.7rem; color: #6B7280; font-weight: 600; letter-spacing: 0.5px;">MAHASISWA</p>
            <h4 style="margin: 4px 0 2px 0; font-size: 0.95rem; font-weight: 700; color:#1F2937;">Nama Kamu</h4>
            <p style="margin: 0; font-size: 0.85rem; color: #3B82F6; font-weight: 600;">NIM. XXXXXXXXX</p>
        </div>
    """, unsafe_allow_html=True)

# --- INJEKSI DESAIN ---
with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- HERO SECTION (CLEAN TECH) ---
st.markdown("<h1 class='brand-title'>Gauss Solver</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>Kalkulator Operasi Baris Elementer (OBE) minimalis untuk penyelesaian matriks secara akurat.</p>", unsafe_allow_html=True)

kolom_kiri, kolom_kanan = st.columns([2, 1])

with kolom_kanan:
    st.markdown("### 🛠️ Ordo Matriks")
    n = st.number_input("Ordo N x N:", min_value=2, max_value=10, value=3, step=1, label_visibility="collapsed")
    
    st.write("")
    st.markdown("##### 💡 Contoh Soal Cepat:")
    preset_normal = st.button("Solusi Unik (Normal)", type="secondary")
    preset_no_sol = st.button("Kasus Singular (Eror)", type="secondary")

with kolom_kiri:
    st.markdown("### 📥 Input Nilai Matriks $[A | b]$")
    
    preset_A = [["3", "3/2", "-1"], ["2", "-2", "4"], ["-1", "0.5", "-1"]]
    preset_b = ["1", "-2", "0"]
    
    if preset_no_sol and n == 3:
        preset_A = [["1", "1", "1"], ["2", "2", "2"], ["1", "-1", "2"]]
        preset_b = ["3", "4", "1"]
        
    A, b = [], []
    input_valid = True
    
    with st.container():
        for i in range(n):
            cols = st.columns(n + 1)
            baris_A = []
            for j in range(n):
                with cols[j]:
                    nilai_inisial = preset_A[i][j] if (preset_normal or preset_no_sol) and n == 3 else "0"
                    teks_A = st.text_input(f"A_{i}_{j}", value=nilai_inisial, key=f"A_{i}_{j}", label_visibility="collapsed")
                    try:
                        teks_bersih = teks_A.strip()
                        nilai_A = float(Fraction(teks_bersih)) if teks_bersih != "" else 0.0
                    except Exception:
                        st.error("Format salah")
                        input_valid = False
                        nilai_A = 0.0
                    baris_A.append(nilai_A)
            A.append(baris_A)
            
            with cols[n]:
                nilai_b_inisial = preset_b[i] if (preset_normal or preset_no_sol) and n == 3 else "0"
                teks_b = st.text_input(f"b_{i}", value=nilai_b_inisial, key=f"b_{i}", label_visibility="collapsed")
                try:
                    teks_b_bersih = teks_b.strip()
                    nilai_b = float(Fraction(teks_b_bersih)) if teks_b_bersih != "" else 0.0
                except Exception:
                    input_valid = False
                    nilai_b = 0.0
                b.append(nilai_b)

st.write("---")

# --- EKSEKUSI PROSES ---
st.markdown("### 🎬 Lembar Kerja OBE")
if st.button("MULAI PROSES KOMPUTASI", key="run_sim"):
    if not input_valid:
        st.error("Periksa kembali nilai matriks Anda.")
    else:
        solusi, riwayat, verifikasi = eliminasi_gauss_ultimate(A, b, n, format_output)
        
        status_simulasi = st.empty()
        progress_bar = st.progress(0)
        container_langkah = st.container()
        
        total_langkah = len(riwayat)
        for indeks, langkah in enumerate(riwayat):
            status_simulasi.markdown(f"<div class='status-badge'>Langkah {indeks + 1} dari {total_langkah}</div>", unsafe_allow_html=True)
            progress_bar.progress((indeks + 1) / total_langkah)
            
            with container_langkah:
                st.markdown(f"<div class='premium-card'>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='color: #1E3A8A; margin-top:0; margin-bottom:12px;'>Tahap Ke-{indeks + 1}</h4>", unsafe_allow_html=True)
                st.markdown(langkah["teks"])
                st.table(data=langkah["data"])
                st.markdown("</div>", unsafe_allow_html=True)
            
            time.sleep(kecepatan_simulasi)
            
        status_simulasi.markdown("<div class='status-badge' style='color:#FFFFFF !important; background-color:#3B82F6; border-color:#3B82F6;'>✓ Perhitungan Selesai</div>", unsafe_allow_html=True)
        
        st.write("---")
        if solusi is None:
            if verifikasi == "TIDAK_ADA_SOLUSI":
                st.error("Sistem tidak memiliki solusi.")
            elif verifikasi == "SOLUSI_TAK_BERHINGGA":
                st.warning("Sistem memiliki solusi tak berhingga.")
        else:
            st.markdown("<h3 style='color:#1E3A8A; margin-bottom:25px;'>📊 Hasil Akhir Vektor X:</h3>", unsafe_allow_html=True)
            
            cols_hasil = st.columns(n)
            for i in range(n):
                with cols_hasil[i]:
                    st.markdown(f"<div class='metric-card'>", unsafe_allow_html=True)
                    st.metric(label=f"Variabel X_{i+1}", value=format_angka(solusi[i], format_output))
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.write("")
            with st.expander("🔬 Detail Validasi Akurasi"):
                for v_langkah in verifikasi:
                    st.markdown(f"<div class='verify-card'>{v_langkah}</div>", unsafe_allow_html=True)
