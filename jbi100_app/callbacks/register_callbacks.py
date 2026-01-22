def register_callbacks():
    # Import modules so callbacks register on the shared app instance
    import jbi100_app.callbacks.ranking_callbacks
    import jbi100_app.callbacks.country_selection
    import jbi100_app.callbacks.detail_callbacks