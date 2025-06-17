import wikitextparser as wtp
import sys
import os
# Add the parent directory of 'sanitizer' to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Now you can use absolute imports
from sanitizer.templates.main import sanitizeTemplates



path = os.getcwd() + '/info/'

files = os.listdir(path)

def get_CSV_from_table(table_data):
    
    csv = ''
    
    for row in table_data:
        
        csv = csv + ",".join(row) + '\n'
    
    return csv
    


def sanitize_tables(text):
    parser = wtp.parse(text)

    tables = parser.get_tables()
    
    table_body = '' 
    
    for table in tables:
        
        data = table.data()
        
        table_original = str(table)
        table_body = table_body + get_CSV_from_table(data)    
        table_head = "Table data:\n" if table.caption == None else f"Table data: {table.caption}\n"
        replacement = table_head + table_body
        print(replacement)
        text = text.replace(str(table),replacement)
    
    return text
        

# for file in files:
#     filePath = 'info/' + file
#     outputFilePath = 'outputs/' + file
#     with open(filePath,"r") as file:
#         text = file.read()
#         print(f"Processing {filePath} for tables, length={len(text)=}")
#         replacementText = sanitize_tables(text)
        
            
#     with open(outputFilePath,'w') as outputFile:
#         outputFile.write(replacementText)
#         print(f"output file generated' {outputFilePath}  {len(replacementText)=}")        
       
replacementText = ''
with open("info/Evelyn.txt","r") as file:
    text = file.read()
    text = sanitizeTemplates(text) 
    text =  sanitize_tables(text)

with open('Peepee.txt','w') as outputFile:
    outputFile.write(text)
    print('output file generated',  f'{len(text)=}')  