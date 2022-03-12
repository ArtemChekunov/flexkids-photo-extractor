#!/usr/bin/env python
import argparse
import logging
import time
from pathlib import Path

from requests_html import HTMLSession

logging.basicConfig(format='t=%(asctime)s level=%(levelname)s msg=%(message)s', level='INFO')


class FlexKids:
    def __init__(self, url, login, password):
        self.url = url
        self.session = HTMLSession()
        req_login = self.session.post(f'{url}/login/login', data={"username": login, "password": password, "role": 7})
        req_login.raise_for_status()

    def get(self, path):
        return self.session.get(f'{self.url}/{path}')

    def post(self, path: str, data: dict):
        return self.session.post(f'{self.url}/{path}', data=data)

    @property
    def months(self):
        r = self.get('ouder/fotoalbum')
        return [{"month": i.attrs['data-month'], "year": i.attrs['data-year']} for i in
                r.html.xpath('//*[@id="select_maand"]/option')]

    @property
    def foto_albums(self):
        return [FlexKidsFotoAlbum(flex_kids=self, year=i['year'], month=i['month']) for i in self.months]


class FlexKidsFotoAlbum:
    def __init__(self, flex_kids: FlexKids, year, month):
        self.flex_kids = flex_kids
        self.year = year
        self.month = month

    @property
    def photo_ids(self):
        req = self.flex_kids.post('ouder/fotoalbum/standaardalbum', data={"year": self.year, "month": self.month})
        return req.json()['FOTOS']

    @property
    def photos(self):
        return [FlexKidsFoto(self.flex_kids, content_id=i) for i in self.photo_ids]


class FlexKidsFoto:
    def __init__(self, flex_kids: FlexKids, content_id):
        self.flex_kids = flex_kids
        self.id = content_id

    def write(self, dir_path):
        req = self.flex_kids.get(f'ouder/media/download/media/{self.id}')
        file_name = req.headers['Content-disposition'].split('=')[-1]
        path = Path(f'{dir_path}/{file_name}')
        if not path.parent.is_dir():
            path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            logging.info(f'skip exist photo: {path}')
            return False

        logging.info(f'fetch photo: {path}')
        with path.open('wb') as f:
            f.write(req.content)

        return True


def main(args):
    logging.info(f'init session: {args.url}')
    fk = FlexKids(url=args.url, login=args.login, password=args.password)

    logging.info('fetching albums')
    for album in fk.foto_albums:
        logging.info(f'fetching photos from {album.year}/{album.month}')
        for photo in album.photos:
            is_written = photo.write(f'{args.target_dir}/{album.year}/{album.month}')
            if is_written:
                time.sleep(args.sleep)  # avoid sleep if the file was prefetched


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', required=True, help='example: https://<kinderopvang>.flexkids.nl')
    parser.add_argument('--login', '-l', required=True)
    parser.add_argument('--password', '-p', required=True)
    parser.add_argument('--target-dir', '-d', default='photos')
    parser.add_argument('--sleep', '-s', type=int, default=1, help='sleep between fetching photos (avoiding ddos)')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    try:
        main(args)
    except KeyboardInterrupt:
        pass
