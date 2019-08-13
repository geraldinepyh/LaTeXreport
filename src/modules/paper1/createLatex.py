from logs import logDecorator as lD 
import jsonref, pprint
import os

from lib.databaseIO import pgIO 
from psycopg2 import sql
import numpy as np
import pandas as pd
import pickle

from lib.LaTeXreport import createLatex as lt
import pylatex
from pylatex import Document, Section, Subsection, Tabular, Tabularx, MultiColumn, MultiRow, Package, NoEscape, Command, Figure

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.paper1.createLatex'


@lD.log(logBase + '.main')
def main(logger, resultsDict):
    '''
    Creates a sample report in pdf format.
    '''
    try:
        
        jsonConfig = jsonref.load(open('../config/paper1/createLatex.json'))
        tables = jsonConfig["tables"] 
        # Creates Tables
        for tbl in tables:
            lt.saveTable(table = jsonConfig["tables"][tbl]["files"],  
                fname = "../results/Paper1/{}".format(tbl))

        # Creates PDF Document
        makeReport(exportAsPDF=True)

        return
    except Exception as e: 
        logger.error(f'Unable to run main \n {e}')

@lD.log(logBase + '.makeReport')
def makeReport(logger, exportAsPDF = True):
    '''
    String pieces of latex together to form a report. 
    Assumes Latex have already been written to the same output location.
    '''
    try:
        jsonConfig = jsonref.load(open('../config/paper1/createLatex.json'))
        fpath = jsonConfig['output']['savePath']

        # # Configure Document 
        doc = Document()
        packages = jsonConfig["packages"]
        for p in packages: doc.packages.append(Package(p))
        preambles = jsonConfig["preamble"]

        # Add Title/Authors
        for pa in preambles:
            doc.preamble.append(Command(pa, preambles[pa]))
        doc.append(NoEscape(r"\maketitle"))
        # Abstract          
        doc.append(NoEscape(r"\begin{abstract}"))
        doc.append(jsonConfig["abstract"])
        doc.append(NoEscape(r"\end{abstract}"))

        # # # String pieces into a report
        lt.addSections(doc, 1)
        lt.addTable(doc, 2, wideTable = True)
        lt.addSections(doc, 2)     
        lt.addTable(doc, 3)
        lt.addSections(doc, 3)     
        lt.addTable(doc, 4)
        lt.addFigure(doc, 1)

        # # Add image
        for fig in jsonConfig["figures"]:
            with doc.create(Figure(position='h!')) as fig_:
                fig_.add_image("Paper1/" + jsonConfig["figures"][fig]["filename"])
                fig_.add_caption(jsonConfig["figures"][fig]["caption"])

        # # Build the document
        if exportAsPDF:
            doc.generate_pdf(fpath+"finalReport")
        else:
            doc.generate_tex(fpath+"finalReport")

        return doc
    except Exception as e: 
        logger.error(f'Unable to run makeReport \n {e}')

