def get_next_target(page):
	start_link=page.find('<a href=')
	if start_link==-1:
		return None,0
	start_quote=page.find('"',start_link)
	end_quote=page.find('"',start_quote+1)
	url=page[start_quote+1:end_quote]
	return url,end_quote

def print_all_links(page):
	while 1:
		url,endpos=get_next_target(page)
		if url:
			print url
			page=page[endpos:]
		else:
			break

def get_all_links(page):
	links=[]
	while 1:
		url,endpos=get_next_target(page)
		if url:
			links.append(url)
			page=page[endpos:]
		else:
			break
	return links

def get_page(url):
	try:
		import urllib
		return urllib.urlopen(url).read()
	except:
		return ""

cache = {
   'http://udacity.com/cs101x/urank/index.html': """<html>
<body>
<h1>Dave's Cooking Algorithms</h1>
<p>
Here are my favorite recipies:
<ul>
<li> <a href="http://udacity.com/cs101x/urank/hummus.html">Hummus Recipe</a>
<li> <a href="http://udacity.com/cs101x/urank/arsenic.html">World's Best Hummus</a>
<li> <a href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen's Hummus Recipe</a>
</ul>

For more expert opinions, check out the
<a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>
and <a href="http://udacity.com/cs101x/urank/zinc.html">Zinc Chef</a>.
</body>
</html>






""",
'http://www.udacity.com/cs101x/index.html':"""<html>
<body>
This is a test page for learning to crawl!
<p>
It is a good idea to 
<a href="http://www.udacity.com/cs101x/crawling.html">learn to crawl</a>
before you try to 
<a href="http://www.udacity.com/cs101x/walking.html">walk</a> or 
<a href="http://www.udacity.com/cs101x/flying.html">fly</a>.
</p>
</body>
</html>


""",
'http://www.udacity.com/cs101x/walking.html':"""<html>
<body>
I can't get enough 
<a href="http://www.udacity.com/cs101x/index.html">crawling</a>!
</body>
</html>



""",
'http://www.udacity.com/cs101x/flying.html':"""<html>
<body>
The magic words are Squeamish Ossifrage!
</body>
</html>

""",
'http://www.udacity.com/cs101x/kicking.html':"""<html>
<body>
<b>Kick! Kick! Kick!</b>
</body>
</html>



""",
'http://www.udacity.com/cs101x/crawling.html':"""<html>
<body>
I have not learned to crawl yet, but I am quite good at 
<a href="http://www.udacity.com/cs101x/kicking.html">kicking</a>.
</body>
</html>



""",

   'http://udacity.com/cs101x/urank/zinc.html': """<html>
<body>
<h1>The Zinc Chef</h1>
<p>
I learned everything I know from
<a href="http://udacity.com/cs101x/urank/nickel.html">the Nickel Chef</a>.
</p>
<p>
For great hummus, try
<a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/nickel.html': """<html>
<body>
<h1>The Nickel Chef</h1>
<p>
This is the
<a href="http://udacity.com/cs101x/urank/kathleen.html">
best Hummus recipe!
</a>

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/kathleen.html': """<html>
<body>
<h1>
Kathleen's Hummus Recipe
</h1>
<p>

<ol>
<li> Open a can of garbonzo beans.
<li> Crush them in a blender.
<li> Add 3 tablesppons of tahini sauce.
<li> Squeeze in one lemon.
<li> Add salt, pepper, and buttercream frosting to taste.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/arsenic.html': """<html>
<body>
<h1>
The Arsenic Chef's World Famous Hummus Recipe
</h1>
<p>

<ol>
<li> Kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>.
<li> Force her to make hummus for you.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/hummus.html': """<html>
<body>
<h1>
Hummus Recipe
</h1>
<p>

<ol>
<li> Go to the store and buy a container of hummus.
<li> Open it.
</ol>

</body>
</html>




""",
}
'''
def get_page(url):
    if url in cache:
        return cache[url]
    else:
        return None
'''

def union(a,b):
	for e in b:
		if e not in a:
			a.append(e)
	return a

def add_to_index(index, keyword, url):
    if keyword in index:
    	index[keyword].append(url)
    else:
    	index[keyword]=[url]

def add_page_to_index(index,url,content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
    	return None

def crawl_web(seed):
	tocrawl = [seed]
	crawled = []
	graph = {}
	index = {} 
	while tocrawl: 
		page = tocrawl.pop()
		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			outlinks = get_all_links(content)
			graph[page]=outlinks
			union(tocrawl, outlinks)
			crawled.append(page)
			return index, graph

def compute_ranks(graph):
	d=0.8
	numloops=10
	ranks={}
	npages=len(graph)
	for page in graph:
		ranks[page]=1.0/npages
	for i in range(0,numloops):
		newranks={}
		for page in graph:
			newrank=(1-d)/npages
			for node in graph:
				if page in graph[node]:
					newrank=newrank+d*(ranks[node]/len(graph[node]))
			newranks[page]=newrank
		ranks=newranks
	return ranks

#print get_page('https://www.hackerrank.com/interviewstreet')
import os
#content=os.system("curl http://leetcode.com/")
#content = os.popen('curl http://leetcode.com/onlinejudge').read()
import subprocess
'''
content = subprocess.check_output("curl http://www.iitg.ac.in/", shell=True)
print "-------------------------------------------------------"
print "-------------------------------------------------------"
print "-------------------------------------------------------"
#content= get_page('http://leetcode.com/')
#print content
print "-------------------------------------------------------"
print "-------------------------------------------------------"
print "-------------------------------------------------------"
print print_all_links(content)
#print crawl_web('http://www.iitg.ac.in/')
#print crawl_web('http://www.hackerrank.com/interviewstreet')
'''
print get_page('http://xkcd.com/353')
print "-------------------------------------------------------"
print "-------------------------------------------------------"
print "-------------------------------------------------------"
index,graph=crawl_web('http://xkcd.com/353')
print graph
print "-------------------------------------------------------"
print "-------------------------------------------------------"
print "-------------------------------------------------------"
ranks=compute_ranks(graph)
print ranks

'''
def hashtable_update(htable,key,value):
    # Your code here
    bucket = hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0] == key:
            entry[1]=value
    return htable

def hashtable_lookup(htable,key):
    bucket = hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0] == key:
            return entry[1]
    return None

def hashtable_add(htable,key,value):
    bucket = hashtable_get_bucket(htable,key)
    bucket.append([key,value])

def hashtable_get_bucket(htable,keyword):
    return htable[hash_string(keyword,len(htable))]


def hash_string(keyword,buckets):
    out = 0
    for s in keyword:
        out = (out + ord(s)) % buckets
    return out

def make_hashtable(nbuckets):
    table = []
    for unused in range(0,nbuckets):
        table.append([])
    return table
'''

#print get_page('http://xkcd.com/353')

#print_all_links(get_page('http://xkcd.com/353'))

#print get_all_links(get_page('http://xkcd.com/353'))
