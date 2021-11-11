import pandas as pd

file = open('job_offers.txt','r')

x = file.read()

y = x.strip().replace('\n',' ').replace(' - ',' ').replace('  ',' ').replace('(','').replace(')','').replace(',','').replace(';','').upper()

z = y.split()

arr = []

my_dict = {i:z.count(i) for i in z}

for i, (k, v) in enumerate(my_dict.items()):
    arr.append((i+1, k, v))

df = pd.DataFrame(arr)
df.columns = ['Index','Phrase','Appearances']
df = df[df['Phrase'].str.contains('HTTP') == False]
df = df.loc[:, df.columns != 'Index']
df = df.sort_values('Appearances', ascending=False)

df.to_excel('phrases.xlsx', index=False)