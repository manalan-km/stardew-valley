import sys
import mwparserfromhell
import os
import logging
import re

def sanitizeTemplateName(string:str):
    string = string.replace('\n','')
    string = string.rstrip()
    string = string.lstrip()
    return string

def get_collection_items(name): 
    match(name):
        case 'Artifacts':
            return [ "Dwarf Scroll I" ,"Dwarf Scroll II","Dwarf Scroll III","Dwarf Scroll IV","Chipped Amphora","Arrowhead","Ancient Doll","Elvish Jewelry", 
                    "Dinosaur Egg","Rare Disc","Ancient Sword","Rusty Spoon","Rusty Spur","Rusty Cog","Chicken Statue","Ancient Seed","Prehistoric Tool","Dried Starfish","Anchor","Glass Shards","Bone Flute","Prehistoric Handaxe","Dwarvish Helm","Dwarf Gadget","Ancient Drum","Golden Mask","Golden Relic","Strange Doll","Strange Doll","Prehistoric Scapula","Prehistoric Tibia","Prehistoric Skull","Skeletal Hand","Prehistoric Rib","Prehistoric Vertebra","Skeletal Tail","Nautilus Fossil","Amphibian Fossil""Palm Fossil","Trilobite" ]
        case 'Cooking':
            return [
                    "Fried Egg", "Omelet", "Salad", "Cheese Cauliflower", "Baked Fish", "Parsnip Soup", "Vegetable Medley", 
                    "Complete Breakfast", "Fried Calamari", "Strange Bun", "Lucky Lunch", "Fried Mushroom", "Pizza", "Bean Hotpot", 
                    "Glazed Yams", "Carp Surprise", "Hashbrowns", "Pancakes", "Salmon Dinner", "Fish Taco", "Crispy Bass", 
                    "Pepper Poppers", "Bread", "Tom Kha Soup", "Trout Soup", "Chocolate Cake", "Pink Cake", "Rhubarb Pie", 
                    "Cookie", "Spaghetti", "Fried Eel", "Spicy Eel", "Sashimi", "Maki Roll", "Tortilla", "Red Plate", 
                    "Eggplant Parmesan", "Rice Pudding", "Ice Cream", "Blueberry Tart", "Autumn's Bounty", "Pumpkin Soup", 
                    "Super Meal", "Cranberry Sauce", "Stuffing", "Farmer's Lunch", "Survival Burger", "Dish O' The Sea", 
                    "Miner's Treat", "Roots Platter", "Triple Shot Espresso", "Seafoam Pudding", "Algae Soup", "Pale Broth", 
                    "Plum Pudding", "Artichoke Dip", "Stir Fry", "Roasted Hazelnuts", "Pumpkin Pie", "Radish Salad", "Fruit Salad", 
                    "Blackberry Cobbler", "Cranberry Candy", "Bruschetta", "Coleslaw", "Fiddlehead Risotto", "Poppyseed Muffin", 
                    "Chowder", "Fish Stew", "Escargot", "Lobster Bisque", "Maple Bar", "Crab Cakes", "Shrimp Cocktail", "Ginger Ale", 
                    "Banana Pudding", "Mango Sticky Rice", "Poi", "Tropical Curry", "Squid Ink Ravioli", "Moss Soup"
                ]
        case 'Fish':
            return [
                    "Pufferfish", "Anchovy", "Tuna", "Sardine", "Bream", "Largemouth Bass", "Smallmouth Bass", "Rainbow Trout", 
                    "Salmon", "Walleye", "Perch", "Carp", "Catfish", "Pike", "Sunfish", "Red Mullet", "Herring", "Eel", 
                    "Octopus", "Red Snapper", "Squid", "Seaweed", "Green Algae", "Sea Cucumber", "Super Cucumber", "Ghostfish", 
                    "White Algae", "Stonefish", "Crimsonfish", "Angler", "Ice Pip", "Lava Eel", "Legend", "Sandfish", 
                    "Scorpion Carp", "Flounder", "Midnight Carp", "Clam", "Mutant Carp", "Sturgeon", "Tiger Trout", "Bullhead", 
                    "Tilapia", "Chub", "Dorado", "Albacore", "Shad", "Lingcod", "Halibut", "Lobster", "Crayfish", "Crab", 
                    "Cockle", "Mussel", "Shrimp", "Snail", "Periwinkle", "Oyster", "Woodskip", "Glacierfish", "Void Salmon", 
                    "Slimejack", "Midnight Squid", "Spook Fish", "Blobfish", "Stingray", "Lionfish", "Blue Discus", "River Jelly", 
                    "Cave Jelly", "Sea Jelly", "Goby"
                ]
        case 'Items Shipped':
            return [
                    "Wild Horseradish", "Daffodil", "Leek", "Dandelion", "Parsnip", "Cave Carrot", "Coconut", "Cactus Fruit", 
                    "Banana", "Sap", "Large Egg (white)", "Egg (white)", "Egg (brown)", "Large Egg (brown)", "Milk", "Large Milk", 
                    "Green Bean", "Cauliflower", "Potato", "Garlic", "Kale", "Rhubarb", "Melon", "Tomato", "Morel", "Blueberry", 
                    "Fiddlehead Fern", "Hot Pepper", "Wheat", "Radish", "Red Cabbage", "Starfruit", "Corn", "Unmilled Rice", 
                    "Eggplant", "Artichoke", "Pumpkin", "Bok Choy", "Yam", "Chanterelle", "Cranberries", "Holly", "Beet", 
                    "Ostrich Egg", "Salmonberry", "Amaranth", "Pale Ale", "Hops", "Void Egg", "Mayonnaise", "Duck Mayonnaise", 
                    "Void Mayonnaise", "Clay", "Copper Bar", "Iron Bar", "Gold Bar", "Iridium Bar", "Refined Quartz", 
                    "Honey (any)", "Pickles (any)", "Jelly (any)", "Beer", "Wine (any)", "Juice (any)", "Poppy", "Copper Ore", 
                    "Iron Ore", "Coal", "Gold Ore", "Iridium Ore", "Wood", "Stone", "Nautilus Shell", "Coral", "Rainbow Shell", 
                    "Spice Berry", "Sea Urchin", "Grape", "Spring Onion", "Strawberry", "Sweet Pea", "Common Mushroom", 
                    "Wild Plum", "Hazelnut", "Blackberry", "Winter Root", "Crystal Fruit", "Snow Yam", "Sweet Gem Berry", "Crocus", 
                    "Red Mushroom", "Sunflower", "Purple Mushroom", "Cheese", "Goat Cheese", "Cloth", "Truffle", "Truffle Oil", 
                    "Coffee Bean", "Goat Milk", "Large Goat Milk", "Wool", "Duck Egg", "Duck Feather", "Caviar", "Rabbit's Foot", 
                    "Aged Roe (any)", "Ancient Fruit", "Mead", "Tulip", "Summer Spangle", "Fairy Rose", "Blue Jazz", "Apple", 
                    "Green Tea", "Apricot", "Orange", "Peach", "Pomegranate", "Cherry", "Bug Meat", "Hardwood", "Maple Syrup", 
                    "Oak Resin", "Pine Tar", "Slime", "Bat Wing", "Solar Essence", "Void Essence", "Fiber", "Battery Pack", 
                    "Dinosaur Mayonnaise", "Roe (any)", "Squid Ink", "Tea Leaves", "Ginger", "Taro Root", "Pineapple", "Mango", 
                    "Cinder Shard", "Magma Cap", "Bone Fragment", "Radioactive Ore", "Radioactive Bar", "Smoked Fish (any)", 
                    "Moss", "Mystic Syrup", "Raisins", "Dried Fruit (any)", "Dried Mushrooms (any)", "Carrot", "Summer Squash", 
                    "Broccoli", "Powdermelon"
                ]
        case 'Minerals':
            return [
                    "Emerald", "Aquamarine", "Ruby", "Amethyst", "Topaz", "Jade", "Diamond", "Prismatic Shard", "Quartz", "Fire Quartz",
                    "Frozen Tear", "Earth Crystal", "Alamite", "Bixite", "Baryte", "Aerinite", "Calcite", "Dolomite", "Esperite", "Fluorapatite",
                    "Geminite", "Helvite", "Jamborite", "Jagoite", "Kyanite", "Lunarite", "Malachite", "Neptunite", "Lemon Stone", "Nekoite",
                    "Orpiment", "Petrified Slime", "Thunder Egg", "Pyrite", "Ocean Stone", "Ghost Crystal", "Tigerseye", "Jasper", "Opal", "Fire Opal",
                    "Celestine", "Marble", "Sandstone", "Granite", "Basalt", "Limestone", "Soapstone", "Hematite", "Mudstone", "Obsidian",
                    "Slate", "Fairy Stone", "Star Shards"
                ]
        

