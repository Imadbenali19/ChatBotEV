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
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import pymysql

from pymysql import Error
from spacy.language import Language

from spacy_language_detection import LanguageDetector
from googletrans import Translator
import jwt

translator = Translator()
def get_lang_detector(nlp, name):
    return LanguageDetector(seed=42)  # We use the seed 42

nlp_model = spacy.load('en_core_web_sm')
Language.factory("language_detector", func=get_lang_detector)
nlp_model.add_pipe('language_detector', last=True)


###################


#
# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        print(message)
        print(message.startswith('salut'))

        #Get the text within the utterance in the domain file
        response_template_list = domain["responses"]["utter_greet"]
        response_template_dict = response_template_list[0]  # assuming there's only one dictionary in the list
        
        # modify the response message
        utter_text = response_template_dict["text"]

        if(language['language']=='fr' or message.lower().startswith('salut') or message.lower().startswith('bonsoir') or message.lower().startswith('bonjour') or message.lower().startswith('cv')):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text)
        else:
            dispatcher.utter_message(text=utter_text)

        token=tracker.get_slot("token")
        username=tracker.get_slot("username")
        userId=tracker.get_slot("userId")

        print("hi your token  : ",token," and username is : ",username, " and userId is : ",userId)
        return []
    
class ActionHappy(Action):

    def name(self) -> Text:
        return "action_happy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        
        #Get the text within the utterance in the domain file
        response_template_list = domain["responses"]["utter_happy"]
        response_template_dict = response_template_list[0]  # assuming there's only one dictionary in the list
        
        # modify the response message
        utter_text = response_template_dict["text"]
        
        if(language['language']=='fr' or message.lower().startswith('vrai') or message.lower().startswith("d'accord")):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text)
        else:
            dispatcher.utter_message(text=utter_text)

        return []

class ActionCheerUp(Action):

    def name(self) -> Text:
        return "action_cheer_up"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        
        #Get the text within the utterance in the domain file
        response_template_list = domain["responses"]["utter_cheer_up"]
        response_template_dict = response_template_list[0]  # assuming there's only one dictionary in the list
        
        # modify the response message
        utter_text = response_template_dict["text"]

        # Get the image URL
        image_url = response_template_dict.get("image")
        
        if(language["language"]=='fr'):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text, image=image_url)
        else:
            dispatcher.utter_message(text=utter_text, image=image_url)

        return []

class ActionDidThatHelp(Action):

    def name(self) -> Text:
        return "action_did_that_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        
        #Get the text within the utterance in the domain file
        response_template_list = domain["responses"]["utter_did_that_help"]
        response_template_dict = response_template_list[0]  # assuming there's only one dictionary in the list
        
        # modify the response message
        utter_text = response_template_dict["text"]
        
        if(language['language']=='fr'):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text)
        else:
            dispatcher.utter_message(text=utter_text)

        return []

class ActionThank(Action):

    def name(self) -> Text:
        return "action_thank"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        
        #Get the text within the utterance in the domain file
        response_template_list = domain["responses"]["utter_thank"]
        response_template_dict = response_template_list[0]  # assuming there's only one dictionary in the list
        
        # modify the response message
        utter_text = response_template_dict["text"]
        
        if(language['language']=='fr' or message.lower().startswith('merci') or message.lower().startswith('mrc')):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text)
        else:
            dispatcher.utter_message(text=utter_text)

        return []

class ActionIamBOT(Action):

    def name(self) -> Text:
        return "action_iamabot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language

        #Get the text within the utterance in the domain file
        response_template_list = domain["responses"]["utter_iamabot"]
        response_template_dict = response_template_list[0]  # assuming there's only one dictionary in the list
        
        # modify the response message
        utter_text = response_template_dict["text"]

        if(language['language']=='fr'):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text)
        else:
            dispatcher.utter_message(text=utter_text)

        return []
    
