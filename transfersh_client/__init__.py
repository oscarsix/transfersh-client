__VERSION__ = '1.1.0'

from pathlib import Path
import random
import requests
import string
import subprocess
import tarfile
import tempfile

class TransfershClientError(Exception):
    pass


class TransfershClientConfigError(TransfershClientError):
    def __init__(self, message):
        self.message = message


class TransfershServerStatusCodeError(TransfershClientError):
    def __init__(self, message):
        self.message = message


class TransfershClient:
    def __init__(self, config):
        try:
            self.config = config
        except Exception as e:
            raise TransfershClientConfigError('Missing config parameter: ' + str(e))

    def upload_file(self, file, filename):
        headers = {
            'Max-Downloads': str(self.config['args'].max_downloads),
            'Max-Days': str(self.config['args'].max_days)
        }
        files = {
            'file': (
                filename,
                open(str(file), 'rb')
            )
        }
        result = requests.post(self.config['server'], files=files, headers=headers)
        if 400 <= result.status_code < 600:
            raise TransfershServerStatusCodeError(str(result.status_code))
        return result

    def upload(self, **kwargs):
        files_or_dirs = kwargs.get('files')
        results = list()
        for file_or_dir in files_or_dirs:
            absolute_file = Path(file_or_dir).resolve()
            p = Path(absolute_file)
            if p.is_file():
                if self.config['args'].encrypt:
                    result, password = self.symmetric_encrypted_upload_file(absolute_file, p.name)
                    results.append({
                        'status_code': result.status_code,
                        'text': result.text,
                        'result': result,
                        'password': password
                    })
                else:
                    result = self.upload_file(absolute_file, p.name)
                    results.append({
                        'status_code': result.status_code,
                        'text': result.text,
                        'result': result
                    })
            elif p.is_dir():
                with tempfile.NamedTemporaryFile() as tmpfile:
                    with tarfile.open(tmpfile.name, "w:gz") as tar:
                        tar.add(absolute_file, arcname=p.name)
                    if self.config['args'].encrypt:
                        result, password = self.symmetric_encrypted_upload_file(tmpfile.name, p.name + '.tar.gz')
                        results.append({
                            'status_code': result.status_code,
                            'text': result.text,
                            'result': result,
                            'password': password
                        })
                    else:
                        result = self.upload_file(tmpfile.name, p.name + '.tar.gz')
                        results.append({
                            'status_code': result.status_code,
                            'text': result.text,
                            'result': result
                        })
            else:
                results.append({
                    'text': 'WARNING: File ' + str(absolute_file) + ' not exist'
                })
        return results

    def symmetric_encrypted_upload_file(self, file, filename):
        password = self.randompassword()
        with tempfile.NamedTemporaryFile() as tmpfile:
            subprocess.check_output(['gpg', '--symmetric', '--armor', '--batch',
                                     '--yes', '--passphrase', password, '-o', tmpfile.name, str(file)])
            result = self.upload_file(Path(tmpfile.name).resolve(), filename + '.asc')
            return result, password

    @staticmethod
    def randompassword():
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        size = random.randint(8, 12)
        return ''.join(random.choice(chars) for x in range(size))