def filterChoiceTemplates(choice_template):
    params = choice_template.params
    quote = str(params[0])
    message = quote
    if len(params) > 1:
        friendship_points = ''
        points = str(params[1])
        if params[1] == '0':
            friendship_points =  friendship_points + '+0 Friendship points'
            
        elif re.match(r"^-", points ):
            friendship_points = friendship_points +  f"{points} Friendship points"
            
        else:
            friendship_points = friendship_points +  f"+{points} Friendship points"
            
        if len(params) >=3:
            npc = str(params[2])
            
            friendship_points = friendship_points + ' with ' + npc
        
        
        message = message + f"({friendship_points})"
    return message
    
def filter_CookingChannel_templates(cc_template):
    params = cc_template.params
    
    date = str(params[0])
    
    return date

def filter_duration_templates(duration_template):
    params = duration_template.params
    
    duration = str(params[0])
    
    return duration

def filter_giftsByItem_template(template_content):
    params = template_content.params
    replacement = 'Gifts:{\n'
    for param in params: 
        replacement = replacement + str(param.name) + '=' + str(param.value) 
    
    replacement = replacement + '}'
    
    return replacement

def filter_heart_event_template(template_content):
    params  = template_content.params
    replacement = 'Heart Event:{\n'
    
    for param in params:
        replacement = replacement + str(param.name) + '=' + str(param.value)
        
    replacement = replacement + '}'
    
    return replacement

