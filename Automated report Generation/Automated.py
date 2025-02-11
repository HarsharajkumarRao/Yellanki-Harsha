from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import os

def read_data(file_path):
    """Reads data from a CSV file and returns a DataFrame."""
    if not os.path.exists(file_path):  # Check if the file exists
        raise FileNotFoundError(f"The file {file_path} was not found.")
    return pd.read_csv(file_path)  # Read and return the CSV data as a DataFrame

def analyze_data(df):
    """Performs basic analysis on the DataFrame."""
    summary = df.describe()  # Generate summary statistics of the dataset
    return summary

def generate_pdf_report(summary, output_file):
    """Generates a PDF report using ReportLab."""
    c = canvas.Canvas(output_file, pagesize=letter)  # Create a new PDF canvas
    width, height = letter  # Get page dimensions
    
    # Set font and title of the report
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Automated Data Analysis Report")
    c.setFont("Helvetica", 12)
    y_position = height - 80  # Initial Y position for text
    
    for col in summary.columns:
        c.drawString(50, y_position, f"Summary statistics for {col}")  # Column title
        y_position -= 20
        c.setFont("Helvetica", 10)
        stats = summary[col].to_string().split("\n")  # Convert statistics to list
        for stat in stats:
            c.drawString(60, y_position, stat)  # Print each stat in the report
            y_position -= 15
        y_position -= 10
        c.setFont("Helvetica", 12)
        
        # Start a new page if the Y position is too low
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50
    
    c.save()  # Save the PDF file

def main():
    input_file = "sample_data.csv"  # Change this to your actual file
    output_file = "report_lab.pdf"
    
    try:
        df = read_data(input_file)  # Read the data
        summary = analyze_data(df)  # Analyze the data
        generate_pdf_report(summary, output_file)  # Generate the PDF report
        print(f"Report generated successfully: {output_file}")
    except FileNotFoundError as e:
        print(e)  # Print an error message if the file is not found

if __name__ == "__main__":
    main()  # Execute the main function
