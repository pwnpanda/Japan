def findMidpoint(user, partner, con):
	#find loc user
	uLat, uLon = getLocUser(user, con)
	#find loc partner
	pLat, pLon = getLocUser(partner, con)
	#calc mean
	print(uLat, uLon, pLat, pLon)
	#TODO error here! Float and Unicode incompatible - tuple?
	meanLat = ((uLat + pLat) / 2)
	meanLon = ((uLon + pLon) / 2)
	#return mean
	return meanLon, meanLat

def insertPair(user, partner, db):
	con = db.cursor()
	midLon, midLat = findMidpoint(user, partner, con)
	con.execute("INSERT INTO pairs (name1, name2, mpLon, mpLat) VALUES (?, ?, ?, ?)", (user,partner, midLon, midLat) )
	db.commit()
#	DEV	
#	con.execute("SELECT * from pairs")
#	for x in con:
#		print(x)

def insertUser(user, lon, lat, db):
	con = db.cursor()
	con.execute("INSERT INTO users (name, locLon, locLat) VALUES (?, ?, ?)", (user,lon,lat) )
	db.commit()

def deleteUser(user, db):
	con = db.cursor()
	con.execute("DELETE FROM users WHERE name=?", (user,))
	db.commit()

def updateMidpoint(user, partner, db):
	con = db.cursor()
	midLon, midLat = findMidpoint(user, partner, con)
	con.execute("UPDATE pairs SET mpLon=?, mplat=? WHERE id=?",(midLon,midLat,(getPairId(user, con)[0])))
	db.commit()

def updateLoc(user, lon, lat, db):
	con = db.cursor()
	con.execute("UPDATE users SET locLon=?, locLat=? WHERE name=?", (lon,lat,user) )
	db.commit()

def updateUsers(user, partner, db):
	con = db.cursor()
	num = getPairId(user, con)[0]
#	DEV
#	print("PairID")
#	print(num)
	con.execute("UPDATE users SET pair=? WHERE name=?", (num,user))
	con.execute("UPDATE users SET pair=? WHERE name=?", (num,partner))
	db.commit()

def getMidLoc(user, con):
	return con.execute("SELECT mpLon, mpLat FROM pairs WHERE name1=? OR name2=?", (user, user)).fetchone()

def getPairId(user, con):
	return con.execute("SELECT id FROM pairs WHERE name1=? OR name2=?", (user,user)).fetchone()

def getLocUser(user, con):
	return con.execute("SELECT locLat, locLon FROM users WHERE name=?", (user,)).fetchone()

def getPair(user, con):
	return con.execute("SELECT pair FROM users WHERE name=? and pair IS NOT NULL", (user,)).fetchone()

def getPartner(user, con):
	return con.execute("SELECT name FROM users WHERE name NOT LIKE ? and pair=?", (user,getPair(user, con)[0])).fetchone()

def getUser(user, con):
	return con.execute("SELECT name FROM users WHERE name=?", (user,)).fetchone()

#TODO handle session
#	def getTimeDc(user):
#		return con.execute("SELECT timeDc FROM users WHERE name=?", (user,)).fetchone()
#	def setTimeDc(user, time):
#		
#	def removeDBEntries(user):
#		otherUser = getPartner(user)
#		if otherUser:
#			pairNum = getPair(user)
#			con.execute("UPDATE users SET pair=NULL WHERE name=?", (otherUser[0],))
#			deleteUser(user)
#			con.execute("DELETE FROM pairs WHERE id=?", (pairNum,))
#		#db.commit()
#	DEV
#		#con.execute("SELECT * FROM users")
#		#for x in con:
#		#	print(x)
#		else:
#			print("WTFFF")