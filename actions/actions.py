# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from datetime import datetime as dt
from typing import Any, Text, Dict, List

import spacy
from pymongo import MongoClient
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymysql
from pymysql import Error
from colorama import init, Fore, Style
from spacy.language import Language

from spacy_language_detection import LanguageDetector

def get_lang_detector(nlp, name):
    return LanguageDetector(seed=42)  # We use the seed 42

nlp_model = spacy.load('en_core_web_sm')
Language.factory("language_detector", func=get_lang_detector)
nlp_model.add_pipe('language_detector', last=True)

#
# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

class ActionShowTime(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"It's {dt.now()}")

        return []

class ActionInformSupportTeams(Action):

    def name(self) -> Text:
        return "action_inform_support_teams"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # info = []
        # with open('ressources/teams.txt', 'r') as file:
        #     for line in file:

        #         team_info = line.strip().split(';')

        #         info.append("\033[1m\033[91m" + team_info[0].strip() + "\033[0m" + " managed by " +"\033[1m\033[91m"+ team_info[1].strip()+ "\033[0m")

        # dispatcher.utter_message(text=f"We have {info[0]}, {info[1]}, {info[2]} and {info[3]} ")

        # return []
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://imadsbsbenali:JEH0cHlnYaP2YpzB@cluster0.lcywgrn.mongodb.net/test?retryWrites=true&w=majority')
        db = client.chatbotEVdb
        collection = db.supportTeams

        # Retrieve all teams and their team leads
        teams = collection.find({}, {'name': 1, 'teamLead': 1})

        # Format and send the response
        info = []
        for team in teams:
            team_name = "" + team['name'].strip() + ""
            team_lead = team['teamLead']['name'].strip()
            info.append(f"**{team_name}** managed by **{team_lead}**\n\n")

        dispatcher.utter_message(text=f"We have {''.join(info)}")
        client.close()
        return []

class ActionInformModuleSupportTeams(Action):

    def name(self) -> Text:
        return "action_inform_module_support_teams"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # team_name = tracker.get_slot('team_name')

        # if team_name:
        #     dispatcher.utter_message(text=f"The modules processed by {team_name}")
        # else:
        #     dispatcher.utter_message(text=f"Nothing")
        # return []
        team_name = None
        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'team_name':
                team_name = entity['value']
                break
        if not team_name:
            dispatcher.utter_message("Sorry, I didn't catch the name of the team. Could you please repeat?")
            return []
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://imadsbsbenali:JEH0cHlnYaP2YpzB@cluster0.lcywgrn.mongodb.net/test?retryWrites=true&w=majority')
        db = client.chatbotEVdb
        collection = db.supportTeams

        # Find the team and retrieve its modules
        team = collection.find_one({'name': team_name})
        if not team:
            dispatcher.utter_message(f"I don't have any information about the {team_name} team. Could you please try another team?")
            return []

        modules = team['modules']

        # Format and send the response
        result = "" + ', '.join([module.strip().upper() for module in modules.split(',')]) + ""
        dispatcher.utter_message(text=f"The modules processed by **{team_name}.upper()** are: **{result}**")
        client.close()
        #return [SlotSet("module_team", result)]
        return [AllSlotsReset()]


class ActionInformTicketType(Action):

    def name(self) -> Text:
        return "action_inform_ticket_type"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # info = []

        # with open('ressources/ticketsTypes.txt', 'r') as file:
        #     for line in file:

        #         ticket_type = line.strip().split(':')
        #         info.append("\033[1m\033[91m" + ticket_type[0].upper() + "\033[0m" + " : " + ticket_type[1])
        client = MongoClient('mongodb+srv://imadsbsbenali:JEH0cHlnYaP2YpzB@cluster0.lcywgrn.mongodb.net/test?retryWrites=true&w=majority')
        db = client.chatbotEVdb

        # retrieve the team names from the 'teamNames' collection
        ticket_type_name = [f"**{ttype['name'].upper()}**" for ttype in db.ticketType.find()]
        ticket_type_desc = [ttype['description'] for ttype in db.ticketType.find()]

        info = [ticket_type_name[i:i+4] for i in range(0, len(ticket_type_name), 4)]
        text = ""
        for i in range(len(info)):
            text += f"We have {len(info[i])} types: \n\n"
            for j in range(len(info[i])):
                text += f"{info[i][j]}: {ticket_type_desc[i*4+j]} \n\n"
            text += "\n\n"

        dispatcher.utter_message(text=f"{text}")



        client.close()
        return []


