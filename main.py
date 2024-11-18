import argparse
import pandas as pd
import sys
import os
import logging

logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")

def read_csv_to_dataframe(input_path):
    # read csv-file into a pandas Dataframe for further customizations
    df = pd.read_csv(input_path)
    return df

def filter_df(df, columns_to_keep):
    # Get the header from the csv-file as a list and compare with columns_to_keep
    header = list(df.columns)
    invalid_columns = [col for col in columns_to_keep if col not in header]

    #check if there are any invalid columns and stop script with error if there are any
    if invalid_columns:
        logging.error(f"The list of columns contain invalid column-names: {invalid_columns}")
        sys.exit(1)
    else:
        # filter Dataframe to only include columns that are shown in the list of columns
        filtered_df = df.filter(columns_to_keep)
        return filtered_df

def format_df(df, format):
    #convert Timestamp to datetime type to be able to format it
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # format Timestamp to match chosen format
    if format == "seconds":
        print("chosen Timestamp format: ", format)
        df["Timestamp"] = df["Timestamp"].dt.strftime('%H:%M:%S')
    elif format == "minutes":
        print("chosen Timestamp format: ", format)
        df["Timestamp"] = df["Timestamp"].dt.strftime('%H:%M')

    return df

def write_dataframe_to_csv(df,output_path):
    # write the DataFrame back to a CSV file
    df.to_csv(output_path, index=False)

def main(args, filename):
    #create file_path to access csv-file
    input_path = os.path.join(args.input, filename)
    output_path = os.path.join(args.output, filename)

    # read csv into a Dataframe to be able to extract and format data
    df = read_csv_to_dataframe(input_path)

    #check columns argument if csv-file will be filtered for specific columns
    if args.columns == ['all']:
        formatted_df = format_df(df, args.format)
        write_dataframe_to_csv(formatted_df, output_path)

    else:
        filtered_df = filter_df(df, args.columns)
        formatted_df = format_df(filtered_df, args.format)
        write_dataframe_to_csv(formatted_df, output_path)
    

if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Read csv-files to extract and format needed data.")
    
    # Add arguments
    parser.add_argument('-i', '--input', type=str, required=True, help="Path to directory of used files.")
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to directory where formatted csv-file will be saved.')
    parser.add_argument('-c', '--columns', action='append', help="columns to be kept in cropped csv-file. If argument not set, all columns will be kept.")
    parser.add_argument('-f', '--format', type=str, default='standard', help="three modi available: standard removes date from Timestamp, seconds removes date and milliseconds and minutes removes date, milliseconds and seconds from Timestamp.")
    

    # Parse the arguments
    args = parser.parse_args()

    valid_formats = {"minutes", "seconds", "standard"}

    if args.format not in valid_formats:
        # format has been set to an invalid value
        logging.error(f"the format you have chosen is invalid: {args.format}")
        print("valid formats are: minutes, seconds, standard")
        sys.exit(1)

    csv_file = [f for f in os.listdir(args.input) if f.endswith('.csv')]

    if csv_file:
        filename = csv_file[0]
    else:
        logging.error(f"No CSV files found in the directory.")
        sys.exit(1)

    output_folder = args.output

    #check if output folder exists and if not, create directory
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print("Output-directory created.")
    
    if "Timestamp" not in args.columns:
        if args.columns != ['all']:
            logging.error(f"you need to include the 'Timestamp' column into your -c argument.")
            sys.exit(1)
    # Pass the arguments to the main function
    main(args, filename)
