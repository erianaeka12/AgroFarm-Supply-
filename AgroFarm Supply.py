import os
import csv
import pandas as pd
from tabulate import tabulate


def cekakun():
    if not os.path.exists('akunlogin.csv'):
        with open ('akunlogin.csv', mode = 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Password'])


def mainmenu():
    os.system('cls')
    while True:
        print('_________________________________________________')
        print('                                                 ')
        print('        ✦◦•● ◉ ✿ AGROFARM SUPPLY ✿ ◉ ●•◦✦         ')
        print('_________________________________________________')
        print("1. Login Admin")
        print("2. Login Customer")
        print("3. Register Customer")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            login_admin()
        elif pilihan == "2":
            logincust()
        elif pilihan == "3":
            register()
        else:
            print("Pilihan tidak valid, coba lagi!")
            mainmenu()


def register():
    os.system('cls')
    print('********************************************')
    print('✦                 REGISTER                 ✦')
    print('********************************************')
    cekakun()

    try:
        while True:
            username = input("Masukkan username baru (min. 4 huruf): ")
            if len(username) < 4:
                print("Username terlalu pendek! Minimal 4 huruf.")
            else:
                break

        while True:
            password = input("Masukkan password (min. 8 karakter): ")
            if len(password) <8:
                print("Password terlalu pendek! Minimal 8 karakter.")
            else:
                break

        with open("akunlogin.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username:
                    print("Username sudah digunakan, silakan pilih yang lain.")
                    input("Klik Enter untuk kembali ke menu...")
                    mainmenu()

        with open("akunlogin.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
    except ValueError:
            print("Input tidak valid!.")

    print("Registrasi berhasil! Silakan login.")
    input("Klik Enter untuk melanjutkan...")
    os.system('cls')
    mainmenu()


def logincust():
    global usernamelogin
    os.system('cls')
    print('********************************************')
    print('✦              LOGIN CUSTOMER              ✦')
    print('********************************************')
    cekakun()
    username = input('Masukkann Username Anda: ')
    password = input('Masukkan Password: ')

    loginsukses = False
    if  not os.path.exists('akunlogin.csv'):
        print('Akun tidak ditemukan, sepertinya kamu belum terdaftar. Silahkan register dulu!')
        input('Klik Enter untuk kembali ke halaman utama...')
        mainmenu()

    with open('akunlogin.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Username'] == username and row['Password'] == password:
                loginsukses = True
                break

    if loginsukses:
        usernamelogin = username
        print('YEAY! LOGIN BERHASIL')
        input('Klik Enter untuk melanjutkan...')
        os.system('cls')
        menucustomer()

    else:
        print('Username atau Password salah')
        input('Klik Enter untuk mencoba lagi...')
        os.system('cls')
        mainmenu()


def menucustomer():
    while True:
        os.system('cls')
        print('********************************************')
        print('          SELAMAT DATANG DI AGROFARM        ')
        print('********************************************')
        print(f'Halo {usernamelogin}! Mau apa hari ini?')
        print('Pilih Menu:')
        print('1. Belanja (lihat produk, lalu tambah ke keranjang)')
        print('2. Cek Keranjang')
        print('3. Status Pembelian')
        print('4. Riwayat Pembelian')
        print('0. Keluar')

        pilihan = input('Masukkan Pilihan Anda:').lower()

        if pilihan == '1' or pilihan == 'belanja':
            os.system('cls')
            menubelanja()
            # break
        elif pilihan == '2' or pilihan == 'tambah ke keranjang':
            os.system('cls')
            keranjang()
        elif pilihan == '3' or pilihan == 'status pembelian':
            os.system('cls')
            statuspembelian()
        elif pilihan == '4' or pilihan == 'riwayat pembelian':
            os.system('cls')
            riwayatpembelian()
        elif pilihan == '0' or pilihan == 'keluar':
            os.system('cls')
            mainmenu()
            break
        else:
            print('Pilihan tidak valid!')
            input('Klik enter untuk mencoba lagi...')
            continue


def menubelanja():
    os.system('cls')
    global usernamelogin
    keranjang_file = f'keranjang_{usernamelogin}.csv'

    try:
        df_produk = pd.read_csv('produk.csv')
    except FileNotFoundError:
        print("Produk.csv tidak ditemukan. Kembali ke menu customer.")
        return menucustomer()

    if not os.path.exists(keranjang_file):
        with open(keranjang_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Produk','Harga','Jumlah'])
            writer.writeheader()

    while True:
        os.system('cls')
        print("===== MENU BELANJA =====")
        print("1. Tampilkan semua produk")
        print("2. Cari produk")
        print("0. Kembali")

        pilih = input("Pilih menu: ")

        if pilih == "0":
            menucustomer()

        elif pilih == "1":
            os.system('cls')
            produk()
            df_produk

        elif pilih == "2":
            os.system('cls')
            hasil = cariproduk()
            if hasil is None:
                continue
            df_produk = hasil

        else:
            print('Pilihan tidak valid!')
            input('Tekan enter untuk mencoba lagi')
            continue

        while True:
            try:
                nomor = int(input("Masukkan nomor produk yang dipilih (0 untuk kembali): "))
                pilihlagi = False

                if nomor == 0:
                    os.system('cls')
                    menubelanja()

                if nomor < 1 or nomor > len(df_produk):
                    print(" Nomor produk tidak valid!")
                    continue

                index = nomor - 1
                produk_pilih = df_produk.iloc[index]

                nama = produk_pilih['Produk']
                harga = int(produk_pilih['Harga'])
                stok = int(produk_pilih['Stok'])

                print(f"Produk dipilih : {nama}")
                print(f"Harga          : {harga}")
                print(f"Stok tersedia  : {stok}")

                jumlah = int(input("Masukkan jumlah yang ingin dibeli: "))

                if jumlah <= 0:
                    print(" Jumlah harus lebih dari 0!")
                    continue

                if jumlah > stok:
                    print(" Stok tidak cukup!")
                    continue

                while True:
                    if pilihlagi:
                        break
                    konfirmasi = input("Yakin ingin membeli? (y/t): ").lower()

                    if konfirmasi == 'y':
                        df_keranjang = pd.read_csv(keranjang_file)

                        if nama in df_keranjang['Produk'].values:
                            idx_update = df_keranjang[df_keranjang['Produk'] == nama].index[0]
                            df_keranjang.at[idx_update, 'Jumlah'] += jumlah
                            df_keranjang.at[idx_update, 'Harga'] += (harga * jumlah)
                        else:
                            new_row = {
                                'Produk': nama,
                                'Harga': harga * jumlah,
                                'Jumlah': jumlah
                            }
                            df_keranjang = pd.concat([df_keranjang, pd.DataFrame([new_row])], ignore_index=True)

                        df_keranjang.to_csv(keranjang_file, index=False)

                        print("Produk berhasil dimasukkan ke keranjang!")

                        while True:
                            lanjut = input("Ingin membeli produk lain? (y/t): ").lower()
                            if lanjut == 'y':
                                pilihlagi = True
                                os.system('cls')
                                produk()
                                break
                            elif lanjut == 't':
                                input('Klik untuk kembali ke menu...')
                                menubelanja()
                            else:
                                print(" Input tidak valid! Harap masukkan y atau t.")

                    elif konfirmasi == 't':
                        print(" Pembelian dibatalkan.")
                        input('Klik untuk kembali memilih...')
                        break

                    else:
                        print(" Input tidak valid!")

            except ValueError:
                print(" Input harus berupa angka!")
            except Exception as e:
                print(f"Terjadi error: {e}")
                break

def cariproduk():
    os.system('cls')
    print('***************************************')
    print("             CARI PRODUK               ")
    print('***************************************')

    try:
        df = pd.read_csv('produk.csv')
    except FileNotFoundError:
        print("produk.csv tidak ditemukan.")
        input("Klik Enter untuk kembali...")
        return

    keyword = input("Masukkan nama produk yang ingin dicari: ").strip().lower()

    hasil = df[df['Produk'].str.lower().str.contains(keyword, na=False)]

    os.system('cls')
    print('***************************************')
    print("             HASIL CARI                ")
    print('***************************************')

    if hasil.empty:
        print("Produk tidak ditemukan.")
        input("Klik Enter untuk kembali...")
        return

    hasil = hasil.reset_index(drop=True)
    hasil.insert(0, "No", range(1, len(hasil) + 1))

    print(tabulate(hasil, headers='keys', tablefmt='fancy_grid', showindex=False))

    keranjang_file = f'keranjang_{usernamelogin}.csv'

    while True:
        try:
            nomor = int(input("Masukkan nomor produk yang dipilih (0 untuk kembali): "))
            pilihlagi = False

            if nomor == 0:
                os.system('cls')
                menubelanja()

            if nomor < 1 or nomor > len(hasil):
                print(" Nomor produk tidak valid!")
                continue

            index = nomor - 1
            produk_pilih = hasil.iloc[index]

            nama = produk_pilih['Produk']
            harga = int(produk_pilih['Harga'])
            stok = int(produk_pilih['Stok'])

            print(f"Produk dipilih : {nama}")
            print(f"Harga          : {harga}")
            print(f"Stok tersedia  : {stok}")

            jumlah = int(input("Masukkan jumlah yang ingin dibeli: "))

            if jumlah <= 0:
                print(" Jumlah harus lebih dari 0!")
                continue

            if jumlah > stok:
                print(" Stok tidak cukup!")
                continue

            while True:
                if pilihlagi:
                    break
                konfirmasi = input("Yakin ingin membeli? (y/t): ").lower()

                if konfirmasi == 'y':
                    df_keranjang = pd.read_csv(keranjang_file)

                    if nama in df_keranjang['Produk'].values:
                        idx_update = df_keranjang[df_keranjang['Produk'] == nama].index[0]
                        df_keranjang.at[idx_update, 'Jumlah'] += jumlah
                        df_keranjang.at[idx_update, 'Harga'] += (harga * jumlah)
                    else:
                        new_row = {
                            'Produk': nama,
                            'Harga': harga * jumlah,
                            'Jumlah': jumlah
                        }
                        df_keranjang = pd.concat([df_keranjang, pd.DataFrame([new_row])], ignore_index=True)

                    df_keranjang.to_csv(keranjang_file, index=False)

                    print("Produk berhasil dimasukkan ke keranjang!")

                    while True:
                        lanjut = input("Ingin membeli produk lain? (y/t): ").lower()
                        if lanjut == 'y':
                            pilihlagi = True
                            os.system('cls')
                            print(tabulate(hasil, headers='keys', tablefmt='fancy_grid', showindex=False))
                            break
                        elif lanjut == 't':
                            input('Klik untuk kembali ke menu...')
                            menubelanja()
                        else:
                            print(" Input tidak valid! Harap masukkan y atau t.")

                elif konfirmasi == 't':
                    print(" Pembelian dibatalkan.")
                    input('Klik untuk kembali memilih...')
                    break

                else:
                    print(" Input tidak valid!")
        except ValueError:
                print(" Input harus berupa angka!")
        except Exception as e:
            print(f"Terjadi error: {e}")
            break

    input("Klik Enter untuk kembali...")



def keranjang():
    os.system('cls')
    global usernamelogin
    keranjang_file = f'keranjang_{usernamelogin}.csv'

    print('********************************************')
    print(f'         KERANJANG {usernamelogin.upper()}           ')
    print('********************************************')

    if not os.path.exists(keranjang_file):
        print("Keranjang Anda kosong.")
        with open(keranjang_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Produk','Harga','Jumlah'])
            writer.writeheader()

        input("Klik enter untuk kembali...")
        menucustomer()
        return

    df = pd.read_csv(keranjang_file)

    if df.empty:
        print("Keranjang Anda kosong.")
        input("Klik Enter untuk kembali...")
        menucustomer()
        return

    df = df.reset_index(drop=True)
    df.index += 1
    df.insert(0, 'No', df.index)
    total_harga = df['Harga'].sum()
    print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
    print(f"Total Harga dalam Keranjang: Rp {total_harga:,}")
    print('Pilih Menu:')
    print('1. Bayar')
    print('0. Keluar')
    while True:
        pilihan = input('Masukkan Pilihan Anda:').lower()

        if pilihan == '1' or pilihan == 'bayar':
            os.system('cls')
            break
        elif pilihan == '0' or pilihan == 'keluar':
            os.system('cls')
            menucustomer()
            break
        else:
            print('Pilihan tidak valid!')
            input('Tekan enter untuk mencoba lagi')
            continue

    while True:
        alamat = input('Masukkan alamat pengiriman: ')
        if alamat:
            break
        print("Alamat tidak boleh kosong!")

    print("*********** PEMBAYARAN ***********")
    print(f"Total yang harus dibayar: Rp {total_harga:,}")

    while True:
        try:
            bayar = int(input("Masukkan nominal uang Anda: Rp "))
            if bayar < total_harga:
                print(f"Uang Anda kurang! Total: Rp {total_harga:,}, Uang Anda: Rp {bayar:,}")
                print("Pembayaran gagal.")
                continue
            else:
                kembalian = bayar - total_harga
                print("Pembayaran berhasil!")
                print(f"Uang diterima : Rp {bayar:,}")
                print(f"Kembalian     : Rp {kembalian:,}")
                metode = f"Nominal: {bayar}, Kembali: {kembalian}"
                break

        except ValueError:
            print("Input tidak valid! Harus angka.")

    print('*********** Konfirmasi Pembayaran ***********')
    print(f'Alamat            : {alamat}')
    print(f'Pembayaran : {metode}')
    print(f'Total Pembayaran  : Rp {total_harga:,}')

    while True:
        konfirmasi = input("Apakah data sudah benar? (y/t): ").lower()
        if konfirmasi == "y":
            print("Checkout berhasil.")
            break
        elif konfirmasi == 't':
            print("Checkout dibatalkan.")
            input('Klik enter...')
            keranjang()
        else:
            print(" Input tidak valid! Harap masukkan y atau t.")


    csvriwayat()

    df_produk = pd.read_csv('produk.csv')

    for _, row in df.iterrows():
        nama = row['Produk']
        jumlah_beli = row['Jumlah']

        if nama in df_produk['Produk'].values:
            idx = df_produk[df_produk['Produk'] == nama].index[0]
            stok_sekarang = int(df_produk.at[idx, 'Stok'])
            df_produk.at[idx, 'Stok'] = stok_sekarang - jumlah_beli

    df_produk.to_csv('produk.csv', index=False)

    transaksi = df[['Produk', 'Harga', 'Jumlah']].copy()
    transaksi['Username'] = usernamelogin
    transaksi['Alamat'] = alamat
    transaksi['Pembayaran'] = metode
    transaksi['status'] = "Telah dipesan"

    transaksi = transaksi[['Username','Produk','Harga','Jumlah', 'Alamat','Pembayaran','status']]
    transaksi.to_csv('pembelian_pending.csv', mode='a', header=False, index=False)

    pd.DataFrame(columns=['Produk','Harga','Jumlah']).to_csv(keranjang_file, index=False)

    print('============================================')
    print('             AGROFARM SUPPLY                ')
    print('============================================')
    print(f'Pengiriman ke Alamat            : {alamat}')
    print(f'Total Pembayaran                : Rp {total_harga:,}')
    print(f'Pembayaran                      : {metode}')
    print('============================================')
    print('           PEMESANAN BERHASIL               ')
    print('        TERIMAKASIH TELAH MEMBELI           ')
    input("Klik Enter untuk kembali ke menu...")
    menucustomer()


def csvriwayat() :
    if not os.path.exists('pembelian_pending.csv'):
        with open('pembelian_pending.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Username','Produk','Harga', 'Jumlah', 'Alamat','Pembayaran','Status'])
            writer.writeheader()


def statuspembelian():
    os.system('cls')
    global usernamelogin

    file_pending = 'pembelian_pending.csv'
    file_selesai = 'pembelian_selesai.csv'

    print('***********************************************')
    print(f"         STATUS PEMBELIAN {usernamelogin.upper()}        ")
    print('***********************************************')

    pending_list = []

    if os.path.exists(file_pending):
        df_pending = pd.read_csv(file_pending)
        user_pending = df_pending[df_pending['Username'] == usernamelogin]

        if not user_pending.empty:
            print(">>> PESANAN MENUNGGU KONFIRMASI ADMIN:")
            print(tabulate(user_pending, headers='keys', tablefmt='fancy_grid', showindex=True))
            pending_list.append(True)

    selesai_list = []

    if os.path.exists(file_selesai):
        df_selesai = pd.read_csv(file_selesai)
        user_selesai = df_selesai[df_selesai['Username'] == usernamelogin]

        if not user_selesai.empty:
            print(">>> PESANAN YANG SUDAH DIKONFIRMASI ADMIN:")
            print(tabulate(user_selesai, headers='keys', tablefmt='fancy_grid', showindex=True))
            selesai_list.append(True)

    if not pending_list and not selesai_list:
        print("Kamu belum memiliki pembelian apapun.")

    input("Klik Enter untuk kembali...")
    menucustomer()


def riwayatpembelian():
    os.system('cls')
    global usernamelogin
    file_selesai = 'pembelian_selesai.csv'

    print('***********************************************')
    print(f"        RIWAYAT PEMBELIAN {usernamelogin.upper()}        ")
    print('***********************************************')

    if not os.path.exists(file_selesai):
        print("Belum ada riwayat pembelian.")
        input("Klik Enter untuk kembali...")
        return

    df = pd.read_csv(file_selesai)
    user_history = df[df['Username'] == usernamelogin]

    if user_history.empty:
        print("Belum ada riwayat pembelian yang selesai.")
        input("Klik Enter untuk kembali...")
        return

    print(tabulate(user_history, headers='keys', tablefmt='fancy_grid', showindex=True))
    input("Klik Enter untuk kembali...")
    menucustomer()





def login_admin():
    os.system('cls')
    print('********************************************')
    print('✦              LOGIN ADMIN                 ✦')
    print('********************************************')
    cekakun()
    username = input('Masukkann Username Anda: ')
    password = input('Masukkan Password: ')

    loginberhasil = False
    if not os.path.exists('akunadmin.csv') :
        with open('akunadmin.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Password'])
            writer.writerow(['admin', 'admin123'])

    with open('akunadmin.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Username'] == username and row['Password'] == password:
                loginberhasil = True
                break

    if loginberhasil:
        print('LOGIN BERHASIL')
        input('Klik Enter untuk melanjutkan...')
        os.system('cls')
        tampilanadmin()

    else:
        print('Username atau Password salah')
        input('Klik Enter untuk mencoba lagi...')
        os.system('cls')
        mainmenu()


def cek_produk() :
    if not os.path.exists('produk.csv'):
        with open('produk.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Produk', 'Harga', 'Stok'])
            writer.writeheader()


def produk():
    cek_produk()
    df = pd.read_csv('produk.csv')
    if df.empty:
        print("Saat ini produk tidak tersedia.")
    else:
        df = df.reset_index(drop=True)
        df.index += 1
        df.insert(0, 'No', df.index)
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))


