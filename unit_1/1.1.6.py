import collections, math

# Using a dictionary with a list as values [pop2010, pop2100, total_land, pop_growth, pop_density]
populations = collections.defaultdict(list)

with open('lecz-urban-rural-population-land-area-estimates-v2-csv/lecz-urban-rural-population-land-area-estimates_continent-90m.csv', 'rU') as input_file:
    header = next(input_file).split(',')
    
    for line in input_file:
        line = line.rstrip().split(',')

        if line[1] == 'Total National Population':
            try: # If array element already exist
               populations[line[0]][0] += int(line[5])
               populations[line[0]][1] += int(line[6])
               populations[line[0]][2] += int(line[7])
            except: # else append new population variable
               populations[line[0]].append(int(line[5]))
               populations[line[0]].append(int(line[6]))
               populations[line[0]].append(int(line[7]))



with open('national_population.csv', 'w') as output_file:
    output_file.write('continent,2010_population\n')
    
    for k, v in populations.iteritems():
       output_file.write(k + ',' + str(v[0]) + '\n')
      
# Q1 Calculate the rate of change
for continent in populations.keys():
    con_2010 = populations.get(continent)[0]
    con_2100 = populations.get(continent)[1]
    
    populations[continent].append((((con_2100 - con_2010)) / float(con_2010)) * 100)
    populations[continent].append((con_2010) / float(populations.get(continent)[2]))

print "=" * 100
print "#" * 100
print "=" * 100
print "\n" 

# Q1.
answer = max(populations.iterkeys(), key = (lambda key : populations[key][3]))
print "The continent estimated to grow the most in the next 90 years is:  {} by approximately {}%".format(answer, math.floor(populations.get(answer)[3]))


print "=" * 100
print "#" * 100
print "=" * 100
print "\n" 

# Q2. 
print "The most densely populated continent in 2010 was:  {}".format(max(populations.iterkeys(), key = (lambda key : populations[key][4])))