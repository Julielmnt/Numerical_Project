# Google Earth engine Streamlit interface : Glourbinterface

## Summary
This is a project to implement an interface for the [GloUrb](https://glourb.universite-lyon.fr/) project. This is a multidisciplinary project studying the effect of urbanization on alluvial plains. They use [Google Earth Engine](https://earthengine.google.com/) to study the evolution of different parameters such as vegetation indices or water indices over time, using data from satellites.
Samuel Dunesme and Barbara Belletti have been extracting their metrics using python : this is the [GloUrbEE](https://github.com/EVS-GIS/glourbee) project, which a lot of the code presented here relies on. Since a lot of the colllaborators of the project aren't used to programming, Glourbinterface has the goal of providing an interface for them to extract their data without diving into code. 

## Usage
You first need to clone the github repository. 

#### Create an environment (recommanded)
Create a [python](https://docs.python.org/3/library/venv.html) (or conda) environment and activate it. 
Then upgrade your pip :

```bash
python -m pip install --upgrade pip
```

#### Install the libraries
Then install the libraries required for the Gloourbinterface, from requirements.txt : 

```bash
pip install -r requirements.txt
```


### Option 1 : create your package :
#### Build
upgrade your build if needed : 

```bash
pip install build --upgrade
```

build the glourbinterface package :

```bash
python -m build
```

and install it :
```bash
pip install -e .
```

#### Use your package
from the directory of the project you can now just type :

```bash
glourbinterface
```
And here is your app !


### Option 2 : use Streamlit command
from the directory of the project you can type :

```bash
Streamlit run .\src\HomePage.py
```
And here is your app !