def tampilanadmin() :
    os.system('cls')
    print('********************************************')
    print('           SELAMAT DATANG ADMIN             ')
    print('              AGORFARM SUPPLY               ')
    print('********************************************')
    produk()
    print('Pilih Menu anda : ')
    print('1. Menambah Produk')
    print('2. Edit Produk')
    print('3. Hapus Produk')
    print('4. Konfirmasi Pemesanan Customer')
    print('5. Cek Pemesanan Customer')
    print('0. Keluar')
    while True :
        pilihan = input('Masukkan menu pilihan anda : ')
        if pilihan == '1':
            os.system('cls')
            tambahproduk()
        elif pilihan == '2':
            os.system('cls')
            editproduk()
        elif pilihan == '3':
            os.system('cls')
            hapusproduk()
        elif pilihan == '4':
            os.system('cls')
            konfirmasipesanan()
        elif pilihan == '5':
            os.system('cls')
            pesananpelanggan()
        elif pilihan == '0':
            os.system('cls')
            mainmenu()
        else :
            input('Pilihan tidak ada,enter untuk ulang')
            os.system('cls')
            tampilanadmin()


def tambahproduk():
    os.system('cls')
    cek_produk()
    produk()

    while True:
        try:
            nama = input('Masukkan nama produk (Contoh: Cangkul): ').title()
            harga = int(input('Masukkan harga produk (Contoh: 15000): '))
            stok = int(input('Masukkan stok produk (Contoh: 3/4/5/6): '))

            if (['Produk'] == nama):
                print("Nama produk sudah terdaftar, silahkan gunakan nama lain!")
                input("Klik Enter untuk melanjutkan...")
                tambahproduk()
            else:
                df = pd.read_csv('produk.csv')
                new_row = {
                    'Produk': nama,
                    'Harga': harga,
                    'Stok': stok
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv('produk.csv', index=False)
                print("Produk berhasil ditambahkan")
        except ValueError:
            print("Inputan tidak valid!")
        input("Klik Enter untuk melanjutkan...")
        os.system('cls')
        tampilanadmin()


def editproduk():
    os.system('cls')
    cek_produk()
    produk()
    df = pd.read_csv('produk.csv')

    if df.empty:
        print("Tidak ada produk untuk diedit.")
        input("Klik Enter untuk kembali...")
        tampilanadmin()
        return

    while True:
        try:
            nomor = int(input("Masukkan nomor produk (Masukkan 0 untuk kembali): "))

            if nomor == 0:
                    os.system('cls')
                    tampilanadmin()

            if nomor < 1 or nomor > len(df):
                print("Nomor produk tidak valid!")
                input("Klik Enter untuk Mengulang...")
                os.system('cls')
                produk()
                continue

            no = nomor - 1

            nama = input("Masukkan nama produk baru: ").title()
            harga = int(input("Masukkan harga produk baru: "))
            stok = int(input("Masukkan stok produk baru: "))

            while True:
                konfirmasi = input("Apakah Anda yakin ingin mengubah produk ini? (y/t): ").lower()
                if konfirmasi == 'y':
                    df.at[no, 'Produk'] = nama
                    df.at[no, 'Harga'] = harga
                    df.at[no, 'Stok'] = stok
                    df.to_csv('produk.csv', index=False)
                    print("Produk berhasil diperbarui!")
                    input("Klik Enter untuk melanjutkan... ")
                    os.system('cls')
                    tampilanadmin()
                elif konfirmasi == 't':
                    input("Klik Enter untuk kembali ke menu... ")
                    os.system('cls')
                    tampilanadmin()
                else:
                    print("Input tidak valid!")

        except ValueError:
            print("Input tidak valid! Harus angka.")


def hapusproduk():
    os.system('cls')
    cek_produk()
    print("Pilih Produk yang ingin dihapus :")
    produk()
    df = pd.read_csv('produk.csv')

    while True:
        try:
            nomor = int(input("Masukkan nomor produk yang akan dihapus: "))

            if nomor == 0:
                os.system('cls')
                tampilanadmin()

            if nomor < 1 or nomor > len(df):
                print("Nomor produk tidak valid!")
                input("Klik Enter untuk melanjutkan...")
                os.system('cls')
                produk()
                continue

            no = nomor - 1
        except ValueError:
            print('Inputan harus berupa angka')
            input('Klik enter untuk kembali memilih...')
            hapusproduk()

        while True:
            konfirmasi = input('Apakah Anda yakin ingin menghapus produk ini (y/t) : ').lower()
            if konfirmasi == 'y' :
                df = df.drop(df.index[no])
                df.to_csv('produk.csv', index=False)
                print("Produk berhasil dihapus!")
                input('Klik enter untuk melanjutkan...')
                os.system('cls')
                tampilanadmin()
            elif konfirmasi == 't' :
                print("Penghapusan produk dibatalkan")
                input('Klik enter untuk kembali...')
                os.system('cls')
                tampilanadmin()
            else :
                print('Inputan Invalid')


def konfirmasipesanan():
    os.system('cls')
    print("******** KONFIRMASI PESANAN CUSTOMER ********")

    if not os.path.exists('pembelian_pending.csv'):
        print("Belum ada transaksi.")
        input("Klik Enter untuk kembali...")
        tampilanadmin()
        return

    df = pd.read_csv('pembelian_pending.csv')

    pending = df[df['Status'] == "Telah dipesan"]

    if pending.empty:
        print("Tidak ada pesanan yang perlu dikonfirmasi.")
        input("Klik Enter untuk kembali...")
        tampilanadmin()
        return

    print("Daftar pesanan yang belum dikonfirmasi:")
    nomor_urut = 1
    indx = {}

    for idx in pending.index:
        row = pending.loc[idx]
        print(f"{nomor_urut}. Username : {row['Username']}")
        print(f"   Produk     : {row['Produk']}")
        print(f"   Harga      : {row['Harga']}")
        print(f"   Jumlah     : {row['Jumlah']}")
        print(f"   Alamat     : {row['Alamat']}")
        print(f"   Pembayaran : {row['Pembayaran']}")
        print(f"   Status     : {row['Status']}")
        print("----------------------------------------------")
        indx[nomor_urut] = idx
        nomor_urut += 1

    while True:
        try:
            pilihan = int(input("Masukkan nomor pesanan yang ingin dikonfirmasi (0 untuk kembali): "))
            pilihkembali = False

            if pilihan == 0:
                tampilanadmin()

            if pilihan not in indx:
                print("Nomor tidak valid!")
                continue

            idx_asli = indx[pilihan]
            data_konfirmasi = df.loc[idx_asli]

            while True:
                if pilihkembali:
                        break
                konfirmasi = input("Konfirmasi pesanan ini? (y/t): ").lower()

                if konfirmasi == "y":
                    if not os.path.exists("pembelian_selesai.csv"):
                        with open("pembelian_selesai.csv", "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow(["Username","Produk","Harga","Jumlah","Alamat","Pembayaran", "Status"])

                    df.at[idx_asli, 'Status'] = "Telah dikonfirmasi"
                    data_konfirmasi = df.loc[idx_asli]

                    with open("pembelian_selesai.csv", "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            data_konfirmasi["Username"],
                            data_konfirmasi["Produk"],
                            data_konfirmasi["Harga"],
                            data_konfirmasi["Jumlah"],
                            data_konfirmasi["Alamat"],
                            data_konfirmasi["Pembayaran"],
                            data_konfirmasi["Status"]
                        ])

                    df = df.drop(idx_asli)
                    df.to_csv("pembelian_pending.csv", index=False)

                    print("Pesanan berhasil dikonfirmasi!")
                    input("Klik Enter untuk melanjutkan...")
                    while True:
                            lanjutin = input("Ingin konfirmasi customer lain? (y/t): ").lower()
                            if lanjutin == 'y':
                                pilihkembali = True
                                os.system('cls')
                                konfirmasipesanan()
                            elif lanjutin == 't':
                                input('Klik untuk kembali ke menu...')
                                tampilanadmin()
                            else:
                                print(" Input tidak valid! Harap masukkan y atau t.")

                elif konfirmasi == "t":
                    print("Konfirmasi dibatalkan.")
                    input("Klik Enter untuk kembali...")
                    tampilanadmin()

                else:
                    print("Input tidak valid!")

        except ValueError:
            print("Input harus berupa angka!")



def pesananpelanggan():
    os.system('cls')
    file_pending = 'pembelian_selesai.csv'

    print("***********************************************")
    print("               PESANAN CUSTOMER                ")
    print("***********************************************")

    if not os.path.exists(file_pending):
        print("Belum ada pesanan pelanggan.")
        input("Klik Enter untuk kembali...")
        tampilanadmin()

    df = pd.read_csv(file_pending)

    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=True))

    input("Klik Enter untuk kembali ke menu admin...")
    tampilanadmin()

mainmenu()
