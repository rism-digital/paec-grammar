
from pypaec.pypaec import parse_incipit
import csv
import numpy as np


with open('incipit_report.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)



error_messages = []
for i in range(1,len(data)):
    message = data[i][10]
    s1 = message.split(': line 1' )[0]
    error_messages.append(s1)

error_messages_unique = list(set(error_messages))

print(len(error_messages))
print(len(error_messages_unique))

dict_error_messages = {i:error_messages.count(i) for i in error_messages_unique}  
dict_error_messages_sorted_ = {k: v for k, v in sorted(dict_error_messages.items(), key=lambda item: item[1])}
dict_error_messages_sorted = dict(reversed(list(dict_error_messages_sorted_.items())))


with open('message_analysis.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in dict_error_messages_sorted.items():
       writer.writerow([key, value])


#error_messages = []
#for i in range(1,len(data)):
#  error_messages.append(data[i][10])
##error_messages_unique = list(set(error_messages))
##error_messages = error_messages_unique.copy()
#
#error_mis_input = []
#error_via_alt = []
#error_ext_input = []
#error_missing = []
#error_else = []
#for i in range(len(error_messages)):
#    if('mismatched input' in error_messages[i]):
#      error_mis_input.append( error_messages[i] )
#    elif('no viable alternative' in error_messages[i]):
#      error_via_alt.append( error_messages[i] )
#    elif('extraneous input' in error_messages[i]):
#      error_ext_input.append( error_messages[i] )
#    elif('missing' in error_messages[i]):
#      error_missing.append( error_messages[i] )      
#    else:
#      error_else.append( error_messages[i] )
#
#print(len(error_messages))
#print(len(error_mis_input))
#print(len(error_via_alt))
#print(len(error_ext_input))
#print(len(error_missing))
#print(len(error_else))
#
#
########      
### mismatched input
########
#
#
#analyse_mis_input = False
#if(analyse_mis_input):
#    
#  error_mis_input_symbols = []
#  
#  for i in range(len(error_mis_input)):     
#    s1 = error_mis_input[i].split('mismatched input ')[1]
#    s2 = s1.split(' expecting')[0]  
#    error_mis_input_symbols.append(s2)
#  
#  error_mis_input_symbols_unique = list(set(error_mis_input_symbols))
#  
#  print(error_mis_input_symbols_unique)
#
#
#
#analyse_ext_input = False
#if(analyse_ext_input):
#  
#  ext_input_symbols = []
#  for i in range(len(error_ext_input)):
#    s1 = error_ext_input[i].split('extraneous input ')[1]
#    s2 = s1.split(' expecting')[0]
#    ext_input_symbols.append(s2)
#    
#  ext_input_symbols_unique = list(set(ext_input_symbols))
#  dict_ext_input = {i:ext_input_symbols.count(i) for i in ext_input_symbols_unique}  
#  print(dict_ext_input)






