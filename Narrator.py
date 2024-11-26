class Narrator:
    def __init__(self,name,birthDate,deathDate):
        self.name=name
        self.birthDate=birthDate
        self.deathDate=deathDate

    def __repr__(self):
        return f"Name: {self.name}; birthDate: {self.birthDate}; deathDate: {self.deathDate}\n"
    
    def __str__(self):
        return f"Narrator( Name: {self.name} \n\t  birthDate: {self.birthDate} \n\t  deathDate: {self.deathDate})"
    

    @staticmethod
    def load_narrators(df):
        narrators={}
        df.columns=['fullName','name','birthDate','deathDate']
        for _,row in df.iterrows():
            narrators[row['fullName']]=Narrator(row['name'], row['birthDate'], row['deathDate'])
        return narrators
