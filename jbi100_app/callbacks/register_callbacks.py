def register_callbacks():
    # Import modules so callbacks register on the shared app instance
    import jbi100_app.callbacks.global_map_coloring
    import jbi100_app.callbacks.country_selection
    import jbi100_app.callbacks.detail_callbacks
    import jbi100_app.callbacks.mini_map_callbacks
    import jbi100_app.callbacks.ranking_panel_callbacks
