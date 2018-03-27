__VERSION__ = '1.1.6'

from pathlib import Path
import random
import requests
import shutil
import string
import subprocess
import tarfile
import tempfile


class TransfershClient:

    def __init__(self, **kwargs):
        self.server_url = kwargs.get('server_url')
        self.max_downloads = kwargs.get('max_downloads', 1000)
        self.max_days = kwargs.get('max_days', 1000)
        self.gpg_binary = kwargs.get('gpg_binary', 'gpg')
        self.gpg_options = kwargs.get('gpg_options', ['--symmetric', '--armor', '--batch', '--no-tty', '--yes'])

    def upload_file(self, file, filename=None):
        headers = {
            'Max-Downloads': str(self.max_downloads),
            'Max-Days': str(self.max_days)}

        f = {'file': (filename, open(str(file), 'rb'))}
        result = requests.post(self.server_url, files=f, headers=headers)

        if 400 <= result.status_code < 600:
            raise Exception('status_code = ' + str(result.status_code))

        return result

    def upload(self, **kwargs):
        files_or_dirs = kwargs.get('files')
        encrypt = kwargs.get('encrypt', False)

        if encrypt and shutil.which(self.gpg_binary) is None:
            raise Exception('gpg not found')

        results = list()

        for file_or_dir in files_or_dirs:

            absolute_file = Path(file_or_dir).resolve()
            p = Path(absolute_file)
            password = None

            if p.is_file():
                if encrypt:
                    result, password = self.symmetric_encrypted_upload_file(absolute_file, p.name)
                else:
                    result = self.upload_file(absolute_file, p.name)
            elif p.is_dir():
                with tempfile.NamedTemporaryFile() as tmpfile:
                    with tarfile.open(tmpfile.name, "w:gz") as tar:
                        tar.add(str(absolute_file))

                    if encrypt:
                        result, password = self.symmetric_encrypted_upload_file(tmpfile.name, p.name + '.tar.gz')
                    else:
                        result = self.upload_file(tmpfile.name, p.name + '.tar.gz')
            else:
                result = 'WARNING: File ' + str(absolute_file) + ' not exist'

            results.append({
                'result': result,
                'password': password
            })

        return results

    def symmetric_encrypted_upload_file(self, file, filename):
        password = self.randompassword()
        with tempfile.NamedTemporaryFile() as tmpfile:
            subprocess.check_output([self.gpg_binary] + self.gpg_options + ['--passphrase', password, '-o', tmpfile.name, str(file)])
            result = self.upload_file(Path(tmpfile.name).resolve(), filename + '.asc')
            return result, password

    @staticmethod
    def randompassword():
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        size = random.randint(8, 12)
        return ''.join(random.choice(chars) for x in range(size))