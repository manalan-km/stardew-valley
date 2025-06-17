import re
with open("./logs.txt","r") as file: 
    template_names = set()
    text = file.read()
    
    lines = text.split('\n')
    
    for line in lines: 
        match = re.search(r'Not replacing (\w+) template', line)
        if match:
            template_name = match.group(1)
            template_names.add(template_name)
            
            
print(sorted(template_names))