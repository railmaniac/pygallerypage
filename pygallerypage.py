#pygallerypage serves a webpage containing a gallery with images in a directory.
#Copyright (C) 2011  railmaniac
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#email: railmaniac@gmail.com 

import os
import random

class GalleryClass():
    port = 8000
    path = ""
    usage = "usage: %prog [options] [DIR [PORT]]"
    imglist = []
    imgexts = ['.jpg', '.png', '.gif']
    prefix = "python"
    def __init__(self, path, port=8000):
        self.path = path
        self.port = int(port)
        listdir = os.listdir(path) # No checking [](/trollface)
        for file in listdir:
            for ext in self.imgexts:
                if ext in file:
                    self.imglist.append(file)
                    break

    """Function to generate just the javascript required"""
    def generateJavascript(self):
        pre = self.prefix
        text = "var {0}_arr = new Array();\nvar {1}_arrsize = 0;\n".format(pre, pre)
        for i in self.imglist:
            text = text + "{1}_arr[{2}_arrsize++] = \"{0}\";\n".format(i, pre, pre)
        text = text + "var {0}_index = 0;".format(pre)
        text = text + "function {0}_load20() ".format(pre) + '{'
        text = text + "var txt = document.getElementById(\"{0}_images\").innerHTML;".format(pre)
        text = text + "var i=0;"
        text = "for(i=0;i<20 && {0}_index < {1}_arrsize;i++, {2}_index++)".format(pre, pre, pre)
        text = text + '{' + "txt = txt + '<img src="' + {0}_arr[{1}_index] + '" />';".format(pre, pre) + '}'
        text = text + "document.getElementById(\"{0}_images\").innerHTML = txt;".format(pre)
        text = text + "if ({0}_index == {1}_arrsize) ".format(pre, pre) + '{'
        text = text + "document.getElementById(\"{0}_morelink\").innerHTML = \"\";".format(pre) + '}'
        return text

    """Function to generate the HTML part to bind the JS with"""
    def generateHTML(self):
        pre = self.prefix
        text = "<div id=\"{0}_images\"></div>".format(pre)
        text = "<script type=\"text/javascript\">\n{0}_load20();\n</script>".format(pre)
        text = text + "<div id=\"{0}_morelink\">".format(pre)
        text = text + "<a href=\"#\" onClick=\"{0}_load20(); return false;\">More ...</a>".format(pre)
        text = text + "</div>"
        return text

    """Function to generate entire HTML"""
    def generateCompleteHTML(self):
        js = self.generateJavascript()
        html = self.generateHTML()
        text = "<html><head><script type=\"text/javascript\">{0}</script></head>".format(js)
        text = text + "<body>{0}</body></html>".format(html)
        return text

    """Function to randomize directory order"""
    def randomize(self):
        random.shuffle(self.imglist)

if __name__ == "__main__":
    import SimpleHTTPServer
    import SocketServer
    from optparse import OptionParser
    import sys
    
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
    
    class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            gallery = GalleryClass(curdir, port)
            for filetype in gallery.imgexts:
                if filetype in self.path:
                    SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
                    return
            if "random" in self.path:
                gallery.randomize()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(gallery.generateCompleteHTML())
    
    try:
        httpd = SocketServer.TCPServer(("", port), CustomHandler)
        print "serving at port", port
        httpd.serve_forever()
    except Exception as e:
        print (e)
        sys.exit()
