#! /bin/env python3.8

from libs import main
from settings import modules

if __name__ == "__main__":
    try:
        while True:
            main(modules)
    except KeyboardInterrupt:
        print('[!] Detected Ctr+C, Quiting...')

    