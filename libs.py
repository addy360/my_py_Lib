import random
import string
import time

try:
    from colorama import Fore, Style
    from PyPDF2 import PdfFileReader, PdfFileWriter
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

class PasswdGen():
    def __init__(self):
        self.LETTERS = string.ascii_letters
        self.NUMBERS = string.digits
        self.SYM = string.punctuation
        self.app_instrucions()

    def app_instrucions(self):
        Console.info('lets generate your new password')
        time.sleep(.5)

    def is_choice_valid(self, choice):
        required_choices = [1,2,3,4]
        try:
            required_choices.index(int(choice))
            return True
        except ValueError:
            return False
        
    def get_passwd_lenght(self):
        try:
            self.password_length = int(input('[-] Length of a password > '))
        except ValueError:
            Console.error('Invalid password length')
            self.get_passwd_lenght()

    def instructions(self):
        self.get_passwd_lenght()
        print(f'\t\t[!] Enter 1 for ( {Console.yellow(self.LETTERS)} )')
        print(f'\t\t[!] Enter 2 for ( {Console.yellow(self.NUMBERS)} )')
        print(f'\t\t[!] Enter 3 for ( {Console.yellow(self.SYM)} )')
        print(f'\t\t[!] Enter 4 for mixed')
        time.sleep(.5)

    def get_user_choice(self):
        self.user_choice = input('[-] Your choice > ')

    def get_chosen_chars(self):
        choice  = int(self.user_choice)
        if choice  == 1:
            return self.LETTERS
        elif choice  == 2:
            return self.NUMBERS
        elif choice  == 3:
            return self.SYM
        else:
            return self.LETTERS + self.NUMBERS +self.SYM

    def generate_password(self):
        passwd_chars = self.get_chosen_chars()
        Console.info('Generating password, Please wait...')
        Console.info(f'Your choice {passwd_chars}')
        time.sleep(1)
        pass_list  = random.sample(passwd_chars,int(self.password_length))
        generated_passwd = "".join(pass_list)
        Console.info(f'Your newly generated password is {Console.green(generated_passwd)}')
        time.sleep(.4)
        Console.log('[+] Done')
        raise KeyboardInterrupt
        

    def getUserOptions(self):
        self.instructions()
        self.get_user_choice()
            
        
        while self.is_choice_valid(self.user_choice) is False :
            Console.error('Please enter a valid option')
            self.get_user_choice()
        self.generate_password()

    def run(self):
        while True:
            try:
                self.getUserOptions()
            except KeyboardInterrupt:
                Console.info('Quitting')
                break
            

class SecurePdf():
    def __init__(self,file=None,passwd='Password'):
        self.file=file
        self.passwd=passwd

    def write_encripted_data_to_file(self, file_data):
        file = f'encrypted_{self.file}'
        Console.info('Writting encrypted data to file...')
        with open(file,'wb') as f:
            time.sleep(1)
            file_data.write(f)
            Console.log(f'{file} written successfully')

    def get_pdf_file(self):
        try:
            return PdfFileReader(self.file)
        except FileNotFoundError as e:
            Console.error(e)
            exit(1)
        

    def enc_pdf(self):
        parser=PdfFileWriter()
        Console.info(f'Loading {self.file}...')
        time.sleep(.5)
        pdf = self.get_pdf_file()
        for page in range(pdf.numPages):
            parser.addPage(pdf.getPage(page))
        Console.info('Encrypting data...')
        time.sleep(.4)
        parser.encrypt(self.passwd)

        self.write_encripted_data_to_file(parser)

    def run(self):
        self.file = input('Please enter a valid pdf file name > ')
        passwd = input(f'Please enter a secure password Default ({self.passwd})> ') 
        if passwd.strip(): self.passwd = passwd 
        self.enc_pdf()
        

def appFactory(choice, modules):
    try:
        return modules[str(choice)]['name']
    except KeyError as e:
        Console.error('Wrong module')
        exit(1)

def instructions(modules):
    for mod in modules:
        print(f'[{mod}] {modules[mod]["desc"]}')
        time.sleep(.3)

def main(modules):
    Console.info('Welcome to libs helper\n')
    time.sleep(.5)
    instructions(modules)
    try:
        choice = int(input('\nPick your poison > '))
        app = appFactory(choice, modules)
        app().run()
    except ValueError as e:
        Console.error('Invalid input')
        exit(1)
    

