#!/usr/bin/env python

from csscompressor import compress
from pathlib import Path


def main() -> None:
    css = Path('.') / '..' / '..' / 'tiny.css'

    if not css.exists():
        raise FileNotFoundError
    with open(css.as_posix(), mode='r', encoding='utf-8') as f:
        print(compress(f.read()))


if __name__ == '__main__':
    main()
