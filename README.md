This is a FitPrediction model, where with the measurements how it will suit on an individual will be predicted. 



# Steps to follow:

## STEP 1

Create the virtual enviornment first

```
conda create -p venv python==3.11.8

``` 

## STEP 2

```
Create setup.py: It consists of the following.

1. Importing Modules: It imports necessary functions from the setuptools module for packaging and distribution purposes and also imports List from the typing module for type hinting.

2. Function Definition: Defines a function get_requirements that takes a file path as input and returns a list of requirements.

3. Reading Requirements File: The get_requirements function reads the contents of a requirements file specified by the file_path argument. It then processes each line, removing newline characters and appending each requirement to a list.

4. Package Setup: Sets up the package metadata for distribution using setuptools. It defines the name of the package (FitPrediction), author information, description, and author email. It also specifies the installation requirements using the install_requires parameter, where it calls the get_requirements function to dynamically fetch the dependencies from the requirements.txt file. Finally, it includes all found packages using find_packages().

```

## STEP 3 

```
Create README.md, .gitignore

```

## STEP 4

```
Create the structure of the pipeline:

src --> 
        Components -->
                    __init__.py
                    data_ingestion.py
                    data_transformation.py
                    model_trainer.py

        Pipeline -->
                    __init__.py
                    prediction_pipeline.py
                    train_pipeline.py
    __init__.py
    exception.py
    logger.py
    utils.py

```

