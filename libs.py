import random
import string
import time
import os
import tarfile
from utils import Console, Page, get_file_or_folder_path

try:
    from PyPDF2 import PdfFileReader, PdfFileWriter
except Exception as e:
    missing_package = str(e).split("'")[-2]
    print(f'[!] Missing package(s), run pip3 install {missing_package}')
    exit(1)





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
        Console.info(f'Your choice {passwd_chars}')
        time.sleep(.2)
        Console.info('Generating password, Please wait...')
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

    def get_file(self):
        file = input('Please enter a valid pdf file name > ')
        file_path, file_name, file_root_dir = get_file_or_folder_path(file)
        if not file_path:
            Console.error(f'{file} does not exist. Try again or (Ctrl + C) to quit')
            self.get_file()
        self.file = file_path
        self.file_name = file_name
        self.file_root_dir = file_root_dir
        

    def write_encripted_data_to_file(self, file_data):
        file = f'encrypted_{self.file_name}'
        file = os.path.join(self.file_root_dir,file)
        Console.info('Writting encrypted data to file...')
        with open(file,'wb') as f:
            time.sleep(1)
            file_data.write(f)
            Console.log(f'{file} written successfully')

    def get_pdf_file(self):
        try:
            print(f"[+] file being processed {self.file}")
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
        self.get_file()
        passwd = input(f'Please enter a secure password Default ({self.passwd})> ') 
        if passwd.strip(): self.passwd = passwd 
        self.enc_pdf()

class MillardAyo(Page):
    def __init__(self):
        super().__init__('https://millardayo.com/')
        self.posts = []
        self.cached_posts = {}

    def line(self, sentense, line_type = '='):
        return ''.ljust(len(sentense),line_type)

    def parse_post_details(self, post_detail_html):
        soup = self.get_soup(post_detail_html)
        post_header = soup.select_one('div#post-header>h1').text
        post_content = soup.select_one('div.post-section')
        print('\n')
        print(Console.yellow(self.line(post_header)))
        print(post_header)
        print(Console.yellow(self.line(post_header)))
        print('\n')
        post_detail = post_content.text.strip()
        print(post_detail)



    def get_post_details(self, post_url):
        self.URL = post_url
        post_html = self.get_res()
        self.parse_post_details(post_html)

    def user_choice(self,next_page_url=None):
        choice = input(f"\n{Console.green('Enter (n) for next page or post number for post details > ')}")
        try:
            post_url = self.posts[int(choice)-1]['post_link']
            self.get_post_details(post_url)
        except Exception:
            if choice.strip().lower() == 'n':
                self.parse_next_page(next_page_url)
            else:
                Console.error("Wrong choice")
                self.user_choice()
    
    def parse_next_page(self,next_page_url):
        Console.info('Going to next page')
        # TODO caching for easier backward navigation
        # self.cached_posts[self.URL] = self.posts
        self.posts = []
        self.URL = next_page_url
        
        self.parse_result()

    def print_posts(self, posts):
        for i,post in enumerate(posts):
            time.sleep(.2)
            Console.warn(f'{i+1} : {post.h2.a.text}')
            self.posts.append({'post_title':post.h2.a.text , 'post_link':post.h2.a['href']})

    def parse_result(self):
        html_result = self.get_res()
        soup = self.get_soup(html_result)
        list_posts = soup.find_all('li', class_="infinite-post")
        next_page_url = soup.select('div.pagination>a:not(.inactive)')[-2]['href']
        
        
        self.print_posts( list_posts)
        self.user_choice(next_page_url)

    def get_res(self):
        res = self.get_page()
        return res

    def run(self):
        self.parse_result()

class FileCompressor:
    def __init__(self):
        pass

    def get_user_input(self):
        time.sleep(.3)
        path = input(f"\n{Console.green('Enter path to file or folder you want to compress > ')}")
        if len(path) == 0:
            Console.error('Path can not be empty')
            return None, False
        abs_path_turple = get_file_or_folder_path(path)
        
        if not abs_path_turple:
            Console.error('Path to file or folder does not exist. Try again...')
            return None, False 

        return abs_path_turple, True

    def compress(self,root_dir, path_to_file):
        if os.path.isdir(path_to_file[0]):
            compress_name = f'{path_to_file[0]}.tar.gzip'
        elif os.path.isfile(path_to_file[0]):
            file_name = path_to_file[0]
            file_name = file_name.split('.')[-2]
            compress_name = f'{file_name}.tar.gzip'
        time.sleep(.3)
        Console.info(f'Compressing to {compress_name}')
        #TODO actual compression


        return path_to_file, True
        
    
    def process(self, path_to_file):
        root_dir = path_to_file[2]
        f_name = path_to_file[1]
        compressed_file, was_success = self.compress(root_dir,path_to_file)


    def run(self):
        time.sleep(.5)
        Console.log('Compress files and folders, even encrypt them if option chosen')
        is_valid = False
        while is_valid is False:
            abs_path_turple, is_valid = self.get_user_input() 

        self.process(abs_path_turple)        
        

def appFactory(choice, modules):
    try:
        Console.info(f"{modules[str(choice)]['desc']}")
        time.sleep(.5)
        return modules[str(choice)]['name']()
    except KeyError as e:
        Console.error('Wrong module')
        exit(1)

def instructions(modules):
    for mod in modules:
        print(f'[{mod}] {modules[mod]["desc"]}')
        time.sleep(.3)

def main(modules):
    time.sleep(.3)
    Console.info('Welcome to libs helper\n')
    time.sleep(.5)
    instructions(modules)
    try:
        choice = int(input('\nPick your poison > '))
        app = appFactory(choice, modules)
        app.run()
    except ValueError as e:
        Console.error('Invalid input')
        exit(1)
    