class ActionCreateTicket(Action):

    def name(self) -> Text:
        return "action_create_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        def getPreviousDate(str):
            previous_date=str.split('_')[0][1:]
            return previous_date

        def updateRefNum(current_date,previous_date,ref_num):
            if(int(current_date)>int(previous_date)):
                ref_num=1
            else:
                ref_num+=1
            return ref_num

        def returnCode(ticket_type):
            if(ticket_type=="incident"):
                code="I"
            elif(ticket_type=="demande de service"):
                code="S"
            else:
                code="C"
            return code
        # ticket_type = tracker.get_slot('ticket_type')
        # if not ticket_type:
        #     dispatcher.utter_message(text=f"I don't know your ticket type repeat again please!!")
        #     return []

        # client = MongoClient('mongodb+srv://imadsbsbenali:JEH0cHlnYaP2YpzB@cluster0.lcywgrn.mongodb.net/test?retryWrites=true&w=majority')
        # db = client.chatbotEVdb
        # tickets_collection = db.tickets

        ticket_reference="I230417_111"
        ticket_type=tracker.get_slot("ticket_type")
        ticket_title=tracker.get_slot("ticket_title")
        ticket_description=tracker.get_slot("ticket_description")
        ticket_emergency=tracker.get_slot("ticket_emergency")
        ticket_impact=tracker.get_slot("ticket_impact")
        ticket_environnement=tracker.get_slot("ticket_environnement")
        ####priority calcul#########
        priority = min(int(ticket_emergency) + int(ticket_impact) - 1, 4)
        ticket_priority = f"P{priority}"
        ####priority calcul#########
        ticket_description_str = ticket_description[:100] + "..." if len(ticket_description) > 100 else ticket_description
        bank_name="bank1"
        # beneficiaire="b1"
        product="Amplitude v11.2"
        # environnement="Production"
        ticket_option=tracker.get_slot("ticket_option")
        #mongodb
        # ticket = {
        #     "reference": ticket_reference,
        #     "type": ticket_type,
        #     "titre": ticket_title,
        #     "description": ticket_description,
        #     "emergency": ticket_emergency,
        #     "impact": ticket_impact,
        #     "priority": ticket_priority,
        #     "product": product,
        #     "bank_name": bank_name,
        #     "option": ticket_option,
        #     "environnement": environnement,
        #     "status":"open",
        #     "creation_date":dt.now(),
        #     "closure_date":none,
        #     "affected":'0',
        #     "agentid":none,
        #     "clientid":"supportTeam"

        # }

        # tickets_collection.insert_one(ticket)

        # client.close()


        # establish a connection to the MySQL database
        try:
            connection = pymysql.connect(
                host='localhost',
                database='helpbot',
                user='root',
                password=''
            )


            cursor = connection.cursor()
            query = "SELECT reference FROM ticket ORDER BY creation_date DESC LIMIT 1;"
            cursor.execute(query)
            result = cursor.fetchone()[0]
            ref_num=result.split('_')[1]
            previous_date=getPreviousDate(result)
            current_date=dt.now().strftime('%y%m%d')

            ref_num=updateRefNum(current_date, previous_date, int(ref_num))
            ref_num_str = '{:04d}'.format(ref_num)
            ticket_reference=returnCode(ticket_type)+current_date+'_'+ref_num_str


            # create a prepared statement for the SQL query
            query = "INSERT INTO ticket (reference, type, title, description, emergency, impact, priority, product, bank_name, option, environnement, status, creation_date, closure_date, affected, agentid, clientid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = connection.cursor()

            # insert the new ticket into the table
            ticket_data = (ticket_reference, ticket_type, ticket_title, ticket_description, ticket_emergency, ticket_impact, ticket_priority, product, bank_name, ticket_option, ticket_environnement, 'open', dt.now(), None, b'\x00', None, None)
            cursor.execute(query, ticket_data)

            # commit the changes to the database
            connection.commit()
            print("New ticket added successfully.")

        except Error as e:
            print("Error while connecting to MySQL:", e)

        finally:
            # close the database connection
            try:
                cursor.close()
                connection.close()
                print("MySQL connection closed.")
            except Error as e:
                print("Error while closing MySQL connection:", e)

        created_suc="has been  created successfully !"
        dispatcher.utter_message(text=f"Your Ticket {ticket_type} under {ticket_reference} : \n\n -*Title*: **{ticket_title}** \n\n -*Description*: **{ticket_description_str}** \n\n -*Emergency*: **{ticket_emergency}** \n\n -*Impact*: **{ticket_impact}** \n\n -*Priority*: **{ticket_priority}** \n\n -*Product*: **{product}** \n\n -*Client*: **{bank_name}** \n\n -*Beneficiaire*:  \n\n -*Product/Option*: **{product}/{ticket_option}** \n\n -*Version*:  \n\n -*Environnement*: **{ticket_environnement}** \n\n")
        dispatcher.utter_message(text=f" **{created_suc}** \n\n")
        dispatcher.utter_message(text=f"Your ticket's reference is **{ticket_reference}** \n\n")

        #client.close()
        return [AllSlotsReset()]


