import logging
import argparse
from src import create_configurations, arguments_validation
from src.services import utils


def main(config):
    logging.debug(f"I'm starting, get ready to fly!")
    logging.info(f"[START_TIMESTAMP]: {config.START_TIMESTAMP} - [END_TIMESTAMP]: {config.END_TIMESTAMP}")
    logging.info(f"[STEP]: Loading datasets - STARTED")
    batch_registry_df = utils.load_df_from_csv(config.BATCH_REGISTRY_FILE_PATH)
    cooking_metrics_df = utils.load_df_from_csv(config.COOKING_METRICS_FILE_PATH)
    faulty_intervals_df = utils.load_df_from_csv(config.FAULTY_INTERVALS_FILE_PATH)
    logging.info(f"[STEP]: Loading datasets - [RESULT]: COMPLETED")
    logging.debug(batch_registry_df.to_markdown())
    logging.debug(cooking_metrics_df.to_markdown())
    logging.debug(faulty_intervals_df.to_markdown())
    for kitchen in config.COMBINATION_TO_COMPUTE['k']:
        for machine in config.COMBINATION_TO_COMPUTE[kitchen]:
            for arepas in config.COMBINATION_TO_COMPUTE[machine]:
                logging.info(f"[STEP]: Filtering dataframes for combination {kitchen}, {machine}, {arepas} - STARTED")
                br_df, cm_df, fi_df = utils.filter_datasets(machine, arepas,
                                                            batch_registry_df,
                                                            cooking_metrics_df,
                                                            faulty_intervals_df)
                logging.info(f"[STEP]: Filtering dataframes for combination {kitchen}, {machine}, {arepas} - [RESULT]: COMPLETED")
                cm_df = utils.remove_faulty_intervals(cm_df, fi_df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start-timestamp", help="Start timestamp")
    parser.add_argument("-e", "--end-timestamp", help="End timestamp")
    args = parser.parse_args()
    args = arguments_validation(args)
    config = create_configurations(args)
    logging.info("Pirelli Data Challenge setup completed")

    main(config)
