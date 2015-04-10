import urllib2
import sre
import sys

#implementation taken from
#http://www.techrepublic.com/article/parsing-data-from-the-web-in-python/

def title_from_url( streamurl ):
    website = None
    streamtitle = None
    try:
        website = urllib2.urlopen(streamurl)
    except urllib2.HTTPError, e:
            print("Cannot retrieve URL: HTTP Error Code", e.code)
    except urllib2.URLError, e:
            print("Cannot retrieve URL: " , e.reason)
    if website:
        pagehtml = website.read()
        streamtitle = sre.findall("<meta content='(.*?)' property='og:description'>",pagehtml)[0]
    return streamtitle

if __name__ == '__main__':
    if len(sys.argv) == 1:
        streamurl = 'http://twitch.tv/morrow' #test string
    else:
        streamurl = sys.argv[1]
    print(title_from_url( streamurl ) )
