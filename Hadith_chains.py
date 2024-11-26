class Hadith_chains:
    def __init__(self,id,mainSource,chain):
        self.id=id
        self.mainSource=mainSource
        self.chain=chain.copy()

    def __repr__(self):
        return f"Hadith: {self.id}; MainSourece: {self.mainSource} Chain: {self.chain}\n"

    def __str__(self):
        return f"Hadith( id: {self.id}; MainSourece: {self.mainSource}; Chain: {self.chain})"
    

    @staticmethod
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