"""Common functions and paths for this project."""

import os

ROOT_PATH = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))

DATASETS_PATH = os.path.join(ROOT_PATH, 'data', 'datasets')

assert os.path.isfile(os.path.join(ROOT_PATH, '.gitignore'))
