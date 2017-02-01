# -*- coding: utf-8 -*-

import os
import click
import requests
from collections import OrderedDict

__version__ = '0.1.2'
__author__ = 'Takuro Wada'
__email__ = "taxpon@gmail.com"
__url__ = "https://github.com/taxpon/gopher"
__license__ = "MIT"


class GopherIcon(object):
    def __init__(self, output="gopher.png", overwrite=False):
        self.categories = OrderedDict()
        self.output = output
        self.overwrite = overwrite
        self.get_artwork()

    def get_artwork(self):
        resp = requests.get("https://gopherize.me/api/artwork")
        j = resp.json()
        for cat in j['categories']:
            self.categories[cat['id']] = cat['images']

    def __get_category_items(self, cat_name):
        pass

    def __build_params(self):
        import random
        id_list = list(self.categories.keys())
        params = []
        for _id in id_list:
            if _id in ["artwork/010-Body", "artwork/020-Eyes"]:
                c = random.choice(self.categories[_id])
            else:
                c = random.choice(self.categories[_id] + [None])
            if c:
                params.append(c['id'])
        return params

    def get_image(self):
        params = {"images": "|".join(self.__build_params())}
        resp = requests.get("https://gopherize.me/api/render", params=params)

        filename = self.output
        if not self.overwrite:
            c = 1
            while os.path.exists(filename):
                s = os.path.splitext(self.output)
                filename = os.path.join(s[0] + str(c) + s[1])
                c += 1

        with open(filename, "wb") as f:
            f.write(resp.content)


@click.command()
@click.option('--output', '-o', default='gopher.png', help='Output file name (png).')
@click.option('--overwrite', '-w', is_flag=True, help='Overwrite if the same name file already exists.')
def main(output, overwrite):
    GopherIcon(output, overwrite).get_image()

if __name__ == "__main__":
    main()
