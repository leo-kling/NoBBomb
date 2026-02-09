#!/bin/bash
#MISE alias=["fmt","format"]
#MISE description="Format code using predefined style guidelines"

isort src/*

black src/*

pylint src/*