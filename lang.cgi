#!/usr/bin/env python

# Copyright (c) 2011-2012, Koninklijke Bibliotheek (National library of the Netherlands).
# 
# This file is part of the STITCHplus project.
# (http://www.catchplus.nl/en/diensten/deelprojecten/stitchplus/)
# 
# lang.cgi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# DBpedia_to_solr.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with lang.cgi. If not, see <http://www.gnu.org/licenses/>.

"""
    To get this program to work you must place this file in your document root Apache directory, and make it executable. (Depends on python's CGI module.)
    Place the textcat-1.0.1.jar file in your local bin directory and make sure java -jar /usr/local/bin/textcat-1.0.1.jar -categorize works.
"""

__author__  = "Willem Jan Faber"
__version__ = "0.01b"

import os
import cgi

import cgitb
import urllib

try:
    import json
except:
    import simplejson as json

from lxml import etree

cgitb.enable()
form = cgi.FieldStorage()
q = form.getvalue("text")
mode = form.getvalue("mode")

if mode:
    if "xml" in mode:
        mode="xml"
    else:
        mode="json"
else:
    mode='json'

def response(text, mode):
    """ Write the incoming text to a tempfile on disk, and execute the Java language detector.\n
        Response format is either JSON or XML depending on the users request. \n
    """

    if not type(text) == str:
        print("Content-Type: text/html;charset=UTF-8\n\n")
        print("<h3>KB language detect version: %s</h3><br/>Missing text<br/><br/>" % __version__)
        print("This is a wrapper based upon <a href='http://textcat.sourceforge.net/'>http://textcat.sourceforge.net/</a><br/><br/>")
        print("Optional parameter mode  either 'xml' or 'json'<br/><br/>")
        print("Examples : <br/><br/><li/><a href='http://kbresearch.nl/lang.cgi?text=\"Ground controll to mayor Tom\"'>http://kbresearch.nl/lang.cgi?text=\"Ground controll to mayor Tom\"</a><br/>")
        print("<li/><a href='http://kbresearch.nl/lang.cgi?text=\"Ground controll to mayor Tom\"&mode=xml'>http://kbresearch.nl/lang.cgi?text=\"Ground controll to mayor Tom\"&mode=xml</a> <br/>")
        return()
    else:
        if len(text) > 5000:
            print("Content-Type: text/html;charset=UTF-8\n\n")
            print("<h3>KB Language detect v.0.01b</h3><br />Text size to large<br /><br />")
            return()
        if len(text) <1:
            print("Content-Type: text/html;charset=UTF-8\n\n")
            print("<h3>KB Language guesser v.0.01b</h3><br />Text size to small<br /><br />")
            return()
    try:
        with tempfile.NamedTemporaryFile() as fh:
            fh.write(text)
        res = os.popen('cat '+fh.name+' | java -jar /usr/local/bin/textcat-1.0.1.jar -categorize').read()
        try:
            os.unlink(fh.name)
        except:
            pass
    except:
        res=""
        try:
            os.unlink(fh.name)
        except:
            pass
        return()

    if not (len(res) > 1 and len(res) < 100):
        print("Content-Type: text/html;charset=UTF-8\n\n")
        print("Fatal exception!")
    if mode == "json":
        print("Content-Type: application/json;charset=UTF-8\n")
        r={"lang" : res}
        print(simplejson.dumps(r))
    if mode == "xml":
        print("Content-Type: text/xml;charset=UTF-8\n")
        print("<lang>"+res+"</lang>")
        return()

response(q,mode)