def filter_history_templates(history_template_content):
    params = history_template_content.params
    replacement = '-'
    
    for param in params:
        replacement = replacement + str(param.value) + '. '
        
    return replacement

def filter_name_template(name_template):
    params = name_template.params
    replacement = ''
    
    replacement = replacement + str(params[0].value)
    
    if len(params) > 1:
          second_param_lowercase_name = str(params[1].name).lower()
          if not (second_param_lowercase_name == 'size' or second_param_lowercase_name == 'link' or second_param_lowercase_name == 'class'):
            replacement = replacement + f"({params[1].value})"
    
    return replacement
    
def filter_npc_template(npc_template):
    replacement = ''

    params = npc_template.params
    
    replacement = replacement + str(params[0].value) 
    
    if(len(params)>1): 
        replacement = replacement + f"({str(params[1].value)})"
        
    return replacement   

def filter_price_template(price_template):
    
    params = price_template.params
    
    return f"Price: {params[0].value}(Currency:{params[1].value})" if len(params) > 1 else f"Price: {params[0].value} coins" 

def filter_probability_template(prob_template):
    params = prob_template.params
    
    return f"Probability: {params[0].value}"
    
def filter_quality_template(quality_template):
    params = quality_template.params
    
    itemName = str(params[0].value)
    
    quality = str(params[1].value)
    
    return f"{quality} {itemName}"   

