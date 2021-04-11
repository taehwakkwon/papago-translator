from selenium import webdriver
from tqdm import tqdm

import time, json, argparse, sys, os
from copy import deepcopy
from multiprocessing import Pool
from itertools import chain
from collections import OrderedDict

def load_json(json_dir):
    with open(json_dir, encoding='UTF8') as f:
        json_file = json.load(f)
    return json_file


def save_json(save_dir, result_dict):
    with open(save_dir,'w', encoding='UTF8') as f:
        json.dump(result_dict, f, ensure_ascii=False)


def load_text(text_dir):
    with open(text_dir, encoding='UTF8') as f:
        text_file = f.readlines()
    return text_file


def en2kr(text, driver, time_delay, res_dict):

    input_box = driver.find_element_by_css_selector('#sourceEditArea textarea')
    
    input_box.clear(); input_box.clear(); input_box.clear(); input_box.clear(); 
    
    input_box.send_keys(text)
    driver.find_element_by_css_selector('#btnTranslate').click()

    time.sleep(time_delay)
    
    result = str(driver.find_element_by_css_selector("#txtTarget").text)

    input_box.clear(); input_box.clear(); input_box.clear(); input_box.clear(); 
    return result


def init_driver(cpath, linux=True):
    options = webdriver.ChromeOptions()    
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome(executable_path=cpath, chrome_options=options)

    driver.implicitly_wait(15)
    driver.get('https://papago.naver.com/')

    return driver


def preprocessing(kr_json_dir, corpus_part, size):

    res_dict = OrderedDict()
    if os.path.isfile(kr_json_dir):
        print(f'You have file of {kr_json_dir}')

        corpus_not_completed = []
        
        kr_json_file = load_json(kr_json_dir)

        for idx, cps in enumerate(corpus_part):
            if cps.strip() in kr_json_file:
                continue
            else:
                corpus_not_completed.append(cps.strip())

        print(f'you have left {len(corpus_not_completed)} of {len(corpus_part)}')
        res_dict = kr_json_file
    else:
        print(f'You have file nothing.\n Just start from the beginning!')
        corpus_not_completed = deepcopy(corpus_part)

    corpus_part = []
    for i in tqdm(range(0, len(corpus_not_completed)-size+1, size)):
        tmp = ''
        for j in range(size):
            tmp += corpus_not_completed[i+j].strip() + '\n'
        corpus_part.append(tmp[:].strip())   #erase latest \n
    return corpus_part, res_dict


def main(args):
    size = args.size
    cpath = args.path
    divider = args.divider
    part = args.part
    en_txt_dir = args.en_txt_dir
    kr_json_dir = args.kr_json_dir

    corpus = load_text(en_txt_dir)
    
    n = len(corpus)//divider

    corpus_part = deepcopy(corpus[n*part:n*(part+1)])
    check_corpus = deepcopy(corpus[n*part:n*(part+1)])
    
    corpus_part, res_dict = preprocessing(kr_json_dir, corpus_part, size)
    result = ''
    prev_result = ''
    for idx, line in tqdm(enumerate(corpus_part)): #
        if idx % 100 == 0:
            driver = init_driver(cpath)
            print('driver initialized')

        time_delay = 2
        
        while result == prev_result or (len(result.split('\n')) != size and all(map(lambda x:len(x) > 3, result.split('\n')))):
            if time_delay > 3:
                print(time_delay, result.split('\n'), line.split('\n'), sep='\n', end='\n\n')

            result = en2kr(line, driver, time_delay, res_dict)
            time_delay += 1

        prev_result = result

        for en, tstd in zip(line.split('\n'), result.split('\n')):
            res_dict[en] = tstd
        
        save_json(kr_json_dir, res_dict)

    cnt = 0
    kr_json_file = load_json(kr_json_dir)
    for idx, cps in enumerate(check_corpus):
        if cps.strip() not in kr_json_file:
            print(cps.strip())
            cnt += 1
    if cnt == 0 or len(kr_json_file) == n:
        print('translation completed')
    elif cnt < size:
        print(f'you have {cnt} sentences that are not translated')
    else:
        print(f'you have {cnt} sentences that are not translated')
        return main(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Before get started you need to download chromedriver')
    parser.add_argument('--path', type=str, help='type chromedriver\'s abs dir',
                        default='chromedriver')

    parser.add_argument('--size', type=int, help='size of translate at once',
                        default=int(10))
    
    parser.add_argument('--divider', type=int, help='divider size for parallel',
                        default=int(1))

    parser.add_argument('--part', type=int, help='part for parallel',
                        default=int(0))
        
    parser.add_argument('--en_txt_dir', type=str, help='directory of english json file',
                        default='english.txt')

    parser.add_argument('--kr_json_dir', type=str, help='directory of translated json file to save',
                        default='en2kr.json')
    
    args = parser.parse_args()
    main(args)
    
'''
    tmp = deepcopy(args)
    settings = [
        ['chromedriver', 4, 0, 'english.txt', 'en2kr_part0.json'],
        ['chromedriver', 4, 1, 'english.txt', 'en2kr_part1.json'],
        ['chromedriver', 4, 2, 'english.txt', 'en2kr_part2.json'],
        ['chromedriver', 4, 3, 'english.txt', 'en2kr_part3.json'],
        ]
    parsers = []
    for stgs in settings:
        tmp.path, tmp.divider, tmp.part, tmp.en_txt_dir, tmp.kr_json_dir = stgs
        parsers.append(deepcopy(tmp))
    
    pool = Pool(4)
    pool.map(main, parsers)
'''