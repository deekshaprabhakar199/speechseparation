import argparse
from num2words import num2words
import pandas as pd
import re

# Canonicalizes transcripts
# converts to lower case
# will remove square brackets
# will convert numbers to words
# will remove punctuation

# wont handle times like 4:10 pm
# wont handle other subtext like (this) or <this> or {this}

def number_replace(x):
    number = x.group(1)
    extract_num = re.findall(r'\d+', number)[0]
    ret = re.sub('-', ' ', num2words(extract_num)) # 25 is output as twenty-five; turn the '-' to a ' '
    return ret

def ordinal_replace(x):
    number = x.group(1)
    extract_num = re.findall(r'\d+', number)[0]
    return num2words(extract_num, ordinal=True)

def canonicalize(ser):
    # print(ser.head())
    
    # convert to lower case
    ser=ser.str.lower()

    # remove commentary
    ser=ser.str.replace(r"\[.*\]","")

    # convert ordinal numbers to words
    ser=ser.str.replace(r'(\d+(st|nd|rd|th))', ordinal_replace)

    # remove special characters
    ser=ser.str.replace(r'[^A-Za-z0-9 ]+', '')
    
    # convert remaining numbers to words
    ser=ser.str.replace(r'(\d+)', number_replace)

    # remove leading whitespace
    ser=ser.str.strip()

    # remove filler words. '\b' matches to word boundary so we can get the beginning and end of the transcript
    ser=ser.str.replace(r'(\bah\b|\buh\b|\bhm\b|\bhmm\b|\bagh\b|\buhm\b|\bum\b)', '')

    # show the output
    # print(ser.head())
    return ser


def loop_clean(df, cols):
    # loop through columns specified and check if they're actually in the dataframe
    # if so, then perform the cleaning
    for col in cols:
        print(col)
        if col not in df.columns:
            print("{} is not in the dataframe, check the spelling".format(col))
            exit()
        df[col]=canonicalize(df[col])

    return df

def __main__():
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding arguments
    parser.add_argument("file", help = "Specify csv to process")
    parser.add_argument("output", help = "Specify file for output")
    parser.add_argument('-s', '--separator', nargs=1, default=',', help="Specify column separator. Ex: -s ',' (default separator = ',')")
    parser.add_argument('-e', '--exclude-list', nargs='+', default=[], help="Specify columns to exclude from processing. Ex: '-e col1 col2 col3'")
    parser.add_argument('-i', '--include-list', nargs='+', default=[], help="Specify the columns to include for processing. Ex: '-i col1 col2 col3")
     
    # Read arguments from command line
    args = parser.parse_args()
    sep = args.separator[0]

    # Open file
    df=pd.read_csv(args.file, sep=sep)

    # check that exclude and include are not simultaneously specified
    # then convert an exclude list into an include list
    process_cols=args.include_list
    if args.exclude_list:
        if args.include_list:
            print('Only the include or exclude should be specified')
            exit()
        else:
            process_cols=list(set(df.columns) - set(args.exclude_list))
    else:
        if not args.include_list:
            print('Either the include or exclude should be specified')
            exit()



    # Loop through columns and clean them
    df=loop_clean(df, process_cols)

    # Write new file
    df.to_csv(args.output, index=False, sep=sep)


if __name__ == '__main__':
    __main__()
