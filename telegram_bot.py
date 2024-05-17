import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()
TOKEN = os.getenv('TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
SLEEP_TIME = 5  # Check for new messages every n seconds

running = True
last_update_id = -1

while running:  ## Laeuft ewig
    try:

        reply = requests.get(f'{BASE_URL}/getupdates?offset={last_update_id}')

        for data in reply.json().get('result'):
                # Hole den Nachrichtentext, den Vornamen, die ChatID und die id der letzten Nachricht
                message = str(data["message"]["text"])
                first_name = data["message"]["from"]["first_name"]
                chat_id = data["message"]["chat"]["id"]
                last_update_id = data["update_id"] + 1

                # Build Response Dictionary
                response = {"chat_id": chat_id, }

                # Reagiere auf die Eingabe
                # Fallunterscheidung
                if message.startswith('/start'):
                    response['text'] = f"Hello {first_name}".encode("utf8")
                    requests.post(f"{BASE_URL}/sendMessage", response)

                elif message.startswith('/example1 '):
                    pass

                # Hier können jetzt noch weitere Kommandos eingetragen werden

                else:
                    response['text'] = f"Please /start, {first_name}".encode("utf8")
                    requests.post(f"{BASE_URL}/sendMessage", response)

    except KeyboardInterrupt:  # Bei Abbruch mit CTRL-C
        print('Bot wird beendet')
        running = False
    except Exception as e:
        print(e)

    time.sleep(SLEEP_TIME)
