
from pypaec.pypaec import parse_incipit
import csv


with open('incipits.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

n_tot_incipits = len(data)-1
n_incipits = range(100000,200000)

d_incipits = []
d_indexes = [2,3,4,6]
d_symbols = ['%','@','$',' ']
    
for i in n_incipits:

  d_data = data[i+1]
  d_selected = [d_data[index] for index in d_indexes]

  d_symbols_temp = d_symbols.copy()  

  if(d_selected[0]==''): d_symbols_temp[0] = ''
  if(d_selected[1]==''): d_symbols_temp[1] = ''
  if(d_selected[2]==''): d_symbols_temp[2] = ''
  if(d_selected[3]==''): d_symbols_temp[3] = ''

  d_dict = dict(zip(d_symbols_temp,d_selected))
  d_string = ''
  for k,v in d_dict.items():
    d_string = d_string + str(k) + str(v)
  
  d_incipits.append(d_string)
    


list_of_incipits: list = d_incipits
to_check: list = []
num_incipits: int = len(list_of_incipits)
incipits_to_check: list = []

for i in range(len(list_of_incipits)):
    
    incipit = list_of_incipits[i]

    parse_results: dict = parse_incipit(incipit)
    is_valid: bool = parse_results.get("valid")

    if not is_valid:
        syntax_errors: dict = parse_results.get("syntax_errors")

        num_new_errors = len(syntax_errors) - len(to_check)
        for j in range(num_new_errors):
          to_check.append({
              "source": data[i+1][0],
              "work": data[i+1][1],
              "clef": data[i+1][2],
              "timesig": data[i+1][3],
              "keysig": data[i+1][4],
              "mode": data[i+1][5],
              "notes": data[i+1][6],
              "incipit": incipit,
              "num. of errors": num_new_errors,
              "segment": "\n".join([serr.get("location") for serr in [syntax_errors[-(num_new_errors-j)]]]),
              "message": "\n".join([smsg.get("msg") for smsg in [syntax_errors[-(num_new_errors-j)]]])
          })

        incipits_to_check.append(incipit)
        
        
        
with open("incipit_report.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["source","work","clef","timesig","keysig","mode","notes","incipit", "num. of errors", "segment", "message"])
    writer.writeheader()
    writer.writerows(to_check)

num_errors = len(incipits_to_check)

print(f"Number of incipits checked: {num_incipits}")
print(f"Number of incipits to check: {num_errors}")
print(f"Error rate: {(num_errors / num_incipits) * 100}%")



