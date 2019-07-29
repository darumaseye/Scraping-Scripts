from time import sleep
from  bs4 import BeautifulSoup
from collections import defaultdict
import requests
import csv

def href_search( tag ):
	return tag.has_attr('href')

def csv_write( dictionary ):
	with open( 'anon_italy_post_list.csv','a', newline='' ) as csvfile:
		fieldn = ["Num","Name","Date","Url"]
		writer = csv.DictWriter( csvfile, delimiter='|', quotechar='\\',fieldnames=fieldn )
		for row in dictionary:
			writer.writerow(row)

def csv_read():
	dictionary = []
	with open( 'anon_italy_post_list.csv', newline='' ) as csvfile:
		reader = csv.DictReader( csvfile, delimiter='|', quotechar='\\' )
		for row in reader:
			dictionary.append( {"Num":row["Num"],"Name":row["Name"],"Date":row["Date"],"Url":row["Url"]} )
	return dictionary

def anon_soup( url ):
	head={  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
		'Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate, br','Connection': 'keep-alive','Upgrade-Insecure-Requests': '1' }
	#TODO _Handle error if tor service is down
	#TODO _Handle error if http_response_code 
	session 	= requests.session()
	session.proxies = { 'http':'socks5://127.0.0.1:9050','https':'socks5://127.0.0.1:9050' }
	req 		= session.get( url , headers=head ).text
	soup 		= BeautifulSoup( req , "html.parser" )
	return soup

def check_last_downloaded_post( url , csv_list ):
	
	n = 0
	temp_list = defaultdict( lambda : None )
	if ( csv_list != None and csv_list ):
		for row in csv_list:
			m = int( row["Num"] )
			n = m if  m>n  else n
			temp_list[ int( row["Num"] ) ] = row["Url"]
	 
		if( url ==  temp_list[n]):
			print( "Last post appears downloaded already" )			
			exit( 0 )

		else:
			return n,temp_list[n]
	else:
		return 0,"https://anon-italy.blogspot.com/2012/04/wwwfimiit-database-hack3d-anonymous.html"



soup 	= anon_soup( "https://anon-italy.blogspot.com" )
url	= soup.find( attrs={"class","post-title entry-title"} ).a

print("First connection done. Now checking if first post is present in csvfile")		

csv_list  = csv_read()
n,url 	  = check_last_downloaded_post( url.attrs["href"] , csv_list )
soup 	  = anon_soup( url )
if csv_list:
	url	  = soup.find(attrs={"title":"Post più recente"})

while( url != None ):
	
	n += 1
	if csv_list:
		url 	= url.attrs["href"]
		soup 	= anon_soup( url )

	date       = soup.find( attrs={"class","date-header"} ).string
	title	   = soup.find( attrs={"class","post-title entry-title"} )
	if title != None:
		title = title.string.strip()
	else:
		title = "NULL"

	body_soup  = soup.find( attrs={"class","post-body entry-content"} )
	links	   = body_soup.find_all( href_search )	

	fname = url[ url.rfind("/")+1: ].replace( ".html","" )
	print( str(n)+". Writing "+ fname + " ~ "+ date )	
	
	with open( "anon_posts/"+str(n)+" ~ "+fname + " ~ "+date + ".txt","w") as file:
		file.write( title +" ~ "+ date +" ~ "+ url )
		file.write( body_soup.get_text() )
	
	with open( "anon_links/"+str(n)+" ~ "+fname + " ~ "+date + "_LINKS.txt","w") as file:
		file.write( title +" ~ "+ date +" ~ "+ url +"\n" )		
		for link in links:
			link = link.attrs["href"]
			if( "blogspot" not in link ):
				file.write("\n"+ link)
			else:
				print( "Discarding "+link )
	
	dictionary = { "Num":n,"Name":fname.replace("|","_"),"Date":date,"Url":url }
	csv_list.append( dictionary )

	url = soup.find( attrs={"title":"Post più recente"} )

	sleep(2)


csv_write( csv_list )




