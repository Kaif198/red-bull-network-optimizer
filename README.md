# Red Bull Global Supply Chain Network Optimizer

Strategic supply chain optimization platform demonstrating network design, scenario planning, and data storytelling.

**Portfolio Project** | Mohammed Kaif Ahmed | MSc Strategy Management, DCU

📧 kaifahmed6864@gmail.com | 💼 [LinkedIn](https://www.linkedin.com/in/kaif-ahmed-bb972421a)

---

## 🎯 What It Does

Optimizes Red Bull's global distribution network (4 plants, 12 DCs, 25 markets) using linear programming. Identifies €30M cost savings and €47M disruption risks through scenario analysis.

**Key Results:**
- €30M optimization opportunity identified
- €47M disruption risk quantified
- Supply chain resilience: 80/100
- <5 second optimization solve time

---

## 🚀 Quick Start
```bash
git clone https://github.com/YOUR_USERNAME/red-bull-network-optimizer.git
cd red-bull-network-optimizer
python -m venv venv
venv\Scripts\activate  # Windows | source venv/bin/activate (Mac/Linux)
pip install -r requirements.txt
python data/generate_data.py
python app.py
```

Open `http://localhost:5000`

---

## 📊 Features

**3 Scenarios:**
- Baseline (current network)
- Cost Optimized (€30M savings potential)
- Disruption Response (Austria plant offline)

**Visualizations:**
- Interactive network map (Leaflet.js)
- Cost breakdown charts (Chart.js)
- KPI dashboard with business context
- Excel export

**Tech Stack:** Python, Flask, PuLP, Chart.js, Leaflet, Pandas

---

## 🛠️ Project Structure
```
├── app.py                    # Flask API
├── optimization/             # PuLP models
├── data/                     # CSV files
├── static/                   # CSS/JS
└── templates/                # HTML
```

---

## 📈 Sample Insight

**Current Network:** €338.7M annual cost (11.2% above optimal)

**Recommendation:** Close Moscow DC, shift to Vienna = €1.9M/year savings

**Disruption Impact:** Austria shutdown = €1,872M cost spike, 54% fill rate

---

## 🎓 Skills Demonstrated

- Supply chain optimization & network design
- Linear programming (1,200+ variables)
- Full-stack development (Python + JavaScript)
- Data visualization & business storytelling
- Strategic analysis with ROI quantification

---

## 📄 License

MIT License | Not affiliated with Red Bull GmbH

---

**Built in Dublin, Ireland | February 2026**