def filter_quote_template(quote_template ):
    params = quote_template.params
    quote = str(params[0].value)
    author = ''
    if len(params) > 1:
        author = params[1].value
    
    quote = quote.replace('(Name)', '<player-name>').replace('(name)', '<player-name>') 
    
    return f"{quote}(said by {author})" if len(author)> 0 else f"{quote}"

def filter_energy_templates(energy_template):
    params = energy_template.params
    
    if len(params) == 0:
        return 'Energy: +0'
    else:
        energy_value = str(params[0].value)
        
        if re.match(r"^-", energy_value ):
            return f"Energy: -{energy_value}"
        elif re.match(r"^\d+$", energy_value):
           return f"Energy: +{energy_value}" 
        return f"Energy: {energy_value}"
    
def filter_health_templates(health_template):
    params = health_template.params
    
    if len(params) == 0:
        return 'Health: +0'
    else:
        health_value = str(params[0].value)
        
        if re.match(r"^-", health_value ):
            return f"Health: -{health_value}"
        elif re.match(r"^\d+$", health_value):
           return f"Health: +{health_value}" 
        return f"Health: {health_value}"
    
def filter_season_template(season_template):
    params  = season_template.params
    season = str(params[0].value)
    day = ''
    if len(params)>1:
        day = params[1].value
    
    return f"Day {day} {season} Season" if len(day)> 0 else f"{season} Season"

def filter_spoiler_template(spoiler_template):
    pass
        
def filter_weather_template(weather_template):
    params = weather_template.params
    weather = str(params[0].value)
    
    return f"{weather} weather"

def remove_template(template):
    return ''    

def filter_collapse_template(collapse_template):
    params = collapse_template.params
    first_param = params[0]
    first_param_name = str(first_param.name) 
    first_param_value = str(first_param.value)
    if first_param_name == 'content':
        return first_param_value
    
    return f"{first_param_value}: {params[1].value} "

def filter_bundle_templates(bundle_template):
    params = bundle_template.params
    bundle_name = str(params[0].value)
    
    return f"{bundle_name} Bundle" 

def filter_collections_template(collection_template):
    
    collection_name = str(collection_template.name)
    collection_name_list = collection_name.split(" ")
    collection_name_list.pop(0)
    collection_type = " ".join(collection_name_list).strip() 
    
    collection_items = get_collection_items(collection_type)
    return f"Collection {collection_type}: { ",".join(collection_items) + '.' }"
    
def filter_heart_templates(heart_template):
    number_of_hearts = str(heart_template.params[0])
    
    return f"{number_of_hearts} heart(s)"

def filter_key_templates(key_template):
    key = str(key_template.params[0].value)
    
    return f"{key}"

def filter_schedule_header_templates(sch_header_template):
    season = str(sch_header_template.params[0].value)
    
    return f"Schedule for {season} season"

def filter_infobox_templates(infobox_templates):
    params = infobox_templates.params
    message = 'Quick Information:{\n'

    for parameter in params: 
        key = str(parameter.name).strip()
        value = str(parameter.value).strip()
        
        message = message + f"{key}={value}\n"
    
    message = message + '}' 

    return message

