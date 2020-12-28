import random
import string
import time
import os
import tarfile
import json
from utils import Console, Page, get_file_or_folder_path, delete_file, line

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
        if not file_path or file_name.split('.')[-1].lower() != 'pdf' :
            Console.error(f'{file} does not exist or not pdf. Try again or (Ctrl + C) to quit')
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
        
    def choose_to_delete(self, file_name):
        choice = input(Console.yellow(f'Do you wish to delete {file_name}? (N/y) > '))
        choice = choice.strip().lower()
        not_valid = choice  not in ['n','y']
        if not_valid:
            Console.error('Please choose a valid input!')
            time.sleep(.2)
            self.choose_to_delete(file_name)

        if choice == 'n':
            Console.log('Bye!')
            return
        Console.info(f'Deleting {file_name}...')
        delete_file(file_name)

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
        time.sleep(.2)
        self.choose_to_delete(self.file)

    def run(self):
        self.get_file()
        passwd = input(f'Please enter a secure password Default ({self.passwd})> ') 
        if passwd.strip(): self.passwd = passwd 
        try:
            self.enc_pdf()
        except Exception as e:
            Console.error(str(e))
            self.run()

class MillardAyo(Page):
    def __init__(self):
        super().__init__('https://millardayo.com/')
        self.posts = []
        self.cached_posts = {}


    def parse_post_details(self, post_detail_html):
        soup = self.get_soup(post_detail_html)
        post_header = soup.select_one('div#post-header>h1').text
        post_content = soup.select_one('div.post-section')
        print('\n')
        print(Console.yellow(line(post_header)))
        print(post_header)
        print(Console.yellow(line(post_header)))
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

class FileFinder():
    def __init__(self):
        pass

    def find_file(self,file_name):
        Console.log(f'Finding "{Console.green(file_name[0])}" in {Console.green(file_name[1][0])}. Please wait...')
        results_counter = 0
        for file_obj in os.walk(file_name[1][0]):
            fname = file_obj[2]
            for filename in fname:
                file_ = f'{file_obj[0]}{os.sep}{filename}'
                if file_name[0].lower() in file_.lower():
                    results_counter += 1
                    time.sleep(.3)
                    Console.log(f'file found at : {Console.yellow(file_)}') 
        print('\n')
        print_out = f"found {results_counter} resluts of '{self.file_name}'"
        time.sleep(.2)
        Console.warn(line(print_out))
        time.sleep(.2)
        Console.log(print_out)
        time.sleep(.2)
        Console.warn(line(print_out,'-'))
                
    

    def get_file(self):
        file_name = input(f"\n{Console.green('Enter name of a file you would like to find > ')}")
        valid = len(file_name.strip()) > 1
        if valid :
            self.file_name = file_name
            return
        Console.error('Can not be empty, please try again...')
        self.get_file()

    def get_place(self):
        place_name = input(f"\n{Console.green('Where to find the file (Valid path) > ')}")
        folder_path = get_file_or_folder_path(place_name)
        if folder_path:
            self.folder_path = folder_path
            return
        Console.error('Path should be valid...')
        self.get_place()


    def get_user_input(self):
        self.get_file()
        self.get_place()
        return self.file_name , self.folder_path

    def run(self):
        search_query = self.get_user_input()
        self.find_file(search_query)


class Tanzania(Page):
    def __init__(self):
        super().__init__('https://en.wikipedia.org/wiki/Districts_of_Tanzania')

    def get_regions(self, soup):
        regions = soup.select('li.toclevel-1')
        return list(map(lambda region: ' '.join(region.text.split(' ')[1:]) , regions))[1:-3]

    def get_local_soup(self):
        page = self.get_page()
        return self.get_soup(page)

    def get_district_list(self,dhead):
        dis = []
        for ol in dhead.parent.next_siblings:
            try:
                return ol.find_next_sibling('ol')
            except Exception:
                continue

    def parse_wards(self, wards_page):
        for p in wards_page.select('p'):
            if 'administratively' in p.text.lower():
               return p.text
        return "NaN"
        

    def get_wards(self,url):
        self.URL =  url
        soup = self.get_local_soup()
        return self.parse_wards(soup)

            
    def get_nice_format(self, dists):
        dist_dict =[]
        dist_population = 0
        dist_name = ''
        base_url = "https://en.wikipedia.org/"
        urls = dists.select('a')
        for index, dist in enumerate(dists.text.split('\n')):     
            url = base_url + urls[index]['href']    
            pop = dist.strip().split(' ')
            if len(pop) == 2:
                dist_name = ' '.join(pop)
                dist_population = 'NaN'
            elif len(pop)  == 4:
                dist_name =' '.join(pop[:-1])
                if 'http' in pop[-1] : 
                    dist_population = pop[-1].strip(':')[0] 
                else:
                    dist_population = pop[-1]
            elif len(pop) in [3,8]:
                dist_name = ' '.join(pop[:-1])
                dist_population = pop[-1]
            elif len(pop) == 5: # with url as last element
                dist_name = ' '.join(pop[:3])
                dist_population =pop[3].strip(':')
            elif len(pop) == 6:
                dist_name =' '.join(pop[:3])
                dist_population =' '.join(pop[3:])
            elif len(pop) == 7:
                dist_name =' '.join(pop[:3])
                dist_population =pop[3]
            else:
                print(len(pop))
            ward_details = self.get_wards(url)
            dist_dict.append({'distict': dist_name, 'population': dist_population, 'ward_details':ward_details})

        return dist_dict

    def get_district(self, soup):
        districts_heads = soup.select('h2>span.mw-headline')
        districts = {}
        for dis in list(districts_heads)[1:-3]:
            districts[dis.text] =  self.get_nice_format(self.get_district_list(dis))
        return districts
    def write_to_file(self, data):
        fname = 'districts.json'
        Console.log(f'Writting results to {fname}...')
        time.sleep(.5)
        with open(fname, 'w') as f:
            f.write(json.dumps(data))

    def process_page(self):
        soup = self.get_local_soup()
        regions = self.get_regions(soup)
        districts = self.get_district(soup)
        
        self.write_to_file({'districts':districts})

    def run(self):
        self.process_page()

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
    

