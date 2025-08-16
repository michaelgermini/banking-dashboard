# 🏦 Executive Banking Dashboard

A comprehensive **Streamlit-based banking dashboard** designed for executive-level financial monitoring, risk assessment, and automated report generation. This application provides real-time insights into banking performance metrics with interactive visualizations and scenario analysis capabilities.

## 🌟 Features

### 📊 **Real-time Financial Monitoring**
- **Revenue & Margin Tracking**: Monitor monthly revenue trends and gross margin performance
- **Balance Sheet Analytics**: Track deposits and Assets Under Management (AUM) growth
- **Profitability Analysis**: Segment-wise operating profit breakdown (Retail, Private, Corporate)
- **Key Performance Indicators**: Real-time KPI dashboard with growth metrics

### ⚠️ **Risk Management & Compliance**
- **Liquidity Coverage Ratio (LCR)**: Real-time monitoring with color-coded alerts
- **Non-Performing Loan (NPL) Ratio**: Track credit quality indicators
- **Market Value at Risk (VaR)**: Monitor market risk exposure
- **Counterparty Exposure**: Track credit concentration risks
- **Automated Risk Alerts**: Color-coded warnings for threshold breaches

### 📈 **Scenario Analysis**
- **Baseline Scenario**: Normal market conditions
- **Adverse Scenario**: Economic downturn simulation
- **Severe Scenario**: Crisis scenario modeling
- **Customizable Timeframes**: 12-60 months analysis periods

### 📋 **Professional Reporting**
- **PDF Report Generation**: Automated executive reports with charts
- **Interactive Charts**: Plotly-powered visualizations
- **Export Capabilities**: Download reports in PDF format
- **Professional Templates**: Executive-ready report formatting

### 🎨 **Modern User Interface**
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Sidebar**: Easy parameter adjustment
- **Real-time Updates**: Dynamic chart updates based on scenario changes
- **Professional Styling**: Clean, executive-friendly interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/michaelgermini/banking-dashboard.git
   cd banking-dashboard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   .\.venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Launch the application**
   ```bash
   python -m streamlit run streamlit_app.py
   ```

6. **Access the dashboard**
   - Open your browser and go to: `http://localhost:8501`
   - The dashboard will automatically open in your default browser

## 📱 Live Demo

Experience the dashboard online: **[data-banking-dashboard.streamlit.app](https://data-banking-dashboard.streamlit.app/)**

## 🛠️ Usage Guide

### Dashboard Navigation
1. **Sidebar Controls**: Adjust scenario, time period, and export settings
2. **KPI Metrics**: View key performance indicators in the top row
3. **Risk Alerts**: Monitor risk indicators with color-coded status
4. **Interactive Charts**: Explore financial trends with zoom and hover capabilities
5. **Report Generation**: Create and download PDF reports

### Scenario Selection
- **Baseline**: Normal economic conditions with steady growth
- **Adverse**: Economic downturn with reduced growth and increased volatility
- **Severe**: Crisis scenario with negative growth and high risk

### Report Export
1. Configure report settings in the sidebar
2. Click "Generate PDF" button
3. Download the executive report with charts and analysis

## 🏗️ Architecture

### Core Components
- **`streamlit_app.py`**: Main application interface and user interactions
- **`data.py`**: Financial data generation and KPI calculations
- **`reporting.py`**: PDF report generation and HTML templating
- **`templates/`**: HTML templates for report generation

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Data Visualization**: Plotly (Interactive charts)
- **Data Processing**: Pandas, NumPy
- **Report Generation**: xhtml2pdf, Jinja2
- **Styling**: Streamlit native components

## 📦 Dependencies

Key packages include:
- `streamlit>=1.36` - Web application framework
- `pandas>=2.2` - Data manipulation and analysis
- `plotly>=5.22` - Interactive data visualization
- `xhtml2pdf>=0.2.15` - PDF report generation
- `jinja2>=3.1` - HTML templating
- `kaleido>=0.2.1` - Static image export for charts

## 🚀 Deployment

### Streamlit Community Cloud
1. Push this repository to GitHub
2. Connect your repository to Streamlit Cloud
3. Select `streamlit_app.py` as the main file
4. Deploy with one click

### Local Production
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Michael Germini** - [GitHub Profile](https://github.com/michaelgermini)

## 📞 Support

For questions, issues, or feature requests, please open an issue on GitHub or contact the author.

---

**Built with ❤️ using Streamlit and Python**

