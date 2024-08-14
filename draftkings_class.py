import asyncio
import websockets
import requests
import json
from traceback import print_exc
from draftkings_stream import stream

id_dict = {"NHL": "42133", "NFL": "88808",
           "NBA": "42648", "England - Premier League": "40253"}


class DraftKings:
    def __init__(self, league="NHL"):
        """
        Initializes a class object
        Include more leagues simply by adding the league with its ID to id_dict above

        :league str: Name of the league, NHL by default
        """
        self.league = league
        self.pregame_url = f"https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/{id_dict[self.league]}?format=json"
        self.uri = "wss://ws-draftkingseu.pusher.com/app/490c3809b82ef97880f2?protocol=7&client=js&version=7.3.0&flash=false"
        self.player_url = "https://gaming.draftkings.com/sportsbook/configuration/widgets/us-nh-sb/home/v1/widgets.json"
        self.test_url = "https://sportsbook-nash-usmi.draftkings.com/sites/US-MI-SB/api/v3/event/30091760?format=json"

    def store_odds(self, game_file, appendable):
        with open(game_file, 'r') as g:
            game_data = json.load(g)
            game_data.append(appendable)
            json.dump(game_data, g)
    def run_all_games(self):
        store = self.get_event_ids().values()
        myList = []
        #for d in store:
            #print("https://sportsbook-nash-usmi.draftkings.com/sites/US-MI-SB/api/v3/event/",d,"?format=json")
        for d in store:
            
            myList.append(self.get_playerOdds(("https://sportsbook-nash-usmi.draftkings.com/sites/US-MI-SB/api/v3/event/" + d + "?format=json")))
        return myList   
        
    def get_event_ids(self) -> dict:
        """
        Finds all the games & their event_ids for the given league

        :rtype: dict
        """
        event_ids = {}
        response = requests.get(self.pregame_url).json()
        for event in response['eventGroup']['events']:
            event_ids[event['name']] = event['eventId']
        return event_ids

 

    
  
    def get_playerOdds(self, url) -> list:
    # Dict that will contain player name: player points
        valDict = {}

    # Requests the content from DK's API, loops through the different categories & collects all the material deemed relevant
        response = requests.get(url).json()
        categories = response['eventCategories']

    # Loop through each category
        for category in categories:
            if category['categoryId'] == 1215:  # If the category is "Player Points"
                offers = category['componentizedOffers']
            
            # Loop through each offer
                for offer in offers:
                    offer_details = offer['offers']

                # Loop through each offer detail
                    for detail in offer_details:
                        for d in detail: 

                        # Get over under points for each player
                            outcomes = d['outcomes']
                            outcome = outcomes[0]

                            # Get player's name
                            player_name = outcome['participant']
                            
                            # Get over or under points
                            player_points = {outcome['label']: outcome.get('line', 'none')}

                            # If player already exists in dictionary, update their points
                            if player_points != 'none':
                                if player_name not in valDict:
                                    valDict[player_name] = player_points
        valList = []
        for player, stats in valDict.items():
            points = stats['Over']  # Assuming 'Under' is always present in the label
            valList.append([player, points])
        return valList
        # Print player names and points in the desired format
        

    
    




    def get_gameScore(self) -> dict:
    # Request the content from the event API
        response = requests.get(self.test_url).json()

    # Get team names and current scores 
    # Note: 'team1' and 'team2' are nested under 'event' key 
        team1Name = response['event']['team1']['name']
        team1Score = response['event']['eventStatus']['homeTeamScore']
    
        team2Name = response['event']['team2']['name']
        team2Score = response['event']['eventStatus']['awayTeamScore']
    
    # Put information into a dictionary
        valDict = {team1Name: team1Score, team2Name: team2Score}
    
        return valDict
    
   
    
   
    
   
    
    def compare_odds(self, halftime_file, game_file):
    # Load the json files
        with open(halftime_file, 'r') as f:
            halftime_data = json.load(f)

        with open(game_file, 'r') as g:
            game_data = json.load(g)

    # Create a dictionary to store the differences
            differences = {}

    # Iterate over the halftime_data
        for player, odds in halftime_data.items():
        # If the player is also in the game_data
            if player in game_data:
            # Calculate the difference in odds
                difference = game_data[player]['Under'] - odds['Under']
            # Assign the difference to the player in the differences dictionary
                differences[player] = difference

    # Print the differences
        for player, difference in differences.items():
            print(f"The difference in odds for {player} is {difference}")


    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
    def get_pregame_odds(self) -> list:
        """
        Collects the market odds for the main markets [the ones listed at the league's main url] for the league

        E.g. for the NHL, those are Puck Line, Total and Moneyline

        Returns a list with one object for each game

        :rtype: list
        """
        # List that will contain dicts [one for each game]
        games_list = []

        # Requests the content from DK's API, loops through the different games & collects all the material deemed relevant
        response = requests.get(self.pregame_url).json()
        games = response['eventGroup']['offerCategories'][0]['offerSubcategoryDescriptors'][0]['offerSubcategory']['offers']
        for game in games:
            # List that will contain dicts [one for each market]
            market_list = []
            for market in game:
                try:
                    market_name = market['label']
                    if market_name == "Moneyline":
                        home_team = market['outcomes'][1]['label']
                        away_team = market['outcomes'][0]['label']
                    # List that will contain dicts [one for each outcome]
                    outcome_list = []
                    for outcome in market['outcomes']:
                        try:
                            # if there's a line it should be included in the outcome description
                            line = outcome['line']
                            outcome_label = outcome['label'] + " " + str(line)
                        except:
                            outcome_label = outcome['label']
                        outcome_odds = outcome['oddsDecimal']
                        outcome_list.append(
                            {"label": outcome_label, "odds": outcome_odds})
                    market_list.append(
                        {"marketName": market_name, "outcomes": outcome_list})
                except Exception as e:
                    if self.league == "NBA" and "label" in str(e):
                        # odds for NBA totals are not available as early as the other markets for
                        # games a few days away, thus raises a KeyError: 'label'
                        # in this case we simply ignore the error and continue with the next market
                        continue
                    else:
                        # if there was another problem with a specific market, print the error and
                        # continue with the next one...
                        print_exc()
                        print()
                        continue
            games_list.append(
                {"game": f"{home_team} v {away_team}", "markets": market_list})

        return games_list

    def live_odds_stream(self, event_ids=None, markets=None):
        """
        Sets up the live odds stream by calling the async stream function with given parameters

        :param event_id list: If a list of event_ids is specified [else it's None], the stream/listener considers updates
                              only if they're updates for those particular games
        :param markets list: If a list of markets is specified [else markets == None], the stream/listener considers updates
                             only if they're updates for those particular markets
                             Hint: If uncertain about market names, run it for a minute for all markets and collect the correct
                             names of the markets this way
        """
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(stream(uri=self.uri, league_id=id_dict[self.league], event_ids=event_ids, markets=markets))
        else:
            loop.run_until_complete(stream(uri=self.uri, league_id=id_dict[self.league], event_ids=event_ids, markets=markets))
        
        
        
        
        
        

    def store_as_json(self, games_list, file_path: str = None):
        """
        Dumps the scraped content into a JSON-file in the same directory

        :rtype: None, simply creates the file and prints a confirmation
        """
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(games_list, file)
            print(f"Content successfully dumped into '{file_path}'")
        else:
            with open('NBA.json', 'w') as file:
                json.dump(games_list, file)
            print("Content successfully dumped into 'NBA.json'")
            
     
    def store_as_json2(self, games_list, file_path: str = None):
         """
         Dumps the scraped content into a JSON-file in the same directory

         :rtype: None, simply creates the file and prints a confirmation
         """
         if file_path:
             with open(file_path, 'w') as file:
                 json.dump(games_list, file)
             print(f"Content successfully dumped into '{file_path}'")
         else:
             with open('NbaHalfTime.json', 'w') as file:
                 json.dump(games_list, file)
             print("Content successfully dumped into 'NbaHalfTime.json'")
    




    def to_excel(self, games_list):
        """
        ...
        """
        pass
    
  

    def send_email(self, content):
        """
        ...
        """
        pass
