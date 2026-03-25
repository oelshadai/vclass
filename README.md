# Malaria Epidemiology PDF Report Generator

A Flask-based web application that generates professional PDF reports from Jupyter notebook analysis of malaria epidemiology data in Ghana and Nigeria.

## Overview

This project converts malaria epidemiology analysis results into professionally formatted PDF reports using ReportLab. The system processes Jupyter notebook outputs and creates structured reports with charts, tables, and statistical summaries.

## Features

- **Automated PDF Generation**: Convert analysis results to professional PDF reports
- **Chart Integration**: Embed matplotlib visualizations directly in PDFs
- **Statistical Tables**: Format data tables with proper styling
- **Professional Layout**: Multi-page reports with headers, footers, and consistent formatting
- **REST API**: Simple endpoint for programmatic PDF generation
- **Error Handling**: Robust error handling with detailed logging

## Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Setup

1. **Clone or download the project files**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python -c "import reportlab; print('ReportLab installed successfully')"
```

## Usage

### Starting the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Generating PDF Reports

#### Via Web Interface
Navigate to `http://localhost:5000/generate-pdf` in your browser

#### Via API
```bash
curl -X POST http://localhost:5000/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{"title": "Custom Report Title"}'
```

#### Via Python Script
```python
import requests

response = requests.post('http://localhost:5000/generate-pdf', 
                        json={'title': 'Malaria Analysis Report'})

if response.status_code == 200:
    with open('report.pdf', 'wb') as f:
        f.write(response.content)
```

## Project Structure

```
school sasa report/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── test_pdf_api.py       # API testing script
├── README.md             # This file
└── generated_reports/    # Output directory (created automatically)
    └── *.pdf            # Generated PDF reports
```

## API Reference

### POST /generate-pdf

Generates a PDF report with malaria epidemiology analysis.

**Request Body** (JSON, optional):
```json
{
  "title": "Custom Report Title"
}
```

**Response**:
- **Success (200)**: PDF file download
- **Error (500)**: JSON error message

**Example Response Headers**:
```
Content-Type: application/pdf
Content-Disposition: attachment; filename=malaria_report_YYYYMMDD_HHMMSS.pdf
```

## Report Contents

The generated PDF includes:

1. **Title Page**
   - Report title and subtitle
   - Generation timestamp
   - Author information

2. **Executive Summary**
   - Key findings overview
   - Statistical highlights

3. **Data Analysis Sections**
   - Country-specific analysis (Ghana & Nigeria)
   - Comparative statistics
   - Trend analysis

4. **Visualizations**
   - Embedded charts and graphs
   - Data distribution plots
   - Correlation matrices

5. **Statistical Tables**
   - Formatted data summaries
   - Key metrics and indicators

## Configuration

### Customizing Report Content

Edit the `generate_pdf_report()` function in `app.py` to modify:
- Report sections
- Data sources
- Chart types
- Styling preferences

### PDF Styling

Key styling parameters in `app.py`:
```python
# Page settings
PAGE_WIDTH = letter[0]
PAGE_HEIGHT = letter[1]
MARGIN = 72

# Colors
PRIMARY_COLOR = colors.HexColor('#2E86AB')
SECONDARY_COLOR = colors.HexColor('#A23B72')

# Fonts
TITLE_FONT = 'Helvetica-Bold'
BODY_FONT = 'Helvetica'
```

## Testing

### Run API Tests
```bash
python test_pdf_api.py
```

### Manual Testing
1. Start the server: `python app.py`
2. Open browser to `http://localhost:5000/generate-pdf`
3. Verify PDF downloads correctly

## Troubleshooting

### Common Issues

**Import Error: No module named 'reportlab'**
```bash
pip install reportlab
```

**Permission Error: Cannot create directory**
- Ensure write permissions in project directory
- Run with administrator privileges if needed

**PDF Generation Fails**
- Check server logs for detailed error messages
- Verify all dependencies are installed
- Ensure sufficient disk space

### Debug Mode

Enable debug logging by setting:
```python
app.debug = True
```

## Dependencies

- **Flask**: Web framework
- **ReportLab**: PDF generation library
- **Matplotlib**: Chart generation
- **NumPy**: Numerical computations
- **Requests**: HTTP client (for testing)

## Performance Notes

- PDF generation typically takes 2-5 seconds
- Memory usage scales with chart complexity
- Concurrent requests are handled sequentially

## Security Considerations

- Input validation on API endpoints
- File path sanitization
- No sensitive data in generated PDFs
- Local development server only (not production-ready)

## Future Enhancements

- [ ] Template-based report customization
- [ ] Multiple output formats (HTML, Word)
- [ ] Database integration
- [ ] User authentication
- [ ] Batch report generation
- [ ] Email delivery integration

## License

This project is for educational purposes. Please ensure compliance with data usage policies when working with epidemiological data.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review server logs for error details
3. Verify all dependencies are correctly installed

---

**Generated**: Malaria Epidemiology PDF Report Generator v1.0