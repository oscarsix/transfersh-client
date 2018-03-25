# transfersh-client

Command line tool for Transfer.sh server.

[![PyPI version](https://badge.fury.io/py/transfershclient.svg)](https://badge.fury.io/py/transfershclient)

## Configutation file

You can set the transfersh server url in a configuration file:

> User level: `$HOME/.transfersh/config.yaml`

> System level: `/etc/transfersh/config.yaml`

    ---
    server: 'https://transfer.sh'

## Install

    pip install transferclient

## Usage

    usage: transfer [-h] [--verbose] [--server SERVER] [-d MAX_DOWNLOADS] [-t MAX_DAYS] F [F ...]

    Transfersh client.

    positional arguments:
    F                         Files for upload

    optional arguments:
    -h, --help                show this help message and exit
    -v, --verbose
    --server SERVER           Transfersh server url
    -d MAX_DOWNLOADS, --max-downloads MAX_DOWNLOADS
                              Max possible downloads
    -t MAX_DAYS, --max-days MAX_DAYS
                              Max days saved
     -e, --encrypt            symmetric gpg encryted upload

### From TTY

    transfer ./testfile.txt ./testdir

### From PIPE

    cat /var/log/syslog | transfer
