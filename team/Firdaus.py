def perkenalan(nama, nim, peran): 
    print("Halo! Perkenalkan, nama saya", nama)
    print("NIM :", nim)
    print("Peran saya yaitu:")
    print(peran)

if __name__ == "__main__":
    nama = "Muhammad Firdaus Al-Farizi"
    nim = "2213010411"
    peran = (
        "- Implementasi fitur tambah, edit, hapus, dan daftar perjalanan\n"
        "- Implementasi model perjalanan untuk mengelola data perjalanan\n"
    )
    perkenalan(nama, nim, peran)