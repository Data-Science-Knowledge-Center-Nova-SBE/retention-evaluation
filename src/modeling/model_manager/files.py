import paramiko
import pickle
import environment


def get_sftp_connection():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(environment.HOST, 22, environment.SERVER_USERNAME, environment.SERVER_PASSWORD)
    sftp = ssh.open_sftp()
    return sftp, ssh


def close_connect(sftp, ssh):
    sftp.close()
    ssh.close()


def upload_file(localpath, name):
    sftp, ssh = get_sftp_connection()

    path = environment.FILES_PATH + "/" + name
    sftp.put(localpath, path)

    close_connect(sftp, ssh)

def download_file(name):
    sftp, ssh = get_sftp_connection()

    path = environment.FILES_PATH + "/" + name
    remote_file = sftp.open(path, 'rb')
    try:
        file = pickle.load(remote_file)
    finally:
        remote_file.close()

    close_connect(sftp, ssh)
    return file