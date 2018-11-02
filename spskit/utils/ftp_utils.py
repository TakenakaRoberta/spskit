from datetime import datetime
import os

import logging
import contextlib


class FTPService(object):

    def __init__(
            self,
            host='localhost',
            port='21',
            user='anonymous',
            passwd='anonymous'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.ftp = None

    def connect(self, timeout=60):
        if self.ftp is None:
            self.ftp = FTP()
        self.ftp.connect(self.host, self.port, timeout=timeout)
        self.ftp.login(user=self.user, passwd=self.passwd)

    def close(self):
        try:
            self.ftp.quit()
        except:
            self.ftp.close()

    @contextlib.contextmanager
    def session_context(self, timeout=60):
        self.connect(timeout)
        yield
        self.close()

    def mkdirs(self, dirs, timeout=60):
        with self.session_context(timeout):
            folders = dirs.split('/')
            for folder in folders:
                try:
                    self.ftp.mkd(folder)
                except:
                    logging.info('FTP: MKD (%s)' % (dirs, ), exc_info=True)
                self.ftp.cwd(folder)

    def send_file(self, local_filename, remote_filename, timeout=60):
        with self.session_context(timeout):
            f = open(local_filename, 'rb')
            try:
                self.ftp.storbinary('STOR {}'.format(remote_filename), f)
            except all_errors:
                logging.info(
                    'FTP: Unable to send %s to %s' %
                    (local_filename, remote_filename), exc_info=True)
            f.close()


def send_collections_reports(ftp_host, ftp_user, ftp_passwd,
                             local_path='collections_reports',
                             remote_path='collections_reports'):
    ftp_service = FTPService(ftp_host, user=ftp_user, passwd=ftp_passwd)
    reports_root_path = XML_ERRORS_ROOT_PATH

    zips_root_path = local_path
    if not os.path.isdir(zips_root_path):
        os.makedirs(zips_root_path)

    for collection_name in os.listdir(reports_root_path):
        print(collection_name)
        path = os.path.join(reports_root_path, collection_name)
        if os.path.isdir(path):
            reports = CollectionReports(
                        collection_name, reports_root_path, zips_root_path)
            reports.zip(delete=False)
            reports.ftp(ftp_service, remote_path, delete=True)



def ftp_connect(ftp_host='localhost',
                user='anonymous',
                passwd='anonymous'):

    ftp = FTP(ftp_host)
    ftp.login(user=user, passwd=passwd)

    return ftp


def send_to_ftp(file_name,
                ftp_host='localhost',
                user='anonymous',
                passwd='anonymous'):

    now = datetime.now().isoformat()[0:10]

    target = 'scielo_{0}.zip'.format(now)

    ftp = ftp_connect(ftp_host=ftp_host, user=user, passwd=passwd)
    f = open('{0}'.format(file_name), 'rb')
    ftp.storbinary('STOR inbound/{0}'.format(target), f)
    f.close()
    ftp.quit()
    logging.debug('file sent to ftp: %s' % target)

    send_collections_reports(ftp_host, user, passwd)


def send_take_off_files_to_ftp(ftp_host='localhost',
                               user='anonymous',
                               passwd='anonymous',
                               remove_origin=False):

    ftp = ftp_connect(ftp_host=ftp_host, user=user, passwd=passwd)

    for fl in os.listdir('controller'):
        if fl.split('.')[-1] == 'del':
            f = open('controller/{0}'.format(fl), 'rb')
            ftp.storbinary('STOR inbound/{0}'.format(fl), f)
            f.close()
            logging.debug('Takeoff file sent to ftp: %s' % fl)

            if remove_origin:
                os.remove('controller/{0}'.format(fl))
                logging.debug('Takeoff file removed from origin: %s' % fl)

    ftp.quit()


def remove_previous_unbound_files_from_ftp(ftp_host='localhost',
                           user='anonymous',
                           passwd='anonymous',
                           remove_origin=False):

    ftp = ftp_connect(ftp_host=ftp_host, user=user, passwd=passwd)
    ftp.cwd('inbound')
    report_files = ftp.nlst('*')

    for report_file in report_files:
        logging.debug('Previous unbound files removed from ftp: %s' % report_file)
        ftp.delete(report_file)


def get_sync_file_from_ftp(ftp_host='localhost',
                           user='anonymous',
                           passwd='anonymous',
                           remove_origin=False):

    ftp = ftp_connect(ftp_host=ftp_host, user=user, passwd=passwd)
    ftp.cwd('reports')
    report_files = ftp.nlst('SCIELO_ProcessedRecordIds*')
    with open('controller/validated_ids.txt', 'wb') as f:
        def callback(data):
            f.write(data)
        for report_file in report_files:
            ftp.retrbinary('RETR %s' % report_file, callback)

    ftp.quit()
    f.close()

    if remove_origin:
        for report_file in report_files:
            logging.debug('Syncronization files removed from ftp: %s' % report_file)
            ftp.delete(report_file)


def get_to_update_file_from_ftp(ftp_host='localhost',
                                user='anonymous',
                                passwd='anonymous',
                                remove_origin=False):

    ftp = ftp_connect(ftp_host=ftp_host, user=user, passwd=passwd)
    ftp.cwd('controller')
    with open('controller/toupdate.txt', 'wb') as f:
        def callback(data):
            f.write(data)
        try:
            ftp.retrbinary('RETR %s' % 'toupdate.txt', callback)
        except error_perm:
            return None

    if remove_origin:
        ftp.delete('toupdate.txt')

    ftp.quit()
    f.close()


def get_keep_into_file_from_ftp(ftp_host='localhost',
                                user='anonymous',
                                passwd='anonymous',
                                remove_origin=False):

    ftp = ftp_connect(ftp_host=ftp_host, user=user, passwd=passwd)
    ftp.cwd('controller')
    with open('controller/keepinto.txt', 'wb') as f:
        def callback(data):
            f.write(data)
        try:
            ftp.retrbinary('RETR %s' % 'keepinto.txt', callback)
        except error_perm:
            return None

    if remove_origin:
        ftp.delete('keepinto.txt')

    ftp.quit()
    f.close()


def get_take_off_files_from_ftp(ftp_host='localhost',
                                user='anonymous',
                                passwd='anonymous',
                                remove_origin=False):

    ftp = ftp_connect(ftp_host=ftp_host, user=user, passwd=passwd)
    ftp.cwd('controller')
    report_files = ftp.nlst('takeoff_*.del')
    with open('controller/takeoff.txt', 'wb') as f:
        def callback(data):
            f.write(data)
        for report_file in report_files:
            ftp.retrbinary('RETR %s' % report_file, callback)

    if remove_origin:
        for report_file in report_files:
            ftp.delete(report_file)

    ftp.quit()
    f.close()
