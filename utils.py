import os
import shutil
import subprocess
import concurrent.futures

try:
    from colorama import Fore, Style
    import requests
    from bs4 import BeautifulSoup
    from cryptography.fernet import Fernet
    from Crypto.PublicKey import RSA
    from Crypto import Random
except Exception as e:
    missing_package = str(e).split("'")[-2]
    print(f'[!] Missing package(s), run pip3 install {missing_package}')
    exit(1)


class Console():
    def __init__(self):
        pass

    def info(output):
        print(f'{Fore.BLUE}[*] {output}{Style.RESET_ALL}')

    def log(output):
        print(f'{Fore.GREEN}[+] {output}{Style.RESET_ALL}')

    def error(output):
        print(f'{Fore.RED}[-] {output}{Style.RESET_ALL}')

    def warn(output):
        print(f'{Fore.YELLOW}[!] {output}{Style.RESET_ALL}')

    def blue(output):
        return f'{Fore.BLUE}{output}{Style.RESET_ALL}'

    def red(output):
        return f'{Fore.RED}{output}{Style.RESET_ALL}'

    def green(output):
        return f'{Fore.GREEN}{output}{Style.RESET_ALL}'

    def yellow(output):
        return f'{Fore.YELLOW}{output}{Style.RESET_ALL}'


class Page:
    def __init__(self, url):
        self.URL = url

    def get_response(self):
        Console.log(f'Sending request to {self.URL}')
        try:
            with requests.get(self.URL) as response:
                return response
        except Exception as e:
            Console.error(str(e))
            exit(1)

    def get_soup(self, html):
        return BeautifulSoup(html, features="html.parser")

    def get_page(self):
        return self.get_response().text

    def get_content(self):
        return self.get_response().content


class GenKeys:
    @staticmethod
    def generate_key():
        key = Fernet.generate_key()
        return key

    @staticmethod
    def generate_keys():
        modulus_length = 256*8
        privatekey = RSA.generate(modulus_length, Random.new().read)
        publickey = privatekey.publickey()
        return privatekey, publickey

    @staticmethod
    def write_keys_to_files():
        os.makedirs('.keys')
        os.chdir('.keys')
        key = GenKeys.generate_key()
        priv, pub = GenKeys.generate_keys()
        with open('pub.pem', 'wb') as f:
            f.write(pub.exportKey())

        with open('priv.pem', 'wb') as f:
            f.write(priv.exportKey())

        with open('ky.key', 'wb') as f:
            f.write(key)

    @staticmethod
    def generate():
        try:
            GenKeys.write_keys_to_files()
        except FileExistsError as e:
            print(e.strerror)

    @staticmethod
    def encrypt(filename):
        Console.info(f'Encrypting your file ( {filename} ), Please wait...')

    @staticmethod
    def decrypt(filename):
        pass


def get_file_or_folder_path(fname):
    f_path = os.path.abspath(fname)
    if os.path.exists(f_path):
        return f_path, os.path.basename(f_path), os.path.dirname(f_path)
    return None


def line(sentense, line_type='='):
    return ''.ljust(len(sentense), line_type)


def delete_file(file_name):
    file_turple = get_file_or_folder_path(file_name)
    if not file_turple:
        raise FileNotFoundError(
            f'{file_name} you are trying to delete does not exist.')
    file_path = file_turple[0]
    os.unlink(file_path)
    Console.log(f'{file_name} deleted successfully.')


def copy_file(file_name, destination_file):
    file_tuple = get_file_or_folder_path(file_name)

    if file_tuple is None:
        raise FileNotFoundError(
            f'{file_name} you are trying to copy to {destination_file} does not exist.')

    Console.log(f'Copying "{file_name}" to "{destination_file}"')
    try:
        return shutil.copy(file_name, destination_file)
    except Exception:
        pass


def run_cmd(cmd=[]):
    try:
        subprocess.call(cmd)
    except subprocess.CalledProcessError as e:
        Console.error(str(e))


def multi_process_this(_list, _func):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(_func, _list)
