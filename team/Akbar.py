def perkenalan(nama, nim, peran): 
    print("Halo! Perkenalkan, nama saya", nama)
    print("NIM :", nim)
    print("Peran saya yaitu:")
    print(peran)

if __name__ == "__main__":
    nama = "Syakara Akbar"
    nim = "2213010384"
    peran = (
        "- Membuat dan mengatur tampilan halaman untuk fitur-fitur yang ada\n"
        "- Menambahkan dan mengatur gaya CSS untuk tampilan halaman\n"
    )
    perkenalan(nama, nim, peran)