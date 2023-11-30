import pytest
import app
import os

def test_working_dir():
    cwd = os.getcwd()
    assert(app.file_params["working_dir"] == cwd)
