import os
import random
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def ping_endpoints(
        endpoints: list[str],
        base_interval: int = 55,
        extra_interval_min: int = 5,
        extra_interval_max: int = 10,
        base_pings: int = 1000
    ) -> None:
    """
    Pings a random endpoint from the list a total number of times equal to
    base_pings.
    
    Each ping is delayed by a time equal to base_interval plus a random number
    between extra_interval_min and extra_interval_max seconds.
    """

    for _ in range(base_pings):

        endpoint = random.choice(endpoints)

        try:
            response = requests.get(endpoint)
            # Use a ternary operator to print different messages based on response status.
            print(f"Pinged {endpoint}: {response.status_code}" if response.ok  else f"Ping failed for {endpoint}: {response.status_code}")

        except Exception as e:
            print(f"Error pinging {endpoint}: {e}")

        time.sleep(base_interval + random.randint(extra_interval_min, extra_interval_max))


if __name__ == "__main__":
    endpoints = os.getenv("URLS").split(",")

    ping_endpoints(endpoints)