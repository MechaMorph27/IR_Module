IR Module Testing System

A Python-based testing and monitoring application for battery module electrical characterization, designed to acquire, validate, and record cell-level and module-level electrical measurements.

The system communicates with a measurement device over a local network, evaluates measurements against configurable acceptance limits, and maintains test records for traceability and analysis.

Overview

The IR Module Testing System is developed to streamline the testing of battery modules by providing a structured workflow for measurement acquisition, validation, visualization, and result logging.

The application supports:

Cell-by-cell voltage measurement
Cell internal resistance (IR) measurement
Complete module voltage measurement
Complete module internal resistance measurement
Configurable acceptance limits
Automatic measurement validation
Pass/Fail evaluation
Test result logging
Application-level administrator access
Configurable application themes and settings
Local network communication with measurement equipment

Key Features

🔋 Electrical Measurement

The system supports measurement points including:

B-

B1

B2

B3

B4

B5

B6

B7

B8

B9

B10

B11

B12

B13

Module

Measurements include:

Cell Voltage
Cell Internal Resistance
Module Voltage
Module Internal Resistance

📊 Automated Validation

Measured values are compared against configurable minimum and maximum limits.

Example:

Measurement	Minimum	Maximum

Cell Voltage	 3.565 V	 3.580 V

Cell IR 	1.50 mΩ	 1.98 mΩ

Module Voltage	 49.91 V	50.12 V

Module IR	 18.0 mΩ	19.9 mΩ


The limits can be modified according to the required battery/module specifications.

🖥️ Application Interface

The application provides a graphical interface for:

User login
Test execution
Measurement monitoring
Result visualization
Configuration management
Theme management
Test result review

📁 Test Data Logging

Test results are recorded for traceability and future analysis.

The application can generate and maintain an Excel-based test log:

Module_Test_Log.xlsx

System Architecture
The application is organized into modules responsible for different aspects of the testing workflow.

                    ┌─────────────────────┐
                    │     User Interface  │
                    │  Login / Dashboard  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Test Engine      │
                    │ Measurement & Logic │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       ┌─────────────────┐          ┌─────────────────┐
       │ Measurement     │          │ Configuration   │
       │ Device / Network│          │ & Security      │
       └────────┬────────┘          └─────────────────┘
                │
                ▼
       ┌─────────────────┐
       │ Validation &    │
       │ Pass / Fail     │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Excel Test Log  │
       └─────────────────┘

Project Structure

IR_Module/
│
├── main.py
├── bt3562_client.py
│
├── test_engine.py
├── test_telnet_device.py
├── range_checker.py
│
├── config_store.py
├── security_manager.py
├── operator_store.py
├── issue_store.py
│
├── theme_manager.py
├── theme_store.py
│
├── ui_login.py
├── ui_dashboard.py
├── ui_splash.py
│
├── config.json
├── config_data.json
├── security.json
├── operators.json
├── issues.json
├── theme.json
│
├── excel_logger.py
│
├── Module_Test_Log.xlsx
│
└── README.md

The project structure may evolve as additional features are developed.

Measurement Device Communication
The application communicates with the measurement equipment through a local network connection.

Example configuration:

Device IP:
192.168.1.1

Measurement Command:
READ?

The communication parameters can be configured according to the connected measurement instrument.

Configuration
The application uses JSON-based configuration files for managing measurement parameters and application settings.

Typical configuration includes:

Measurement device IP address
Measurement commands
Measurement points
Cell voltage limits
Cell IR limits
Module voltage limits
Module IR limits
Excel output file
Application settings
Example:

{
    "ip": "192.168.1.1",
    "read_command": "READ?\n",
    "points": [
        "B-",
        "B1",
        "B2",
        "B3",
        "B4",
        "B5",
        "B6",
        "B7",
        "B8",
        "B9",
        "B10",
        "B11",
        "B12",
        "B13",
        "Module"
    ]
}

Security
The application includes administrator-level access control.

For production deployments, sensitive credentials should not be stored directly in a public Git repository.

Recommended approaches include:

Environment variables
Local configuration files excluded using .gitignore
Secure credential storage
Dedicated secret-management systems
Configuration templates can be provided for deployment without exposing production credentials.

Requirements
The application requires:

Python 3.x

Compatible measurement hardware

Network connectivity to the measurement device

Required Python dependencies

Windows environment recommended for the current application setup

Install project dependencies, if a requirements.txt file is provided:

pip install -r requirements.txt

Installation
Clone the repository:

git clone https://github.com/MechaMorph27/IR_Module.git

Navigate to the project directory:

cd IR_Module

Install the required dependencies:

pip install -r requirements.txt

Configure the measurement device and application settings before starting the application.

Running the Application
Start the application using:

python main.py

The application will initialize the user interface and required testing components.

Typical Test Workflow

1. Start Application
       ↓
2. User Authentication
       ↓
3. Configure / Verify Test Parameters
       ↓
4. Connect to Measurement Device
       ↓
5. Start Module Test
       ↓
6. Acquire Cell Measurements
       ↓
7. Acquire Module Measurements
       ↓
8. Validate Measurements
       ↓
9. Generate Pass / Fail Result
       ↓
10. Log Test Result

Test Result
The system evaluates measured parameters against the configured limits and determines whether the tested module satisfies the defined criteria.

Test data can be stored in:

Module_Test_Log.xlsx

This provides a historical record that can be used for:

Quality tracking
Production testing
Troubleshooting
Measurement analysis
Test traceability
Development Goals

Future development may include:

Automated test sequencing

Improved measurement-device integration

Enhanced data visualization

Test report generation

Production database integration

User role management

Advanced test history and filtering

Additional measurement instrument support

Automated diagnostics

Production-line integration

Project Status

Status: Active Development

The project is being developed as a dedicated battery module testing solution and may undergo changes as new testing requirements and hardware integrations are introduced.

Author
MechaMorph27

Project: IR Module Testing System

