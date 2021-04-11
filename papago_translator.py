from selenium import webdriver
from tqdm import tqdm

from math import ceil
import time, json, os, argparse
from copy import deepcopy
from multiprocessing import Pool, Manager

from collections import OrderedDict
from itertools import repeat


class Translator(object):
    def __init__(self, english_dir, korean_dir, multiprocessor=1, path='chromedriver'):
        self.english_dir = english_dir
        self.korean_dir = korean_dir
        self.multiprocessor = multiprocessor
        self.cpath = path
        manager = Manager()
        self.translated = manager.dict()
        
        #Load not translated words
        if os.path.isfile(korean_dir):
            self.translated = manager.dict(self.load_json(korean_dir))
            
            tmp = self.load_text(english_dir)
            corpus = []
            for i in range(len(tmp)):
                if tmp[i].strip() not in self.translated:
                    corpus.append(tmp[i].strip())
            self.n = len(corpus)
            print(f'You got file of {korean_dir} \n{len(tmp) - len(corpus)} lines translated')
            print(f'You have left {self.n} of total {len(tmp)}')
        else:
            corpus = self.load_text(english_dir)
            self.n = len(corpus)
            print(f'You have left {self.n}')        

        self.parts = [deepcopy(corpus[ceil(self.n/multiprocessor)*i:ceil(self.n/multiprocessor)*(i+1)]) for i in range(self.multiprocessor)]

    def en2kr(self, sentence, driver, time_delay):

        input_box = driver.find_element_by_css_selector('#sourceEditArea textarea')
        
        input_box.clear(); input_box.clear(); input_box.clear(); input_box.clear(); 
        
        input_box.send_keys(sentence)
        driver.find_element_by_css_selector('#btnTranslate').click()

        time.sleep(time_delay)
        
        result = str(driver.find_element_by_css_selector("#txtTarget").text)

        input_box.clear(); input_box.clear(); input_box.clear(); input_box.clear(); 
        return result

    def translate(self):
        pool = Pool(self.multiprocessor)
        pool.starmap(self._translate, zip(range(self.multiprocessor), repeat(self.translated)))
        self.save_json(self.korean_dir, self.translated._getvalue())
        print('file translation completed')

    def _translate(self, corpus_number, translated):
        corpus = self.parts[corpus_number]

        prev_result = result = ''

        for idx, sentence in tqdm(enumerate(corpus)):
            if idx % 100 == 0:
                driver = self.init_driver(self.cpath)
                print('driver initialized')
            
            time_delay = 2
            while result == prev_result and time_delay < 10:
                if time_delay > 3:
                    print(time_delay, result.split('\n'), sentence.split('\n'), sep='\n', end='\n\n')
                
                result = self.en2kr(sentence, driver, time_delay)
                time_delay += 1
            
            prev_result = result

            for en, tstd in zip(sentence.split('\n'), result.split('\n')):
                translated[en.strip()] = tstd.strip()
            
        if self.multiprocessor > 1:
            print(f'processor {corpus_number} completed')
        else:
            print('translation completed')
        return translated
    
    def load_json(self, json_dir):
        with open(json_dir, encoding='UTF8') as f:
            json_file = json.load(f)
        print(f'{json_dir} loaded')
        return json_file
    
    def save_json(self, save_dir, result_dict):
        with open(save_dir,'w', encoding='UTF8') as f:
            json.dump(result_dict, f, ensure_ascii=False)
    
    def load_text(self, text_dir):
        with open(text_dir, encoding='UTF8') as f:
            text_file = f.readlines()
        print(f'{text_dir} loaded')
        return text_file

    def init_driver(self, cpath=None):
        if cpath == None:
            cpath = self.cpath
        options = webdriver.ChromeOptions()    
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

        driver = webdriver.Chrome(executable_path=cpath, chrome_options=options)

        driver.implicitly_wait(15)
        driver.get('https://papago.naver.com/')

        return driver


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Before get started you need read README')

    parser.add_argument('--english_dir', type=str, help='directory of english text file',
                        default='english.txt')

    parser.add_argument('--kr_json_dir', type=str, help='directory of translated json file to save',
                        default='translated.json')
    
    parser.add_argument('--multiprocessor', type=int, help='multiprocessor number you want to use',
                        default=int(1))                    

    parser.add_argument('--path', type=str, help='type chromedriver\'s abs dir',
                        default='chromedriver')                    


    args = parser.parse_args()
    
    translator = Translator(args.english_dir, args.kr_json_dir, args.multiprocessor, args.path)

    translator.translate()