import collections, math

populations_2010 = collections.defaultdict(int)
populations_2100 = collections.defaultdict(int)
populations_diff = collections.defaultdict(int)
populations_land = collections.defaultdict(int)
populations_density = collections.defaultdict(int)

with open('lecz-urban-rural-population-land-area-estimates-v2-csv/lecz-urban-rural-population-land-area-estimates_continent-90m.csv', 'rU') as input_file:
    header = next(input_file).split(',')
    
    for line in input_file:
        line = line.rstrip().split(',')
        if line[1] == 'Total National Population':
            populations_2010[line[0]] += int(line[5])
            populations_2100[line[0]] += int(line[6])
            populations_land[line[0]] += int(line[7])

            
with open('national_population.csv', 'w') as output_file:
    output_file.write('continent,2010_population\n')
    
    for k, v in populations_2010.iteritems():
       output_file.write(k + ',' + str(v) + '\n')
      
# Q1 Calculate the rate of change
for continent in populations_2010.keys():
    continent_2100 = populations_2100.get(continent)
    continent_2010 = populations_2010.get(continent)
    populations_diff[continent] = (((continent_2100 - continent_2010)) / float(continent_2010)) * 100
    populations_density[continent] = (continent_2010) / float(populations_land.get(continent))

print max(populations_density.iterkeys(), key = (lambda key : populations_density[key]))

print "The continent estimated to grow the most in the next 90 years is:  {}".format(max(populations_diff.iterkeys(), key = (lambda key : populations_diff[key])))


print "=" * 50


# Q2. 