import streamlit as st
import time
from fractions import Fraction

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Gauss Solver High Contrast",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 🎨 REKAYASA CSS KUSTOM: KONTRAS TINGGI & FONT UNIVERSAL JELAS ---
st.markdown("""
    <style>
    /* 1. Paksa Semua Elemen Menggunakan Font Arial & Warna Putih Bersih */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stMarkdown, p, span, label, th, td, input {
        font-family: 'Arial', 'Helvetica', sans-serif !important;
        color: #FFFFFF !important; /* Semua teks default wajib putih agar terlihat jelas */
    }
    
    /* Latar belakang hitam pekat untuk area utama */
    [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
    }
    [data-testid="stHeader"] {
        background-color: #000000 !important;
    }
    
    /* Latar belakang hitam sedikit abu untuk sidebar */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 2px solid #222222 !important;
    }
    
    /* 2. Judul Utama (Hijau Terang ke Putih) */
    .brand-title {
        background: linear-gradient(135deg, #22c55e 0%, #FFFFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 3.2rem;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }
    .brand-subtitle {
        color: #E2E8F0 !important; /* Putih keabu-abuan terang */
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 25px;
    }
    
    /* Sub-heading tebal dan putih */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    
    /* 3. Kotak Input Matriks (Teks Putih Tebal, Border Hijau Jelas) */
    .stTextInput>div>div>input {
        text-align: center;
        font-weight: 900 !important; /* Angka dibuat sangat tebal */
        font-size: 1.2rem !important;
        border-radius: 8px !important;
        border: 2px solid #22c55e !important; /* Border hijau tegas */
        background-color: #111111 !important;
        color: #FFFFFF !important;
        transition: all 0.2s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4ade80 !important;
        background-color: #222222 !important;
        box-shadow: 0 0 10px #4ade80 !important;
    }
    
    /* Keterangan label input tersembunyi/terlihat tetap dipaksa putih tebal */
    .stTextInput label {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
    
    /* 4. Perbaikan Total Tabel Simulasi (Teks Harus Hitam di Header, Putih di Baris) */
    .stTable table {
        background-color: #111111 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        border: 2px solid #222222 !important;
    }
    .stTable th {
        background-color: #22c55e !important; /* Hijau terang untuk header tabel */
        color: #000000 !important; /* Teks header HITAM agar kontras dengan background hijau */
        font-weight: 900 !important;
        font-size: 1rem !important;
    }
    .stTable td {
        color: #FFFFFF !important; /* Teks isi tabel PUTIH BERSIH */
        font-size: 1rem !important;
        font-weight: bold !important;
        border-bottom: 1px solid #222222 !important;
    }
    
    /* 5. Kartu Kotak Proses OBE */
    .premium-card { 
        background-color: #111111; 
        padding: 22px; 
        border-radius: 12px; 
        margin-bottom: 25px; 
        border: 2px solid #22c55e; /* Border hijau mengitari proses */
    }
    
    .metric-card {
        background-color: #111111;
        padding: 18px;
        border-radius: 12px;
        border: 2px solid #FFFFFF; /* Border putih tegas untuk hasil akhir */
        text-align: center;
    }
    
    .verify-card {
        background-color: #052e16;
        padding: 15px 20px;
        border-radius: 8px;
        border-left: 5px solid #22c55e;
        margin-top: 12px;
        color: #FFFFFF !important; /* Teks verifikasi putih */
        font-weight: bold;
    }
    
    /* Status Badge */
    .status-badge { 
        font-weight: 900; 
        color: #22c55e !important; 
        background-color: #000000;
        padding: 10px 20px;
        border-radius: 8px;
        border: 2px solid #22c55e;
        display: inline-block;
        font-size: 1rem;
    }
    
    /* 6. Tombol Utama (Hijau Terang - Teks Putih Tebal) */
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        font-weight: 900;
        font-size: 1.1rem;
        background: #22c55e !important; /* Hijau solid berkejelasan tinggi */
        color: #000000 !important; /* Teks tombol hitam agar terbaca jelas */
        border: none !important;
        padding: 14px 0;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: #4ade80 !important;
        transform: translateY(-1px);
    }
    
    /* Memaksa nilai komponen Metric bawaan Streamlit menjadi Putih Kontras */
    div[data-testid="stMetricValue"] > div {
        color: #22c55e !important; /* Nilai variabel warna hijau terang */
        font-weight: 900 !important;
        font-size: 2rem !important;
    }
    div[data-testid="stMetricLabel"] > div {
        color: #FFFFFF !important; /* Label variabel warna putih */
        font-weight: bold !important;
    }
    
    /* Kotak info sidebar */
    .stAlert {
        background-color: #222222 !important;
        border: 2px solid #22c55e !important;
    }
    .stAlert p, .stAlert strong {
        color: #FFFFFF !important;
    }
    
    /* Mengatasi caption agar tetap putih */
    .stCaption {
        color: #E2E8F0 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #22c55e;'>KONTROL UTAMA</h2>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("### 👥 Kredensial Mahasiswa")
    st.info("👤 **Nama Kamu**\n\n🆔 NIM. XXXXXXXXX\n\n💻 Teknik Informatika")
    st.write("---")
    
    st.markdown("### 🎛️ Format Hasil")
    format_output = st.selectbox(
        "Pilih Format Output:",
        ["Pecahan / Fraction (1/3)", "Desimal (0.3333)"]
    )
    
    st.write("---")
    st.markdown("### ⏱️ Pengatur Waktu")
    kecepatan_simulasi = st.slider("Jeda Langkah (Detik):", min_value=1, max_value=5, value=2, step=1)
    st.write("---")
    st.markdown("<p style='text-align:center; color:#FFFFFF; font-size:0.9rem; font-weight:bold;'>EDISI KONTRAS TINGGI V10</p>", unsafe_allow_html=True)

# --- AREA UTAMA ---
st.markdown("<h1 class='brand-title'>🧮 GAUSS MATRIX SOLVER</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>Aplikasi Penghitung Operasi Baris Elementer (OBE) - Berkinerja Tinggi & Jelas</p>", unsafe_allow_html=True)

# Membagi tata letak kolom utama
kolom_kiri, kolom_kanan = st.columns([2, 1])

with kolom_kanan:
    st.markdown("### ⚙️ Pengaturan Matriks")
    n = st.number_input("Masukkan Ukuran Matriks (N x N):", min_value=2, max_value=10, value=3, step=1)
    
    st.write("")
    st.markdown("### 🔮 Tombol Otomatis Soal:")
    preset_normal = st.button("✨ Muat Soal Solusi Unik", type="secondary")
    preset_no_sol = st.button("🚨 Muat Kasus Matriks Singular", type="secondary")

with kolom_kiri:
    st.markdown("### 📥 Isi Nilai Matriks $[A | b]$")
    st.caption("Isi kotak di bawah ini dengan angka bebas (bisa pecahan seperti 1/3):")
    
    preset_A = [["3", "3/2", "-1"], ["2", "-2", "4"], ["-1", "0.5", "-1"]]
    preset_b = ["1", "-2", "0"]
    
    if preset_no_sol and n == 3:
        preset_A = [["1", "1", "1"], ["2", "2", "2"], ["1", "-1", "2"]]
        preset_b = ["3", "4", "1"]
        
    A = []
    b = []
    input_valid = True
    
    with st.container():
        for i in range(n):
            cols = st.columns(n + 1)
            baris_A = []
            
            for j in range(n):
                with cols[j]:
                    if (preset_normal or preset_no_sol) and n == 3:
                        nilai_inisial = preset_A[i][j]
                    else:
                        nilai_inisial = "0"
                        
                    teks_A = st.text_input(f"A_{i}_{j}", value=nilai_inisial, key=f"A_{i}_{j}", label_visibility="collapsed" if i > 0 else "visible")
                    try:
                        teks_bersih = teks_A.strip()
                        nilai_A = float(Fraction(teks_bersih)) if teks_bersih != "" else 0.0
                    except Exception:
                        st.error("Format salah!")
                        input_valid = False
                        nilai_A = 0.0
                    baris_A.append(nilai_A)
            A.append(baris_A)
            
            with cols[n]:
                if (preset_normal or preset_no_sol) and n == 3:
                    nilai_b_inisial = preset_b[i]
                else:
                    nilai_b_inisial = "0"
                    
                teks_b = st.text_input(f"b_{i}", value=nilai_b_inisial, key=f"b_{i}", label_visibility="collapsed" if i > 0 else "visible")
                try:
                    teks_b_bersih = teks_b.strip()
                    nilai_b = float(Fraction(teks_b_bersih)) if teks_b_bersih != "" else 0.0
                except Exception:
                    input_valid = False
                    nilai_b = 0.0
                b.append(nilai_b)

st.write("---")

# --- FUNGSI FORMATTING ---
def format_angka(nilai):
    if format_output == "Pecahan / Fraction (1/3)":
        frac = Fraction(nilai).limit_denominator()
        return f"{frac}"
    else:
        return f"{nilai:.4f}"

def buat_tabel_matriks(A_curr, b_curr):
    matriks_tabel = []
    header = [f"X{k+1}" for k in range(n)] + ["Hasil (b)"]
    for k in range(n):
        baris_formatted = [format_angka(elemen) for elemen in A_curr[k]] + [format_angka(b_curr[k])]
        matriks_tabel.append(baris_formatted)
    return header, matriks_tabel

# --- FUNGSI LOGIKA CORE ---
def eliminasi_gauss_ultimate(A, b):
    A_proses = [[float(elemen) for elemen in baris] for baris in A]
    b_proses = [float(elemen) for elemen in b]
    riwayat_langkah = [] 

    h_awal, t_awal = buat_tabel_matriks(A_proses, b_proses)
    riwayat_langkah.append({
        "teks": "🏁 **Matriks Awal Sebelum Diproses:**",
        "header": h_awal,
        "data": t_awal
    })

    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(A_proses[k][i]) > abs(A_proses[max_row][i]):
                max_row = k
        
        if max_row != i:
            A_proses[i], A_proses[max_row] = A_proses[max_row], A_proses[i]
            b_proses[i], b_proses[max_row] = b_proses[max_row], b_proses[i]
            h_pivot, t_pivot = buat_tabel_matriks(A_proses, b_proses)
            riwayat_langkah.append({
                "teks": f"🔀 **Pertukaran Baris:** Menukar Baris ke-{i+1} dengan Baris ke-{max_row+1}.",
                "header": h_pivot,
                "data": t_pivot
            })

        if abs(A_proses[i][i]) < 1e-9:
            if abs(b_proses[i]) < 1e-9:
                return None, riwayat_langkah, "SOLUSI_TAK_BERHINGGA"
            else:
                return None, riwayat_langkah, "TIDAK_ADA_SOLUSI"
        
        for j in range(i + 1, n):
            if A_proses[j][i] != 0:
                faktor = A_proses[j][i] / A_proses[i][i]
                for k in range(i, n):
                    A_proses[j][k] -= faktor * A_proses[i][k]
                b_proses[j] -= faktor * b_proses[i]
                
                h_elim, t_elim = buat_tabel_matriks(A_proses, b_proses)
                riwayat_langkah.append({
                    "teks": f"🔄 **Rumus OBE:** Baris ke-{j+1} dikurangi ({format_angka(faktor)}) kali Baris ke-{i+1}",
                    "header": h_elim,
                    "data": t_elim
                })

    x = [0] * n
    for i in range(n - 1, -1, -1):
        total = b_proses[i]
        for j in range(i + 1, n):
            total -= A_proses[i][j] * x[j]
        x[i] = total / A_proses[i][i]
        
    log_verifikasi = []
    for i in range(n):
        hitung_ulang = 0
        teks_rumus = []
        for j in range(n):
            hitung_ulang += A[i][j] * x[j]
            teks_rumus.append(f"({format_angka(A[i][j])} × {format_angka(x[j])})")
        simbol_hubung = " + ".join(teks_rumus)
        log_verifikasi.append(f"Persamaan {i+1}: {simbol_hubung} = **{format_angka(hitung_ulang)}** (Target b={format_angka(b[i])})")
        
    return x, riwayat_langkah, log_verifikasi

# --- EKSEKUSI ---
st.markdown("### 🎬 Alur Langkah Pemrosesan Matriks")
if st.button("▶️ MULAI HITUNG SEKARANG", key="run_sim"):
    if not input_valid:
        st.error("Periksa kembali format input angka Anda.")
    else:
        solusi, riwayat, verifikasi = eliminasi_gauss_ultimate(A, b)
        
        status_simulasi = st.empty()
        progress_bar = st.progress(0)
        
        st.write("")
        container_langkah = st.container()
        
        total_langkah = len(riwayat)
        for indeks, langkah in enumerate(riwayat):
            status_simulasi.markdown(f"<div class='status-badge'>⚡ PROSES: MENJALANKAN LANGKAH KE-{indeks + 1} DARI {total_langkah}...</div>", unsafe_allow_html=True)
            progress_bar.progress((indeks + 1) / total_langkah)
            
            with container_langkah:
                st.markdown(f"<div class='premium-card'>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='color: #22c55e; margin-top:0; margin-bottom:10px;'>🟢 LANGKAH KE-{indeks + 1}</h4>", unsafe_allow_html=True)
                st.markdown(langkah["teks"])
                st.table(data=langkah["data"])
                st.markdown("</div>", unsafe_allow_html=True)
            
            time.sleep(kecepatan_simulasi)
            
        status_simulasi.markdown("<div class='status-badge' style='color:#000000 !important; background-color:#22c55e; border-color:#22c55e;'>🏆 HITUNGAN SELESAI SUKSES!</div>", unsafe_allow_html=True)
        
        st.write("---")
        if solusi is None:
            if verifikasi == "TIDAK_ADA_SOLUSI":
                st.error("🚨 **Sistem Tidak Memiliki Solusi / Matriks Rusak**")
            elif verifikasi == "SOLUSI_TAK_BERHINGGA":
                st.warning("⚠️ **Sistem Memiliki Solusi Tak Berhingga**")
        else:
            st.balloons()
            st.markdown("<h3 style='color:#22c55e; margin-bottom:15px;'>📊 HASIL AKHIR NILAI VARIABEL:</h3>", unsafe_allow_html=True)
            
            cols_hasil = st.columns(n)
            for i in range(n):
                with cols_hasil[i]:
                    st.markdown(f"<div class='metric-card'>", unsafe_allow_html=True)
                    st.metric(label=f"NILAI X_{i+1}", value=format_angka(solusi[i]))
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.write("")
            with st.expander("🔬 DETAIL VERIFIKASI AKURASI"):
                for v_langkah in verifikasi:
                    st.markdown(f"<div class='verify-card'>{v_langkah}</div>", unsafe_allow_html=True)