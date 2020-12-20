try:
    from colorama import Fore, Style
    import requests
    from bs4 import BeautifulSoup
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