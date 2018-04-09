#!usr/bin/pyhton
#
# This script will clear data
import sys

file_list=sys.argv[1:]

for file_name in file_list:
    new_file_name='./bitcointxjson/'+file_name+'.json'
    with open(file_name) as f:
        new = open(new_file_name,"w")
        num_curly=0

        for line in f:
            line=line.replace(' ','')
            if '{' in line:
                num_curly+=1
                new.write(line.replace('\n',''))
            elif '}' in line:
                num_curly-=1
                if num_curly==0:
                    new.write(line)

                else:
                     new.write(line.replace('\n',''))
            else:
                 new.write(line.replace('\n',''))
        new.close()
      
