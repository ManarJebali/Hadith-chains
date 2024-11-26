import pandas as pd

from Narrator import Narrator
import Hadith_chains
import NarratorsGraph
import transmissionChainInsertion


#Load data from excel files
file_path1='annexe2_2hadith2.xlsx'
file_path2='anexe2_1_hadith1.xlsx'

df_narrators = pd.read_excel(file_path1)
df_chains=pd.read_excel(file_path2, header=None, usecols=[0])

def load_narrators(df):
        narrators={}
        df.columns=['fullName','name','birthDate','deathDate']
        for _,row in df.iterrows():
            narrators[row['fullName']]=Narrator(row['name'], row['birthDate'], row['deathDate'])
        return narrators


def prepare_chains(df):
        chains = {}
        current_chain = []
        current_key = 1

        for _, row in df.iterrows():
            text=row[0]
            
            if isinstance(text,str):
                if "سلسلة رواة الحديث عدد" in text:
                    if current_chain:
                        chains[current_key]=current_chain
                        current_chain=[]
                        current_key+=1

                else:
                    current_chain.append(text.strip())
                
        if current_chain:
            chains[current_key]=current_chain

        
        #Cleaning Narrator Names
        for key, value in chains.items():
            chains[key]=[narrator.replace('\xa0',' ').strip() for narrator in value]

        return chains

print(prepare_chains(df_chains))