class ActionShowTime(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        print("doc : ",doc)
        print("job_title : ",job_title)
        print("msg : ",message)
        
        if(language['language']=='fr'):
            dispatcher.utter_message(text=f"C'est {dt.now()}")
        else:
            dispatcher.utter_message(text=f"It's {dt.now()}")

        return []

class ActionInformSupportTeams(Action):

    def name(self) -> Text:
        return "action_inform_support_teams"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Connect to MongoDB
        client = MongoClient('mongodb+srv://imadsbsbenali:JEH0cHlnYaP2YpzB@cluster0.lcywgrn.mongodb.net/test?retryWrites=true&w=majority')
        db = client.chatbotEVdb
        collection = db.supportTeams

        # Retrieve all teams and their team leads
        teams = collection.find({}, {'name': 1, 'teamLead': 1})

        #Detect the language
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        print("doc : ",doc)
        print("job_title : ",job_title)
        print("msg : ",message)

        managed_string="managed by"

        if(language["language"]=='fr'):
            managed_string="gérée par"

        # Format and send the response
        info = []
        for team in teams:
            team_name = "" + team['name'].strip() + ""
            team_lead = team['teamLead']['name'].strip()
            info.append(f"**{team_name}** {managed_string} **{team_lead}**\n\n")

        if(language["language"]=='fr'):
            dispatcher.utter_message(text=f"On a {''.join(info)}")
        else:
            dispatcher.utter_message(text=f"We have {''.join(info)}")

        client.close()
        return []

class ActionInformModuleSupportTeams(Action):

    def name(self) -> Text:
        return "action_inform_module_support_teams"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #Detect the language
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        print("doc : ",doc)
        print("job_title : ",job_title)
        print("msg : ",message)

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

        if(language["language"]=='fr'):
            modules = team['modules']
            msg="Les modules traités par "
            msg2=" sont: "
        else:
            modules = team['modulesEN']
            msg="The modules processed by "
            msg2=" are: "

        # Format and send the response
        result = "" + ', '.join([module.strip().upper() for module in modules.split(',')]) + ""
        
        dispatcher.utter_message(text=f"{msg} **{team_name.upper()}** {msg2}: **{result}**")
        client.close()
        #return [SlotSet("module_team", result)]
        # return [AllSlotsReset()]
        return [SlotSet("team_name", None)]

class ActionInformTicketType(Action):

    def name(self) -> Text:
        return "action_inform_ticket_type"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        client = MongoClient('mongodb+srv://imadsbsbenali:JEH0cHlnYaP2YpzB@cluster0.lcywgrn.mongodb.net/test?retryWrites=true&w=majority')
        db = client.chatbotEVdb

        #Detect the language
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        print("doc : ",doc)
        print("job_title : ",job_title)
        print("msg : ",message)

        # retrieve the team names from the 'teamNames' collection
        ticket_type_name = [f"**{ttype['name'].upper()}**" for ttype in db.ticketType.find()]
        msg="We have "
        if(language["language"]=='fr' or message.startswith('Types de tickets')):
            ticket_type_desc = [ttype['description'] for ttype in db.ticketType.find()]
            msg="Nous avons "
        else:  
            ticket_type_desc = [ttype['descriptionEN'] for ttype in db.ticketType.find()]
            
        info = [ticket_type_name[i:i+4] for i in range(0, len(ticket_type_name), 4)]
        text = ""
        for i in range(len(info)):
            text += f"{msg} {len(info[i])} types: \n\n"
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

        print("create ticket class")

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
        user_id=tracker.get_slot("userId")
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
        


        # establish a connection to the MySQL database
        try:
            connection = pymysql.connect(
                host='localhost',
                database='helpboot',
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

            #extract the client id from the jwt token
            print("user id : ",user_id)
            cursor = connection.cursor()
            query = "SELECT id FROM client WHERE userid = %s;"
            user_data = (user_id,)
            cursor.execute(query, user_data)
            resultId = cursor.fetchone()[0]

            urgence=None
            impact=None
            if ticket_emergency=="1":
                urgence='E'
            elif ticket_emergency=="2":
                urgence='M'
            else:
                urgence='F'
            if ticket_impact=="1":
                impact='E'
            elif ticket_impact=="2":
                impact='M'
            else:
                impact='F'

            # create a prepared statement for the SQL query
            query = "INSERT INTO ticket (reference, type, title, description, emergency, impact, priority, module, environnement, status, creation_date, closure_date, affected, agentid, clientid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = connection.cursor()

            # insert the new ticket into the table
            ticket_data = (ticket_reference, ticket_type, ticket_title, ticket_description, urgence, impact, ticket_priority, ticket_option, ticket_environnement, 'O', dt.now(), None, b'\x00', None, resultId)
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
        # dispatcher.utter_message(text=f"Your Ticket {ticket_type} under {ticket_reference} : \n\n -*Title*: **{ticket_title}** \n\n -*Description*: **{ticket_description_str}** \n\n -*Emergency*: **{ticket_emergency}** \n\n -*Impact*: **{ticket_impact}** \n\n -*Priority*: **{ticket_priority}** \n\n -*Product*: **{product}** \n\n -*Client*: **{bank_name}** \n\n -*Beneficiaire*:  \n\n -*Product/Option*: **{product}/{ticket_option}** \n\n -*Version*:  \n\n -*Environnement*: **{ticket_environnement}** \n\n")
        # dispatcher.utter_message(text=f" **{created_suc}** \n\n")
        # dispatcher.utter_message(text=f"Your ticket's reference is **{ticket_reference}** \n\n")
        dispatcher.utter_message(text=f"Your ticket {ticket_type}  **{created_suc}**, its reference is **{ticket_reference}** \n\n")

        #client.close()
        # return [AllSlotsReset()]
        return [SlotSet("ticket_type", None), SlotSet("ticket_title", None), SlotSet("ticket_description", None), SlotSet("ticket_option", None), SlotSet("ticket_emergency", None), SlotSet("ticket_impact", None), SlotSet("ticket_environnement", None)]



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
        #Detect the language
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        print("doc : ",doc)
        print("job_title : ",job_title)
        print("msg : ",message)

        if(language["language"]=='fr'):
            dispatcher.utter_message(response="utter_steps_creating_incident_fr")
            dispatcher.utter_message(response="utter_step_creating_i_1_fr")
            dispatcher.utter_message(response="utter_step_creating_i_2_fr")
            dispatcher.utter_message(response="utter_step_creating_i_3_fr")
            dispatcher.utter_message(response="utter_step_creating_i_4_fr")
            dispatcher.utter_message(response="utter_step_creating_i_5_fr")
            dispatcher.utter_message(response="utter_step_creating_i_6_fr")
            dispatcher.utter_message(response="utter_step_creating_i_7_fr")
            dispatcher.utter_message(response="utter_step_creating_i_8_fr")
            dispatcher.utter_message(response="utter_step_creating_i_9_fr")
            dispatcher.utter_message(response="utter_step_creating_i_10_fr")
        else:
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
        #Detect the language
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        print("doc : ",doc)
        print("job_title : ",job_title)
        print("msg : ",message)

        if(language["language"]=='fr'):
            dispatcher.utter_message(response="utter_steps_creating_demande_de_service_fr")
            dispatcher.utter_message(response="utter_step_creating_s_1_fr")
            dispatcher.utter_message(response="utter_step_creating_s_2_fr")
            dispatcher.utter_message(response="utter_step_creating_s_3_fr")
            dispatcher.utter_message(response="utter_step_creating_s_4_fr")
            dispatcher.utter_message(response="utter_step_creating_s_5_fr")
            dispatcher.utter_message(response="utter_step_creating_s_6_fr")
            dispatcher.utter_message(response="utter_step_creating_s_7_fr")
            dispatcher.utter_message(response="utter_step_creating_s_8_fr")
            dispatcher.utter_message(response="utter_step_creating_s_9_fr")
        else:
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

        #Detect the language
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        print("doc : ",doc)
        print("job_title : ",job_title)
        print("msg : ",message)

        if(language["language"]=='fr'):
            dispatcher.utter_message(response="utter_steps_creating_demande_de_change_fr")
            dispatcher.utter_message(response="utter_step_creating_c_1_fr")
            dispatcher.utter_message(response="utter_step_creating_c_2_fr")
            dispatcher.utter_message(response="utter_step_creating_c_3_fr")
            dispatcher.utter_message(response="utter_step_creating_c_4_fr")
            dispatcher.utter_message(response="utter_step_creating_c_5_fr")
            dispatcher.utter_message(response="utter_step_creating_c_6_fr")
            dispatcher.utter_message(response="utter_step_creating_c_7_fr")
            dispatcher.utter_message(response="utter_step_creating_c_8_fr")
            dispatcher.utter_message(response="utter_step_creating_c_9_fr")
        else:
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

class ActionHabilitationClient(Action):

    def name(self) -> Text:
        return "action_habilitation_client"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        
        #Get the text within the utterance in the domain file
        response_template_list = domain["responses"]["utter_habilitation_client"]
        response_template_dict = response_template_list[0]  # assuming there's only one dictionary in the list
        
        # modify the response message
        utter_text = response_template_dict["text"]

        # Get the image URL
        image_url = response_template_dict.get("image")
        
        if(language["language"]=='fr'):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text, image=image_url)
        else:
            dispatcher.utter_message(text=utter_text, image=image_url)

        return []

class ActionExplainChampProduct(Action):

    def name(self) -> Text:
        return "action_explain_Champ_Product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        
        #Get the text within the utterance in the domain file
        response_template_list = domain["responses"]["utter_explain_Champ_Product"]
        response_template_dict = response_template_list[0]  # assuming there's only one dictionary in the list
        
        # modify the response message
        utter_text = response_template_dict["text"]
        
        if(language["language"]=='fr'):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text)
        else:
            dispatcher.utter_message(text=utter_text)

        return []

