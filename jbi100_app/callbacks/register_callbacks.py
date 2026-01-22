def register_callbacks():
    # Import modules so callbacks register on the shared app instance
    import jbi100_app.callbacks.ranking_callbacks
    import jbi100_app.callbacks.country_selection

    # keep these if you use them elsewhere
    import jbi100_app.callbacks.region_map_callbacks
    import jbi100_app.callbacks.detail_callbacks
    import jbi100_app.callbacks.global_map_hover
    import jbi100_app.callbacks.resize_callbacks
    import jbi100_app.callbacks.view_toggle
    import jbi100_app.callbacks.url_region_sync