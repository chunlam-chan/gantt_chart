# Gantt Chart

This script generates a Gantt chart from an Excel file. It is adapted from [How to Make a Gantt Chart in Python with Matplotlib](https://www.datacamp.com/tutorial/how-to-make-gantt-chart-in-python-matplotlib) and has been modified to expand the features and customize functionality.

## Features

- An Excel file with [template](/plan.xlsx).
- An example Gantt chart as follows.

![Alt text](/gantt_chart.png)

## Requirements

The script requires the following Python libraries:

- `pandas`
- `numpy`
- `matplotlib`
- `argparse`
- `openpyxl` (for reading Excel files)

## Usage

Run the script from the command line with the following options:
`python gen_gantt.py --input <input_file> --output <output_file> --year <year> --title <chart_title> --fig_width <width> --fig_height <height>`

Arguments
- input (optional): Path to the Excel file containing task data. Default: input.xlsx.
- output (optional): Path to save the generated Gantt chart image. Default: gantt_chart.png.
- year (optional): The current year. Default: 2025.
- title (optional): Title for the Gantt chart. Default: Timeline for xxx Project.
- fig_width (optional): Width of the figure in inches. Default: 18.
- fig_height (optional): Height of the figure in inches. Default: 6.

