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


def upload(ftp, filepath, remote_path):
    f = open(filepath, 'rb')
    ftp.cwd(remote_path)
    file_name = os.path.split(filepath)[-1]
    try:
        ftp.storbinary('STOR ' + file_name, f, CONST_BUFFER_SIZE)
    except ftplib.error_perm:
        return False
    return True


def ftp_upload(local_path, remote_path):
    ftp = connect()
    success_list = []
    failed_list = []
    file_list = os.listdir(local_path)
    print(file_list)
    for up_file in file_list:
        if not os.path.exists(local_path + up_file):
            print("UPLOAD:file not exist:" + str(up_file))
            continue
        elif not os.path.isfile(local_path + up_file):
            print("UPLOAD:is not a file:" + str(up_file))
            continue
        if upload(ftp, local_path + up_file, remote_path):
            success_list.append(local_path + up_file)
        else:
            failed_list.append(local_path + up_file)
    if len(success_list) > 0:
        print('UPLOAD SUCCESS:' + " ".join(success_list))
    if len(failed_list) > 0:
        print("UPLOAD FAILED: %s" + " ".join(failed_list))

    disconnect(ftp)


if __name__ == '__main__':
    ftp_upload('D:/pabank2/', '/amazon')
