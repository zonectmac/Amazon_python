import os
import config
import zipfile


def read_file_email():
    f = open(os.path.abspath(config.EMAIL_CONTENT))  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    text = line
    while line:
        # print(line, end='')  # 在 Python 3中使用# 后面跟 ',' 将忽略换行符
        line = f.readline()
        text += line

    f.close()  # 获取文件夹大小自己用list(os.walk(path))解决
    return text


def is_file_writing(filepath):
    if os.path.exists(filepath) and os.path.isfile(filepath):
        try:
            os.renames(filepath, filepath)
            print('文件未被操作')
            return False
        except Exception as e:
            print('文件正在下载')
            return True


def del_allfile(path):
    file_dir = os.listdir(path)
    for tmp in file_dir:
        if os.path.exists(path + tmp) and os.path.isfile(path + tmp):
            os.remove(path + tmp)


# 字节bytes转化kb\m\g
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


# 获取文件大小
def getdoc_size(path):
    try:
        if os.path.exists(path) and os.path.isfile(path):
            size = os.path.getsize(path)
            return format_size(size)
    except Exception as err:
        print(err)
        return 0


def file_num(path, end):
    num = 0
    file_dir = os.listdir(path)
    for tmp in file_dir:
        if os.path.exists(path + tmp) and os.path.isfile(path + tmp):
            if os.path.splitext(tmp)[1] == end:
                num += 1

    return num


# 判断某个路径下文件是否存在
def file_is_exist(path, file_name):
    if os.path.exists(path+file_name) and os.path.isfile(path+file_name):
        return True
    return False


def del_file(filepath):
    if os.path.exists(filepath) and os.path.isfile(filepath):
        os.remove(filepath)


# 压缩文件夹
def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        # print arcname
        zf.write(tar, arcname)
    zf.close()
