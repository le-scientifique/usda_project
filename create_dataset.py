import re
import pandas as pd
#import docx2txt

#text = docx2txt.process("Txt file sample.docx")

data_dict_list = []
'''
with open("ssdm1_splitaa.txt","r") as ip, open("clean_data.csv","w") as op:
	# print len(ip.readlines())
	op.write("Social_Security_no_Last_name_Suffix,First_name,MI,DoD_DoB\n")
	for line in ip.readlines():
		# print line
		if line.strip() != "":
			cells = re.split("\s+",line.strip())
			data_dict = {}
			try:
				if len(cells) == 3:
					data_dict["Social_Security_no_Last_name_Suffix"] = cells[0]
					data_dict["First_name"] = cells[1]
					data_dict["MI"] = ""
					data_dict["DoD_DoB"] = cells[2]
				elif len(cells) == 4:
					data_dict["Social_Security_no_Last_name_Suffix"] = cells[0]
					data_dict["First_name"] = cells[1]
					data_dict["MI"] = cells[2]
					data_dict["DoD_DoB"] = cells[3]
				elif len(cells) == 5:
					data_dict["Social_Security_no_Last_name_Suffix"] = cells[0] + "_" + cells[1]
					data_dict["First_name"] = cells[2]
					data_dict["MI"] = cells[3]
					data_dict["DoD_DoB"] = cells[4]
				# else:
					#print "length not in 3,4,5 ",cells
				if "Social_Security_no_Last_name_Suffix" in data_dict.keys():
					data_dict_list.append(data_dict)
					op.write(",".join(data_dict.values())+"\n")

			except:
				pass
				#print "exception ",cells
				#traceback.print_exc()

print "length of data_dict %d" %len(data_dict_list)			
'''



df_raw = pd.read_csv('clean_data.csv')
# df_raw = pd.DataFrame(data_dict_list)

#Splits Social_Security_no_Last_name into Cols - SSN and Last_Name
#(?P<SSN>\d+) - all digits match, column name - SSN
#(?P<Last_Name>[A-Z]+) - all caps match, column name - Last_Name
df_ssn_lst = df_raw['Social_Security_no_Last_name_Suffix'].str.extract('(?P<SSN>\d+)(?P<Last_Name>[A-Z_]+)')

#Splits DoD_DoB into Cols - V, DoD and DoB
#(?P<V>V?) - Look for beginning V in the DoD_DoB value (What does V even mean?), column name - V
#(?P<DoD>\d{8}) - first 8 digits, column name - DoD
#(?P<DoB>\d{8}) - next 8 digits, column name - DoB
df_dod_dob = df_raw['DoD_DoB'].str.extract('(?P<V>V?)(?P<DoD>\d{8})(?P<DoB>\d{8})')

#print df_ssn_lst

#print df_dod_dob

df = pd.concat([df_raw,df_ssn_lst,df_dod_dob],axis = 1)

#print df

#writer = pd.ExcelWriter('output.xlsx')
df.to_csv("clean_data_modified.csv", sep='\t',index=False,columns=["SSN","Last_Name","MI","First_name","V","DoD","DoB"],header=["SSN","Last_Name","MI","First_name","V","DoD","DoB"])
# df.to_excel(writer,'clean_data',index=False,columns=["SSN","Last_Name","MI","First_name","V","DoD","DoB"],header=["SSN","Last_Name","MI","First_name","V","DoD","DoB"])
# df.to_excel(writer,'raw_data',index=False,columns=["Social_Security_no_Last_name","First_name","MI","DoD_DoB"],header=["Social_Security_no_Last_name","First_name","MI","DoD_DoB"])
# writer.save()
