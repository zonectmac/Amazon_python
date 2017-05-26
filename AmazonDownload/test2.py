import ftplib, socket, os, sys

server = '120.77.2.209'
username = 'financeftp'
password = 'ftp#666!'
CONST_BUFFER_SIZE = 1024 * 20


def connect():
    try:
        ftp_connection = ftplib.FTP(server, username, password)
        return ftp_connection
    except socket.error and socket.gaierror:
        print("FTP is unavailable,please check the host,username and password!")
        sys.exit(0)


def disconnect(ftp):
    ftp.quit()


def upload(ftp, filepath):
    f = open(filepath, 'rb')
    file_name = os.path.split(filepath)[-1]
    try:
        ftp.storbinary('STOR ' + file_name, f, CONST_BUFFER_SIZE)
    except ftplib.error_perm:
        return False
    return True


def download(ftp, filename):
    f = open(filename, 'wb').write
    try:
        ftp.retrbinary('RETR ' + filename, f, CONST_BUFFER_SIZE)
    except ftplib.error_perm:
        return False
    return True


def ftp_list(ftp):
    ftp.dir()


def find(ftp, filename):
    ftp_f_list = ftp.nlst()
    if filename in ftp_f_list:
        return True
    return False


def ftp_help():
    print("help info:")
    print("[./ftp.py l]\t show the file list of the ftp site ")
    print("[./ftp.py f filenamA filenameB]\t check if the file is in the ftp site")
    print("[./ftp.py p filenameA filenameB]\t upload file into ftp site")
    print("[./ftp.py g filenameA filenameB]\t get file from ftp site")
    print("[./ftp.py h]\t show help info")
    print("other params are invalid")


def stp_upload():
    args = sys.argv[1:]
    if len(args) == 0:
        print("Params needed!")
        sys.exit(0)
    ftp = connect()
    success_list = []
    failed_list = []
    if args[0] == 'p':
        f_list = args[1:]
        for up_file in f_list:
            if not os.path.exists(up_file):
                print("UPLOAD:file not exist" % up_file)
                continue
            elif not os.path.isfile(up_file):
                print("UPLOAD:is not a file" % up_file)
                continue
            if upload(ftp, up_file):
                success_list.append(up_file)
            else:
                failed_list.append(up_file)
    if len(success_list) > 0:
        print('UPLOAD SUCCESS:' + " ".join(success_list))
    if len(failed_list) > 0:
        print("UPLOAD FAILED: %s" + " ".join(failed_list))

    disconnect(ftp)


if __name__ == '__main__':
    stp_upload()
