from openai import OpenAI
import json
import os
import steps.step0_setup

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
# https://platform.openai.com/docs/guides/function-calling
# https://medium.com/@remisharoon/creating-a-chatgpt-plugin-for-real-time-weather-updates-a-comprehensive-guide-dbfd36208d21

def get_current_weather(location, time, unit="fahrenheit"):
    print(f'get_current_weather called ({location}, {time}, {unit})')
    import random
    return random.choice(["sunny", "rainy", "cloudy", "snowy"])


def run_conversation(location):
    # Step 1: send the conversation and available functions to the model

    # TODO: Write a prompt (into content field) that will give you result like this based on location variable:
    # Conversation result: Based on the weather conditions in New York today:
    # At 10:00, as it's sunny, you should take your dog for a walk in Central Park. Enjoy the fresh air and green spaces at 59th St to 110th St between Fifth and Eighth Ave.
    # At 11:00, continue enjoying the sunny weather, perhaps, at Riverside Park. It's a beautiful place by Hudson River and you can get there at Riverside Drive and 79th Street.
    # At 12:00, it's still sunny. How about a little change of scenery? Take your dog to Bryant Park at 6th Ave & W 42nd St.
    # At 13:00, the weather is sunny. Perfect for a walk at Fort Tryon Park, located at Riverside Dr To Broadway, W 192 St To Dyckman St.
    # By 14:00, grab your winter coat! It's getting snowy. Perhaps it's time to appreciate some art indoor at The Metropolitan Museum of Art located at 1000 5th Ave.
    # At 15:00, the weather becomes cloudy. Visit the American Museum of Natural History and enjoy a journey through various exhibits. Find it at Central Park West and 79th St.
    # By 16:00, it's sunny again. Time to get back outdoor! Walk your dog at Madison Square Park at Madison Ave, E 23 St, E 26 St, 5 Ave to Broadway.
    # At 17:00, it's beginning to rain. Shield yourself from the rain at MoMA. Appreciate the art exhibits at 11 W 53rd St.
    # For the hour of 18:00, the weather is still cloudy. It's a good time to explore The Guggenheim Museum at 1071 5th Ave.
    # At 19:00, it remains cloudy, perfect for a quiet time at the New York Historical Society Museum at 170 Central Park W.
    # Lastly, at 20:00, it remains cloudy. Maybe consider visiting the Museum of the City of New York. You will find it at 1220 Fifth Avenue. Enjoy!
    
    messages = [{"role": "user", "content": f"""
    

    """}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location and time",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "time": {
                            "type": "string",
                            "description": "Time, like: 12:00 or 4:00PM",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location", 'time'],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                location=function_args.get("location"),
                time=function_args.get("time"),
                unit=function_args.get("unit"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response.choices[0].message.content

if __name__ == '__main__':
    import streamlit as st

    st.title('Dog Walk Scheduler')
    location = st.text_input('Enter location', 'New York')
    if st.button('Run Conversation'):
        result = run_conversation(location)
        st.write('Conversation result:', result)

