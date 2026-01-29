# Callback registration - imports all callback modules to register them with the Dash app
# Each import registers callbacks defined with @app.callback decorators
def register_callbacks():
    # Import all callback modules - each contains @app.callback decorators that auto-register
    import jbi100_app.callbacks.ranking_callbacks
    import jbi100_app.callbacks.country_selection
    import jbi100_app.callbacks.detail_callbacks
    import jbi100_app.callbacks.mini_map_callbacks
    import jbi100_app.callbacks.metric_cards_callbacks
    import jbi100_app.callbacks.metric_expand_callbacks