from dash import Dash

# Single shared Dash instance to avoid circular imports across callbacks
app = Dash(__name__, suppress_callback_exceptions=True)
