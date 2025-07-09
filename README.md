Halo CME Detection Using Aditya-L1 SWIS Data
🌞 Project Overview
This project focuses on developing an early warning system for Halo Coronal Mass Ejections (CMEs) using particle data from the Solar Wind Ion Spectrometer (SWIS) instrument aboard India's Aditya-L1 mission. By analyzing real-time solar wind parameters at the L1 Lagrange point, we aim to detect dangerous solar events before they reach Earth, providing crucial lead time for protecting space assets and ground-based infrastructure.
Why This Matters

Space Weather Impact: Halo CMEs can cause severe geomagnetic storms, damaging satellites, disrupting GPS, and affecting power grids
Early Warning: Aditya-L1's position at L1 provides ~1 hour advance warning before solar wind disturbances reach Earth
Asset Protection: Early detection enables protective measures for spacecraft, astronauts, and critical infrastructure

🎯 Project Objectives

Identify Halo CME Events using SWIS Level-2 data from Aditya-L1
Analyze Particle Signatures during CME transit (flux, density, temperature, velocity)
Develop Detection Algorithms with statistical thresholds for automated CME identification
Validate Results against known CME databases (CACTUS, DONKI, OMNI)

📊 Dataset Description
Primary Data Sources

SWIS Level-2 Data: From Indian Space Science Data Centre (ISSDC)

Particle flux measurements
Proton number density (cm⁻³)
Temperature (K)
Bulk velocity (km/s)
Spatial coordinates (X, Y, Z positions)


CME Catalogs:

CACTUS CME Database: Computer Aided CME Tracking
DONKI (NASA): Database of Notifications, Knowledge, Information
OMNI Data: Solar wind parameters from multiple spacecraft



Study Period
October 2024 - Selected for comprehensive multi-source analysis and validation
🔧 Technical Implementation
Tools & Technologies

Language: Python 3.8+
Core Libraries:

pandas, numpy - Data manipulation and analysis
matplotlib, seaborn - Visualization
cdflib - Reading NASA CDF files
scipy - Signal processing and statistics
requests - API data retrieval



Key Features

Multi-source Data Integration: Combines SWIS, CACTUS, DONKI, and OMNI datasets
Automated Data Processing: Scripts for downloading and parsing various data formats
Advanced Analytics: Statistical thresholds, moving averages, and derivative calculations
Visualization Suite: Comprehensive plotting functions for time-series analysis

📁 Repository Structure
├── DONKIDATAIMPORT.py          # NASA DONKI API data retrieval
├── octcmes.py                  # CACTUS CME data parser
├── mergel2th2blk.py           # SWIS Level-2 data processor
├── FINAL_COMPLETE.py          # Complete analysis pipeline
├── data/
│   ├── cdf_files/             # Raw SWIS CDF files
│   ├── cactus_data/           # CACTUS CME catalog
│   ├── donki_data/            # NASA DONKI event data
│   └── processed/             # Merged and cleaned datasets
├── plots/                     # Generated visualizations
├── results/                   # Analysis outputs and reports
└── README.md                  # This file
🚀 Getting Started
Prerequisites
bashpip install pandas numpy matplotlib seaborn cdflib scipy requests
Quick Start

Clone the repository:
bashgit clone https://github.com/yourusername/halo-cme-detection.git
cd halo-cme-detection

Download SWIS data from ISSDC and place CDF files in data/cdf_files/
Run the complete pipeline:
bashpython FINAL_COMPLETE.py

Check results in the results/ directory

📈 Methodology
1. Data Acquisition

SWIS Data: Direct download from ISSDC in CDF format
CME Catalogs: API calls to DONKI, manual parsing of CACTUS data
Quality Control: Automated filtering of fill values and invalid measurements

2. Feature Engineering

Temporal Features: Moving averages, gradients, rate of change
Composite Metrics: Combined parameters (speed × density, thermal pressure)
Statistical Measures: Standard deviations, percentiles, anomaly scores

3. CME Detection Algorithm

Threshold-based Detection: Multi-parameter criteria for CME identification
Temporal Correlation: Matching SWIS signatures with known CME arrival times
Validation: Cross-verification with multiple CME databases

4. Transit Time Modeling

Drag Model: Accounts for solar wind interaction during CME propagation
Arrival Prediction: Estimates Earth arrival time based on initial parameters
Accuracy Assessment: Comparison with observed arrival times

📊 Key Results
CME Signature Characteristics

Velocity Enhancement: 2-3x increase in solar wind speed
Density Compression: Sharp spikes in proton density
Temperature Elevation: Significant thermal signatures
Flux Variations: Dramatic changes in particle flux

Detection Performance

Sensitivity: Ability to identify true CME events
Specificity: Minimization of false positive alerts
Lead Time: Average warning time before Earth impact

📸 Sample Visualizations
The project generates comprehensive time-series plots showing:

SWIS parameter evolution during CME events
Overlay comparisons between different data sources
Statistical threshold boundaries for detection
CME arrival time predictions vs. observations

🔍 Analysis Insights
CME Interaction Effects

Multi-CME Events: Detection of successive CME interactions
Halo vs. Partial Halo: Distinguishing characteristics
Geoeffectiveness: Correlation with geomagnetic activity

Statistical Thresholds

Velocity Threshold: >600 km/s sustained increase
Density Enhancement: >5x baseline values
Temperature Spike: >10⁶ K thermal signatures
Flux Anomaly: Multi-channel particle flux variations

🎯 Future Enhancements
Machine Learning Integration

Automated Pattern Recognition: Deep learning for CME signature identification
Predictive Modeling: Advanced transit time prediction algorithms
Real-time Processing: Live data stream analysis capabilities

Extended Analysis

Multi-mission Correlation: Integration with other L1 missions (WIND, ACE)
Long-term Studies: Seasonal and solar cycle variations
Operational Deployment: Real-time warning system development

📚 Scientific Context
Solar Wind Physics
Understanding of solar wind-CME interaction mechanisms and their signatures in particle data measured at L1.
Space Weather Applications
Direct relevance to operational space weather forecasting and mitigation strategies.
Mission Contribution
Supporting Aditya-L1's scientific objectives in solar physics and space weather research.
🤝 Contributing
We welcome contributions from the space weather community! Please see our contribution guidelines for:

Code style and documentation standards
Data validation procedures
Testing protocols
Scientific review processes

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

Indian Space Research Organisation (ISRO) for Aditya-L1 mission data
Physical Research Laboratory (PRL) for SWIS instrument
NASA SPDF for DONKI database access
Royal Observatory of Belgium for CACTUS CME catalog
Space Weather research community for validation datasets

📧 Contact
For questions, collaborations, or technical support:

Project Lead: Ricky Kharsel - 
Research Group: Parala Maharaja Engineering College 
Issue Tracker: [GitHub Issues URL]
