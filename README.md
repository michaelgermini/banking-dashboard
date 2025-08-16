# 🏦 Executive Banking Dashboard

A comprehensive **Streamlit-based banking dashboard** designed for executive-level financial monitoring, risk assessment, and automated report generation. This application provides real-time insights into banking performance metrics with interactive visualizations and scenario analysis capabilities.

## 📱 Live Demo

Experience the dashboard online: **[data-banking-dashboard.streamlit.app](https://data-banking-dashboard.streamlit.app/)**

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

---

## 🔍 **Code Audit Report**

### 📊 **Executive Summary**

**Overall Score: 8.5/10** - Well-structured application with recommended improvements

---

## ✅ **Strengths**

### 🏗️ **Architecture & Structure**
- **Excellent modularity**: Clear separation of responsibilities
- **Clean code**: Use of type hints and dataclasses
- **Logical structure**: `streamlit_app.py`, `data.py`, `reporting.py`
- **Separated templates**: HTML in `templates/` folder

### 🔒 **Security**
- **No sensitive data**: Uses simulated data only
- **Input validation**: User parameter controls
- **Secure file handling**: `tempfile.TemporaryDirectory()`
- **No SQL injection**: No database queries

### 📈 **Performance**
- **Streamlit caching**: `@st.cache_data` for performance optimization
- **Efficient generation**: Vectorized calculations with NumPy/Pandas
- **Memory management**: Automatic cleanup of temporary files

### 🎨 **User Interface**
- **Responsive design**: Adaptive layout
- **User feedback**: Spinners and status messages
- **Visual alerts**: Color coding for risks (red/yellow/green)

---

## ⚠️ **Areas for Improvement**

### 🛠️ **Code Quality**

#### **1. Error Handling**
```python
# ❌ Issue: No robust error handling
def generate_pdf_from_html(html: str) -> bytes:
    buffer = BytesIO()
    result = pisa.CreatePDF(src=html, dest=buffer, encoding="UTF-8")
    if result.err:
        return buffer.getvalue()  # Returns corrupted PDF
    return buffer.getvalue()

# ✅ Recommendation: Proper error handling
def generate_pdf_from_html(html: str) -> bytes:
    try:
        buffer = BytesIO()
        result = pisa.CreatePDF(src=html, dest=buffer, encoding="UTF-8")
        if result.err:
            raise ValueError(f"PDF generation failed: {result.err}")
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Failed to generate PDF: {str(e)}")
        return b""
```

#### **2. Data Validation**
```python
# ❌ Issue: No parameter validation
def generate_financial_data(periods: int = 36, scenario: str = "Baseline"):
    # No validation of 'periods' or 'scenario'

# ✅ Recommendation: Input validation
def generate_financial_data(periods: int = 36, scenario: str = "Baseline"):
    if periods < 1 or periods > 120:
        raise ValueError("Periods must be between 1 and 120")
    if scenario not in SCENARIOS:
        raise ValueError(f"Invalid scenario: {scenario}")
```

#### **3. Documentation**
- **Missing docstrings** for main functions
- **No comments** on complex business logic

### 🔒 **Advanced Security**

#### **1. Template Validation**
```python
# ❌ Issue: No template validation
def render_html_report(context: Dict[str, Any]) -> str:
    template = env.get_template("report.html")
    html = template.render(**context)  # No context validation

# ✅ Recommendation: Context validation
def render_html_report(context: Dict[str, Any]) -> str:
    required_keys = ["scenario", "period_start", "period_end", "kpis", "risks"]
    for key in required_keys:
        if key not in context:
            raise ValueError(f"Missing required key: {key}")
```

#### **2. Data Sanitization**
```python
# ❌ Issue: Unsanitized user data
st.metric("Revenue", format_currency_chf_m(kpis["revenue_chf_m"]))

# ✅ Recommendation: Type validation
def safe_format_currency(value: Any) -> str:
    if not isinstance(value, (int, float)):
        raise ValueError("Invalid currency value")
    return format_currency_chf_m(float(value))
```

### 📊 **Robustness**

#### **1. Missing Data Handling**
```python
# ❌ Issue: No NaN handling
deposits_growth = np.r_[np.nan, np.diff(deposits)] / np.r_[np.nan, deposits[:-1]] * 100.0

# ✅ Recommendation: Handle missing values
deposits_growth = np.r_[np.nan, np.diff(deposits)] / np.r_[np.nan, deposits[:-1]] * 100.0
deposits_growth = np.nan_to_num(deposits_growth, nan=0.0)
```

#### **2. Logging**
```python
# ❌ Issue: No logging
# ✅ Recommendation: Add logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_financial_data(...):
    logger.info(f"Generating data for scenario: {scenario}")
    # ... code ...
    logger.info(f"Generated {len(df)} data points")
```

---

## 🚀 **Priority Recommendations**

### **1. Immediate (Security)**
- [ ] Add user parameter validation
- [ ] Implement robust error handling
- [ ] Add data sanitization

### **2. Short term (Quality)**
- [ ] Add docstrings and comments
- [ ] Implement logging
- [ ] Add unit tests

### **3. Medium term (Robustness)**
- [ ] Handle missing data
- [ ] Validate templates
- [ ] Performance monitoring

---

## 🔒 **Security Checklist**

- ✅ **No sensitive data exposed**
- ✅ **Secure temporary file handling**
- ✅ **No code injection**
- ⚠️ **User input validation** (needs improvement)
- ⚠️ **Error handling** (needs improvement)
- ⚠️ **Data sanitization** (needs to be added)

---

## 📋 **Conclusion**

The software has a **solid architecture** and **clean codebase**. The main improvements concern **robustness** and **error handling** rather than critical security issues. The application is **production-ready** with the recommended improvements.

**Recommendation**: Implement security and robustness improvements before critical production deployment.

---

## 📞 Support

For questions, issues, or feature requests, please:
- Open an issue on GitHub, or
- Contact the author directly: **michael@germini.info**

---

**Built with ❤️ using Streamlit and Python**

