from draftkings_class import DraftKings
import mysql.connector 




#cnx = mysql.connector.connect(user = "root",
#                              host = "127.0.0.1",
#                              database = "DraftKingsStats",
 #                             password = "Comrad_38")
#cursor = cnx.cursor(buffered = True)




dk = DraftKings(league = "NBA")
#print(dk.run_all_games())
myList = dk.get_playerOdds(dk.test_url)



#halfTimeScore = dk.get_gameScore()
#dk.store_as_json(myList)
print(myList)
#print(dk.get_event_ids())

#print(halfTimeScore)
#dk.compare_odds('NbaHalfTime.json', 'NBA.json')

#inserts = dk.get_playerOdds(dk.test_url)
#statement = "INSET INTO test (playerName, odds) VALUES(%s, %s)"
#cursor.execute(statement, inserts)
#cnx.commit()