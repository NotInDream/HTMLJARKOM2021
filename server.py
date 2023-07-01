from socket import *                        # Library buat bikin soket
import sys                                  # Library buat stop program.
serverSocket = socket(AF_INET, SOCK_STREAM) # Membuat socket server baru dengan menggunakan protokol IPv4 (AF_INET) dan protokol TCP (SOCK_STREAM).
serverName = '127.0.0.1'                    # 127.0.0.1 adalah server local, bisa juga gunakan "localhost"            
serverPort = 12345                             # port server yang digunakan disini adalah port 80
serverSocket.bind((serverName, serverPort)) # Mengaitkan server dan port
serverSocket.listen(1)              # Socket server bisa menerima maksimal 1 sinyal.
while True:                         # Program akan running sambil menunggu sinyal.
    print('Ready to Serve...')      # Jika berhasil terkoneksi akan mengeluarkan output ready to serve 
    connectionSocket, addr = serverSocket.accept()      # Penyimpanan alamat ip dan port pada variabel addr
    try:                                                # Cek data dari klient
        message = connectionSocket.recv(1024).decode()  # Proses decode
        filename = message.split()[1]                   # Proses memparsing 
        f = open(filename[1:], 'rb')                    # Membuka file 'rb' untuk mode membaca file non teks dalam bentuk biner
        outputdata = f.read()                           # Pembacaan isi file
        status_line = "HTTP/1.1 200 OK\r\n"                     # HTTP response jika berhasil diterima
        if filename.endswith('.jpg') or filename.endswith('.jpeg'): # Pengecekan tipe file gambar jpg atau jpeg
            content_type = "Content-Type: image/jpeg\r\n\r\n"  # HTTP response untuk menampilkan gambar jpg atau jpeg
        elif filename.endswith('.png'):                             # Pengecekan tipe file gambar jpg atau jpeg
            content_type = "Content-Type: image/png\r\n\r\n"   # # HTTP response untuk menampilkan gambar png
        else:
            content_type = "Content-Type: text/html; charset=utf-8\r\n\r\n"  # HTTP response untuk text/html
        response = status_line+content_type                # Header dari HTTP Response
        connectionSocket.send(response.encode())           # Proses pengiriman data dan encode
        for i in range(0, len(outputdata)):                # Looping pada isi file yang berada di variable outputdata
            connectionSocket.send(outputdata[i:i+1])       # Mengirim isi file melalui connectionSocket
        connectionSocket.send("\r\n".encode())             # Melakukan escape sequence (\r\n) melalui connectionSocket ketika loop berakhir
    except IOError:                                        # Jika data yang dikirim tidak ada di pengkondisian di atas
        error = "HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n" # HTTP response untuk not found    
        connectionSocket.send(error.encode())                               # response dikirim ke klien melalui connectionSocket
        connectionSocket.send("<html><head><link rel='stylesheet' href='style.css'><title>Error</title></head><body><h1>ERROR 404 NOT FOUND :(</h1><h2><a href=\"index.html#slider-image-1\">Back to home</a></h2></body></html>".encode())  # Page not found
    connectionSocket.close()        # Hentikan koneksi socket; memperbolehkan ada koneksi baru
serverSocket.close()                # Hentikan socket server; memutus koneksi antar klien dan server
sys.exit()                          # Exit program
