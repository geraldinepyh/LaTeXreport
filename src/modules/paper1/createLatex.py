from lib.LaTeXreport import reportWriter as rw
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
df1 = df.groupby('species').mean()
df2 = df.groupby('species').min()
df3 = df.groupby('species').max()

rep = rw.Report('Top_Secret_Project')
rep.title = "My Top Secret Project Report"
rep.initialize(rep.fpath)

# Add media 
rep.saveFigure('Figure1', '/home/gerpang/LaTeXreport/results/Paper1/s0102.png', caption='This is the first figure.', option='scale=0.8', override=True)
rep.saveFigure('Figure2', '/home/gerpang/LaTeXreport/results/Paper1/figure1.png', caption='This is the second figure.', option='scale=0.6', override=True)
rep.saveTable('Table1', df1, caption='Table of results 1.')
rep.saveTable('Table2', df2, caption='Table of past results.', override=False)
rep.saveTable('Table3', df3, caption='Table of new results.', override=True)

# Add sections
rep.addSection('Introduction')
rep.addSection('Methodology')
rep.addSection('Data Collection', level=2)
rep.addSection('Models', level=2)
rep.addSection('Results')
rep.addSection('Discussion')
rep.addSection('Conclusion')
print(rep.sections)

# Generate PDF/Tex
rep.makeReport(tex_only=False)