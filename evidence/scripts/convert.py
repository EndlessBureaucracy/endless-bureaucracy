import csv
import os

def read_csv(filename):
    dict = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        labels = reader.next()[1:]
        for row in reader:
            dict[row[0]] = [r for r in row[1:] if r != "NULL"]
        return labels, dict

resources, prices = read_csv('prices.csv')
for i, r in enumerate(resources):
    if " " in r:
        resources[i] = '"' + r + '"'

_, suburbs = read_csv('suburbs.csv')
all_suburbs = [s for lga in suburbs.values() for s in lga]

_, links = read_csv('links.csv')

_, summaries = read_csv('summaries.csv')

_, positions = read_csv('positions.csv')

systems = prices.keys()
default_system = systems[0]

def print_description(planet):
    try:
        for line in summaries[planet][1].split("\n"):
            print "\tdescription `" + line + "`"
    except KeyError:
        print "\tdescription `placeholder`"

def print_landscape(planet, default):
    filename = planet.replace(" ", "_")
    path = 'endless-sky/images/planets/' + filename + '.jpg'
    if os.path.isfile(path):
        print "\tlandscape planets/" + filename
    else:
        print "\tlandscape " + default

current_system = ""
finished_with_systems = False
started_planets = False
description_complete = False
with open('map.txt', 'r') as map_file:
    for line in map_file:
        if not finished_with_systems:
            if line[:6] == "system":
                try:
                    current_system = systems.pop()
                    subs = suburbs[current_system]
                    print 'system "' + current_system + '"'
                except IndexError:
                    finished_with_systems = True
                    #current_system = default_system
                #print line,
            elif line[:6] == "\ttrade":
                for i, resource in enumerate(resources):
                    if line[7:7+len(resource)] == resource:
                        price = prices[current_system][i]
                        print line[:7+len(resource)+1] + str(price)
            elif line[:10] == "\thabitable":
                print line,
                for link in links[current_system]:
                    if " " in link:
                        print '\tlink "' + link + '"'
                    else:
                        print '\tlink ' + link
            elif line[:5] == "\tlink":
                pass
            elif line[:7] == "\tobject":
                try:
                    sub = subs.pop()
                    print '\tobject "' + sub + '"'
                except IndexError:
                    print "\tobject"
            elif line[:8] == "\t\tobject":
                print "\t\tobject"
            elif line[:4] == "\tpos":
                try: 
                    print "\tpos " + \
                            str(positions[current_system][0]) + " " + \
                            str(positions[current_system][1])
                except KeyError:
                    print line,
            else:
                print line,
        else:
            if line[:6] == "planet":
                started_planets = True
        if started_planets:
            if line[:6] == "planet":
                try:
                    current_planet = all_suburbs.pop()
                    description_complete = False
                    print 'planet "' + current_planet + '"'
                except IndexError:
                    break
            elif line[:12] == "\tdescription":
                if not description_complete:
                    description_complete = True
                    print_description(current_planet)
            elif line[:10] == "\tlandscape":
                print_landscape(current_planet, line[11:])
            else:
                print line,


for planet in all_suburbs:
    print 'planet "' + planet + '"'
    print '\tattributes "dirt belt" textiles farming'
    print_landscape(planet, 'land/nasa0')
    print_description(planet)
    print '\tspaceport ` This is a spaceport! Wow.`'
    print '\tshipyard "Basic Ships"'
    print '\toutfitter "Basic Outfits"'
    print '\toutfitter "Ammo South"'
    print '\tsecurity 0.05'
    print '\ttribute 300'
    print '\t\tthreshold 2500'
    print '\t\tfleet "Small Militia" 23'
    print ''
