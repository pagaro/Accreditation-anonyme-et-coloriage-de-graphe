from datetime import datetime, timedelta
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor

anonymous_distribution_channel = {}
lock = threading.Lock() # verrou global

def post_anonymous_message(message: str):
    dateNow = datetime.today()
    with lock:
        anonymous_distribution_channel[dateNow] = message
    return dateNow

def get_anonymous_message(startDate: datetime, endDate: datetime):
    return {
        key: value
        for key, value in anonymous_distribution_channel.items()
        if startDate <= key <= endDate
    }

def get_a_random_bit():
    return random.randint(0,1)

def wait_for_a_random_time_between_1_and_10ms():
    time.sleep(random.randint(1,10) / 1000)

def generate_secret(interlocutor_1: str, interlocutor_2: str, duration_in_seconds: int):
    log_self = {}  # dictionnaire local du participant
    time_start = time.time()
    while time.time() < time_start + duration_in_seconds:
        alice_or_bob_message = interlocutor_2 if get_a_random_bit() else interlocutor_1 # Bob si 1, Alice si 0
        wait_for_a_random_time_between_1_and_10ms()
        timestamp = post_anonymous_message(alice_or_bob_message)
        log_self[timestamp] = alice_or_bob_message  # je garde une copie locale
    return log_self

def extract_secret(log_self: dict, name_self: str):
    secret_bits = []
    for timestamp in sorted(anonymous_distribution_channel.keys()):
        message = anonymous_distribution_channel[timestamp]
        if timestamp in log_self:  # j'ai envoyé ce message
            if message == name_self:
                secret_bits.append(0)
            else:
                secret_bits.append(1)
        else:  # message envoyé par l'autre
            if message == name_self:
                secret_bits.append(1)
            else:
                secret_bits.append(0)
    return secret_bits

anonymous_distribution_channel.clear()

duration = 3

# ThreadPoolExecutor pour pouvoir récupérer les résultats des threads
with ThreadPoolExecutor(max_workers=2) as executor:
    thread_generate_secret_Alice = executor.submit(generate_secret, "Alice", "Bob", duration) # Alice envoie
    thread_generate_secret_Bob   = executor.submit(generate_secret, "Bob", "Alice", duration) # Bob envoie
    logAlice = thread_generate_secret_Alice.result()
    logBob   = thread_generate_secret_Bob.result()

secret_Alice = extract_secret(logAlice, "Alice")
secret_Bob = extract_secret(logBob, "Bob")
print("Secret identiques ?", secret_Alice == secret_Bob)


