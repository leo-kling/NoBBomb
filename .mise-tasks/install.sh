#!/bin/bash
#MISE alias="i"
#MISE description="Install base uv/pip dependencies"

# Contributors Only
uv pip install -r pip/requirements.txt
uv pip install pylint==4.0.3
uv pip install isort==7.0.0
uv pip install black==25.11.0
uv pip install google-cloud-firestore==2.23.0
uv pip install google-cloud-bigquery==3.40.0
uv pip install google-cloud-aiplatform==1.133.0
uv pip install pytest==9.0.2
uv pip install pytest-sugar==1.1.1