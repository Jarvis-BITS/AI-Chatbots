# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction
import urllib
import json

# ENDPOINTS = {
#     "base": "https://data.medicare.gov/resource/{}.json",
#     "xubh-q36u": {
#         "city_query": "?city={}",
#         "zip_code_query": "?zip_code={}",
#         "id_query": "?provider_id={}"
#     },
#     "b27b-2uc7": {
#         "city_query": "?provider_city={}",
#         "zip_code_query": "?provider_zip_code={}",
#         "id_query": "?federal_provider_number={}"
#     },
#     "9wzi-peqs": {
#         "city_query": "?city={}",
#         "zip_code_query": "?zip={}",
#         "id_query": "?provider_number={}"
#     }
# }

hospitals = {
    "110070": "Fortis Flt Vasant Kunj"
}


class ActionFindAndShowTimeZone(Action):

    def name(self) -> Text:
        return "action_find_and_show_time_zone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        url = "https://www.amdoren.com/api/timezone.php?api_key=QbQVAKsgdVP6KtUVxngHQPScRAaVHt&loc={}".format(
            city)
        data = requests.get(url)
        json_data = data.json()
        timezone = json_data["time"]

        if timezone is None:
            output = "Could not find the time zone for {}".format(city)
        else:
            output = "The current time in {} is {} derived from {}".format(
                city, timezone, json_data)

        dispatcher.utter_message(text=output)

        return []

# class FacilityForm(FormAction):

#         def name(self) -> Text:
#             return "timezone_form"

#     @staticmethod

#     def required_slots(tracker:Tracker) -> List[Text]:

#         return["city"]

#     def slot_mappings(self) -> Dict[Text, Any]:
#         return{"city": self.from_entity(entity="city",
#                                         intent=[])}


#      def submit(self,
#                dispatcher: CollectingDispatcher,
#                tracker: Tracker,
#                domain: Dict[Text, Any]
#                ) -> List[Dict]:
