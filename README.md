## Papago translator with selenium(en2kr)

https://papago.naver.com/

Naver supports papago API. However, the amount of text is limited which is so small.



Therefore, I made this program which helps you to translate tons of english sentences. 



This programs should be run in linux os.



Before get started run this following code on your shell.



```shell
git clone https://github.com/taehwakkwon/papago-translator.git
cd papago-translator
pip install -r requirements.txt
apt-get update
apt install chromium-chromedriver
```



I uploaded an example english.txt. You can run it by this following code in shell.

`python papago_translator.py`



English file that you want to translate should following these rules

- You could use this program on your own text file. Text file should be separated by \n.

- A bunch of sentences **must not exceed 5000 characters**(cuz they does not support it. I recommend you to put it under 1500 characters)

  ```tex
  Hi, this is Taehwak ~~~~~~~~ \n -> this should not exceed 5000 characters
  second sentence start from here
  ```



So, you could run this program with this code.

`python papago_translator.py --path <chromedriver path> --size <size of translate at once unit(\n)> --en_txt_dir <text dir you want to translate> --kr_json_dir <translated file dir>`

And I also divider and part options. These options are for multiprocessing. Divide one english file to 'divider' and take 'part' number. Those are for the fast translation.



[0,~~,100, ~~200, ~~300] -> `--divider 3 --part 0` these options take 0~100 sentences. 

Have a great day😁