class ActionExplainChampOption(Action):

    def name(self) -> Text:
        return "action_explain_Champ_Option"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        
        #Get the text within the utterance in the domain file
        response_template_list = domain["responses"]["utter_explain_Champ_Option"]
        response_template_dict = response_template_list[0]  # assuming there's only one dictionary in the list
        
        # modify the response message
        utter_text = response_template_dict["text"]
        
        if(language["language"]=='fr'):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text)
        else:
            dispatcher.utter_message(text=utter_text)

        return []

class ActionExplainChampEnvironnement(Action):

    def name(self) -> Text:
        return "action_explain_Champ_Environnement"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        
        #Get the text within the utterance in the domain file
        response_template_list = domain["responses"]["utter_explain_Champ_Environnement"]
        response_template_dict = response_template_list[0]  # assuming there's only one dictionary in the list
        
        # modify the response message
        utter_text = response_template_dict["text"]
        
        if(language["language"]=='fr' and "environment".lower() not in message.lower()):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text)
        else:
            dispatcher.utter_message(text=utter_text)

        return []

class ActionExplainChampRGPD(Action):

    def name(self) -> Text:
        return "action_explain_Champ_RGPD"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")

        job_title = message
        doc = nlp_model(job_title)
        language = doc._.language
        
        #Get the text within the utterance in the domain file
        response_template_list = domain["responses"]["utter_explain_Champ_RGPD"]
        response_template_dict = response_template_list[0]  # assuming there's only one dictionary in the list
        
        # modify the response message
        utter_text = response_template_dict["text"]
        
        if(message.lower().startswith("RGPD".lower())):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text)
        elif(message.lower().startswith("GDPR".lower())):
            dispatcher.utter_message(text=utter_text)
        elif(language["language"]=='fr'):
            translated_text = translator.translate(utter_text, dest='fr')
            dispatcher.utter_message(text=translated_text.text)
        else:
            dispatcher.utter_message(text=utter_text)

        return []

