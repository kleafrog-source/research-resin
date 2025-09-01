# Resin Simulation Application Setup

This guide will help you set up and run the Resin Simulation application on your local machine.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

## Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd research-resin
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Access the application**:
   Open your web browser and navigate to `http://localhost:8501`

## Project Structure

```
research-resin/
├── src/                     # Source code
│   ├── models/             # Data models and enums
│   ├── core/               # Core simulation logic
│   └── ui/                 # User interface components
│       └── pages/          # Application pages
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
└── SETUP.md               # This file
```

## Development

### Adding New Features

1. **New Ion Types**:
   - Add new ion types to `src/models/firmware.py`
   - Create corresponding semantic functions in `src/core/semantics.py`

2. **New UI Pages**:
   - Create a new file in `src/ui/pages/`
   - Import and register the page in `src/ui/__init__.py`

### Testing

To run tests (when available):
```bash
pytest tests/
```

## Troubleshooting

- **Module Not Found Errors**: Ensure your virtual environment is activated and all dependencies are installed
- **Port Already in Use**: Change the port with `streamlit run app.py --server.port 8502`
- **Performance Issues**: For large simulations, consider increasing the Streamlit memory limit with `--server.maxUploadSize=1024`

## License

This project is proprietary and confidential. All rights reserved.
