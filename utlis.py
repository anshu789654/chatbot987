import os
import pycountry
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-server.json"



import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newsbot-kutsvf"

import wikipedia
from gnewsclient import gnewsclient
from pymongo import MongoClient

cl = MongoClient("mongodb+srv://test1:test1@cluster0-j9qwg.mongodb.net/test?retryWrites=true&w=majority")
db = cl.get_database('search_db')
records = db.search_records



client = gnewsclient.NewsClient(max_results=3)

def get_news(parameters):
	print(parameters)
	client.topic = parameters.get('news_type')
	client.language = parameters.get('language')
	client.location = parameters.get('geo-country')
	return client.get_news()



def wiki(parameters):
	str1=parameters.get('geo-country')
	str2=wikipedia.summary ( str1,sentences=4 )
	return str2,pycountry.countries.get(name = str1).alpha_2

def wiki2(parameters):
	str1=parameters.get('geo-city')
	try:
	    str2=wikipedia.summary ( str1,sentences=4 )
	except wikipedia.exceptions.DisambiguationError as e:
		str3=e.options[:1]
		print("############################",str3)
		str2=wikipedia.summary ( str3,sentences=4 )
	
	return str2,None

    



def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def fetch_reply(msg,session_id):
	response=detect_intent_from_text(msg, session_id)
	print('#######################',response.intent.display_name)

	

	

	if response.intent.display_name=="get_news":
		new_data={'name':msg}
		records.insert_one(new_data)
		news = get_news(dict(response.parameters))
		news_str = 'Here is your news:'
		for row in news:
			news_str += "\n\n{}\n\n{}\n\n".format(row['title'],
				row['link'])
		return news_str, None
		 #"ok, I willshow you news{}".format(dict(response.parameters))
	elif response.intent.display_name=="get_country":
		new_data={'name':msg}
		records.insert_one(new_data)
		
		news_str,country=wiki(dict(response.parameters))
		return news_str,country

	elif response.intent.display_name=="get_city":
		new_data={'name':msg}
		records.insert_one(new_data)
		
		rstsr,country=wiki2(dict(response.parameters))
		return rstsr,None

	elif response.intent.display_name=="get_history":
		list(records.find())
		ret_str=''
		for i in reversed(list(records.find())):
			ret_str+='\n{}'.format(i['name'])
		return ret_str,None




	else:
		return response.fulfillment_text,None
