import pytest
import app
import os
import yaml

def test_yamlfile():
    with open("process_file.yml", "r") as ymlfile:
        params = yaml.safe_load(ymlfile)
    assert params == app.file_params

def test_working_dir():
    cwd = os.getcwd()
    assert(app.app.config["WORKING_DIR"] == cwd)

def test_process_file():
    # assert app.process_excel_js("Something") == 0
    assert app.process_excel_js("Research_Calls") == 0