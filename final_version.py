from pymarc import MARCReader

def get_lc_class_from_call_number(call_number):
	lc_class = ""
	for char in call_number:
		if char.isalpha():
			lc_class = lc_class + char
		elif char == '.':
			break
		else:
			continue
	return lc_class

def get_simple_page_number_from_marc_300(marc_300):
	simple_page_number = ""
	for char in marc_300:
		if char.isnumeric():
			simple_page_number = simple_page_number + char
		elif char == '[':
			break
		else:
			continue
	return simple_page_number

def get_numeric_year_from_marc_26Xc(marc_26Xc):
	numeric_year = ""
	for char in marc_26Xc:
		if char.isnumeric():
			numeric_year = numeric_year + char
		else:
			continue
	return numeric_year

def remove_final_comma_from_publisher(marc_26Xb):
	if marc_26Xb[-1:] == ',':
		return marc_26Xb[:-1]
	else:
		return marc_26Xb

def remove_final_comma_from_author(marc_100a):
	if marc_100a[-1:] == ',':
		return marc_100a[:-1]
	else:
		return marc_100a


def display_found_record():
	print("   Record Number: " + record.get('record_number',""))
	print("      Main Title: " + record.get('record_title',""))
	print("        Subtitle: " + record.get('record_subtitle',""))
	print("          Author: " + record.get('record_author',""))
	print("            ISBN: " + record.get('record_isbn',""))
	print("            LCCN: " + record.get('record_lccn',""))
	print("     OCLC number: " + record.get('record_oclc_number',""))
	print("        LC Class: " + record.get('record_lc_class',""))
	print("       Publisher: " + record.get('record_publisher',""))
	print("Publication Date: " + record.get('record_publication_date',""))
	print(" Number of pages: " + record.get('record_number_of_pages',""))
	print()




print("Loading...Please wait.")
print("Source data may have a few problems. Warnings will appear below before the program runs.")

infile = open('data.mrc', 'rb')
reader = MARCReader(infile)

record_list = list()
for record in reader:
	entry_dict = dict()
	# Record Number
	record_number = str(record['001'])[6:]
	entry_dict['record_number'] = record_number
	if record_number == "None":
		entry_dict.pop('record_number')	

	# Title
	record_title = str(record['245']['a'])
	entry_dict['record_title'] = record_title
	if record_title == "None":
		entry_dict.pop('record_title')


	# Subtitle
	record_subtitle = str(record['245']['b'])
	entry_dict['record_subtitle'] = record_subtitle
	if record_subtitle == "None":
		entry_dict.pop('record_subtitle')


	# Author:
	try:
		record_author = str(remove_final_comma_from_author(record['100']['a']))
		entry_dict['record_author'] = record_author
		if record_author == "None":
			entry_dict.pop('record_author')
	except TypeError:
		pass


	# ISBN:
	record_isbn = str(record.isbn())
	entry_dict['record_isbn'] = record_isbn
	if record_isbn == "None":
		entry_dict.pop('record_isbn')

	# LCCN:
	try:
		record_lccn = str(record['010']['a'].lstrip())
		entry_dict['record_lccn'] = record_lccn
		if record_lccn == "None":
			entry_dict.pop('record_lccn')
	except (TypeError, AttributeError):
		pass

	# OCLC Number:
	try:
		oclc_number = str(record['035']['a'])
		record_oclc_number = str(oclc_number[7:])
		entry_dict['record_oclc_number'] = record_oclc_number
		if record_oclc_number == "None":
			entry_dict.pop('record_oclc_number')
	except TypeError:
		entry_dict['record_oclc_number'] = 'to_be_popped'
		entry_dict.pop('record_oclc_number')


	# LC Class
	try:
		record_lc_class = get_lc_class_from_call_number(record['050']['a'])
		entry_dict['record_lc_class'] = record_lc_class
		if record_lc_class == "None":
			entry_dict.pop('record_lc_class')
	except TypeError:
		pass

	# Publisher
	try:
		record_publisher = remove_final_comma_from_publisher(record.publisher())
		entry_dict['record_publisher'] = record_publisher
		if record_publisher == "None":
			entry_dict.pop('record_publisher')
	except TypeError:
		pass

	# Publication Date
	try:
		record_publication_date = str(get_numeric_year_from_marc_26Xc(record.pubyear()))
		entry_dict['record_publication_date'] = record_publication_date
		if record_publication_date == "None":
			entry_dict.pop('record_publication_date')
	except TypeError:
		pass

	# Number of pages
	try:
		record_number_of_pages = str(get_simple_page_number_from_marc_300(record['300']['a']))
		if len(record_number_of_pages) == 0:
			record_number_of_pages = "to_be_popped"
		entry_dict['record_number_of_pages'] = record_number_of_pages
		if entry_dict['record_number_of_pages'] == "to_be_popped":
			entry_dict.pop("record_number_of_pages")
	except:
		pass


	record_list.append(entry_dict)


infile.close()




# Search program starts here:

print("\n\n\n\n\n\n\n\n")
print("This is a program for searching MARC records stored in a single ")
print("MARC file saved with a .mrc file extension.")
print()
print("The MARC file to be searched should be named 'data.mrc' and ")
print("should be saved in the same directory that this py file is saved in.")
print()
print("The file currently saved as 'data.mrc' contains " + str(len(record_list)) + " records.")
print()


valid_search_codes_list = ["rn", "ti", "st", "au", "bn", "ln", "on", "lc", "pu", "dt"]

search_code_record_key_dictionary = {
	"rn" : "record_number", 
	"ti" : "record_title", 
	"st" : "record_subtitle",
	"au" : "record_author",
	"bn" : "record_isbn",
	"ln" : "record_lccn",
	"on" : "record_oclc_number",
	"lc" : "record_lc_class",
	"pu" : "record_publisher",
	"dt" : "record_publication_date"
	}





# Start While loop here.
while True:
	print("Key in one of the following codes to search in that field:")
	print("rn - Record Number")
	print("ti - Main Title")
	print("st - Subtitle")
	print("au - Author")
	print("bn - ISBN")
	print("ln - LCCN")
	print("on - OCLC Number")
	print("lc - LC class")
	print("pu - Publisher")
	print("dt - Publication Date")




	print()
	while True:
		selected_search_code = input("Please enter a search code: ")
		print()
		selected_search_code = selected_search_code.lower()
		if selected_search_code in valid_search_codes_list:
			print("You have selected the search code " + selected_search_code + ".")
			print()
			break
		else:
			print("You need to enter a valid search code.")

	selected_search_key = search_code_record_key_dictionary[selected_search_code]
	search_string = str(input("Please enter a search string: "))
	search_string = search_string.lower()
	print()



	records_found_count = 0
	for record in record_list:
		if record.get(selected_search_key,"missing") != 'missing' and search_string in record[selected_search_key].lower():
			display_found_record()
			records_found_count += 1


	if records_found_count == 0:
		record_sing_plur = 'records'
	elif records_found_count == 1:
		record_sing_plur = 'record'
	else:
		record_sing_plur = 'records'

	print("\nThe search returned " + str(records_found_count) + " " + record_sing_plur + ".")
	print()

	while True:
		yes_or_no = input("Perform another search? Key in 'y' for yes or 'n' for no: ")
		yes_or_no = yes_or_no.lower()
		print()
		if yes_or_no in ['y','n']:
			break
		else:
			print("You need to key in either 'y' for yes or 'n' for no!")

	if yes_or_no == 'n':
		print("Goodbye!\n\n\n\n")
		exit()