class ActionTellToken(Action):
    def name(self) -> Text:
        return "action_tell_token"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")
        print("message : ",message)
        
        if message!="clientTOKEN":
            token_start_index = message.find('"token":"') + len('"token":"')
            token_end_index = message.find('"', token_start_index)
            token = message[token_start_index:token_end_index]
            token_parts = token.split(':')
            token_value = token_parts[0].strip("'")
        else:
            token_value="clientTOKEN"
        
        print(token_value)

        if token_value!="clientTOKEN":
            # Decode the JWT token without verifying the secret key
            decoded_token = jwt.decode(token_value, options={'verify_signature': False})
            print("Payload : ",decoded_token)
            userId=decoded_token['sub']
            print("userId: ",userId)

            username=decoded_token['username']
            if "@" in username:
                username = username.split("@")[0]
                
            print(username)
        else:
            decoded_token="client"
            username="client"
            userId="1"
        
        
        dispatcher.utter_message(response="utter_started", user = username)
    
        return [SlotSet("token", token), SlotSet("userId", userId), SlotSet("username", username)]


class ValidateTicketForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_ticket_form"

    
    #################################################

    def validate_ticket_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `ticket_type` value."""

        ttype = slot_value.lower()  # Convert to lowercase for case-insensitive matching
        # Check if ticket type is a demand of service  
        if ttype=="demande de service":
            print("yes demand of service")
            return {"ticket_type": ttype, "ticket_impact": "4","ticket_emergency":"4"}
        else:
            print("not demand of service")
            return {"ticket_type": ttype, "ticket_impact": None,"ticket_emergency": None}
       
    def validate_ticket_description(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `ticket_description` value."""

        description = slot_value.lower()  # Convert to lowercase for case-insensitive matching
        #keywords for the option
        caisseKey = ["caisse","caisses", "billetage", "nomenclature 004","bkcaib","bkcai","nomenclature 095", "cash position"]
        parametrageKey = ["Nomenclature 098", "parametrage","configuration","code 098"]
        referentielKey = ["tiers", "clients","referentiels","gestionnaire","decisionnaire","niveau de forçage","customer"]
        paymentKey = ["swift","cheques"]
        tfjKey = ["tfj","cbmaj600","cbmaj500","cbmaj540"]
        arreteKey = ["arretes de comptes","calcul des arretes","interets debiteurs","interets crediteurs","calcul des agios"]
        #Keywords for P1
        p1key = ["plantage programme tfj","probleme tfj","plantage interface","blocage chaine tfj","blocage tfj","blocage dans tfj", "blocking of tfj", "crash of tfj program"]
        ticket_option = None
        
        # Check if the description contains the keywords of caisse    
        if any(keyword in description for keyword in caisseKey):
            print("yes given caisse")
            ticket_option = "Guichet"
        elif any(keyword in description for keyword in parametrageKey):
            print("yes given parametrage")
            ticket_option = "Parametrage"
        elif any(keyword in description for keyword in referentielKey):
            print("yes given referentiels")
            ticket_option = "Referentiels"
        elif any(keyword in description for keyword in paymentKey):
            print("yes given referentiels")
            ticket_option = "Payment"
        elif any(keyword in description for keyword in tfjKey):
            print("yes given TFJ")
            ticket_option = "TFJ"
        elif any(keyword in description for keyword in arreteKey):
            print("yes given arrêtes comptes")
            ticket_option = "Arrêtés des comptes"
        else:
            print("no")
        ticket_emergency = tracker.get_slot("ticket_emergency")
        ticket_impact = tracker.get_slot("ticket_impact")
        if  ticket_emergency is None and ticket_impact is None : 
            ticket_emergency = None
            ticket_impact = None
            if any(keyword in description for keyword in p1key):
                print("yes P1")
                ticket_impact = "1"
                ticket_emergency = "1"
            else:
                print("not sure P1")

        return {
            "ticket_description": description,
            "ticket_option": ticket_option,
            "ticket_impact": ticket_impact,
            "ticket_emergency": ticket_emergency
        }       
    

