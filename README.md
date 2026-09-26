# AstroRisk

## Near-Earth Asteroid Characteristics & Close-Approach Research Platform

**AstroRisk** is a NASA NeoWs-powered research and data-analysis platform for exploring the characteristics of near-Earth objects (NEOs) and their close approaches to Earth.

The project analyzes relationships between:

- Asteroid diameter
- Relative velocity
- Miss distance
- Close-approach dates
- Near-Earth object characteristics

It also includes an exploratory machine-learning component using **K-Means clustering** to categorize observed objects based on their measured characteristics. If you want to view what it looks like, look at the screenshots
folder :)

---

## Author & Developer

**Eva J. Patel**

AstroRisk is designed, developed, and maintained by **Eva J. Patel**.

Contributions are welcome, but the original authorship and developer attribution of AstroRisk must remain with Eva J. Patel.

> **AstroRisk — Developed by Eva J. Patel**

This project is an independent educational and research project and is **not affiliated with, sponsored by, or endorsed by NASA or JPL**.

---

## Research Question

> **How do asteroid diameter, relative velocity, and miss distance relate to the characteristics of near-Earth asteroid close approaches, and how effectively can a data-driven model categorize observed objects?**

AstroRisk investigates this question through:

1. NASA API data collection
2. Data cleaning and preprocessing
3. Exploratory data analysis
4. Statistical analysis
5. Interactive visualization
6. Correlation analysis
7. Machine-learning-based clustering
8. Research-oriented interpretation

The goal is to investigate patterns within publicly available near-Earth object data rather than create an operational asteroid-impact prediction system.

---

## Research Scope

AstroRisk focuses primarily on three quantitative variables:

| Variable | Description |
|---|---|
| Diameter | Estimated asteroid diameter in kilometers |
| Relative Velocity | Object velocity relative to Earth during close approach |
| Miss Distance | Distance between the object and Earth during close approach |

Additional information may include:

- Object designation
- Close-approach date
- Potentially hazardous object status
- Orbit-related information
- Multiple close approaches
- NASA NeoWs metadata

---

## Features

### NASA NeoWs Data Integration

AstroRisk retrieves near-Earth object information using NASA's **Near Earth Object Web Service (NeoWs)**.

The application can process information including:

- Asteroid identifiers
- Estimated diameter
- Close-approach dates
- Relative velocity
- Miss distance
- Potentially hazardous object status

### Data Analysis

The research dashboard provides statistical analysis of collected observations.

Current analysis includes:

- Mean
- Median
- Minimum
- Maximum
- Percentiles
- Standard deviation
- Correlation analysis
- Distribution analysis

Both **Pearson** and **Spearman** correlation methods can be used when appropriate.

### Interactive Visualizations

AstroRisk provides visual analysis of asteroid characteristics, including:

- Diameter distributions
- Relative velocity distributions
- Miss-distance distributions
- Diameter vs. velocity
- Diameter vs. miss distance
- Velocity vs. miss distance
- Cluster distributions

---

## Machine Learning

AstroRisk includes an exploratory **K-Means clustering** component.

The model uses selected asteroid characteristics to identify groups of observations with similar numerical properties.

The primary variables are:

- Diameter
- Relative velocity
- Miss distance

Because these variables can exist on very different numerical scales, the analysis can apply:

1. Log transformation where appropriate
2. Feature standardization
3. K-Means clustering

The resulting clusters are interpreted descriptively.

For example, a cluster may contain observations characterized by relatively smaller diameters, higher velocities, or shorter miss distances.

However, cluster labels do **not** represent official NASA classifications or levels of danger.

The clustering model is an exploratory research tool.

---

## Scientific Disclaimer

AstroRisk is an **educational and exploratory research project**.

The machine-learning model does **not** calculate:

- Official asteroid impact probability
- Official NASA risk scores
- Planetary-defense recommendations
- Collision probabilities
- Future asteroid trajectories
- Official hazardous-object classifications

A K-Means cluster should not be interpreted as a measure of danger or impact risk.

The results represent patterns found within the analyzed dataset.

NASA and JPL maintain official scientific resources for monitoring and studying near-Earth objects.

---

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn

### Data Science

- Pandas
- NumPy
- SciPy
- scikit-learn

### Visualization

- Matplotlib
- Chart.js
- HTML
- CSS
- JavaScript

### Research Interface

- Gradio

### Data Source

- NASA Near Earth Object Web Service (NeoWs)

---

## Architecture

    NASA NeoWs API
           |
           v
    Data Collection
           |
           v
    Data Cleaning
           |
           v
    Feature Extraction
           |
           +--------------------+
           |                    |
           v                    v
    Statistical Analysis    ML Analysis
           |                    |
           v                    v
    Visualizations        K-Means Clustering
           |                    |
           +---------+----------+
                     |
                     v
            AstroRisk Dashboard

