# 🏗️ Technical Construction Suitability Advisor

A modular, Python-based decision support system for **preliminary construction site due diligence**.

Built with **Streamlit**, this application functions as a digital feasibility analyst.  
It accepts **35+ technical parameters**—from geotechnical metrics to environmental risk scores—and evaluates a site's suitability for construction project types such as **Residential Complexes**, **Warehouses**, and **Farms**.

---

## 🚀 Key Features

### **🔧 Modular Architecture**
Decoupled into:
- Logic  
- Data  
- State management  
- UI rendering  

Ensures clean maintainability and high scalability.

---

### **📊 Deep Technical Analysis**
Evaluates sites using engineering-grade metrics:

#### **Geotechnical**
- SPT N-values  
- Bearing Capacity  
- CBR  
- Proctor Compaction  
- Atterberg Limits  

#### **Environmental**
- EIA status  
- Flood Zones  
- Seismic Hazard  
- Phase I/II ESA  

#### **Infrastructure**
- Traffic Impact  
- Utility Availability  
- Population Density  

---

### **📌 Stateful Interaction**
- Uses `st.session_state` to preserve all form data  
- Allows switching between tabs without losing progress  

---

### **🧭 3-Tab Workflow**

#### **1. Measure**
- Full-screen input wizard  
- Organized by technical discipline  

#### **2. Analyze**
- Real-time pass/fail results  
- Detailed engineering warnings and explanations  
- Downloadable summary  

#### **3. Requirements**
- Reverse lookup tool  
- Shows minimum engineering standards for any building type  

---

### **📝 Report Generation**
Automatically generates **timestamped .txt reports** containing:
- The full site profile  
- Complete analysis results  
- Engineering notes  

---

## 📂 Project Structure

 - ConstructionAdvisor/
  ├── main.py # Entry point — initializes state and renders tab layout
  ├── state.py # Manages session_state and prevents data loss
  ├── ui.py # All Streamlit UI components (forms, buttons, layout)
  ├── logic.py # Core analysis logic (suitability rules, report builder)
  ├── data.py # Site parameter options + rules engine dictionary
  ├── requirements.txt # Dependencies
  └── README.md # Documentation


---

## 🛠️ Installation & Setup

### **Prerequisites**
- Python **3.8+**

---

### **Step 1: Clone or Download**
Place all files in a folder named **ConstructionAdvisor**.

---

### **Step 2: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 3: Run the Application**
```bash
streamlit run main.py
```
