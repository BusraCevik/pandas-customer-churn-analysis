import os
from src.data_preparation import prepare_data
from src.feature_engineering import create_feature_dataset
from src.churn_analysis import compute_churn_metrics
from src.visualization import generate_visualizations
from src.dashboard import build_churn_dashboard




BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
DATA_DIR = os.path.join(BASE_DIR, 'data')
DOC_DIR = os.path.join(BASE_DIR, 'docs', 'index.html')


RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw', "dataset.csv")
CLEANED_DATA_PATH = os.path.join(DATA_DIR, 'cleaned', "cleaned.csv")
FEATURED_DATA_PATH = os.path.join(DATA_DIR, 'featured', "featured.csv")


DATA_PREPARATION_PATH = os.path.join(SRC_DIR, 'data_preparation.py',)
FEATURE_ENGINEERING_PATH = os.path.join(SRC_DIR, 'feature_engineering.py',)
CHURN_ANALYSIS_PATH = os.path.join(SRC_DIR, 'churn_analysis.py',)
VISUALIZATION_PATH = os.path.join(SRC_DIR, 'visualization.py',)

FIGURE_PATH = os.path.join( OUTPUT_DIR, 'figures')
CSV_PATH = os.path.join(OUTPUT_DIR, "csv")

def main():

    prepare_data(RAW_DATA_PATH, CLEANED_DATA_PATH)
    create_feature_dataset(CLEANED_DATA_PATH, FEATURED_DATA_PATH)
    compute_churn_metrics(FEATURED_DATA_PATH, CSV_PATH)
    generate_visualizations(CSV_PATH, FIGURE_PATH)
    build_churn_dashboard(CSV_PATH, FEATURED_DATA_PATH, DOC_DIR)


if __name__ == "__main__":
    main()