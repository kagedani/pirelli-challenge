import pandas
import logging
import numpy as np


def load_df_from_csv(file_path):
    """
    :param file_path: path where to load the csv from
    :return: a pandas dataframe with the csv content
    """
    try:
        return pandas.read_csv(file_path, sep=';', header=0)
    except RuntimeError as e:
        raise RuntimeError(f"Error loading csv file {file_path}, {e}")


def filter_datasets(machine, arepas, br_df, cm_df, fi_df):
    """
    :param machine: machine selected to perform the computation on
    :param arepas: arepa type selected to perform the computation on
    :param br_df: batch registry dataframe
    :param cm_df: cooking metrics dataframe
    :param fi_df: faulty intervals dataframe
    :return: the three dataframe filtered with consistent data
    """
    fi_usefull_machine_df = fi_df.loc[fi_df['machine_id'] == machine]
    logging.debug(f"Filtered faulty intervals: \n{fi_usefull_machine_df.to_markdown()}")
    br_arepa_filtered_df = br_df.loc[br_df['arepa_type'] == arepas]
    logging.debug(f"Filtered batch registries: \n{br_arepa_filtered_df.to_markdown()}")
    list_of_batch_with_arepa_type_searched = br_arepa_filtered_df['batch_id'].values.tolist()
    logging.debug(f"List of batches considered: {list_of_batch_with_arepa_type_searched}")
    cm_batch_filtered_df = cm_df.loc[cm_df['batch_id'].isin(list_of_batch_with_arepa_type_searched)]
    logging.debug(f"Filtered cooking metrics: \n{cm_batch_filtered_df.to_markdown()}")
    return br_arepa_filtered_df, cm_batch_filtered_df, fi_usefull_machine_df


def remove_faulty_intervals(cm_df, fi_df):
    """
    Remove faulty interval rows from cooking metrics dataframe
    :param cm_df: cooking metrics dataframe
    :param fi_df: faulty intervals dataframe
    :return: cooking metrics dataframe with faulty row removed
    """
    faulty_intervals = list(zip(fi_df['start_time'], fi_df['end_time']))
    logging.debug(f"List of faulty_intervals: {faulty_intervals}")
    for (start, end) in faulty_intervals:
        logging.debug(f"[FAULTY START TIME]: {start}, [FAULTY END TIME]: {end}")
        cm_df = cm_df.drop(cm_df[(cm_df.timestamp >= start) & (cm_df.timestamp <= end)].index)
    logging.debug(f"Cooking metrics without faulty intervals: \n{cm_df.to_markdown()}")
    return cm_df


def convert_metrics_column_to_numeric(metrics_list, cm_df):
    """
    :param metrics_list: list of metrics to convert into numeric data type
    :param cm_df: cooking metrics dataframe
    :return: cooking metrics dataframe with converted metric columns
    """
    comma = ","
    dot = "."
    for metric in metrics_list:
        logging.debug(f"Converting metric {metric} to numeric")
        cm_df[metric] = pandas.to_numeric(cm_df[metric].str.replace(comma, dot, regex=True))

    return cm_df


def save_output(output_path, output_df):
    """
    :param output_path: destination path with filename to save the output df at
    :param output_df: the output structure
    :return: -
    :raise RuntimeError if there is any problem writing the file. E.g. file path not found
    """
    try:
        output_df.to_csv(output_path)
    except RuntimeError as e:
        raise RuntimeError(f"Error writing csv file {output_path}, {e}")


