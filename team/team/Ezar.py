def perkenalan(nama, nim, peran): 
    print("Halo! Perkenalkan, nama saya", nama)
    print("NIM :", nim)
    print("Peran saya yaitu:")
    print(peran)

if __name__ == "__main__":
    nama = "Ezar Ramadhan"
    nim = "2213010387"
    peran = (
        "- Implementasi login, register, logout, dan reset password pada controllers.py\n"
        "- Menampilkan statistik perjalanan di dashboard pada controllers.py\n"
        "- Implementasi model pengguna untuk autentikasi pada models.py"
    )
    perkenalan(nama, nim, peran)