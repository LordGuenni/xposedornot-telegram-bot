import requests
import json
import os
import json
from datetime import datetime, timedelta

TOKEN = os.getenv('TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
BASE_API = "https://api.xposedornot.com/v1/breach-analytics?email="

not_breached_data = {
    'BreachesSummary': {'domain': '', 'site': '', 'tmpstmp': ''}, 
    'PastesSummary': {'cnt': 0, 'domain': '', 'tmpstmp': ''}
}


def get_json_from_api(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
    return response.json()
    
def get_recent_breaches():
    api_url = "https://api.xposedornot.com/v1/breaches"
    try:
        response = get_json_from_api(api_url)
        exposed_breaches = response.get('exposedBreaches', [])
    except Exception as e:
        return f"Failed to get data from API: {e}"
    
    one_month_ago = datetime.now() - timedelta(days=30)
    recent_breaches = [breach for breach in exposed_breaches if datetime.fromisoformat(breach['breachedDate'].split('T')[0]) >= one_month_ago]
    
    formatted_breaches = []
    for breach in recent_breaches:
        formatted_breach = (
            f"<b>Breach ID:</b> {breach['breachID']}\n\n"
            f"<b>Breached Date:</b> {breach['breachedDate'].split('T')[0]}\n\n"
            f"<b>Domain:</b> {breach['domain']}\n\n"
            f"<b>Exposed Data:</b> {', '.join(breach['exposedData'])}\n\n"
            f"<b>Exposure Description:</b> {breach['exposureDescription']}\n\n"
            f"<b>Industry:</b> {breach['industry']}\n\n"
            f"<b>Password Risk:</b> {breach['passwordRisk']}\n\n"
            f"<b>Reference URL:</b> {breach['referenceURL']}\n\n"
        )
        formatted_breaches.append(formatted_breach)
    
    # Join all formatted breaches into a single text
    response_text = '\n'.join(formatted_breaches)
    
    return response_text
    

    
def parse_data(data):
    breaches = data.get('ExposedBreaches', {}).get('breaches_details', [])
    parsed_breaches = []

    for breach in breaches:
        parsed_breach = {
            'Breach': breach.get('breach'),
            'Details': breach.get('details'),
            'Exposed Data': breach.get('xposed_data'),
            'Exposed Date': breach.get('xposed_date'),
            'Domain': breach.get('domain'),
            'Industry': breach.get('industry'),
            'Logo': breach.get('logo'),
            'Password Risk': breach.get('password_risk'),
            'References': breach.get('references'),
            'Searchable': breach.get('searchable'),
            'Verified': breach.get('verified'),
            'Exposed Records': breach.get('xposed_records')
        }
        parsed_breaches.append(parsed_breach)

    return parsed_breaches
        
def lambda_handler(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        first_name = data["message"]["chat"]["first_name"]
        chat_id = data["message"]["chat"]["id"]

        response = {"chat_id": chat_id, }
        help_message = """
        /start - Start the bot
        /breaches - Shows the Recent Data-breaches (Last 30 Days)
        /breached [email] - Check if an email has been pwned
        /help - Show this help message
        """
        
        if message.startswith('/start'):
            response['text'] = f"Hello {first_name}".encode("utf8")
            requests.post(f"{BASE_URL}/sendMessage", response)

        
        elif message.startswith('/breached'):
            if len(message.split()) < 2:
                response['text'] = "Please provide an email address after breached command."
                requests.post(f"{BASE_URL}/sendMessage", response)
            else:
                email = str(message.split()[1])
                try:
                    data2 = get_json_from_api(BASE_API + email)
                except Exception as e:
                    response['text'] = f"Failed to get data from API: {e}"
                    
                if data2 == not_breached_data:
                    # Send checkmark icon
                    checkmark_message = {
                        "chat_id": chat_id,
                        "photo": "https://static.vecteezy.com/system/resources/previews/001/200/261/non_2x/check-png.png",
                        "caption": "No Breaches Found"
                    }
                    requests.post(f"{BASE_URL}/sendPhoto", checkmark_message)
                else:
                    parsed_data = parse_data(data2)[:10]
                    for breach in parsed_data:
                        # Send logo as a separate message
                        logo_message = {"chat_id": chat_id, "photo": breach['Logo']}
                        requests.post(f"{BASE_URL}/sendPhoto", logo_message)
                        
                        # Format the main message text with HTML
                        response_text = (
                            f"<b>Description:</b>\n"
                            f"<i>{breach['Details']}</i>\n\n"
                            f"<b>Date:</b> <i>{breach['Exposed Date']}</i>\n\n"
                            f"<b>Source of Breach:</b> <i>{breach['Breach']}</i>"
                        )
                    
                        response['text'] = response_text
                        response['parse_mode'] = 'HTML'
                        requests.post(f"{BASE_URL}/sendMessage", response)


        
        elif message.startswith('/breaches'):
            response_text = get_recent_breaches()
            response = {
                "chat_id": chat_id,
                "text": response_text,
                "parse_mode": "HTML"
            }
            requests.post(f"{BASE_URL}/sendMessage", response)
            
    
            
        elif message.startswith('/help'):
            response['text'] = help_message.encode("utf8")
            requests.post(f"{BASE_URL}/sendMessage", response)

        else:
            response['text'] = f"Please /start, {first_name}".encode("utf8")
            requests.post(f"{BASE_URL}/sendMessage", response)

    except Exception as exception:
        print(exception)

    return {"statusCode": 200}