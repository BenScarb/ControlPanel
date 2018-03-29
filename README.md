# ControlPanel
Shed Control Panel

A simple control panel that reads in an HTML file, makes it available using CherryPy.
Exposes simple "APIs" to allow the page to update elements with data from a dictionary.
The dictionary is updated with data pulled from a MQTT broker (using paho-mqtt component)
