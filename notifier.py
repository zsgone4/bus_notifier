import requests
from datetime import datetime
from local import API_KEY, YOUR_NAME,YOUR_NUMBER

MESSAGE_BIRD_URL = 'https://rest.messagebird.com/messages'
TFL_URL = 'https://api.tfl.gov.uk/line/{0}/arrivals'

def get_bus_data(bus_line):
    """
    The purpose of this function is to call the Transport For London API
    to get the predicted arrival time of a specific bus route.

    It takes the following value as input:
    bus_line - string (The number of the bus)

    returns
    expected_arr - datetime (The expected arrival time)
    destinationName - string (The name of the destination)
    stationName - string (The name of the station)

    """

    response  =  requests.get(url=TFL_URL.format(bus_line))
    arrival_predictions_data  = response.json()

    expected_arr = arrival_predictions_data[0]['expectedArrival']
    expected_arr = datetime.strptime(expected_arr,'%Y-%m-%dT%H:%M:%SZ')

    destinationName = arrival_predictions_data[0]['destinationName']
    stationName = arrival_predictions_data[0]['stationName']

    return expected_arr,destinationName,stationName


def compose_message(bus_line,expected_arr,destinationName,stationName):
    """
    The purpose of this function is to compose a message.

    It takes the following values as inputs:
    bus_line - string (The number of the bus)
    expected_arr - datetime (The expected arrival time)
    destinationName - string (The name of the destination)
    stationName - string (The name of the station)

    returns

    message - string

    """

    message = """ETA for the bus {0} at {1} is {2} and it\'s heading towards {3}""" \
        .format(bus_line,stationName,datetime.strftime(expected_arr,'%H:%M'),destinationName)

    print(message)

    return message


def send_message(recipients,message,originator):
    """
    The purpose of the function is to use Message bird's API to send a message.

    The function take the following input value:

    recipients - string (The phone number, you want to send the message to)
    message - string (The message you want to send)
    originator - string (Your name)

    """

    payload= {
        'access_key':API_KEY,
        'originator':originator,
        'body':message,
        'recipients':recipients
    }

    response = requests.post(MESSAGE_BIRD_URL,data=payload)

    print(response.ok)

    try:
        print(response.json()['recipients']['items'][0]['status'])
    except Exception as e:
        print(e)


def main():
    """
    The main function does the following:

    step - 1 : Get an input from the user containing the value of the bus number.
    step - 2:  Calls the function get_bus_data()
    step - 3:  Calls the function compose_message()
    step - 4:  Calls the function send_message()
    """
    bus_line = input("Please enter the bus line number: ")
    expected_arr,destinationName,stationName = get_bus_data(bus_line)
    message = compose_message(bus_line,expected_arr,destinationName,stationName)
    send_message(YOUR_NUMBER,message,YOUR_NAME)


if __name__ == '__main__':
    main()
