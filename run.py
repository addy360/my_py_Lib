#! /bin/env python3

from libs import main
from settings import modules

if __name__ == "__main__":
    try:
        main(modules)
    except KeyboardInterrupt:
        print('[!] Detected Ctr+C, Quiting...')

    