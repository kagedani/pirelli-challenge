import pandas
import logging


def load_df_from_csv(file_path):
    try:
        return pandas.read_csv(file_path, sep=';')
    except RuntimeError as e:
        raise RuntimeError(f"Error loading csv file {file_path}, {e}")


def filter_datasets(machine, arepas, br_df, cm_df, fi_df):
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
    faulty_intervals = list(zip(fi_df['start_time'], fi_df['end_time']))
    logging.debug(f"List of faulty_intervals: {faulty_intervals}")
    for (start, end) in faulty_intervals:
        logging.debug(f"[FAULTY START TIME]: {start}, [FAULTY END TIME]: {end}")
        cm_df = cm_df.drop(cm_df[(cm_df.timestamp >= start) & (cm_df.timestamp <= end)].index)
    logging.debug(f"Cooking metrics without faulty intervals: \n{cm_df.to_markdown()}")
    return cm_df


