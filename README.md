# CSV Formatter

## Description
This Python script is designed to read CSV files, filter specific columns, and format the Timestamp column based on user-specified configurations. The tool leverages the pandas library for data manipulation and provides a flexible way to handle CSV data programmatically.

## Features
- Reads a CSV file from a specified input directory.
- Filter the Dataframe to include specified columns.
- Format the Timestamp column into one of three formats: 
	- Standard: removes the date from Timestamp
	- Seconds: removes the date and milliseconds
	- Minutes: removes the date, milliseconds and seconds
- Writes the formatted Dataframe back to a CSV file in the output directory.
- Automatically validates input arguments and directories.
- Creates the output directory if it does not exist.

## Prerequisites: 
- Python 3.6+
- Required Python libraries: 
	- pandas
Install the required library using: pip install pandas

## Usage
Run the script using following arguments: 
-i <input_directory>
-o <output_directory>
-c <columns_to_keep>
-f <format>

### Arguments: 
-i, --input: Path to the input directory containing the CSV file.
-o, --output: Path to the output directory where the formatted CSV file will be saved. 
-c, --columns: Columns to be kept in resulting CSV file. Use multiple -c flags for each column: -c Timestamp -c Tool -c "NC Program"
Note: 
- when there is a blank space in the column name use " to make sure it's seen as one argument
- if you want to keep all columns in the CSV file use -c all
-f, --format: Format for the Timestamp column. 
Options:
- standard: removes the date from the Timestamp. 
- seconds: removes the date and milliseconds. 
- minutes: removes the date, milliseconds and seconds. 
Default setting if not set in argument list: standard

## Examples
1. Format a CSV file and keep all columns
-i <input_directory> -o <output_directory> -f standard
Note: argument -f is optional and will be set to standard by default.

2. Filter specific columns and remove milliseconds from Timestamp
-i <input_directory> -o <output_directory> -c Timestamp -c Tool -c "NC Program" -c "Spindle Speed" -f seconds

3. Handle missing output directory
-i <input_directory> -o <new_output_directory> -f standard
Note: the script will create the output directory if it does not already exist.

## Validation and Error Handling
- the script ensures that the -i and -o directories exist or creates the output directory if needed.
- Validates that the Timestamp column is included in filtered columns if filtering is applied. 
- Stops execution and logs an error if: 
	- No CSV files are found in the input directory.
	- Invalid column names are provided. 
	- an invalid format is specified for the -f argument. 

## Script Workflow
1. Input directory
reads the first CSV file from the specified input directory. 
2. Validation
validates columns names against the header of the CSV file and checks if Timestamp column is included. 
3. Data Processing
Filters and formats the Dataframe based on user specifications.
4. Output
writes the processed Dataframe back to the specified output directory as a CSV file. 

## Example Output
### Input file
Timestamp,Tool,NC Program
2023-11-13 10:31:00.120,Drill,Program1
2023-11-13 15:45:00.094,Lathe,Program2

### Command
-i input_directory/example.csv -o output_directory/formatted.csv -c Timestamp -c Tool -f minutes

### Output file
Timestamp,Tool
10:31,Drill
15:45,Lathe

## Logging
Errors and warnings are logged using Python's logging module: 
- Invalid column names or formats.
- Missing Timestamp column in specified column list.
- No CSV files in input directory.