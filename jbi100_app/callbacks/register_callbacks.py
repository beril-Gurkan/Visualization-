# Callback registration - imports all callback modules to register them with the Dash app
# Each import registers callbacks defined with @app.callback decorators
#
# COMPLEXITY NOTE: This project uses 16+ callbacks coordinated across 6 modules:
# - State sharing via dcc.Store components (selected-countries-data, metric-weights, brush-selection)
# - Circular dependency prevention through careful Input/Output design
# - Bidirectional sync between overview and detailed views
# The callback architecture was the most complex part of this project, requiring careful
# coordination to avoid infinite loops, race conditions, and stale state issues.

def register_callbacks():
    # Import all callback modules - each contains @app.callback decorators that auto-register
    import jbi100_app.callbacks.ranking_callbacks
    import jbi100_app.callbacks.country_selection
    import jbi100_app.callbacks.detail_callbacks
    import jbi100_app.callbacks.mini_map_callbacks
    import jbi100_app.callbacks.metric_cards_callbacks
    import jbi100_app.callbacks.metric_expand_callbacks