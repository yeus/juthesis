# class PrettyTable

#representing objects in jupyter:
#http://nbviewer.jupyter.org/github/ipython/ipython/blob/1.x/examples/notebooks/Part%205%20-%20Rich%20Display%20System.ipynb

from string import Template
import xml.etree.ElementTree as ET
from xml.dom import minidom

import collections

ctorgb = lambda c: '"#{:02X}{:02X}{:02X}"'.format(*[int(round(i*255.0)) for i in c])

def prettify(mystring):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(ET.fromstring(mystring), 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def taggify(data,tag, attr = None):
    if attr: 
        attr = " ".join([i+ "=" + j for i,j in attr.items()])
        #print(attr)
    else: attr = ""
    return "<"+tag + " " + attr +">" + str(data) + "</"+tag+">"

def htmllist(elemlist, tag = "td", align=False):
    html = ""
    #align="left|right|center|justify|char
    for i in elemlist:
        if align == True:
            if type(i) == int: 
                #print("int!" + str(i))
                aligntag = tag + ' align="right"'                
            else:
                aligntag = tag
        else: aligntag = tag
        
        html += "<{}>{}</{}>".format(aligntag,i,tag)
    return html

def html_table(data, header=None):
    if header!=None:
        boldheader = ["<b>{}</b>".format(i) for i in header]
        head = "<thead><tr>{0}</tr></thead>\n".format(htmllist(boldheader, "td"))
    else: head=""    
    
    rows = htmllist([htmllist(i, align = True) for i in data], "tr")
    body = "<tbody>{}</tbody>".format(rows)

    return "<table>{}</table>".format(head + body)

def html_tree(data, horiz=False, color="#FFFFFF"):
    head=""
    if type(data)==str:
        return data
    
    try:
        if type(data)==dict:
            if "label" in data : head = data["label"]
            if "color" in data: color = data["color"]
            if "data" in data: data = data["data"]
            else: 
                head = list(data.keys())[0]
                data = list(data.values())[0]

        rows = ""
        for i in data:
            if type(i)==dict and "color" in i:  
                color = i["color"]
                #print(color)
            attr = {#"style":"\"text-align:center;\"",
                    "bgcolor":color}
            if horiz:
                rows += taggify(html_tree(i, horiz=False, color = color),
                            "td")
            else:
                rows += taggify(taggify(html_tree(i, horiz=True, color = color),
                            "td"),"tr")                
                
        if horiz: rows = taggify(rows, "tr")
            
        body = rows
        head = taggify(head,"thead")
        #return taggify("<table>{}</table>".format(head + body),"div", attr={"align":"center"})
        return "<table>{}</table>".format(head + body)
        #return body

    except TypeError:
        #print("final")
        return str(data)
    except:
        print(traceback.format_exc())

class PrettyTable(object):
    def __init__(self, initlist=[], caption = "TODO", label = "TODO", 
                 header=None, maxsize = 40, hcolor=(0.5,0.5,0.5),
                 latexalignment=None):
        self.s = "not initialized"
        if len(initlist) < maxsize:
            self.table = initlist
        else: print("table too big!")
        self.header = header
        self.caption = caption
        self.label = label
        self.hcolor = ",".join([str(i) for i in hcolor])
   
    def _repr_html_(self):
        return html_table(self.table, self.header)
    
    def _repr_latex_(self):
        tabletmpl=Template("""
\\begin{table}[$position]
\centering
\\begin{tabularx}{0.9\\textwidth}{| $formatting |}
    \hline
    \\rowcolor[rgb]{$hcolor}
    $header
    \\\\ \hline
    $rows
    \\\\ \hline
\end{tabularx}
\caption{$caption}
\label{tab:$label}
\end{table}
""") #this template needs the latex booktabs package
        if self.header:
            header = " & ".join(["\\textbf{"+str(i).replace("_","\_")+"}" for i in self.header])
        else: header = ""
        rows = " \\\\ \hline\n\t".join([" & ".join([str(i).replace("_","\_") for i in row]) for row in self.table])
        formatting = " | ".join("X" * len(self.table[0]))

        latex = tabletmpl.substitute(rows = rows, header = header,
                                     formatting = formatting,
                                     caption = self.caption,
                                     label = self.label,hcolor = self.hcolor,
                                     position = "H")
        return latex
        
#    def __repr__(self):
#        return "huhuhuu"
