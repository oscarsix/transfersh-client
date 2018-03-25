__VERSION__ = '0.0.2'

from pathlib import Path
import requests
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
            self.transfersh_server = config['server']
        except Exception as e:
            raise TransfershClientConfigError('Missing config parameter: ' + str(e))

    def upload_file(self, file, **kwargs):
        max_downloads = kwargs['max_downloads']
        max_days = kwargs['max_days']
        filename = kwargs['filename']
        headers = {
            'Max-Downloads': str(max_downloads),
            'Max-Days': str(max_days)
        }
        files = {
            'file': (
                filename,
                open(str(file), 'rb')
            )
        }
        result = requests.post(self.transfersh_server,
                               files=files,
                               headers=headers)
        if 400 <= result.status_code < 600:
            raise TransfershServerStatusCodeError(str(result.status_code))
        return result

    def upload(self, **kwargs):
        files_or_dirs = kwargs['files']
        max_downloads = kwargs['max_downloads']
        max_days = kwargs['max_days']
        results = list()
        for file_or_dir in files_or_dirs:
            absolute_file = Path(file_or_dir).resolve()
            p = Path(absolute_file)
            if p.is_file():
                result = self.upload_file(absolute_file,
                                          filename=p.name,
                                          max_downloads=max_downloads,
                                          max_days=max_days)
                results.append({
                    'status_code': result.status_code,
                    'text': result.text,
                    'result': result
                })
            elif p.is_dir():
                with tempfile.NamedTemporaryFile() as tmpfile:
                    with tarfile.open(tmpfile.name, "w:gz") as tar:
                        tar.add(absolute_file, arcname=p.name)
                    result = self.upload_file(tmpfile.name,
                                              filename=p.name + '.tar.gz',
                                              max_downloads=max_downloads,
                                              max_days=max_days)
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
