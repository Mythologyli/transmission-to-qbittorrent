import json
import time
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

import qbittorrentapi
import transmission_rpc


def main():
    # Get config from config.json.
    config: dict = json.load(open('./config.json', 'r'))

    # Skip check or not.
    skip_check: bool = config['skip_check']

    # qBittorrent settings.
    qb_host: str = config['qbittorrent']['host']
    qb_port: int = config['qbittorrent']['port']
    qb_username: str | None = config['qbittorrent']['username'] or None
    qb_password: str | None = config['qbittorrent']['password'] or None

    # Transmission settings.
    tr_protocol: Literal['http', 'https'] = config['transmission']['protocol']
    tr_host: str = config['transmission']['host']
    tr_port: int = config['transmission']['port']
    tr_path: str = config['transmission']['path']
    tr_username: str | None = config['transmission']['username'] or None
    tr_password: str | None = config['transmission']['password'] or None
    tr_torrent_dir: str = config['transmission']['torrent_dir']

    # Connect qBittorrent.
    qb_client = qbittorrentapi.Client(
        host=qb_host,
        port=qb_port,
        username=qb_username,
        password=qb_password
    )

    # Check if login is successful.
    qb_client.auth_log_in()
    print(f"Connected to qBittorrent {qb_client.app.version}.")

    # Connect Transmission.
    tr_client = transmission_rpc.Client(
        protocol=tr_protocol,
        username=tr_username,
        password=tr_password,
        host=tr_host,
        port=tr_port,
        path=tr_path
    )

    # Check if login is successful.
    tr_session = tr_client.session_stats()
    print(f"Connected to Transmission {tr_session.version}.")

    # Get all hashes of torrents in qBittorrent.
    qb_torrents = qb_client.torrents_info()
    qb_torrent_hashes: list[str] = [torrent.hash for torrent in qb_torrents]
    print(f"Found {len(qb_torrent_hashes)} torrents in qBittorrent.")

    # Get all torrents in Transmission.
    tr_torrents = tr_client.get_torrents()
    print(f"Fetched {len(tr_torrents)} torrents in Transmission. Transfer them to qBittorrent...")

    for tr_torrent in tr_torrents:
        # Pause the torrent in Transmission.
        tr_torrent.stop()

        # Skip torrents that already exist in qBittorrent.
        if tr_torrent.hashString in qb_torrent_hashes:
            print(f"Torrent {tr_torrent.name} already exists in qBittorrent, skipping.")
            continue

        # Get torrent file path.
        tr_torrent_path = str(Path(tr_torrent_dir).expanduser().joinpath(tr_torrent.hashString + '.torrent').absolute())

        # Add torrent to qBittorrent.
        qb_client.torrents_add(
            torrent_files=open(tr_torrent_path, 'rb'),
            save_path=tr_torrent.download_dir,
            is_skip_checking=skip_check,
            is_paused=True
        )

        try:
            tr_torrent_tracker_domain = urlparse(tr_torrent.trackers[0]['announce']).netloc
        except IndexError:
            tr_torrent_tracker_domain = 'None'
        print(f"Torrent: {tr_torrent.name} Path: {tr_torrent.download_dir} Tracker: {tr_torrent_tracker_domain}")

        time.sleep(1)


if __name__ == "__main__":
    main()
