# Installation Guide: Research Resin - Ion Exchange Analysis

This guide provides step-by-step instructions for setting up and running the Research Resin application on your local machine.

## Prerequisites

- Python 3.8 or higher
- `pip` (Python package manager)
- `git` (for cloning the repository)

## Installation Steps

1. **Clone the Repository:**
   Open your terminal or command prompt and run the following command to clone the repository:
   ```bash
   git clone https://github.com/kleafrog-source/research-resin.git
   cd research-resin
   ```

2. **Create a Virtual Environment (Recommended):**
   A virtual environment helps manage project dependencies and avoids conflicts.

   - **On Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

   - **On macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   Install the required Python packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Application:**
   Once the dependencies are installed, run the following command to start the Streamlit server:
   ```bash
   streamlit run app.py
   ```

2. **Access in Your Browser:**
   Open your web browser and navigate to the following URL:
   [http://localhost:8501](http://localhost:8501)

## Key Dependencies

The project relies on the following major libraries:
- `streamlit`
- `numpy`
- `pandas`
- `scipy`
- `scikit-learn`
- `matplotlib`
- `plotly`
- `pydantic`
- `joblib`
- `seaborn`