---

## Project Structure

    astrorisk-neows/
    │
    ├── .github/
    │   └── CODEOWNERS
    │
    ├── app/
    │   ├── __init__.py
    │   ├── analytics.py
    │   ├── main.py
    │   ├── nasa.py
    │   ├── sample_data.py
    │   │
    │   └── static/
    │       └── index.html
    │
    ├── .env.example
    ├── .gitignore
    ├── CONTRIBUTING.md
    ├── LICENSE
    ├── README.md
    ├── START_HERE.md
    ├── requirements.txt
    ├── run.bat
    └── run.py

Generated API cache files and local datasets are intentionally excluded from Git.

---

## Requirements

Before running AstroRisk, make sure you have:

- Python 3.10+
- Git
- Internet access
- A NASA API key

Python 3.12 is recommended for the current project setup.

---

## Installation

### 1. Clone the Repository

    git clone https://github.com/YOUR-USERNAME/astrorisk-neows.git
    cd astrorisk-neows

### 2. Create a Virtual Environment

#### Windows

    py -3.12 -m venv .venv

Activate it:

    .venv\Scripts\Activate.ps1

If PowerShell prevents activation, you can also run:

    .venv\Scripts\activate.bat

### 3. Install Dependencies

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

---

## NASA API Key

AstroRisk uses NASA's NeoWs API.

Create a local `.env` file based on `.env.example`.

Example:

    NASA_API_KEY=YOUR_NASA_API_KEY

**Do not commit your `.env` file to GitHub.**

For basic testing, NASA's public `DEMO_KEY` may also be used, although it has more restrictive rate limits.

---

## Running AstroRisk

After installing the dependencies and configuring your API key:

    python run.py

Or on Windows:

    run.bat

The application should start locally.

Open:

    http://127.0.0.1:8000

---

## Research Lab

The AstroRisk research interface is available at:

    http://127.0.0.1:8000/lab

The research lab provides access to the project's analytical workflow and visualizations.

---

## API Documentation

FastAPI automatically provides interactive API documentation.

Open:

    http://127.0.0.1:8000/docs

The API documentation allows developers and researchers to inspect available endpoints and test requests.

---

## Health Check

AstroRisk provides a health endpoint:

    http://127.0.0.1:8000/api/health

This can be used to verify that the backend is running.

---

## Research Workflow

A typical AstroRisk analysis follows this process:

### Step 1 — Collect Data

Asteroid and close-approach information is retrieved from NASA NeoWs.

### Step 2 — Clean Data

The raw API response is transformed into a structured analytical dataset.

### Step 3 — Extract Variables

The project extracts relevant numerical features such as:

- Diameter
- Relative velocity
- Miss distance

### Step 4 — Explore Distributions

Statistical summaries and visualizations are generated.

### Step 5 — Analyze Relationships

Correlation analysis is performed between the primary variables.

### Step 6 — Transform Features

Variables may be log-transformed and standardized before machine-learning analysis.

### Step 7 — Apply K-Means

K-Means clustering is used to identify groups of observations with similar characteristics.

### Step 8 — Interpret Results

The resulting groups are analyzed descriptively.

### Step 9 — Document Limitations

Results are evaluated in the context of the dataset, methodology, and limitations.

---

## Example Research Questions

AstroRisk can be used to investigate questions such as:

### Diameter and Velocity

> Is asteroid diameter associated with relative velocity during close approaches?

### Diameter and Miss Distance

> Do larger observed objects have systematically different miss distances?

### Velocity and Miss Distance

> Is relative velocity associated with the distance of an asteroid during a close approach?

### Multivariate Structure

> Can diameter, velocity, and miss distance be used to identify naturally occurring groups of observations?

### Model Interpretation

> How interpretable are the clusters generated by K-Means?

---

## Reproducibility

For reproducible research, document:

- Date of data collection
- API parameters
- Number of observations
- Variables used
- Data-cleaning procedures
- Transformations
- Standardization method
- Number of clusters
- Random seed
- Software versions
- Analysis limitations

Because NASA NeoWs data can change over time, analyses conducted at different times may not produce identical datasets.

For publication-oriented research, preserving a documented dataset snapshot is recommended.

---

## Data Caching

AstroRisk may locally cache API responses to reduce unnecessary API requests and improve development performance.

Local cache files are not intended to be committed to the Git repository.

For example:

    data/.neocache

should remain local.

If a curated dataset is later created for research publication, it should be stored separately with documentation describing:

- Collection date
- Source
- API endpoint
- Query parameters
- Processing steps
- Dataset version

---

## Limitations

### Dataset Limitations