class ActionSendDoc(Action):

    def name(self) -> Text:
        return "action_send_doc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = tracker.latest_message.get("text", "")
        print("message : ",message)

        # Connect to MongoDB
        client = MongoClient('mongodb+srv://imadsbsbenali:JEH0cHlnYaP2YpzB@cluster0.lcywgrn.mongodb.net/test?retryWrites=true&w=majority')
        db = client.chatbotEVdb
        collection = db.documentations

        
        if message.lower().find("referentiels users") != -1 or message.lower().find("referentiels utilisateurs") != -1:
            doc = collection.find_one({'parametre': "referentiels users"})
        elif message.lower().find("referentiels accounts") != -1 or message.lower().find("referentiels comptes") != -1:
            doc = collection.find_one({'parametre': "referentiels comptes"})
        elif message.lower().find("referentiels 098") != -1:
            doc = collection.find_one({'parametre': "referentiels 098"})
        elif message.lower().find("module caisses") != -1 or message.lower().find("module caisse") != -1:
            doc = collection.find_one({'parametre': "module caisse"})
        
        file_id=doc['file_id']
        # Google Drive file ID of the document
        # file_id = "1R6cp81bJRIjmdN3PJtR8eU9t6QyJHo_S"
        
        # https://drive.google.com/uc?export=download&id=1R6cp81bJRIjmdN3PJtR8eU9t6QyJHo_S
        # https://drive.google.com/file/d/1R6cp81bJRIjmdN3PJtR8eU9t6QyJHo_S/view?usp=drive_link
        # Generate the link to open the document in the Google Docs Viewer
        document_link = f"https://drive.google.com/uc?export=download&id={file_id}"
        # document_link = f"https://drive.google.com/file/d/{file_id}/view?usp=drive_link"

        # dispatcher.utter_message(text=f"Documentation: [document_link]")
        dispatcher.utter_message(response="utter_documentation", documentation_link = document_link)

        return []