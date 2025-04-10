# This script is adapted from [How to Make a Gantt Chart in Python with Matplotlib]
# Original source: https://www.datacamp.com/tutorial/how-to-make-gantt-chart-in-python-matplotlib
# Modifications have been made to expand the features and customize functionality.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import datetime as dt
import argparse

def week_to_day(week_number, year, offset_day):
    first_day_of_year = pd.to_datetime(f'{year}-01-01')
    start_of_week = first_day_of_year + pd.DateOffset(weeks=week_number - 1, weekday=6)
    day_of_the_week = start_of_week + pd.Timedelta(days=offset_day)
    return day_of_the_week


def expand_features(df, year):
    df['start_day'] = df['start'].apply(week_to_day, year=year, offset_day=-6)
    df['end_day'] = df['end'].apply(week_to_day, year=year, offset_day=-2)
    df['relative_start_day'] = (df['start_day'] - df['start_day'].min()).dt.days
    df['relative_end_day'] = (df['end_day'] - df['start_day'].min()).dt.days
    df['task_duration'] = df['relative_end_day'] - df['relative_start_day'] + 1
    df['completion_days'] = (df['completion_percentage'] / 100) * df['task_duration']
    df['combined_label'] = df.apply(lambda row: f"{row['label']}. {row['task']}", axis=1)

    return df


def load_checkpoints(input_file):
    check_points = pd.read_excel(input_file, sheet_name='checkpoints')
    check_points['color'] = 'r'
    check_points['offset'] = -2
    new_row = pd.DataFrame({
        'week_number': [pd.Timestamp.now().isocalendar()[1] - 1],
        'description': ['Today'],
        'alpha': [1],
        'color': ['grey'],
        'offset': [0]
    })
    check_points = pd.concat([check_points, new_row], ignore_index=True)

    return check_points


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Gantt chart from an excel file.")
    parser.add_argument('--input', type=str, required=False, default='input.xlsx',
                        help='Path to the Excel file containing task data')
    parser.add_argument('--output', type=str, required=False, default='gantt_chart.png',
                        help='Path to save the generated Gantt chart image')
    parser.add_argument('--year', type=int, required=False, default=2025, 
                        help='The current year')
    parser.add_argument('--title', type=str, required=False, default='Timeline for xxx Project',
                        help='Title for the Gantt chart')
    parser.add_argument('--fig_width', type=int, required=False, default=18,
                        help='Width of the figure in inches')
    parser.add_argument('--fig_height', type=int, required=False, default=6,
                        help='Height of the figure in inches')
    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    # Load the arguments
    input_file = args.input
    output_file = args.output
    year = args.year
    plot_title = args.title
    fig_size = (args.fig_width, args.fig_height)

    # Load the checkpoints
    check_points = load_checkpoints(input_file)

    # Load the status
    df = pd.read_excel(input_file, sheet_name='status')
    df = expand_features(df, year)

    # Styling
    colors = ['tomato', 'indianred', 'mediumpurple', 'royalblue', 'steelblue', 'mediumturquoise', 'lightgreen', 'yellowgreen', 'khaki']
    wps = df['work_package'].unique()
    wp_colors = {wp: colors[i % len(colors)] for i, wp in enumerate(wps)}

    # Xticks
    xtick_end = max(df['end_day'].max(), week_to_day(max(check_points['week_number']), year=year, offset_day=5))
    xtick_relative_end = (xtick_end - df['start_day'].min()).days
    xticks = np.arange(0, xtick_relative_end + 2, 7)
    xticklabels = pd.date_range(start=df['start_day'].min() + dt.timedelta(days=4),
                                end=xtick_end
                                ).strftime('%d/%m')
    
    # Patches
    patches = []
    for wp in wps:
        patches.append(Patch(color=wp_colors[wp]))

    # Plotting
    fig, ax = plt.subplots(figsize=fig_size)
    for _, row in df.iterrows():
        ax.barh(y=row['combined_label'],
                width=row['task_duration'],
                left=row['relative_start_day'],
                color=wp_colors[row['work_package']],
                alpha=0.4
                )
        ax.barh(y=row['combined_label'],
                width=row['completion_days'],
                left=row['relative_start_day'],
                color=wp_colors[row['work_package']],
                )
        ax.text(x=row['relative_start_day'] + row['completion_days'] + 1,
                y=row['combined_label'],
                s=f"{row['completion_percentage']}%",
                fontsize=8,
                va='center',
                ha='left',
                color='black'
                )
        ax.text(x=row['relative_start_day'] + row['task_duration'] + 4,
                y=row['combined_label'],
                s=row['current_status'] if pd.notna(row['current_status']) else '',
                va='center',
                ha='left',
                color='black',
                fontsize=7,
                alpha=0.8
                )
        
    plt.title(plot_title, fontsize=15)
    plt.gca().invert_yaxis()
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels[::7])
    ax.xaxis.grid(True, alpha=0.5)
    ax.legend(handles=patches, labels=wp_colors.keys(), fontsize=11)

    for _, row in check_points.iterrows():
        week, des, alpha, c, o = row
        delivery_date = (week_to_day(week_number=week, year=year, offset_day=o) - df['start_day'].min()).days
        ax.axvline(x=delivery_date, color=c, linestyle='dashed', alpha=alpha)
        ax.text(x=delivery_date, y=9.5, s=des, color=c, alpha=alpha)

    plt.savefig(output_file, bbox_inches='tight')


if __name__ == "__main__":
    main()