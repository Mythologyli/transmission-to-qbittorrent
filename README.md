# Transmission to qBittorrent

[中文](./README.zh.md)

Transfer all torrents in [Transmission](https://transmissionbt.com/) to [qBittorrent](https://www.qbittorrent.org/). Support for skipping checking.

**Warning: Use with caution! I am not responsible for any consequences.**

## Usage

1. Download this repository.

2. Make sure the script can access the Transmission's torrent file directory and resume file directory.
   
   The torrent file directory contains all torrent files <torrent_hash>.torrent.
   
3. If Transmission and qBittorrent are running in Docker containers, make sure their torrent download directories are the same in both Docker containers.

4. Make sure that the Python 3 runtime exists.

5. Create config.json in repository folder according to config.json.template:

   + skip_check: skip check or not
   + qbittorrent:
     + host: IP address of qBittorrent Web
     + port: port of qBittorrent Web
     + username
     + password
   + transmission:
     + protocol: "http" or "https"
     + host: IP address of Transmission Web
     + port: port of Transmission Web
     + path: no need to modify
     + username
     + password
     + torrent_dir: directory of torrent files. If Transmission runs in a Docker container, it is **a path in the host**

6. Run the script: `python3 main.py` or `python main.py`.

7. After running, start torrents manually.

## Thanks

+ [qbittorrent-api](https://github.com/rmartin16/qbittorrent-api)
+ [transmission-rpc](https://github.com/trim21/transmission-rpc)