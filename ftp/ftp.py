import ftplib
import os
import socket

def ftp_put(host,user,passwd,file):
    try:
        ftp=ftplib.FTP(host)
    except (socket.error,socket.gaierror),e:
        print("ERROR:cannot reach {0}".format(host))
        return False
    print "***connected to host %s" %host

    try:
        if user and passwd:
            ftp.login(user,passwd)
        else:
            ftp.login()
    except ftplib.error_perm:
        print("ERROR:cannot login")
        ftp.quit()
        return False

    try:
        command='STOR ' + file
        filehandler = open(file, 'rb')
        ftp.storbinary(command,filehandler,1024)
        filehandler.close()
    except ftplib.error_perm:
        print("ERROR:cannot put file '%s'" %file)
        ftp.quit()
        return False

    print("put file '%s' successful" %file)
    return True

def ftp_del(host,user,passwd,filename):
    try:
        ftp=ftplib.FTP(host)
    except (socket.error,socket.gaierror),e:
        print("ERROR:cannot reach {0}".format(host))
        return False
    print "***connected to host %s" %host

    try:
        if user and passwd:
            ftp.login(user,passwd)
        elif user and passwd is None:
            ftp.login(user)
        else:
            ftp.login()
    except ftplib.error_perm:
        print("ERROR:cannot login")
        ftp.quit()
        return False

    try:
        ftp.delete(filename)
    except:
        print("ERROR:cannot delete file '%s'" %filename)
        ftp.quit()
        return False

    print("delete file '%s' successful" %filename)
    return True

if __name__ == '__main__':
    ftp_put('192.168.1.100','anonymous',None,'Python-3.4.0.tgz')
    ftp_del('192.168.1.100','anonymous',None,'Python-3.4.0.tgz')
        
