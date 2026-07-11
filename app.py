import subprocess
import os
import sys

def main():
    """
    Entry point for the application.
    This script simply launches the Streamlit dashboard.
    """
    print("Starting LangGraph Multi-Agent SQL Assistant Dashboard...")
    
    ui_path = os.path.join(os.path.dirname(__file__), 'ui', 'streamlit_app.py')
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", ui_path])
    except KeyboardInterrupt:
        print("\nShutting down dashboard.")

if __name__ == "__main__":
    main()
