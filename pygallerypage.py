#!/usr/bin/env python2 -c
import os
import SimpleHTTPServer
import SocketServer
from optparse import OptionParser
import sys
import random

# set default values
curdir = os.getcwd()
port = 8000

# get options from command line
usage = "usage: %prog [options] [DIR [PORT]]"
parser = OptionParser(usage=usage, version="%prog 0.1")
parser.add_option("-d", "--directory", dest="curdir", help="Run in directory DIR", metavar="DIR")
parser.add_option("-p", "--port", dest="port", help="Run on port PORT", metavar="PORT")

(options, args) = parser.parse_args()

if len(args) > 1:
    port = args[1]

if len(args) > 0:
    curdir = args[0]

if options.curdir:
    curdir = options.curdir

if options.port:
    port = options.port

#print ("curdir={0}, port={1}".format(curdir,port))
os.chdir(curdir)
port = int(port)

dirlist = os.listdir(curdir)
imglist = []
imgexts = ['.jpg', '.png', '.gif']
for file in dirlist:
    for ext in imgexts:
        if ext in file:
            imglist.append(file)
            break

random.shuffle(imglist)
#print(imglist)

def makeJavascriptArray(arr):
    text = "var pythonarr = new Array();\nvar pythonarrsize = 0;\n"
    for i in arr:
        text = text + "pythonarr[pythonarrsize++] = \"{0}\";\n".format(i)
    return text

#print(makeJavascriptArray(imglist))

def makeMoreJavascript():
    return """
var pythonindex = 0;
function pythonload20() {
    var txt = document.getElementById("images").innerHTML;
    var i=0;
    for (i=0; i<20 && pythonindex < pythonarrsize; i++, pythonindex++) {
        txt = txt + '<img src="' + pythonarr[pythonindex] + '" />';
    }
    document.getElementById("images").innerHTML = txt;
    if (pythonindex == pythonarrsize) {
        document.getElementById("morelink").innerHTML = "";
    }
}"""

#print(makeMoreJavascript())

def generateHTML():
    return """<html><head>
<script type="text/javascript"> 
{0} 
{1}
</script>
</head>
<body onload="pythonload20()">
<div id="images"></div>
<div id="morelink"><a href="#" onClick="pythonload20(); return false">More ...</a>
</div></body></html>""".format(makeJavascriptArray(imglist), makeMoreJavascript())

#print (generateHTML())

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        for filetype in imgexts:
            if filetype in self.path:
                SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
                return
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(generateHTML())

try:
    httpd = SocketServer.TCPServer(("", port), CustomHandler)
    print "serving at port", port
    httpd.serve_forever()
except Exception as e:
    print (e)
    sys.exit()
