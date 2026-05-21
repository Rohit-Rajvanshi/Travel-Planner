# Tools for the LLM to use and function better 
from data.cities import CITIES , TRAVEL_OPTIONS , FOOD_DATA


def get_destination_info(city):
    print(f"tool called for {city} ")
    desitnation_info = CITIES.get(city.lower() , "Unknown city")
    return  f"This is all the information about the {city}: {desitnation_info}"


def get_travel_info (from_city , to_city):
    print(f"tool called for travel info from {from_city} to {to_city}")
    travel_cities = f"{from_city.lower()}-{to_city.lower()}"
    print(travel_cities)
    travel_info = TRAVEL_OPTIONS.get(travel_cities)
    print(travel_info)
    return f"This is the travel info for {from_city} to {to_city}: {travel_info}"


def recommend_food (city):
    print(f"tool called for {city} ")
    food_info = FOOD_DATA.get(city.lower() , "Unknown city")
    return  f"This is all the information about the {city}: {food_info}"

def build_itinerary (city , days , budget):
    print(f"tool called for city: {city}")
    return ({"days" : days , "budget" : budget , "city_info" : get_destination_info(city) , "food_info" : recommend_food(city)})

 

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_destination_info",
            "description": "Get information about an Indian destination city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name in lowercase, e.g. 'goa'"
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    }
    ,
    {
        "type": "function",
        "function": {
            "name": "get_travel_info",
            "description": "Get information about travelling from one city to another",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_city": {
                        "type": "string",
                        "description": "The city to departure from"
                    },
                    "to_city" : {
                        "type" : "string",
                        "description" : "city to travel to"
                    }
                },
                "required": ["from_city" , "to_city"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_food",
            "description": "recommend good food from good restraunts in the city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name in lowercase, e.g. 'goa'"
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "build_itinerary",
            "description": "Get information about an Indian destination city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name in lowercase, e.g. 'goa'"
                    },
                    "days": {
                        "type" : "string" ,
                        "description" : "Number of days to spend in that city"
                    },
                    "budget" : {
                        "type" : "string",
                        "description" : "the budget that can be spent"
                    }
                }, 
                "required": ["city" , "days" , "budget"],
                "additionalProperties": False
            }
        }
    }        

]



    

