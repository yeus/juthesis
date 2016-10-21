#!/usr/bin/python
# -*- coding: utf-8 -*-

#script to take a list of acronyms as input and replace
# all acronyms in a text file with \acro{<acronym>}

import re #regular expressions to search and replace acronyms
import sys
#import getopt

repl = "\\acro{}"

acrolist = re.compile("{(?P<a>.*)}{(?P<b>.*)}")

with open("acronyms.tex") as acrofile:
    acrostr = acrofile.read()
    
acrostr = acrostr.split("\n")[1:-2]
acros = [acrolist.search(i).groups() for i in acrostr]

#open latex file
filename = sys.argv[1]
with open(filename) as texfile:
    texstr = texfile.read()
    
#TODO:  if line starts with "\section"  dont replace!!    

newtex = texstr
for acro, acrolong in acros:
    repl = r'\\ac{{{}}}'.format(acro)
    nosec = r'(?![^{]*})' #make sure, regex does no appear between curly braces
    #TODO: do only not replace in section headings between curly braces
    regex = r'(\b'+acro+r'\b)' + nosec  
    newtex, n = re.subn(regex,repl,newtex)
    #if n>0: print("replacements for {}: {}".format(regex,n))
    
print(newtex)


#class Usage(Exception):
    #def __init__(self, msg):
        #self.msg = msg

#def main(argv=None):
    #if argv is None:
        #argv = sys.argv
    #try:
        #try:
            #opts, args = getopt.getopt(argv[1:], "h", ["help"])
        #except getopt.error, msg:
             #raise Usage(msg)
        ## more code, unchanged
    #except Usage, err:
        #print >>sys.stderr, err.msg
        #print >>sys.stderr, "for help use --help"
        #return 2

#if __name__ == "__main__":
    #sys.exit(main())
