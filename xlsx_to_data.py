"""Rebuild www/data.js from an Excel file.
Usage:  pip install pandas openpyxl
        python tools/xlsx_to_data.py my-list.xlsx
Every sheet is read. Column names (any order, extra columns ignored):
  Ward (number 1-48, or "mixed"), House No, Street, Name, Age, Rel Type (F/H/M/W/O),
  Relation Name, Mobile, Village/Town.
If a sheet has no Ward column, the number in the sheet name is used ("12ward" -> 12).
"""
import sys, re, json, pandas as pd
HM={'ward':'ward','wardnumber':'ward','houseno':'house','house':'house','street':'street','streetarea':'street','villagetown':'village',
    'name':'name','membername':'name','age':'age','reltype':'rel','relationtype':'rel','relname':'relname','relationname':'relname',
    'mobile':'phone','phone':'phone','phonenumber':'phone'}
def clean(v): return '' if v is None or (isinstance(v,float) and v!=v) else str(v).strip()
rows=[]
x=pd.ExcelFile(sys.argv[1])
for sh in x.sheet_names:
    d=x.parse(sh)
    cols={c:HM.get(re.sub(r'[^a-z]','',str(c).lower())) for c in d.columns}
    d=d.rename(columns={c:k for c,k in cols.items() if k})
    if 'name' not in d: continue
    m=re.search(r'\d+',sh)
    for _,r in d.iterrows():
        name=clean(r.get('name'))
        if not name: continue
        w=clean(r.get('ward')) or (m.group(0) if m else '')
        w='mixed' if w.lower()=='mixed' else str(int(float(w))) if re.fullmatch(r'\d+(\.0+)?',w) else ''
        if not w: continue
        ph=re.sub(r'\D','',clean(r.get('phone')))[-10:]
        rel=clean(r.get('rel'))[:1].upper(); rel=rel if rel in 'FHMWO' else ''
        age=clean(r.get('age')); age=int(float(age)) if re.fullmatch(r'\d+(\.0+)?',age) else ''
        rows.append([w,name,rel,clean(r.get('relname')),clean(r.get('house')),clean(r.get('street')),ph,clean(r.get('village')),age,''])
open('www/data.js','w',encoding='utf-8').write("/* Records: [ward, name, relType, relName, house, street, phone, village, age, reviewNote]. Ward 'mixed' = Mixed Data. */\nconst BASE_RAW="+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+";\nconst DROP=new Set([]);\n")
print(len(rows),'records written to www/data.js')
