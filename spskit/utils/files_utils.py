from datetime import datetime
import os
import shutil
import zipfile

import logging


class FileInfo:

    def __init__(self, file_path):
        self.file_path = file_path
        self.basename = os.path.basename(file_path)
        self.dirname = os.path.dirname(file_path)
        self.name, self.ext = os.path.splitext(self.basename)
        if self.basename.endswith('.sgm.xml'):
            self.name, ign = os.path.splitext(self.name)
        self.name_prefix = self.name


def unzip_file(zip_file_path):
    files = []
    with open(zip_file_path, 'rb') as f:
        z = zipfile.ZipFile(f)
        for name in z.namelist():
            z.extract(name, "./")
            files.append(name)
    return files


def delete_file_or_folder(path):
    if os.path.isdir(path):
        for item in os.listdir(path):
            delete_file_or_folder(path + '/' + item)
        try:
            shutil.rmtree(path)
        except:
            logging.info('Unable to delete: %s' % path)

    elif os.path.isfile(path):
        try:
            os.unlink(path)
        except:
            logging.info('Unable to delete: %s' % path)


def update_zipfile(zip_filename, files, src_path, mode='a', delete=False):
    with zipfile.ZipFile(
            zip_filename,
            mode,
            compression=zipfile.ZIP_DEFLATED,
            allowZip64=True) as zipf:
        for f in files:
            src = os.path.join(src_path, f)
            zipf.write(src, arcname=f)
            if delete is True:
                delete_file_or_folder(src)
    logging.info('Files zipped into: %s' % zip_filename)



def packing_zip(files):
    now = datetime.now().isoformat()[0:10]

    target = 'scielo_{0}.zip'.format(now)

    logging.info('zipping XML files to: %s' % target)

    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        for xml_file in files:
            zipf.write('xml/{0}'.format(xml_file), arcname=xml_file)

    logging.debug('Files zipped into: %s' % target)

    return target


def write_file(filename, content, mode='w'):
    content = content.encode('utf-8')
    with open(filename, mode) as f:
        try:
            f.write(content)
        except (IOError, ValueError):
            logging.error('Error writing file: %s' % filename, exc_info=True)
        except Exception as e:
            logging.exception('tools.write_file(): %s' % filename, e)


def write_log(msg):
    now = datetime.now().isoformat()[0:10]
    issn = msg.split(':')[1][1:10]
    if not os.path.isdir("reports"):
        os.makedirs("reports")
    filename = "reports/{0}_{1}_errors.txt".format(issn, now)
    error_report = open(filename, "a")
    msg = u'%s\r\n' % msg
    try:
        error_report.write(msg.encode('utf-8'))
    except Exception as e:
        logging.exception('tools.write_log(%s): ' % filename, e)

    error_report.close()


def read_file(file_path):
    return open(file_path).read()
