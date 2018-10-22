import os
import json


DATASETS_CONFIG_FOLDER = os.path.join("/".join(__file__.split("/")[:-1]),
                                        "..", "datasets-configs")
DATASETS_FOLDER = os.path.join(os.path.expanduser("~"),
                                ".datasets-data-fetcher")


def normalize_filename(filename):
    f_name = filename.split('/')[-1]
    f_name = f_name.split('?')[0]
    return f_name


def normalize_name(s):
    if s is None:
        return ''

    s = s.replace('.json', '')

    new_s = ''
    for c in s:
        if c in ' \t\n':
            new_s += '_'
        else:
            new_s += c
    return new_s


def get_config_dataset(datasetname):

    for config_file in os.listdir(DATASETS_CONFIG_FOLDER):
        cf = config_file.replace(".json", "")
        if cf != datasetname:
            continue

        config = None
        config_file = os.path.join(DATASETS_CONFIG_FOLDER, config_file)
        with open(config_file) as f:
            config = json.load(f)
        return config

    return None


def is_dataset_in_db(datasetname):

    datasetname = normalize_name(datasetname)

    folders = os.listdir(DATASETS_FOLDER)
    if datasetname in folders:
        dataset_folder = os.path.join(DATASETS_FOLDER, datasetname)
        files = os.listdir(dataset_folder)
        print(files)
        if files:
            return True
    return False


def get_datasets_with_tag(tag):
    if tag is None:
        return []

    dataset_names = []

    config_files = os.listdir(DATASETS_CONFIG_FOLDER)
    for cf in config_files:
        cf = os.path.join(DATASETS_CONFIG_FOLDER, cf)
        with open(cf) as f:
            config = json.load(f)

        tags = config.get("tags", [])
        if tag in tags:
            dataset_names.append(config["name"])

    return dataset_names


def update_datafetcher():
    """Updates datafetcher.
    Downloads and executes the "update.sh" script.
    """
    import subprocess

    bash_command = "cd $HOME && curl https://raw.githubusercontent.com/vinzeebreak/data-fetcher-install/master/update.sh -sSf | bash"
    output = subprocess.check_output(['bash','-c', bash_command])
