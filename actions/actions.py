# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for an assistant that schedules reminders and
# reacts to external events.

from typing import Any, Text, Dict, List
import datetime

from rasa_sdk import Action, Tracker
from rasa_sdk.events import ReminderScheduled, ReminderCancelled, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from future import absolute_import from future import division from future import unicode_literals
 

class ActionDB(Action): 

    def name(self) -> Text: 
        return "action_db"

    def run(self, dispatcher, tracker, domain):
        import MySQLdb
        db = MySQLdb.connect("localhost","root","Abcd_1234","DBforChatbot")
        cursor = db.cursor()
        PersonID = tracker.get_slot('personid')
        q = "select * from Persons where PersonID='{0}' limit 1".format(PersonID)
        result = db.query(q)
        return [SlotSet("matches", result if result is not None else [])]
 
def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

    # write the sql query here.
    query = "select * from customer"
    
    #pass the sql query to the getData method and store the results in `data` variable.
    data = getData(query)
    
    print("data: ",data)

    dispatcher.utter_message(text="Hello World!",json_message=data)

    return []

class ActionDB(Action): 
    def name(self) -> Text: 
        return "action_db"

    def run(self, dispatcher, tracker, domain):
	import MySQLdb
	db = MySQLdb.connect("localhost","root","Abcd_1234","DBforChatbot")
	cursor = db.cursor()
	PersonID = tracker.get_slot('personid')
	q = "select * from Persons where PersonID='{0}' limit 1".format(PersonID)
	result = db.query(q)
	return [SlotSet("matches", result if result is not None else [])]
    
class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("I will remind you in 5 seconds.")

        date = datetime.datetime.now() + datetime.timedelta(seconds=5)
        entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )

        return [reminder]


class ActionReactToReminder(Action):
    """Reminds the user to call someone."""

    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        #name = next(tracker.get_slot("PERSON"), "someone")
        #dispatcher.utter_message(f"Remember to call {name}!")
        dispatcher.utter_message("Remember to call Paul!")

        return []


class ActionTellID(Action):
    """Informs the user about the conversation ID."""

    def name(self) -> Text:
        return "action_tell_id"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        conversation_id = tracker.sender_id

        dispatcher.utter_message(f"The ID of this conversation is '{conversation_id}'.")
        dispatcher.utter_message(
            f"Trigger an intent with: \n"
            f'curl -H "Content-Type: application/json" '
            f'-X POST -d \'{{"name": "EXTERNAL_dry_plant", '
            f'"entities": {{"plant": "Orchid"}}}}\' '
            f'"http://localhost:5005/conversations/{conversation_id}'
            f'/trigger_intent?output_channel=latest"'
        )

        return []


class ActionWarnDry(Action):
    """Informs the user that a plant needs water."""

    def name(self) -> Text:
        return "action_warn_dry"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        plant = next(tracker.get_latest_entity_values("plant"), "someone")
        dispatcher.utter_message(f"Your {plant} needs some water!")

        return []


class ForgetReminders(Action):
    """Cancels all reminders."""

    def name(self) -> Text:
        return "action_forget_reminders"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Okay, I'll cancel all your reminders.")

        # Cancel all reminders
        return [ReminderCancelled()]
