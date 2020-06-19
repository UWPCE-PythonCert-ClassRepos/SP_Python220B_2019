# pylint: disable=C0103,E1101
'''
Be sure
'''
import pandas as pd

# https://realpython.com/python-csv/#reading-csv-files-with-pandas
# https://realpython.com/pandas-groupby/
# https://stackoverflow.com/questions/30405413/python-pandas-extract-year-from-datetime-dfyear-dfdate-year-is-not


def good_job(filename):
    '''sdfsdf'''
    df = pd.read_csv(filename,
                     index_col='guid',
                     parse_dates=['Hired'],
                     header=0,
                     names=['guid', 'a', 'b', 'c', 'd', 'Hired', 'AO'])
    df['Year'] = pd.DatetimeIndex(df['Hired']).year
    return df.groupby("Year")['AO'].count()


def main():
    '''Main module launch function'''
    filename = "data/exercise.csv"
    print(good_job(filename))


if __name__ == "__main__":
    main()
