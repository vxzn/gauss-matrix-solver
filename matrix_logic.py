from fractions import Fraction

def format_angka(nilai, format_output):
    if format_output == "Pecahan / Fraction (1/3)":
        frac = Fraction(nilai).limit_denominator()
        return f"{frac}"
    else:
        return f"{nilai:.4f}"

def buat_tabel_matriks(A_curr, b_curr, n, format_output):
    matriks_tabel = []
    header = [f"X{k+1}" for k in range(n)] + ["Hasil (b)"]
    for k in range(n):
        baris_formatted = [format_angka(elemen, format_output) for elemen in A_curr[k]] + [format_angka(b_curr[k], format_output)]
        matriks_tabel.append(baris_formatted)
    return header, matriks_tabel

def eliminasi_gauss_ultimate(A, b, n, format_output):
    A_proses = [[float(elemen) for elemen in baris] for baris in A]
    b_proses = [float(elemen) for elemen in b]
    riwayat_langkah = [] 

    h_awal, t_awal = buat_tabel_matriks(A_proses, b_proses, n, format_output)
    riwayat_langkah.append({
        "teks": "🏁 **Matriks Augmented Awal:** Matriks siap diproses menggunakan Eliminasi Gauss.",
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
            h_pivot, t_pivot = buat_tabel_matriks(A_proses, b_proses, n, format_output)
            riwayat_langkah.append({
                "teks": f"🔀 **Pivoting:** Baris ke-{i+1} ditukar dengan Baris ke-{max_row+1} untuk menjaga stabilitas nilai.",
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
                
                h_elim, t_elim = buat_tabel_matriks(A_proses, b_proses, n, format_output)
                riwayat_langkah.append({
                    "teks": f"🔄 **Operasi OBE:** $B_{j+1} \\leftarrow B_{j+1} - ({format_angka(faktor, format_output)}) \\times B_{i+1}$",
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
            teks_rumus.append(f"({format_angka(A[i][j], format_output)} × {format_angka(x[j], format_output)})")
        simbol_hubung = " + ".join(teks_rumus)
        log_verifikasi.append(f"Baris ke-{i+1}: {simbol_hubung} = **{format_angka(hitung_ulang, format_output)}** (Target b = {format_angka(b[i], format_output)})")
        
    return x, riwayat_langkah, log_verifikasi
