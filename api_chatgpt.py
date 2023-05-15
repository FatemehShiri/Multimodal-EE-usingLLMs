import openai
import os
openai.api_key = "..."
# prompt = open("data/prompt_1.txt", "r").read().strip("\n")

def predict(input_message, prompt):
    # global prompt
    # input_message = {"role": "user", "content": input_text}
    # prompt.append(input_message)
    history.append(input_message)
    completion = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=prompt)
    extracted_content = completion.choices[0].message['content']
    if "No structured event" in extracted_content:
        extracted_content = 'Output: []'
    if "No event" in extracted_content or "No relevant events" in extracted_content :
        extracted_content = 'Output: []'
    prompt.append({"role": "assistant", "content": extracted_content})
    history.append({"role": "assistant", "content": extracted_content})
    print(extracted_content)
    # print(len(prompt))
    print(len(history))
    return history
# input_text= "Input: Americans this weekend are marching against the war and in support of the troops."
# results = predict(input_text)
# print(results)

if __name__ == '__main__':
    prompt_txt = [{"role": "user", "content": """Task Description
    This is an event extraction task where the goal is to extract structured events from the input text. A structured event contains an event trigger word and an event type.   

    Event types and their definitions
    Contact.Meet: A MEET Event occurs when two or more people interact with one another face-to-face at a single location. 
    Life.Die: A DIE Event occurs when the life of a PERSON Entity ends.
    Conflict.Demonstrate: A DEMONSTRATE Event occurs when a large number of people come together in a public area to protest or demand some sort of official action.
    Movement.Transport: A TRANSPORT Event occurs when an ARTIFACT or a PERSON is moved from one PLACE to another.
    Transaction.Transfer-Money: TRANSFER-MONEY Events refer to the giving, receiving, borrowing, or lending money.
    Conflict.Attack: An ATTACK Event is defined as a violent physical act causing harm or damage. 
    Contact.Phone-Write: A PHONE-WRITE Event occurs when two or more people directly engage in discussion but not face-to-face.
    Justice.Arrest-Jail: A ARREST-JAIL Event occurs when the movement of a PERSON is constrained by a state actor.

    Examples   
    Input: Protesters listen to a speaker as they gather for the Women's March against President Donald Trump, Jan. 21, 2017, in Los Angeles."""},
    {"role": "assistant", "content": "Output: [{'trigger': 'gather', 'event_type': 'Conflict.Demonstrate'}]"},
    {"role": "user", "content": "Input: Attacks in Turkey-Turkey has seen a sharp spike in clashes between security forces and Kurdish rebels in recent weeks."},
    {"role": "assistant", "content": "Output: [{'trigger': 'Attacks', 'event_type': 'Conflict.Attack'}]"},
    {"role": "user", "content": "Input: He was then flown to Moroto town in the northeastern subregion of Karamoja."},
    {"role": "assistant", "content": "Output: [{'trigger': 'flown', 'event_type': 'Movement.Transport'}]"},
    {"role": "user", "content": "Input: Ugandan Ex-Supreme Court Justice Questions Besigye Treason Charge-A former Uganda Supreme Court justice says the government and police need to explain a treason charge against jailed opposition leader Kizza Besigye, who was arrested last week."},
    {"role": "assistant", "content": "Output: [{'trigger': 'arrested', 'event_type': 'Justice.Arrest-Jail'}]"},
    {"role": "user", "content": "Input: Three Ibama officials in Santarem were charged last month with taking bribes from logging companies."},
    {"role": "assistant", "content": "Output: [{'trigger': 'bribes', 'event_type':'Transaction.Transfer-Money'}]"},
    {"role": "user", "content": "Input: Very few North Koreans have Internet access, but foreign residents and visitors previously have been able to access web pages with almost no overt restrictions."},
    {"role": "assistant", "content": "Output: [{'trigger': 'phone', 'event_type': 'Contact.Phone-Write'}]"}]

    #
    prompt_des = [{"role": "user", "content": """Task Description  This is an event extraction task where the goal is to extract structured events from the input text and description. A structured event contains an event trigger word and an event type.   
    Event types and their definitions
    Contact.Meet: A MEET Event occurs when two or more people interact with one another face-to-face at a single location. 
    Life.Die: A DIE Event occurs when the life of a PERSON Entity ends.
    Conflict.Demonstrate: A DEMONSTRATE Event occurs when a large number of people come together in a public area to protest or demand some sort of official action.
    Movement.Transport: A TRANSPORT Event occurs when an ARTIFACT or a PERSON is moved from one PLACE to another.
    Transaction.Transfer-Money: TRANSFER-MONEY Events refer to the giving, receiving, borrowing, or lending money.
    Conflict.Attack: An ATTACK Event is defined as a violent physical act causing harm or damage. 
    Contact.Phone-Write: A PHONE-WRITE Event occurs when two or more people directly engage in discussion but not face-to-face.
    Justice.Arrest-Jail: A ARREST-JAIL Event occurs when the movement of a PERSON is constrained by a state actor.

    Examples   
    Input: Protesters listen to a speaker as they gather for the Women's March against President Donald Trump, Jan. 21, 2017, in Los Angeles.   Description: a woman in a green coat is holding a microphone"""},
    {"role": "assistant", "content": "Output: [{'trigger': 'gather', 'event_type': 'Conflict.Demonstrate'}]"},
    {"role": "user", "content": "Input: Attacks in Turkey-Turkey has seen a sharp spike in clashes between security forces and Kurdish rebels in recent weeks. Description: a group of soldiers carrying a casket with a picture on it"},
    {"role": "assistant", "content": "Output: [{'trigger': 'Attacks', 'event_type': 'Conflict.Attack'}, {'trigger': 'casket', 'event_type': 'Life.Die'}]"},
    {"role": "user", "content": "Input: He was then flown to Moroto town in the northeastern subregion of Karamoja. Description: a man is escorted by police officers on a dirt road"},
    {"role": "assistant", "content": "Output: [{'trigger': 'flown', 'event_type': 'Movement.Transport'},{'trigger': 'escorted', 'event_type': 'Justice.Arrest-Jail'}]"},
    {"role": "user", "content": "Input: Ugandan Ex-Supreme Court Justice Questions Besigye Treason Charge-A former Uganda Supreme Court justice says the government and police need to explain a treason charge against jailed opposition leader Kizza Besigye, who was arrested last week. Description: a man is escorted by police officers on a dirt road"},
    {"role": "assistant", "content": "Output: [{'trigger': 'arrested', 'event_type': 'Justice.Arrest-Jail'}]"},
    {"role": "user", "content": "Input: Three Ibama officials in Santarem were charged last month with taking bribes from logging companies. Description: two men loading logs onto the back of a truck"},
    {"role": "assistant", "content": "Output: [{'trigger': 'bribes', 'event_type':'Transaction.Transfer-Money'}]"},
    {"role": "user", "content": "Input: Very few North Koreans have Internet access, but foreign residents and visitors previously have been able to access web pages with almost no overt restrictions. Description: a woman in a red jacket holding a phone and umbrella"},
    {"role": "assistant", "content": "Output: [{'trigger': 'phone', 'event_type': 'Contact.Phone-Write'}]"}]
    #####
    full_prompt_txt = [{"role": "user", "content": """Task Description
    This is an event extraction task where the goal is to extract structured events from the input text. A structured event contains an event trigger, an event type, event arguments and related mentions. Most event arguments will be participants in the Event.
    
    Event types and Event arguments and their definitions
    Contact.Meet: A MEET Event occurs when two or more people interact with one another face-to-face at a single location. MEET Events have two arguments (Participant, Place)
    Life.Die: A DIE Event occurs when the life of a PERSON Entity ends. DIE Events have four arguments (Agent, Victim, Instrument, Place).
    Conflict.Demonstrate: A DEMONSTRATE Event occurs when a large number of people come together in a public area to protest or demand some sort of official action. DEMONSTRATE Events have four arguments (Entity, Police, Instrument, Place)
    Movement.Transport: A TRANSPORT Event occurs when an ARTIFACT or a PERSON is moved from one PLACE to another. TRANSPORT Events have five arguments (Agent, Vehicle, Destination, Origin, Artifact).
    Transaction.Transfer-Money: TRANSFER-MONEY Events refer to the giving, receiving, borrowing, or lending money. TRANSFER-MONEY Events have three arguments (Giver, Recipient, Money)
    Conflict.Attack: An ATTACK Event is defined as a violent physical act causing harm or damage. ATTACK Events have four arguments (Instrument, Target, Place, Attacker)
    Contact.Phone-Write: A PHONE-WRITE Event occurs when two or more people directly engage in discussion but not face-to-face. PHONE-WRITE Events have three arguments (Entity, Instrument, Place)
    Justice.Arrest-Jail: A ARREST-JAIL Event occurs when the movement of a PERSON is constrained by a state actor. ARREST-JAIL Events have four arguments (Agent, Instrument, Place, Person)
    
    Event arguments and their definitions
    PLACE: Where the Event takes place
    ATTACKER: The attacking/instigating agent
    TARGET: The target of the attack
    INSTRUMENT: The instrument used in the Event
    AGENT: The agent responsible for the transport Event or or The attacking agent/The killer in the Die Event or the jailer/the arresting agent in the arrest-jail Event.
    ENTITY: The demonstrating agent for demonstrate Event or the communicating agents for phone-write Event
    VEHICLE: the vehicle doing the transporting
    DESTINATION:Where the transporting is directed
    ORIGIN: Where the transporting originated
    ARTIFACT: The person doing the traveling or the artifact being transported
    VICTIM: The harmed person(s)
    POLICE: The police agent in a demonstrating event
    GIVER: The donating agent
    RECIPIENT: The recipient agent
    MONEY: The amount given, donated or loaned
    PERSON: the person who is jailed or arrested
    PARTICIPANT: The agents who are meeting
    
    Examples
    Input: Protesters listen to a speaker as they gather for the Women's March against President Donald Trump, Jan. 21, 2017, in Los Angeles."""},
    {"role": "assistant", "content": """Output: [{'trigger': 'gather', 'event_type': 'Conflict.Demonstrate', 'Entity':'speaker', 'Police':'', 'Instrument':'', 'Place':'Los Angeles'}]"""},
    {"role": "user", "content": "Input: Attacks in Turkey-Turkey has seen a sharp spike in clashes between security forces and Kurdish rebels in recent weeks."},
    {"role": "assistant", "content": """Output: [{'trigger': 'Attacks', 'event_type': 'Conflict.Attack', 'Instrument':'', 'Target':'security forces', 'Place':'', 'Attacker':'rebels'}]"""},
    {"role": "user", "content": "Input: He was then flown to Moroto town in the northeastern subregion of Karamoja."},
    {"role": "assistant", "content": """Output: [{'trigger': 'flown', 'event_type': 'Movement.Transport', 'Agent':'', 'Vehicle':'', 'Destination':'Karamoja', 'Origin':'', 'Artifact':''}]"""},
    {"role": "user", "content": "Input: Ugandan Ex-Supreme Court Justice Questions Besigye Treason Charge-A former Uganda Supreme Court justice says the government and police need to explain a treason charge against jailed opposition leader Kizza Besigye, who was arrested last week."},
    {"role": "assistant", "content": """Output: [{'trigger': 'arrested', 'event_type': 'Justice.Arrest-Jail', 'Agent':'', 'Instrument':'', 'Place':'', 'Person':'Kizza Besigye'}]"""},
    {"role": "user", "content": "Input: Three Ibama officials in Santarem were charged last month with taking bribes from logging companies."},
    {"role": "assistant", "content": """Output: [{'trigger': 'bribes', 'event_type':'Transaction.Transfer-Money', 'Giver':'logging companies', 'Recipient':'officials', 'Money':''}]"""},
    {"role": "user", "content": "Input: Very few North Koreans have Internet access, but foreign residents and visitors previously have been able to access web pages with almost no overt restrictions."},
    {"role": "assistant", "content": """Output: [{'trigger': 'phone', 'event_type': 'Contact.Phone-Write', 'Entity':'', 'Instrument':'', 'Place':''}]"""}]

    full_prompt_des = [{"role": "user", "content": """Task Description
    This is an event extraction task where the goal is to extract structured events from the input text and the image description. A structured event contains an event trigger, an event type, event arguments and related mentions. Most event arguments will be participants in the Event.

    Event types and Event arguments and their definitions
    Contact.Meet: A MEET Event occurs when two or more people interact with one another face-to-face at a single location. MEET Events have two arguments (Participant, Place)
    Life.Die: A DIE Event occurs when the life of a PERSON Entity ends. DIE Events have four arguments (Agent, Victim, Instrument, Place).
    Conflict.Demonstrate: A DEMONSTRATE Event occurs when a large number of people come together in a public area to protest or demand some sort of official action. DEMONSTRATE Events have four arguments (Entity, Police, Instrument, Place)
    Movement.Transport: A TRANSPORT Event occurs when an ARTIFACT or a PERSON is moved from one PLACE to another. TRANSPORT Events have five arguments (Agent, Vehicle, Destination, Origin, Artifact).
    Transaction.Transfer-Money: TRANSFER-MONEY Events refer to the giving, receiving, borrowing, or lending money. TRANSFER-MONEY Events have three arguments (Giver, Recipient, Money)
    Conflict.Attack: An ATTACK Event is defined as a violent physical act causing harm or damage. ATTACK Events have four arguments (Instrument, Target, Place, Attacker)
    Contact.Phone-Write: A PHONE-WRITE Event occurs when two or more people directly engage in discussion but not face-to-face. PHONE-WRITE Events have three arguments (Entity, Instrument, Place)
    Justice.Arrest-Jail: A ARREST-JAIL Event occurs when the movement of a PERSON is constrained by a state actor. ARREST-JAIL Events have four arguments (Agent, Instrument, Place, Person)

    Event arguments and their definitions
    PLACE: Where the Event takes place
    ATTACKER: The attacking/instigating agent
    TARGET: The target of the attack
    INSTRUMENT: The instrument used in the Event
    AGENT: The agent responsible for the transport Event or or The attacking agent/The killer in the Die Event or the jailer/the arresting agent in the arrest-jail Event.
    ENTITY: The demonstrating agent for demonstrate Event or the communicating agents for phone-write Event
    VEHICLE: the vehicle doing the transporting
    DESTINATION:Where the transporting is directed
    ORIGIN: Where the transporting originated
    ARTIFACT: The person doing the traveling or the artifact being transported
    VICTIM: The harmed person(s)
    POLICE: The police agent in a demonstrating event
    GIVER: The donating agent
    RECIPIENT: The recipient agent
    MONEY: The amount given, donated or loaned
    PERSON: the person who is jailed or arrested
    PARTICIPANT: The agents who are meeting

    Examples
    Input: Protesters listen to a speaker as they gather for the Women's March against President Donald Trump, Jan. 21, 2017, in Los Angeles. Description: a woman in a green coat is holding a microphone"""},
    {"role": "assistant", "content": """Output: [{'trigger': 'gather', 'event_type': 'Conflict.Demonstrate', 'Entity':'speaker', 'Police':'', 'Instrument':'', 'Place':'Los Angeles'}]"""},
    {"role": "user", "content": "Input: Attacks in Turkey-Turkey has seen a sharp spike in clashes between security forces and Kurdish rebels in recent weeks. Description: a group of soldiers carrying a casket with a picture on it"},
    {"role": "assistant", "content": """Output: [{'trigger': 'Attacks', 'event_type': 'Conflict.Attack', 'Instrument':'', 'Target':'security forces', 'Place':'', 'Attacker':'rebels'}, {'trigger': 'casket', 'event_type': 'Life.Die', 'Agent':'rebels' , 'Victim': 'security forces', 'Instrument':'' , 'Place':''}]"""},
    {"role": "user", "content": "Input: He was then flown to Moroto town in the northeastern subregion of Karamoja. Description: a man is escorted by police officers on a dirt road"},
    {"role": "assistant", "content": """Output: [{'trigger': 'flown', 'event_type': 'Movement.Transport', 'Agent':'', 'Vehicle':'', 'Destination':'Karamoja', 'Origin':'', 'Artifact':''}, {'trigger': 'escorted', 'event_type': 'Justice.Arrest-Jail', 'Agent':'police', 'Instrument':'', 'Place':'', 'Person':' a man'}]"""},
    {"role": "user", "content": "Input: Ugandan Ex-Supreme Court Justice Questions Besigye Treason Charge-A former Uganda Supreme Court justice says the government and police need to explain a treason charge against jailed opposition leader Kizza Besigye, who was arrested last week. Description: a man is escorted by police officers on a dirt road"},
    {"role": "assistant", "content": """Output: [{'trigger': 'arrested', 'event_type': 'Justice.Arrest-Jail', 'Agent':'', 'Instrument':'', 'Place':'', 'Person':'Kizza Besigye'}]"""},
    {"role": "user", "content": "Input: Three Ibama officials in Santarem were charged last month with taking bribes from logging companies. Description: two men loading logs onto the back of a truck"},
    {"role": "assistant", "content": """Output: [{'trigger': 'bribes', 'event_type':'Transaction.Transfer-Money', 'Giver':'logging companies', 'Recipient':'officials', 'Money':''}]"""},
    {"role": "user", "content": "Input: Very few North Koreans have Internet access, but foreign residents and visitors previously have been able to access web pages with almost no overt restrictions. Description: a woman in a red jacket holding a phone and umbrella"},
    {"role": "assistant", "content": """Output: [{'trigger': 'phone', 'event_type': 'Contact.Phone-Write', 'Entity':'', 'Instrument':'', 'Place':''}]"""}]

    input_dir = "/Users/fshi0006/Desktop/Monash/workplace/blip/data/"
    for modal in ["txt", "des"]:
        history = []
        input_file_src = os.path.join(input_dir, f'src_{modal}.json')
        output_file_tgt = os.path.join(input_dir, f'output/tgt_{modal}_full.json')
        # output_file_res = os.path.join(input_dir, f'output/results_{modal}.json')
        with open(input_file_src, 'r', encoding='utf-8') as input_file:
            data = input_file.read().splitlines()
            for line in enumerate(data):
                input_text = line[1]
                if modal == "txt":
                    prompt = full_prompt_txt    #### for full extraction
                    # prompt = prompt_txt      #### for only event extraction
                elif modal == "des":
                    prompt = full_prompt_des   #### for full extraction
                    # prompt = prompt_des
                input_message = {"role": "user", "content": input_text}
                prompt.append(input_message)
                history = predict(input_message, prompt)
        input_file.close()
        # res = [(history[i]["content"], history[i+1]["content"]) for i in range(0, len(history)-1, 2)]
        tgt = [history[i+1]["content"] for i in range(0, len(history)-1, 2)]
        # print(res)
        with open(output_file_tgt, "w", encoding='utf-8') as tgt_file:
            for l in tgt:
                tgt_file.write(str(l) + "\n")
                print(l)
        tgt_file.close()

        # with open(output_file_res, "w", encoding='utf-8') as output_file:
        #     output_file.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in res))
        # output_file.close()
