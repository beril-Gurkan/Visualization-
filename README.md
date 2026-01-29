# Business Expander Tool

A visualization tool for evaluating the economic and operational feasibility of international expansion. This interactive tool helps Market Entry Strategists, International Business Development Managers, and Strategic Planning Teams analyze countries across multiple metrics including workforce availability, energy capacity, supply chain connectivity, wage sustainability, and economic resilience.

All data is sourced from the CIA World Factbook Global Statistics Database (https://www.kaggle.com/datasets/kushagraarya10/cia-global-statistical-database).

## Prerequisites

* Python 3.8 or higher
* pip (Python package manager)
* Git (optional, for cloning the repository)

## Installation

1. **Clone or download this repository**
   ```
   git clone https://github.com/beril-Gurkan/Visualization-
   ```
   Or download and extract the ZIP file.

2. **Navigate to the project directory**
   ```
   cd Visualization-
   ```

3. **Create a virtual environment** (recommended)
   
   **Windows:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. **Ensure your virtual environment is activated**

2. **Run the app**
   ```
   python app.py
   ```

3. **Open your browser** and navigate to the local address shown in the terminal (typically `http://127.0.0.1:8050`)
## Dependencies

* **dash** (>=2.0.0) - Web application framework
* **plotly** - Interactive visualization library (installed with dash)
* **pandas** (>=1.3.3) - Data manipulation and analysis
* **numpy** (>=1.21.2) - Numerical computing

## Project Structure

```
./assets/              # CSS stylesheets
./callbacks/           # Interactive callback functions
./data_sets/           # CSV data files
./layouts/             # Page layout definitions
./utils/               # Helper functions and data processing
./views/               # UI component definitions
```

## Implementation Details

The following components were implemented from scratch for this project:

**Core Application Files:**
- `app.py` - Application entry point and layout switcher (partially inspired by the default template)
- `jbi100_app/app_instance.py` - Dash app initialization
- `jbi100_app/data.py` - Data loading and preprocessing functions

**Layout Components:**
- `jbi100_app/layouts/overview_layout.py` - Global overview page structure
- `jbi100_app/layouts/detailed_layout.py` - Detailed view page structure

**View Components (all files in `jbi100_app/views/`):**
- Global overview panels (map, metrics, country selection bar)
- Detailed view panels (complex metrics, scatterplot, ranking, radar chart, mini-map)

**Callback Logic (all files in `jbi100_app/callbacks/`):**
- Country selection and filtering
- Interactive brushing and linking
- Dynamic metric calculations
- Chart updates and synchronization

**Data Processing:**
- `jbi100_app/utils/complex_scores.py` - Custom metric calculations
- `jbi100_app/utils/country_meta.py` - Country metadata handling
- `preprocessing.py` - Data cleaning and preparation

**Styling:**
- All CSS files in `jbi100_app/assets/` - Custom styling for panels and components

### Library Components
The tool relies on the following existing libraries:

- **Plotly/Dash framework** - Used for creating interactive visualizations (scatter plots, bar charts, choropleth maps, radar charts)
- **Pandas DataFrames** - Data structure for handling CSV data
- **NumPy arrays** - Numerical operations in metric calculations

## AI Assistance Acknowledgment

This project was developed with substantial assistance from AI coding tools, primarily GitHub Copilot and Claude. The extent of AI involvement includes:

**AI-Generated Code:**
- Majority of callback functions in `jbi100_app/callbacks/` (interactive logic for filters, brushing, chart updates)
- Significant portions of view components in `jbi100_app/views/` (UI component structure)
- Data processing logic in `preprocessing.py`
- A portion of CSS styling in `jbi100_app/assets/` (layout and visual design)
- Code comments and documentation throughout the project

**Human Contributions:**
- Overall application architecture and design requirements
- Metric definitions and weighting schemes
- Data source selection and integration decisions
- Testing, debugging, and validation of all functionality
- UI/UX design direction and refinement
- Integration and coordination of components

All AI-generated code was reviewed, tested, modified, and validated by the development team. While AI provided implementation assistance, the conceptual design, requirements specification, and quality assurance were human-directed.
