# transfersh-client

Command line tool for Transfer.sh server.

It read a configuration yaml file:
> User level: `$HOME/.transfersh/config.yaml`

> System level: `/etc/transfersh/config.yaml`


    usage: transfer [-h] [--verbose] [--server SERVER] [-d MAX_DOWNLOADS] [-t MAX_DAYS] F [F ...]

    Transfersh client.

    positional arguments:
    F                     Files for upload

    optional arguments:
    -h, --help            show this help message and exit
    -v, --verbose
    --server SERVER       Transfersh server url
    -d MAX_DOWNLOADS, --max-downloads MAX_DOWNLOADS
                          Max possible downloads
    -t MAX_DAYS, --max-days MAX_DAYS
                          Max days saved

## Usage

    pip install transfershclient
