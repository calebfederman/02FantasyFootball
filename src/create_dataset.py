#-------------------------------------------------------------------------------------------------#
# create_dataset.py calls the functions to scrape and clean the dataset in order to have
# clean data for analysis
#
# Author: Caleb Federman
#-------------------------------------------------------------------------------------------------#

import scrape_dataset
import clean_dataset

scrape_dataset.create_raw_csvs()
clean_dataset.clean_data()
