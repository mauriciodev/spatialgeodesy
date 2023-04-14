import re
import pandas as pd
from io import StringIO

"""Opens a sinex file and returns a dict of pandas dataframes containing the data on each sinex block."""
def read_sinex(fname):
    with open(fname) as f:
    #f = open(fname)
        data = f.read()   
        #sinex files declare blocks between +TAG and -TAG.
        blocks = re.findall(r'^\+(.*?)^-', data  , re.MULTILINE|re.DOTALL) 
        #tag=re.findall(r'^.+',blocks[0])[0]
        dictData = {}
        for block in blocks:
            tag = re.findall(r'^.+',block)[0]
            header=' '.join(re.findall(r'\n\*.+',block))
            header=re.sub('(\n\*)','',header).split()
            header=list(map(lambda x: x[1]+str(x[0]), enumerate(header)))
            #counting header size
            #widths=list(map(lambda x: len(x)+1, header))
            widths=list(map(len, header))
            lines=re.findall(r'\n\s.+',block, re.DOTALL)
            if len(lines)>0:
                df=pd.read_fwf(StringIO(lines[0].strip()), widths=widths, names=header, mangle_dupe_cols=True)
                dictData[tag] = df
            else:
                dictData[tag]=None
    return dictData


#fname = '/home/mauricio/Desktop/Doutorado_psq/Monitoria/Geod_Espacial/trabalhos/videos/tropo/braz0010.20zpd'
#data=read_sinex(fname)
#print(data.keys())
#pd.to_numeric(data , errors='ignore')
#print(data['TROP/SOLUTION']['TROTOT2']/1000)

