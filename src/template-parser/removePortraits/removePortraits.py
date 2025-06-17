import mwparserfromhell
import os

path = os.getcwd() + '/info/'

files = os.listdir(path)

for file in files:
    filePath = 'info/' + file
    outputFilePath = 'output' + file
    with open(filePath,"r") as file:
        text = file.read()
        
        parser = mwparserfromhell.parse(text)
        
        headings = parser.filter_headings()
        
        if '==Portraits==' in headings:
            portraitSection = parser.get_sections(matches=r"Portraits")[0]
            parser.remove(portraitSection)
            
            text = str(parser)
            
            with open(outputFilePath,'w') as outputFile:
                outputFile.write(text)
                
                print('output file generated')
    
    