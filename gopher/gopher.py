#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
import os
import click
import requests
from collections import OrderedDict


API_URL = "https://gopherize.me/api/"


class Gopher(object):
    def __init__(self, output="gopher.png", overwrite=False, simple=False):
        self.categories = OrderedDict()
        self.output = output
        self.overwrite = overwrite
        self.simple = simple
        self.binary = None
        self.__get_artwork()

    def __get_artwork(self):
        # type: () -> None
        resp = requests.get(API_URL + "artwork")
        j = resp.json()
        for cat in j['categories']:
            self.categories[cat['id']] = cat['images']

    def __build_params(self):
        # type: () -> List[str]
        import random
        id_list = list(self.categories.keys())
        params = []
        for _id in id_list:
            if _id in ["artwork/010-Body", "artwork/020-Eyes"]:
                c = random.choice(self.categories[_id])
            else:
                if self.simple and random.random() > 0.8:
                    c = random.choice(self.categories[_id] + [None])
            if c:
                params.append(c['id'])
        return params

    def get_image(self):
        # type: () -> str
        params = {"images": "|".join(self.__build_params())}
        resp = requests.get("https://gopherize.me/api/render", params=params)
        self.binary = resp.content
        return resp.content

    def save(self):
        filename = self.output
        if not self.overwrite:
            c = 1
            while os.path.exists(filename):
                s = os.path.splitext(self.output)
                filename = os.path.join(s[0] + str(c) + s[1])
                c += 1

        with open(filename, "wb") as f:
            f.write(self.binary)


@click.command()
@click.option('--output', '-o', default='gopher.png', help='Output file name (png).')
@click.option('--overwrite', '-w', is_flag=True, help='Overwrite if the same name file already exists.')
@click.option('--simple', '-s', is_flag=True, help='Get simple gopher.')
def main(output, overwrite, simple):
    # type: (str, bool, bool) -> None
    gopher = Gopher(output, overwrite, simple)
    gopher.get_image()
    gopher.save()


if __name__ == "__main__":
    main()
