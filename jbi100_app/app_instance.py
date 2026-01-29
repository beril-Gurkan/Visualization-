# Dash app instance - single shared instance to prevent circular import issues
# All callbacks import this instance to register themselves
# Configured with: suppress_callback_exceptions=True for dynamic callback registration

from dash import Dash

# Single shared Dash instance to avoid circular imports across callbacks
app = Dash(__name__, suppress_callback_exceptions=True, title="Business Expander")