def sanitizeTemplates(text:str):
    parser = mwparserfromhell.parse(text)

    templates = parser.filter_templates()
    replacement = ''

    for template in templates:
        
        template_name = sanitizeTemplateName( str(template.name) )
        print(f"Sanitizing {template_name} template")
        
        match(template_name):
            
            case 'bundle'|'Bundle':
                replacement = filter_bundle_templates(template)
            
            case 'Choice' | 'choice':
                replacement = filterChoiceTemplates(template)  
            
            case 'Collections Artifact'|'Collections Artifacts'|'Collections Cooking'|'Collections Fish'| 'Collections Item Shipped'|'Collection Minerals':
                replacement = filter_collections_template(template)
                    
            case 'CookingChannel':
                replacement = filter_CookingChannel_templates(template)
                
            case 'Duration'| 'duration':
                replacement = filter_duration_templates(template)
            
            case 'Energy' | 'energy':
                replacement = filter_energy_templates(template)
            
            case 'GiftsByItem':
                replacement = filter_giftsByItem_template(template)
            
            case 'Health' | 'health':
                replacement = filter_health_templates(template)
            
            case 'hearts' | 'Hearts':
                replacement = filter_heart_templates(template)
            
            case 'heart event':
                replacement = filter_heart_event_template(template)
            
            case 'History' | 'history':
                replacement = filter_history_templates(template)
            
            case 'Infobox' | 'infobox' | 'Infobox animal' | 'Infobox artifact' | 'Infobox building' | 'Infobox clothing'| 'Infobox cooking' | 'Infobox fish' | 'Infobox fruit tree' | 'Infobox furniture' | 'Infobox location' | 'Infobox mineral' | 'Infobox mousehat'| 'Infobox seed' | 'Infobox tool'| 'Infobox tree' | 'Infobox villager' | 'Infobox weapon':
                replacement = filter_infobox_templates(template)
            
            case 'Key' | 'key':
                replacement = filter_key_templates(template)
            
            case 'Name' | 'name':
                replacement = filter_name_template(template)    
            
            case 'NPC':
                replacement = filter_npc_template(template)      
                
            case 'Price' | 'price':
                replacement = filter_price_template(template)
            
            case 'Probability'|'probability':
                replacement = filter_probability_template(template)
            
            case 'quality'|'Quality':
                replacement = filter_quality_template(template)
                
            case 'Quote' | 'quote'| 'Squote':
                replacement = filter_quote_template(template)
            
            case 'Recipe'| 'recipe':
                # Recipe template's first param is the value needed
                recipe = str(template.params[0].value)
                replacement = recipe 
            
            case 'ScheduleHeader' | 'scheduleHeader':
                replacement = filter_schedule_header_templates(template)
                
            case 'Season' | 'season':
                replacement = filter_season_template(template)
                print(replacement)
                
            case 'Weather inline':
                replacement = filter_weather_template(template)
            
            case 'collapse':
                replacement = filter_collapse_template(template)
            
            case 'Basics-top'|'calendar'|'Categoryheader'| 'clear'| 'for' | 'GiftHeader' | 'giftHeader' | 'InfoboxSEO' | 'KegProductivity-top' | 'Main article' | 'MainLinks' | 'Mainmenu' | 'Mainonly' | 'map' | 'Map' | 'PreservesJarProductivity-top' :
                replacement = remove_template(template)
            
            case _ :
                print(f"Not replacing {template_name} template")
                
                
        text = text.replace(str(template), replacement)

    return text 


if __name__ == "__main__":
    path = os.getcwd() + '/info/'

    files = os.listdir(path)

    # logger = logging.getLogger(__name__)
    # logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    #                     handlers= [
    #                         logging.FileHandler("template.log"),
    #                         logging.StreamHandler(sys.stdout)
    #                     ])

    for file in files:
        filePath = 'info/' + file
        outputFilePath = 'outputs/' + file
        with open(filePath,"r") as file:
            text = file.read()
            print(f"Processing {filePath}, length={len(text)=}")
            replacementText = sanitizeTemplates(text)
            
                
        with open(outputFilePath,'w') as outputFile:
            outputFile.write(replacementText)
            print(f"output file generated' {outputFilePath}  {len(replacementText)=}")        
            print('----------------------------------------------------------------------------')  
       
    


# replacementText = ''
# with open("info/Armored Bug.txt","r") as file:
#     text = file.read()
#      # print(text)
#     replacementText =  sanitizeTemplates(text)

# with open('outputs/Peepee.txt','w') as outputFile:
#     outputFile.write(replacementText)
#     print('output file generated',  f'{len(replacementText)=}')     
    
     

