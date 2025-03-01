from google import genai
from google.genai import types
from mail import maily

api_key = "AIzaSyAb1FKxbehH4AJNA5m0epw_AvtHh_JMH08"
client = genai.Client(api_key=api_key)
# response = client.models.generate_content(
#     model="gemma-2-27b-it", contents="Explain how AI works"
# )
# print(response.text)

# For streaming
# response = client.models.generate_content_stream(
#     model="gemini-1.5-flash-8b-latest",
#     contents="What is the meaning of life I wonder? From a technical standpoint",
#     config=types.GenerateContentConfig(
#             system_instruction='you are a helpful AI assistant',
#             response_mime_type= 'application/json',
#             # temperature= 0.5,
#             # max_output_tokens= 400,
#             # top_k= 2,
#             # top_p= 0.5,
#             # stop_sequences= ['\n'],
#             seed=42,
#         )
#     )
# for chunk in response:
#     print(chunk.text, end="")







def get_current_weather(location: str) -> str:
    """Get the current whether in a given location.

    Args:
        location: required, The city and state, e.g. San Franciso, CA
        unit: celsius or fahrenheit
    """
    print(f'Called weather func with: {location=}')
    return "25C"

# def get_current_time(location: str) -> str:
#     """Get the current time in a given location.

#     Args:
#         location: required, The city and state, e.g. San Franciso, CA
#     """

#     from datetime import datetime
#     # Get current date and time
#     now = datetime.now()
#     print(f'Called time func with: {location=}')
#     return now




def get_rndm_cat_fact(nb_facts: int) -> str:
    """Get random facts about cats through an API call.

    Args:
        nb_facts: The number of cat facts to retrieve.

    Returns:
        A string of cat facts.
    """
    
    import requests
    response = requests.get(f"https://meowfacts.herokuapp.com/?count={nb_facts}", verify=False)
    print(f'Called cat fact function with: nb_facts={nb_facts}')

    if response.status_code == 200:
        data = response.json()
        cat_facts = data.get('data', [])
        cat_facts[0] = "* " + cat_facts[0]
        return "\n* ".join(cat_facts)
    else:
        print("Failed to retrieve cat facts.")
        return []

# response = client.models.generate_content(
#    model='gemini-1.5-flash-8b-latest',
#    contents="What is the weather like in Boston?",
#    config=types.GenerateContentConfig(
#        system_instruction="""you are a helpful AI assistant, you have the option to use this tool if necessary:
#        {{"tool_name":get_current_weather
#        "tool_args: 'location'"
#        "description: 'Get the current whether in a given location.
#     Args:
#         location: required, The city and state, e.g. San Franciso, CA"}}
#         """,
#        tools=[get_current_weather],
#     #    automatic_function_calling={'disable': True},
#        seed=42,
#    ),
# # )
# prompt = """I was wondering if you can tell me the weather in Tunisia? Where is Tunisia exactly on the world map?
# Also I would like for you to send an email from marnewi.ey@gmail.com to marnewi.amine@gmail.com telling him a very funny joke, today's date and include 3 random cat facts. 
# """

# prompt = "Morning I was wondering if you could send an email to marnewi.amine@gmail.com telling him the mission's code is OPSDED and providing him with 6 cat facts?"
prompt = "Morning how are you doing this fine evening, I'd like some tech news"

from datetime import datetime
# Get current date and time
now = datetime.now()


response = client.models.generate_content(
   model='gemini-1.5-flash-8b-latest',
#    model='gemini-2.0-flash',
   contents=prompt,
   config=types.GenerateContentConfig(
        system_instruction=(f"""Your name is Job (pronounced Joeb) a helpful, loyal AI assistant named after the loyal servant of god
                            who endured Satan's afflictions but through all the challenges stayed true and loyal without compromise.
            Your personality is a spitting image of Alfred Pennyworth, the dignified and unwaveringly loyal butler of Bruce Wayne. Speak with refined British English, maintaining a polite, formal,
                            and understatedly witty tone. You are wise, resourceful, and always calm—even in the face of chaos. Offer fatherly advice, dry humour, and subtle sarcasm when appropriate.
                            Emphasize your decades of experience, impeccable manners, and deep commitment to your master Amine. Whether discussing daily matters or offering strategic counsel on
                            the endeavors at hand, remain courteous, measured, and ever-so-slightly sardonic, as you blend empathy with practicality. Even so you do not shy away from cursing when instructed to.
            You always address your master as "Master Amine".
            Your only purpose is to provide help to the best of your abilities to your master Amine (Your version of God if you will).
            You have access to tools that might help with depending on master's request.
            Only call one or more tools if you deem it necessary to statisfy your master's requests.
            Today is {now}.
            
            user's info: {{personal_mail:marnewi.ey@gmail.com}} """
        ),
        tools=[get_current_weather,
                # get_current_time,
                get_rndm_cat_fact,
                maily.send_gmail,
            #   types.Tool(google_search=types.GoogleSearch())
                ],
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode=types.FunctionCallingConfigMode.AUTO,
                # allowed_function_names=[
                #                     get_current_weather,
                #                     # get_current_time,
                #                     get_rndm_cat_fact,
                #                     maily.send_gmail,
                #                     # types.Tool(google_search=types.GoogleSearch())
                #                 ]
                )
            ),
        safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.OFF,
                    # method=types.HarmBlockMethod.SEVERITY
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.OFF,
                    # method=types.HarmBlockMethod.SEVERITY
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.OFF,
                    # method=types.HarmBlockMethod.SEVERITY
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.OFF,
                    # method=types.HarmBlockMethod.SEVERITY
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                    threshold=types.HarmBlockThreshold.OFF,
                    # method=types.HarmBlockMethod.SEVERITY
                ),
            ],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False,  # Ensures that function calling is enabled.
                maximum_remote_calls=10,
                ignore_call_history=False
            ),
   ),
)

# function_call = response.candidates[0].content.parts[0].function_call
# print("FUNCTION_CALL: ",function_call)
# print(response)
if response.candidates[0].content.parts == None:
    print(response.candidates[0].content)
else:
    print(response.candidates[0].content.parts[0].text)
# print("RESPONSE: ",response.candidates[0].content.parts[0].text)

