# -*- coding: utf-8 -*-

from __future__ import print_function, division
import argparse
from os import makedirs
from os.path import join, dirname

import subprocess
from urllib.request import Request, urlopen

__author__ = 'Fisher Yu'
__email__ = 'fy@cs.princeton.edu'
__license__ = 'MIT'


def list_categories():
    url = 'http://dl.yf.io/lsun/categories.txt'
    with urlopen(Request(url)) as response:
        return response.read().decode().strip().split('\n')


def download(out_dir, super_category, category, set_name):
    suffix = '.zip'
    if super_category == 'scenes':
        suffix = f'_{set_name}_lmdb.zip'
    url = f'http://dl.yf.io/lsun/{super_category}/{category}{suffix}'
          
    if set_name == 'test':
        assert super_category == 'scenes', f'Test set is only available for the scenes super_category!'
        out_name = '{super_category}/test_lmdb.zip'.format(**locals())
        url = 'http://dl.yf.io/lsun/{super_category}/{set_name}_lmdb.zip'
    else:
        if super_category == 'scenes':
            out_name = '{super_category}/{category}_{set_name}_lmdb.zip'.format(**locals())
        elif super_category == 'objects':
            out_name = '{super_category}/{category}.zip'.format(**locals())
        else:
            raise ValueError(f'super_category should be in ["scenes", "objects"] but is {super_category}')
    out_path = join(out_dir, out_name)
    cmd = ['curl', url, '-o', out_path]
    print(f'Downloading super_category "{super_category}" category "{category}" set "{set_name}" with cmd: {cmd}')
    makedirs(dirname(out_path), exist_ok=True)
    subprocess.call(cmd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out_dir', default='')
    parser.add_argument('-s', '--super_category', default='scenes', help='"scenes" or "objects"')
    parser.add_argument('-c', '--category', default=None)
    args = parser.parse_args()

    categories = list_categories()
    if args.category is None:
        print('Downloading', len(categories), 'categories')
        for category in categories:
            download(args.out_dir, args.super_category, args.category, 'train')
            download(args.out_dir, args.super_category, category, 'val')
        download(args.out_dir, '', 'test')
    else:
        if args.super_category == 'scenes':
            if args.category == 'test':
                download(args.out_dir, args.super_category, '', 'test')
            elif args.category not in categories:
                print('Error:', args.category, "doesn't exist in", 'LSUN release')
            else:
                download(args.out_dir, args.super_category, args.category, 'train')
                download(args.out_dir, args.super_category, args.category, 'val')
        elif args.super_category == 'objects':
            download(args.out_dir, args.super_category, args.category, '')
        else:
            raise ValueError(f'super_category should be in ["scenes", "objects"] but is {args.super_category}')


if __name__ == '__main__':
    main()
