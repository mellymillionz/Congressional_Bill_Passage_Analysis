class DataClean:

    def __init__(self):
        
def cosponsr_clean(x):
    if x <= 44.0:
        return x
    if x > 44.0:
        return 50

def party_clean(x):
    if x == 100.0:
        return 0
    if x == 200.0:
        return 1
    if x == 328.0:
        return 3

def billtype_clean(x):
    if x == 'hr':
        return 0
    if x == 's':
        return 1

def name_clean(x):
    if x >= 400:
        return 1
    if x >= 300 and x <= 399:
        return 2
    if x >= 200 and x <= 299:
        return 3
    if x >= 150 and x <= 199:
        return 4
    if x >=100 and x <= 149:
        return 5
    if x >=50 and x <= 99:
        return 6
    if x < 50:
        return 7

def final_columns(df):
    
    
    df['month'] = df['IntrDate'].apply(lambda x: x.strftime('%B')) 
    
    names = df['NameFull'].value_counts()

    names_dict = names.to_dict() #converts to dictionary

    df['sponsor_count'] = df['NameFull'].map(names_dict) 
    
    df['title_len'] = [len(summary) for summary in df['Title']]
    
    df['clean_cosponsr'] = df['Cosponsr'].map(lambda x: cosponsr_clean(x))

    df['clean_party'] = df['Party'].map(lambda x: party_clean(x))
    
    df['ranked_sponsor_count'] = df['sponsor_count'].map(lambda x: name_clean(x))
    
    
    df.drop(columns=['Cosponsr', 'Party', 'NameFull', 'sponsor_count', 'Title', 'IntrDate'], inplace=True)
        
    return df