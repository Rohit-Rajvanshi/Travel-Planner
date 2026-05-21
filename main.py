from openai import OpenAI
import gradio as gr 
from dotenv import load_dotenv
from tools import get_destination_info , get_travel_info , recommend_food , build_itinerary , tools
import json

load_dotenv()

model = "gpt-4o-mini"
openai = OpenAI()

system_prompt = """
You are a helpful Indian Travel Assistant named TravelIND.
Keep your responses concise.
Always be accurate .If you dont know the answer , say so.

When building itineraries:

1. SANITY CHECK the duration:
   - If user requests more than 5 days for one city, gently suggest extending to nearby destinations OR confirm they really want all days in one city.
   - Don't fill weak days with vague filler ("visit local temples" without naming them).

2. EACH DAY must have:
   - A specific morning activity (named attraction)
   - A specific afternoon activity (named attraction OR food experience)  
   - A specific evening activity (sunset spot, evening market, performance)
   - A specific dinner location (real restaurant name)
   - Brief transport note between major activities

3. NEVER mention:
   - "Local temples" without naming specific ones
   - "Local restaurant" without naming one
   - "Water sports" unless the destination is known for them
   - Activities that don't exist at the location

4. Always include 1 "flex" or "rest" suggestion for trips of 5+ days.

5. End with a brief summary of total cost vs budget AND offer to modify.


Always call tools for factual information. Never make up city details, prices, or recommendations. If a tool doesn't return data, tell the user you don't have that information.



CRITICAL RULES:
1. You can ONLY provide information about cities that exist in our database
2. Always call tools to retrieve information — never answer from your own knowledge
3. If a tool returns no data, empty data, or "not found", you MUST tell the user:
   "I don't have information about [city] in my database. I can help with these cities: [list]"
4. NEVER fill in missing data from your general knowledge
5. NEVER hallucinate prices, attractions, or recommendations

Supported cities:  Delhi, Mumbai, Bangalore, chennai , kolkata 

When a user asks open-ended questions like "where should I go?" or "recommend cities":
- First, ask 1-2 qualifying questions about their preferences (vibe, budget, duration, interests)
- Then recommend 2-3 cities from your available list with a one-line reason for each
- Always tie recommendations to their stated preferences

When listing your available cities, briefly describe each (one phrase per city) so the user has context, not just names.

"""

def chat(message , history):
    history = [{"role" : h["role"] , "content" : h["content"]} for h in history]
    messages = [{"role": "system", "content" : system_prompt}] + history + [{"role" : "user" , "content" : message}]
    response = openai.chat.completions.create(
        model = model , 
        messages = messages,
        tools = tools,
    )
    while response.choices[0].finish_reason == "tool_calls" :
        message = response.choices[0].message
        responses = handle_tool_calls(message)
        messages.append(message)
        messages.extend(responses)
        response = openai.chat.completions.create(
            model = model ,
            messages = messages, 
            tools = tools ,
        )

    return response.choices[0].message.content






def handle_tool_calls(message):
    responses = []

    for tool_call in message.tool_calls:
        arguments = json.loads(tool_call.function.arguments)

        if tool_call.function.name == "get_destination_info":
            response =  get_destination_info(arguments.get("city"))

        elif tool_call.function.name == "get_travel_info":
            response = get_travel_info(arguments.get("from_city") , arguments.get("to_city"))

        elif tool_call.function.name == "recommend_food":
            response = recommend_food(arguments.get("city"))
           

        elif tool_call.function.name == "build_itinerary":
            response =  build_itinerary(arguments.get("city") , arguments.get("days") , arguments.get("budget"))
        


        responses.append({
            "role" : "tool" ,
            "content" : json.dumps(response),
            "tool_call_id" : tool_call.id
        })

    return responses


gr.ChatInterface(fn = chat , multimodal = True, textbox = gr.MultimodalTextbox(file_types=[".png", ".jpg"] , sources = ["upload"] , file_count = "single")).launch()


