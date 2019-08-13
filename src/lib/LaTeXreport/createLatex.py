from logs import logDecorator as lD
import jsonref
import pylatex
from pylatex import Document, Section, Subsection, Tabular,  Tabularx, MultiColumn, MultiRow, NoEscape
import scipy
import pickle
import numpy as np
import pandas as pd
import os

config = jsonref.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.lib.report.createLatex'

@lD.log(logBase + '.addSections')
def addSections(logger, doc, num):
    """
    Adds the required sections from the associated jsonConfig file
    as listed in the 'num' argument. e.g. addSections(doc, [1,3]) 
    will add sections 1-2 from the config file to the document doc
    
    Args:
        doc (LaTeX document): a latex document to write to
        num (LIST): An integer or list of integers specifying 
        which sections to write into doc. 
    """
    try:
        jsonConfig = jsonref.load(open('../config/paper1/createLatex.json'))
        if type(num) is not list: num = [num]
        sections = jsonConfig["sections"]
        for n in num:
            section = sections["section" + str(n)]
            print("Now writing section" + str(n))
           
            with doc.create(Section(section["title"])):
                # doc.append(NoEscape(section["text"]))
                doc.append(NoEscape(r"\lipsum[1-5]")) # For testing
                # if there are subsections, recurse? 
                # if sections["subsections"] is not Null:
        return 

    except Exception as e: 
        logger.error(f'Unable to add a section. \n {e}')


@lD.log(logBase + '.saveTable')
def saveTable(logger, table, fname = None):
    """
    Creates a latex file of the table and saves it in the 
    specified directory.

    If there are multiple files assigned to a table,
    the files will be loaded separately then merged into 1 df.

    Args:
        table (Dictionary): Contains keys of tables that will
        be saved into a tex file. 
        fname (String, optional): save file path name. Tex file 
        will be saved here. 

    """
    try:    
        jsonConfig = jsonref.load(open('../config/paper1/createLatex.json'))
        # if fname == None: fname = jsonConfig["input"]["texfilespath"] + "sampleoutput"

        dfs = [] # for merging multiple tables
        for k in table.keys():
            tbl = table[k]
            print("Now loading {}.".format(tbl))
            loadfile = "{}{}.{}".format(jsonConfig["input"]["filepath"],
                                        tbl,
                                        jsonConfig["input"]["fileformat"])
            data = pickle.load(open(loadfile, "rb"))
            dfs.append(data)
        mergedtable = pd.concat(dfs, axis=1, keys=table.keys(), sort=False)
        mergedtable.fillna(0, inplace=True)
        with open(fname + '.tex','w') as tf:
            tf.write(r"\centering")
            tf.write(mergedtable.to_latex(multirow=True, float_format="%0.0f")) #, column_format=r"0.9\textwidth"))
        return 

    except Exception as e: 
        logger.error(f'Unable to save a table. \n {e}')

@lD.log(logBase + '.addTable')
def addTable(logger, doc, tblno, wideTable=False):
    """
    Adds table from an existing latex file into a document object.
    If the table is specified to be wide, additional formatting 
    will be added to fit the table on the page. 
    
    Args:
        doc (LaTeX document): a latex document to write to
        tblno (Int): Specify the table number which is to be added. 
        This will correspond to the tex files names 
        (e.g. to add table1.tex, use addTable(doc, 1))
        wideTable (bool, optional): Indicate whether the table should
        be treated as a wide table. Adds formatting if True. Default False. 
    
    """
    try:
        tblName = "Table {}".format(tblno) 
        tblPath = os.path.join("Paper1","table" + str(tblno))
        with doc.create(Subsection(tblName)) as tbl:
            if wideTable: 
                tbl.append(NoEscape(r"\setlength{\tabcolsep}{2pt}"))
                tbl.append(NoEscape(r"\resizebox{\textwidth}{!}{"))

            tbl.append(NoEscape(r"\input{" + tblPath + r".tex}")) 

            if wideTable: 
                tbl.append(NoEscape(r"}"))
        return 
    except Exception as e: 
        logger.error(f'Unable to add the table. \n {e}')

@lD.log(logBase + '.addFigure')
def addFigure(logger, doc, figno):
    try:
        jsonConfig = jsonref.load(open('../config/paper1/createLatex.json'))
        figuresConfig = jsonConfig["figures"]
        figPath = os.path.join("Paper1",figuresConfig["figure"+str(figno)]["filename"])
        print(figPath)
        # with doc.create(Figure(position='h!')) as fig_:
        #     fig_.add_image(figPath)
        #     fig_.add_caption(figuresConfig[fig]["caption"])


        for fig in jsonConfig["figures"]:
            with doc.create(Figure(position='h!')) as fig_:
                fig_.add_image("Paper1/" + jsonConfig["figures"][fig]["filename"])
                fig_.add_caption(jsonConfig["figures"][fig]["caption"])
        return 
    except Exception as e: 
        logger.error(f'Unable to add the table. \n {e}')
