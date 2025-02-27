import filecmp
from pathlib import Path

import pandas as pd

import src.analysis.ml as ml

INPUT_DIR = 'test/ml/input/'
OUT_DIR = 'test/ml/output/'
EXPECT_DIR = 'test/ml/expected/'


class TestML:
    @classmethod
    def setup_class(cls):
        """
        Create the expected output directory
        """
        Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    def test_summarize_networks(self):
        dataframe = ml.summarize_networks([INPUT_DIR + 'test-data-s1/s1.txt', INPUT_DIR + 'test-data-s2/s2.txt', INPUT_DIR + 'test-data-s3/s3.txt',
                                           INPUT_DIR + 'test-data-longName/longName.txt', INPUT_DIR + 'test-data-longName2/longName2.txt',
                                           INPUT_DIR + 'test-data-empty/empty.txt', INPUT_DIR + 'test-data-spaces/spaces.txt'])
        dataframe.to_csv(OUT_DIR + 'dataframe.csv')
        assert filecmp.cmp(OUT_DIR + 'dataframe.csv', EXPECT_DIR + 'expected-dataframe.csv')

    def test_pca(self):
        dataframe = ml.summarize_networks([INPUT_DIR + 'test-data-s1/s1.txt', INPUT_DIR + 'test-data-s2/s2.txt', INPUT_DIR + 'test-data-s3/s3.txt'])
        ml.pca(dataframe, OUT_DIR + 'pca.png', OUT_DIR + 'pca-variance.txt',
               OUT_DIR + 'pca-coordinates.csv')
        coord = pd.read_table(OUT_DIR + 'pca-coordinates.csv')
        coord = coord.round(5)  # round values to 5 digits to account for numeric differences across machines
        expected = pd.read_table(EXPECT_DIR + 'expected-pca-coordinates.csv')
        expected = expected.round(5)

        assert coord.equals(expected)

    def test_hac_horizontal(self):
        dataframe = ml.summarize_networks([INPUT_DIR + 'test-data-s1/s1.txt', INPUT_DIR + 'test-data-s2/s2.txt', INPUT_DIR + 'test-data-s3/s3.txt'])
        ml.hac_horizontal(dataframe, OUT_DIR + 'hac-horizontal.png', OUT_DIR + 'hac-clusters-horizontal.txt')

        assert filecmp.cmp(OUT_DIR + 'hac-clusters-horizontal.txt', EXPECT_DIR + 'expected-hac-horizontal-clusters.txt')

    def test_hac_vertical(self):
        dataframe = ml.summarize_networks([INPUT_DIR + 'test-data-s1/s1.txt', INPUT_DIR + 'test-data-s2/s2.txt', INPUT_DIR + 'test-data-s3/s3.txt'])
        ml.hac_vertical(dataframe, OUT_DIR + 'hac-vertical.png', OUT_DIR + 'hac-clusters-vertical.txt')

        assert filecmp.cmp(OUT_DIR + 'hac-clusters-vertical.txt', EXPECT_DIR + 'expected-hac-vertical-clusters.txt')

