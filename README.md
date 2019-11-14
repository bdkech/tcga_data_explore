# TCGA Data exploration tool

This repo contains the necessary code to build a docker image or host a Plotly Dash dashboard to explore TCGA-derived BRCA and OV data.  This tool allows you to filter and select genes to then observe their foldchanges in mRNA, protein, and CNV data.  It also allows you to see how well these features correlate within samples, and how they contributed in successfully classifying samples in either groups.


## Building docker image

To build the docker image simply :

```bash
make docker_build
```

in the project directory

## Local hosting

To host dashboard locally without using docker :

```
virtualenv my_env
source my_env/bin/activate
pip install -r requirements.txt
python src/dash_app.py
```

This will create a virtual environment 'my_env,' activate it, install the necessary requirements, and then host the app on port 8050
