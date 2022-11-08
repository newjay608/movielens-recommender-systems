import pandas as pd
import numpy as np
from pathlib import Path
import click
import logging
from dotenv import find_dotenv, load_dotenv


class FeatureBuilder:

    # @click.command()
    # @click.argument('input_filepath', type=click.Path(exists=True))
    # @click.argument('output_filepath', type=click.Path())
    def __init__(self, input_filepath="~/Data/MovieLens/raw/", output_filepath="~/Data/MovieLens/processed/"):
        if len(input_filepath) > 0:
            self.READ_FILE_PATH = input_filepath
        if len(output_filepath) > 0:
            self.WRITE_FILE_PATH = output_filepath
        self.logger = logging.getLogger(__name__)
        self.GENRES = []

    def build_movie_features(self):
        try:
            logger = self.logger
            logger.info('building movies dataset features')
            logger = logging.getLogger(__name__)
            movies = pd.read_csv(self.READ_FILE_PATH +
                                 'movie.csv')

            # drop duplicate rows in the movies dataframe
            movies.drop_duplicates(inplace=True)

            # add year column to the data frame
            movies['Year'] = movies['title'].str.extract(
                '.*\((.*)\).*', expand=False)

            # remove year from the
            movies['title'] = movies['title'].str.extract(
                '([^(]*)', expand=False)

            # find all genres in the movies
            for g in range(len(movies.genres)):
                for genre in movies.genres[g].split('|'):
                    if genre not in self.GENRES:
                        self.GENRES.append(genre)

            self.GENRES = list(map(lambda x: x.replace(
                '(no genres listed)', 'No_genres'), self.GENRES))
            # add genres column
            for x in self.GENRES:
                movies[x] = 0
            # rename no genres column
            # movies = movies.rename(
            #   columns={"(no genres listed)": "no_genres", "title": "Title"}, errors="raise")

            # encode genres column for each movie
            for g in range(len(self.GENRES)):
                for genre in movies.genres[g].split('|'):
                    # movies[genre][g] = 1
                    movies.loc[g, genre] = 1
            # drop genres column
            movies.drop(columns=['genres'], inplace=True)
            movies.to_csv(self.WRITE_FILE_PATH + 'movies_processed.csv')
            logger.info('done! building movies dataset features')

        except BaseException as e:
            logger.exception(e)
            print("An error has occured")


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    featureBuilder = FeatureBuilder()
    featureBuilder.build_movie_features()
