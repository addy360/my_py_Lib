#! /bin/env python3
import string
import random
import time
from PyPDF2 import PdfFileReader, PdfFileWriter

class PasswdGen():
    def __init__(self):
        self.LETTERS = string.ascii_letters
        self.NUMBERS = string.digits
        self.SYM = string.punctuation
        self.app_instrucions()

    def app_instrucions(self):
        print('[+] lets generate your new password')
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
            print('[+] Invalid password length')
            self.get_passwd_lenght()

    def instructions(self):
        self.get_passwd_lenght()
        print(f'\t\t[!] Enter 1 for ( {self.LETTERS} )')
        print(f'\t\t[!] Enter 2 for ( {self.NUMBERS} )')
        print(f'\t\t[!] Enter 3 for ( {self.SYM} )')
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
        print('[+] Generating password, Please wait...')
        print(f'[+] Your choice {passwd_chars}')
        time.sleep(1)
        pass_list  = random.sample(passwd_chars,int(self.password_length))
        generated_passwd = "".join(pass_list)
        print(f'[+] Your newly generated password is {generated_passwd}')
        time.sleep(.4)
        print('[+] Done')
        raise KeyboardInterrupt
        

    def getUserOptions(self):
        self.instructions()
        self.get_user_choice()
            
        
        while self.is_choice_valid(self.user_choice) is False :
            print('[!] Please enter a valid option')
            self.get_user_choice()
        self.generate_password()

    def run(self):
        while True:
            try:
                self.getUserOptions()
            except KeyboardInterrupt:
                print('[!] Quitting')
                break
            

# pg=PasswdGen()
# pg.run()

class SecurePdf():
    def __init__(self,file=None,passwd='Password'):
        self.file=file
        self.passwd=passwd

    def write_encripted_data_to_file(self, file_data):
        file = f'encrypted_{self.file}'
        print('[+] Writting encrypted data to file...')
        with open(file,'wb') as f:
            time.sleep(1)
            file_data.write(f)
            print(f'[+] {file} written successfully')

    def get_pdf_file(self):
        try:
            return PdfFileReader(self.file)
        except FileNotFoundError as e:
            print(e)
            exit(1)
        

    def enc_pdf(self):
        parser=PdfFileWriter()
        print(f'[+] Loading {self.file}...')
        time.sleep(.5)
        pdf = self.get_pdf_file()
        for page in range(pdf.numPages):
            parser.addPage(pdf.getPage(page))
        print('[+] Encrypting data...')
        time.sleep(.4)
        parser.encrypt(self.passwd)

        self.write_encripted_data_to_file(parser)
        
        
# sp = SecurePdf()
# sp.file='PDF_FILE'
# sp.enc_pdf()