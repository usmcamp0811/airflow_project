import papermill as pm
import sys
import json
import yaml
import os


def get_yaml_params():
    try:
        with open("params.yaml", 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}


def get_args_params():
    args = sys.argv
    print(f"Args are {args}")
    if args is not None:
        try:
            return json.loads(args[1])
        except ValueError:
            print('Failed to parse args.')
            return {}
    return {}


def get_execution_id():
    try:
        return os.environ['EXECUTION_ID']
    except KeyError:
        return 0


execution_id = get_execution_id()
print(f"Execution id seems to be {execution_id}")

yaml_params = get_yaml_params()
print(f"Yaml params are {yaml_params}")

arg_params = get_args_params()
print(f"Arg Params are {arg_params}")

CODE_PATH = 'code.ipynb'
OUTPUT_PATH = f'output/code_{execution_id}.ipynb'
params = {**yaml_params, **arg_params}

pm.execute_notebook(CODE_PATH, OUTPUT_PATH, parameters=params, log_output=True, progress_bar=False)