# class ActionTeamNames(Action):

#     def name(self) -> Text:
#         return "action_team_names"


#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # connect to the MongoDB database
#         client = MongoClient('mongodb+srv://imadsbsbenali:JEH0cHlnYaP2YpzB@cluster0.lcywgrn.mongodb.net/test?retryWrites=true&w=majority')
#         db = client.chatbotEVdb

#         # retrieve the team names from the 'teamNames' collection
#         team_names = []
#         for team in db.teamNames.find():
#             team_names.append(team['name'])

#         # send the team names back to the user
#         if len(team_names) > 0:
#             message = "The team names are: " + ", ".join(team_names)
#         else:
#             message = "There are no team names available."
#         dispatcher.utter_message(text=message)

#         return []

class ActionTellStepsIncident(Action):

    def name(self) -> Text:
        return "action_tell_steps_incident"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_steps_creating_incident")
        dispatcher.utter_message(response="utter_step_creating_i_1")
        dispatcher.utter_message(response="utter_step_creating_i_2")
        dispatcher.utter_message(response="utter_step_creating_i_3")
        dispatcher.utter_message(response="utter_step_creating_i_4")
        dispatcher.utter_message(response="utter_step_creating_i_5")
        dispatcher.utter_message(response="utter_step_creating_i_6")
        dispatcher.utter_message(response="utter_step_creating_i_7")
        dispatcher.utter_message(response="utter_step_creating_i_8")
        dispatcher.utter_message(response="utter_step_creating_i_9")
        dispatcher.utter_message(response="utter_step_creating_i_10")

        return []

class ActionTellStepsDemandeDeService(Action):

    def name(self) -> Text:
        return "action_tell_steps_demande_de_service"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_steps_creating_demande_de_service")
        dispatcher.utter_message(response="utter_step_creating_s_1")
        dispatcher.utter_message(response="utter_step_creating_s_2")
        dispatcher.utter_message(response="utter_step_creating_s_3")
        dispatcher.utter_message(response="utter_step_creating_s_4")
        dispatcher.utter_message(response="utter_step_creating_s_5")
        dispatcher.utter_message(response="utter_step_creating_s_6")
        dispatcher.utter_message(response="utter_step_creating_s_7")
        dispatcher.utter_message(response="utter_step_creating_s_8")
        dispatcher.utter_message(response="utter_step_creating_s_9")

        return []

class ActionTellStepsDemandeDeChange(Action):

    def name(self) -> Text:
        return "action_tell_steps_demande_de_change"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_steps_creating_demande_de_change")
        dispatcher.utter_message(response="utter_step_creating_c_1")
        dispatcher.utter_message(response="utter_step_creating_c_2")
        dispatcher.utter_message(response="utter_step_creating_c_3")
        dispatcher.utter_message(response="utter_step_creating_c_4")
        dispatcher.utter_message(response="utter_step_creating_c_5")
        dispatcher.utter_message(response="utter_step_creating_c_6")
        dispatcher.utter_message(response="utter_step_creating_c_7")
        dispatcher.utter_message(response="utter_step_creating_c_8")
        dispatcher.utter_message(response="utter_step_creating_c_9")

        return []

class ActionCreateFirstStep(Action):

    def name(self) -> Text:
        return "action_create_f_step"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_type_ticket_confirmed")
        # dispatcher.utter_message(response="utter_ask_ticket_title")

        return []

# class ActionUserNames(Action):

#     def name(self) -> Text:
#         return "action_user_names"


#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         db = pymysql.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="dbusers"
#         )
#         try:
#             # create a cursor object
#             cursor = db.cursor()

#             # execute a SQL query
#             cursor.execute("SELECT * FROM users")

#             # get the result
#             result = cursor.fetchall()

#             # process the result
#             for row in result:
#                 dispatcher.utter_message(text=f"Your Ticket {row} ")

#         except Exception as e:
#             # handle the exception
#             print("Error:", e)

#         finally:
#             # close the connection
#             db.close()

#         return []

class ActionGreetFrensh(Action):
    def name(self) -> Text:
        return "action_greet_frensh"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        if(language=='en'):
            print("YES ENGLISH!")
        print(language)
        print(language['language'])
        return []