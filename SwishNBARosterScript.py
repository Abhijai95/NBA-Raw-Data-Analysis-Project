import xlrd
import mysql.connector
import re
# Abhijai Singh 6/4/18
# Open database connection (if database is not created don't give dbname)

db = mysql.connector.connect(host="localhost" , user="root" , passwd="******", db="NBAData") #Better error handling needed when db is not created.
# prepare a cursor object using cursor() method

cursor = db.cursor()

# For creating create db

cursor.execute("SET sql_notes = 0; ")

# Create database here

cursor.execute("create database IF NOT EXISTS NBAData")

# Create table

cursor.execute("SET sql_notes = 0; ")

#Establish dimensions and types of table content.

cursor.execute("create table IF NOT EXISTS pbp_players_on_court (play_id char(6),pl0 char(10),pl1 int(10),pl2 int(10),pl3 int(10),pl4 int(10),pl5 int(10),pl6 int(10),pl7 int(10), pl8 int(10), pl9 int(10));")

cursor.execute("SET sql_notes = 1; ")

#with_index + replace_all : Function definitions of Swap, using 3 arguments
 
def with_index(seq):
    for i in range(len(seq)):
        yield i, seq[i]
		
def replace_all(seq, obj, replacement):
    for j, elem in with_index(seq):
        if elem == obj:
            seq[j] = replacement
		
#Accessing .xlsx files (pbp,rosters,pbp_players)
Rosters1 = xlrd.open_workbook("rosters.xlsx")
Pbp_players2 = xlrd.open_workbook("pbp_players.xlsx")
Pbp3 = xlrd.open_workbook("pbp.xlsx")
#Establishing worksheets within .xlsx files
worksheet1 = Rosters1.sheet_by_name("Sheet1")
worksheet2 = Pbp_players2.sheet_by_name("Sheet1")
worksheet3 = Pbp3.sheet_by_name("Sheet1")
num_rows1 = worksheet1.nrows #Number of Rows
num_cols1 = worksheet1.ncols #Number of Columns
num_rows2 = worksheet2.nrows #Number of Rows
num_cols2 = worksheet2.ncols #Number of Columns
num_rows3 = worksheet3.nrows #Number of Rows
num_cols3 = worksheet3.ncols #Number of Columns

total_rows = worksheet3.nrows #Total number of rows
total_rows = 80 #Limiting field to 80 for testing purposes
total_cols = worksheet3.ncols
#List declarations
table = list() 
record = list()
player_oncourt = list() 
oncourt_table = list()

print ("NBA On-Court Player Data Script")
print ("Warriors @ Celtics (88-92) Game ID 1947160")
print(" Rockets  @ Suns   (142-116)Game ID 1947312")
gameID = int(input('Which game would you like to access? (Enter Game Number)'))
#Read user input

#For loop encompassing majority of script that iterates x by 1 to access data across .xlsx files to retrieve pertinent data.
z = 1	
for x in range(total_rows):	
			
	if gameID == worksheet2.cell(x,2).value: #If statement to prevent script from accessing NBA game data not requested by user.
		
		if worksheet2.cell(x,23).value == 0: #Append player_oncourt list for starting lineup situations (play_eventid == 0)
			
			player_oncourt.append(worksheet2.cell(x,12).value) 
			
					
		if worksheet2.cell(x,23).value == 10 and worksheet2.cell(x,8).value != 2: #If/and statement that runs when condition (play_id == 10 && play_sequence(x+1) !=2 to prevent an overwrite
			
			replace_all(player_oncourt, worksheet2.cell((x+1),12).value, worksheet2.cell(x,12).value) #Calls the replace_all function with 3 arguments.
			
			print(player_oncourt) #Print new list of players to cmd line		
						
		else: #In the event no changes to players on court is present.
		
			print(player_oncourt)
			
	#For loop tasked with maintaining play_id and exporting output of data to MySQL
	for y in range(z):
		record.append(worksheet2.cell(x+1,7).value)
		#table.append(record) Testing		
		#print(len(record[x]),record[x]) Testing
		#Workaround using substitution of copy of record and .pop of data due to "out of range" errors when trying to access record list.
		Gameid=list(record)
		g=[None]*1		
		count =0 
		m=len(Gameid)
		#.Pop all values in Gameid until empty
		while (count < m ):
			g[count]=Gameid.pop(0)
			print(g[count])
			count = count + 1			
				
		#print(len(player_oncourt)) Testing
		
		#Workaround using substitution of copy of player_oncourt and .pop of data due to "out of range" errors when trying to access player_oncourt list.
		Oncourt_backup=list(player_oncourt)
		v=[None]*10
		count=0
		m=len(Oncourt_backup)
		#.Pop all values in Gameid until empty
		while (count < m):
			v[count]=Oncourt_backup.pop(0)
			#print(v[count])
			count = count +1
			
		#print (Oncourt_backup) Testing
		#SQL insert
		#Inserting play_id and 10 player_id values to MySQL table in database NBAdata		
		insert_stmt = ("INSERT INTO pbp_players_on_court(play_id, pl0, pl1, pl2, pl3, pl4, pl5, pl6, pl7, pl8, pl9) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
		data = (g[0], v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9])
		cursor.execute(insert_stmt, data)		
		db.commit()

										
	
	record = []
	x+= 1 


db.close()


