import streamlit as st
import time
from fractions import Fraction
from matrix_logic import eliminasi_gauss_ultimate, format_angka

# --- INITIAL SETUP ---
st.set_page_config(
    page_title="Aljabar Linier - Gauss Solver",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PANEL KONTROL SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0;">
            <p style="margin: 0; font-size: 0.75rem; color: #D4AF37; font-weight: 700; letter-spacing: 1px;">LAB KOMPUTASI</p>
            <h3 style="margin: 5px 0 0 0; font-size: 1.3rem; font-weight:700; color: #FFFFFF;">Konfigurasi Sistem</h3>
        </div>
    """, unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("##### 📥 Opsi Bilangan")
    format_output = st.selectbox(
        "Tipe representasi angka hasil akhir:", 
        ["Pecahan / Fraction (1/3)", "Desimal (0.3333)"], 
        label_visibility="collapsed"
    )
    
    st.write("")
    
    st.markdown("##### ⏱️ Simulasi Jeda")
    kecepatan_simulasi = st.select_slider(
        "Durasi animasi tiap baris:", options=[1, 2, 3, 4, 5], value=2,
        format_func=lambda x: f"{x} Detik"
    )
    
    st.write("---")
    
    # KARTU IDENTITAS MAHASISWA YANG REALISTIS
    st.markdown("""
        <div style="border: 1px solid #252A3C; padding: 16px; border-radius: 12px; background-color: #1A1D29;">
            <p style="margin: 0; font-size: 0.7rem; color: #8E93A6; font-weight: 600; letter-spacing: 0.5px;">TUGAS AKHIR KULIAH</p>
            <h4 style="margin: 6px 0 2px 0; font-size: 1rem; font-weight: 700; color:#FFFFFF;">Nama Kamu</h4>
            <p style="margin: 0; font-size: 0.85rem; color: #D4AF37; font-weight: 500;">NIM. XXXXXXXXX</p>
            <p style="margin: 8px 0 0 0; font-size: 0.8rem; color: #8E93A6;">Prodi Teknik Informatika</p>
        </div>
    """, unsafe_allow_html=True)

# --- INJEKSI DESAIN ---
with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- HERO SECTION (EDITORIAL STYLE) ---
st.markdown("<h1 class='brand-title'>the Gauss Elimination.</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>Sebuah eksperimen kalkulator matriks interaktif untuk menyelesaikan sistem persamaan linier menggunakan aturan OBE.</p>", unsafe_allow_html=True)

kolom_kiri, kolom_kanan = st.columns([2, 1])

with kolom_kanan:
    st.markdown("### 🛠️ Ordo Matriks")
    n = st.number_input("Tentukan N untuk matriks persegi (N x N):", min_value=2, max_value=10, value=3, step=1, label_visibility="collapsed")
    
    st.write("")
    st.markdown("##### 💡 Gunakan Contoh Soal:")
    preset_normal = st.button("Matriks Normal (Solusi Unik)", type="secondary")
    preset_no_sol = st.button("Matriks Singular (Kasus Khusus)", type="secondary")

with kolom_kiri:
    st.markdown("### 📥 Matriks Augmented $[A | b]$")
    
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
if st.button("MULAI HITUNG MATRIKS", key="run_sim"):
    if not input_valid:
        st.error("Periksa kembali angka yang kamu masukkan.")
    else:
        solusi, riwayat, verifikasi = eliminasi_gauss_ultimate(A, b, n, format_output)
        
        status_simulasi = st.empty()
        progress_bar = st.progress(0)
        container_langkah = st.container()
        
        total_langkah = len(riwayat)
        for indeks, langkah in enumerate(riwayat):
            status_simulasi.markdown(f"<div class='status-badge'>Langkah ke-{indeks + 1} dari total {total_langkah} tahapan</div>", unsafe_allow_html=True)
            progress_bar.progress((indeks + 1) / total_langkah)
            
            with container_langkah:
                st.markdown(f"<div class='premium-card'>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='color: #D4AF37; margin-top:0; margin-bottom:12px;'>Iterasi OBE Tahap {indeks + 1}</h4>", unsafe_allow_html=True)
                st.markdown(langkah["teks"])
                st.table(data=langkah["data"])
                st.markdown("</div>", unsafe_allow_html=True)
            
            time.sleep(kecepatan_simulasi)
            
        status_simulasi.markdown("<div class='status-badge' style='color:#12141C !important; background-color:#D4AF37; border-color:#D4AF37;'>✓ Seluruh tahapan selesai dihitung</div>", unsafe_allow_html=True)
        
        st.write("---")
        if solusi is None:
            if verifikasi == "TIDAK_ADA_SOLUSI":
                st.error("Sistem persamaan tidak konsisten.")
            elif verifikasi == "SOLUSI_TAK_BERHINGGA":
                st.warning("Sistem memiliki solusi tak berhingga.")
        else:
            st.markdown("<h3 style='color:#D4AF37; margin-bottom:25px;'>📊 Vektor Hasil Akhir:</h3>", unsafe_allow_html=True)
            
            cols_hasil = st.columns(n)
            for i in range(n):
                with cols_hasil[i]:
                    st.markdown(f"<div class='metric-card'>", unsafe_allow_html=True)
                    st.metric(label=f"Variabel X_{i+1}", value=format_angka(solusi[i], format_output))
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.write("")
            with st.expander("🔬 Lembar Pembuktian Akurasi Rumus"):
                for v_langkah in verifikasi:
                    st.markdown(f"<div class='verify-card'>{v_langkah}</div>", unsafe_allow_html=True)
