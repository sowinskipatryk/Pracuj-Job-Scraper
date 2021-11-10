import pandas as pd

file = open('job_offers.txt','r')

x = file.read()

y = x.strip().replace('\n',' ').replace(' - ',' ').replace('  ',' ').replace('(','').replace(')','')

z = y.split()

a = []

my_dict = {i:z.count(i) for i in z}

a.append(my_dict)

df = pd.DataFrame(a)
df.to_excel('phrases.xlsx', index=False)