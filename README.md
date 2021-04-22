## Papago translator with selenium(en2kr)



*> I utilizes this site to translate english to korean -> https://papago.naver.com/*

**----------------updated----------------**

> Languages can be selected

**---------------------------------------------**



Naver supports papago API. However, the amount of text is limited which is so small.





Therefore, I made this program which helps you to translate tons of english sentences. 





I made this program on linux os. If you set path options to your chromedriver path, you can make this code run.





Before get started run this following code on your shell.



```shell
$git clone https://github.com/taehwakkwon/papago-translator.git
$cd papago-translator
$pip install -r requirements.txt
$apt-get update
$apt install chromium-chromedriver
```



I uploaded an example english.txt. You can run it by this following code in shell.



```
python papago_translator.py
```





English file that you want to translate should following these rules



\- You could use this program on your own text file. Text file should be separated by \n.



\- A bunch of sentences ***\*must not exceed 5000 characters\****(becuase papago supports under 5000 characters. I recommend you to put it under 1500 characters)



```tex
 Hi, this is Taehwak ~~~~~~~~ \n -> this should not exceed 5000 characters

 second sentence start from here
```



So, you could run this program with this code.



```
python papago_translator.py --text_file english.txt --sk en --tk kr --complete_file translated.json --multiprocessor 8 --path chromedriver
```



Thanks😁



