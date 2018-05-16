import requests
import os
import sys
from bs4 import BeautifulSoup

if len(sys.argv)==1:
	print('프로그램 이름을 입력하고 실행해 주세요.. 예)challenge')
	print('프로그램이 종료됩니다')
	sys.exit(1)
program_name = str(sys.argv[1])
url = 'http://tv.naver.com/' + program_name + '/playlists'
res=requests.get(url)
res.raise_for_status() 
soup = BeautifulSoup(res.text, 'html.parser')

file_name = 'list_'+ program_name + '.txt' 
fo = open(file_name, 'w')
strv = '/v/'
vlists = soup.select("li > a")
for vlist in vlists:
	txt = vlist.get('href')
#	print(txt)
	a = txt.find(strv)
	if a==0:
		final_txt = txt[3:10]
		#print(final_txt)
	else: 
		continue
	fo.write(final_txt + '\n')
fo.close()

fi = open(file_name, 'r')
lines = fi.readlines()
for line in lines: 
	keyword_url  = 'http://tv.naver.com/v/' + line
	key_res = requests.get(keyword_url)
	key_res.raise_for_status()
	keysoup = BeautifulSoup(key_res.text, 'html.parser')
	keylists = keysoup.select("[property~=og:video:tag]")
	titlelists = keysoup.select("[property~=og:title]")
	for titlelist in titlelists:
		title = titlelist.get('content')
	output_file_name = 'keyword_' + file_name
	fo2 = open(output_file_name, 'a')
	mylist = []
	for keylist in keylists:
		keytxt = keylist.get('content')
		mylist.append(keytxt)
	fo2.write(line + title + '\n' + ' '.join(mylist)+ '\n')
fo2.close()

