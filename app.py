import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.properties import StringProperty
import random
import requests
import time
from datetime import datetime, timezone
import threading

kivy.require('2.1.0')

class PingApp(App):
    log_text = StringProperty("")

    def build(self):
        self.log_label = Label(text=self.log_text, size_hint_y=None, height=400)
        self.log_label.text = "[b]Pinging endpoints...[/b]\n"
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 400), do_scroll_x=False)
        self.scroll_view.add_widget(self.log_label)

        # Set up the layout
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.scroll_view)

        # Start the ping function in a separate thread to prevent blocking the UI
        threading.Thread(target=self.run_ping_function, daemon=True).start()

        return layout

    def run_ping_function(self):
        endpoints = ["https://vasset-kezx.onrender.com/api/v1/utils/health-check/"]
        self.ping_endpoints(endpoints)

    def update_log(self, message: str):
        """Update the log in the UI thread."""
        self.log_text += message + "\n"
        self.log_label.text = self.log_text

    def ping_endpoints(
        self, 
        endpoints: list[str], 
        base_interval: int = 55, 
        extra_interval_min: int = 5, 
        extra_interval_max: int = 10, 
        base_pings: int = 1000
    ) -> None:
        for _ in range(base_pings):
            endpoint = random.choice(endpoints)
            try:
                response = requests.get(endpoint)
                # Use a ternary operator to print different messages based on response status.
                message = f"[{datetime.now(timezone.utc).strftime("%d-%m-%Y, %H:%M")}] Pinged {endpoint}: {response.status_code}" if response.ok else f"Ping failed for {endpoint}: {response.status_code}"
                self.update_log(message)
            except Exception as e:
                message = f"Error pinging {endpoint}: {e}"
                self.update_log(message)
            time.sleep(base_interval + random.randint(extra_interval_min, extra_interval_max))

if __name__ == "__main__":
    PingApp().run()