The analysis depends on information returned by NASA NeoWs.

Missing or incomplete observations may affect statistical results.

### Temporal Limitations

The dataset represents observations available through the API at the time of collection.

The results may therefore change as new observations and calculations become available.

### Measurement Limitations

Asteroid diameter estimates can contain uncertainty.

Derived quantities such as miss distance and relative velocity should therefore be interpreted as scientific measurements or estimates rather than perfectly known values.

### Machine Learning Limitations

K-Means clustering is sensitive to:

- Feature scaling
- Transformation methods
- Number of clusters
- Initialization
- Dataset composition
- Outliers

Therefore, cluster membership should not be treated as an objective or permanent classification.

### Correlation Limitations

Correlation does not establish causation.

A relationship between two asteroid characteristics does not demonstrate that one variable causes the other.

---

## Ethical & Scientific Use

AstroRisk is intended for:

- Education
- Data science research
- Astronomy exploration
- Statistical analysis
- Machine-learning experimentation
- Software development
- Scientific communication

The project should not be used as a replacement for official planetary-defense systems, scientific publications, or professional astronomical analysis.

---

## NASA Data Attribution

AstroRisk uses NASA's public **Near Earth Object Web Service (NeoWs)** as its primary data source.

NASA and JPL are not the authors or developers of AstroRisk.

This project is independently developed by:

**Eva J. Patel**

---

## Contributing

Contributions are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test the project.
5. Document significant changes.
6. Submit a pull request.

Example:

    git checkout -b feature/my-analysis

After making your changes:

    git add .
    git commit -m "Add new asteroid analysis"
    git push origin feature/my-analysis

Then open a pull request on GitHub.

See `CONTRIBUTING.md` for additional contribution requirements.

---

## Contributor Attribution

Contributors may receive credit for their individual contributions.

However, contributions do not transfer or replace the original authorship or developer attribution of AstroRisk.

The project should continue to identify:

> **AstroRisk — Developed by Eva J. Patel**

Contributors should not represent themselves as the sole author or original developer of AstroRisk.

---

## License

AstroRisk is released under a custom **Source-Available Research License**.

The license permits personal, educational, and research use while maintaining attribution requirements and restricting commercial use without permission.

The full terms are available in:

    LICENSE

Users and contributors must preserve attribution to:

> **Eva J. Patel — Author & Developer of AstroRisk**

This project is source-available and is **not presented as an OSI-approved open-source license**.

---

## GitHub Repository Guidelines

The following files should **not** be committed:

    .env
    .venv/
    __pycache__/
    data/.neocache
    *.csv
    *.json
    *.parquet
    .vscode/
    .idea/

Do not upload:

- NASA API keys
- Passwords
- Private credentials
- Authentication tokens
- Other secrets
- Local virtual environments
- Generated cache files

Use:

    .env.example

to document required environment variables without exposing credentials.

---

## Suggested GitHub Topics

    nasa
    nasa-api
    neows
    asteroids
    near-earth-objects
    astronomy
    data-science
    machine-learning
    python
    fastapi
    gradio
    pandas
    scikit-learn
    data-visualization
    research

---

## Future Development

Potential future improvements include:

- Larger historical NeoWs datasets
- Automated dataset snapshots
- Advanced statistical testing
- Principal Component Analysis (PCA)
- Alternative clustering algorithms
- Cluster validation metrics
- Interactive 3D visualizations
- Time-series analysis
- Automated research reports
- Additional asteroid characteristics
- Improved reproducibility tools
- Publication-ready statistical outputs
- Dataset versioning

Potential future machine-learning experiments could include:

- Hierarchical clustering
- DBSCAN
- Gaussian mixture models
- Dimensionality reduction
- Cluster stability analysis

Any future model should continue to be treated as exploratory unless scientifically validated for a specific purpose.

---

## Project Goals

AstroRisk demonstrates how publicly available scientific data can be transformed into a reproducible computational research workflow.

The project combines:

    NASA Data
        +
    Python
        +
    Statistics
        +
    Data Visualization
        +
    Machine Learning
        +
    Interactive Web Development
        =
    AstroRisk

---

## Author

### Eva J. Patel

**Author & Developer — AstroRisk**

AstroRisk was created as an independent research and software-development project exploring NASA near-Earth object data through Python, statistical analysis, visualization, and machine learning.

---

## Acknowledgments

Data used by AstroRisk is obtained through NASA's public Near Earth Object Web Service (NeoWs).

This project is an independent implementation and is not affiliated with or endorsed by NASA or JPL.

---

## Project Status

**Active Research & Development**

AstroRisk is an evolving research project. Analytical methods, visualizations, and implementation details may change as the project develops.

---

**AstroRisk — Developed by Eva J. Patel**
