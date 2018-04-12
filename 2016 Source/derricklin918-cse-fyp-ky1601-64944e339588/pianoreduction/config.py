# ===================
# module: config.py
# description: basic configuration of the project
# ===================
import os

# the absolute path to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# the absolute path to piano reduction package
LIB_DIR = os.path.join(PROJECT_ROOT, "pianoreduction")
# the absolute path to ./xml_scores
SCORE_DIR = os.path.join(PROJECT_ROOT, "xml_scores")
# the absolute path to ./archive
ARCHIVE_DIR = os.path.join(PROJECT_ROOT, "archive")
# the absolute path to ./log
LOG_DIR = os.path.join(PROJECT_ROOT, "log")
# the absolute path to ./tonalanalysis
TONE_DIR = os.path.join(PROJECT_ROOT, "tonalanalysis")
# the absolute path to datasets for flow model
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
# the absolute path to saved neural network reduction models
MODELS_DIR = os.path.join(PROJECT_ROOT, "saved_reduction_models")

# shortcut paths for unit testing event analyzer
# the absolute path to test scores
TEST_SCORES_DIR = os.path.join(SCORE_DIR, "test_scores")
# the absolute path to test score correct reference data
TEST_SCORES_CORRECT_DATA_DIR = os.path.join(TEST_SCORES_DIR, "correct_results")

# temporary folder directory
TEMP_DIR = os.path.join(PROJECT_ROOT, "temp")

if __name__ == "__main__":
    print("Project root directory: ", PROJECT_ROOT)
    print("Library directory: ", LIB_DIR)
    print("XML scores directory: ", SCORE_DIR)
    print("Archive directory: ", ARCHIVE_DIR)
    print("Log directory: ", LOG_DIR)
    print("Tonal analysis directory: ", TONE_DIR)
    print("Flow dataset directory: ", DATA_DIR)
    print("Saved reduction model directory: ", MODELS_DIR)
    print("Test scores directory: ", TEST_SCORES_DIR)
    print("Test scores sample correct result directory: ", TEST_SCORES_CORRECT_DATA_DIR)
    print("Temporary folder directory: ", TEMP_DIR)