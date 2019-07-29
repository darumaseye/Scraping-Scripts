from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("anon_links") if isfile(join("anon_links", f))]
list=[]
for i in onlyfiles:
	with open("anon_links/"+i) as filef:
		for i,line in enumerate(filef):
			if i>1:
				list.append(line)
with open('links.txt','w') as ff:
	for i in list:
		ff.write(i)
