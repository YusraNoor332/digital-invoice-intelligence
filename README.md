# Haier Open-Architecture Print Automation System

The Haier Open-Architecture Print Automation System is an industrial-grade, vendor-independent middleware platform designed to orchestrate handheld Thermal Inkjet (TIJ) printers on active production lines. 

The system intercepts barcode scans via a high-speed asynchronous FastAPI listener, queries the central database for product specifications, translates metadata into hardware-native byte packets, and routes them to Sojet/MoTix hardware endpoints in real time.

---

## 📈 Version Release History

### 🚀 Version 2.0 — Enterprise Database Migration (Current)
- **Backend Architecture Engine:** Migrated the local system runtime onto a dedicated Microsoft SQL Server instance (`HaierSandboxDB`).
- **Data Integrity Constraints:** Implemented dynamic schemas covering transactional billing management, custom `TechnicianProfile` structures, and multi-tier `CustomerFeedback` validation rules (such as `behavior_rating`, `punctuality_rating`, and `resolution_quality`).
- **Seeding Automation:** Embedded custom interactive Django shell initialization logic to safely pre-populate test layouts dynamically without violating database constraints.

### 🔹 Version 1.0 — Baseline Architecture
- Established the initial open Python middleware platform.
- Integrated the core FastAPI scanner listener daemon and local file configuration.

---

## 🛠️ 1. System Requirements & Environment Setup

This platform is engineered using an open-architecture Python framework and requires **Python 3.10 or higher**.

### Isolation Environment Deployment
Execute the following commands in an elevated PowerShell terminal to initialize the virtual runtime and install all necessary dependencies:

```powershell
# Navigate to the workspace root directory
cd C:\Users\HP\print_automation_system\haier_printing_system

# Initialize an isolated virtual environment
python -m venv venv

# Automatically activate the runtime environment
.\venv\Scripts\Activate.ps1

# Install production and hardware interface dependencies
pip install -r requirements.txt
```

⚙️ 2. Configuration & Network Topology Mapping
Prior to system initialization, network paths for relational databases and edge hardware devices must be explicitly mapped in the global configuration layer.

Open `config.py` and modify the parameters below:

A. Relational Database Interface (RDBMS)
Update the target connection strings to align with your production Microsoft SQL Server instance:

```python
DB_SERVER   = "10.0.0.50"       # Target SQL Server Instance IP
DB_NAME     = "HaierSandboxDB"  # Database Instance Name
DB_USER     = "tij_operator"    # Database Authentication User
DB_PASSWORD = "SecurePassword"  # Database Authentication Password
```

B. Hardware Edge Endpoints (Static IPv4 Routing)
Map the unique physical hardware IDs (broadcast by line scanners) to the corresponding Static IPv4 Addresses assigned to the industrial MoTix printers:

```python
PRINTER_IP_MAP = {
    "LINE_1_PRINTER_A": "192.168.1.55",  # Assembly Line 1 Primary TIJ
    "LINE_1_PRINTER_B": "192.168.1.56",  # Assembly Line 1 Secondary TIJ
}
```

🚀 3. System Initialization
To instantiate the application engine, run the primary entry point script:

```powershell
cd C:\Users\HP\print_automation_system\haier_printing_system
.\venv\Scripts\python main.py
```

ℹ️ Operational Note: Initialization will natively launch the PyQt6 central monitoring dashboard in dark-mode, while the FastAPI listening daemon binds silently to local port 8000 to process edge requests.

📡 4. Hardware Webhook Configuration
Edge printing hardware must be configured to route raw payload triggers directly to this middleware service.

Determine your workstation's network identifier by running `ipconfig` in PowerShell (e.g., Target Host IPv4: 192.168.1.20).

Access the physical MoTix printer touchscreen interface and navigate to **Settings ➡️ Webhook / API Integration**.

Configure the destination endpoint URL string exactly as follows:

```http
http://192.168.1.20:8000/scan
```
Ensure the transmission protocol action is explicitly set to **POST**.

Once set, physical trigger engagement instantly streams telemetry data to the host machine, triggering real-time validation and printing routines.

🧪 5. Sandbox Evaluation (Mock Database Mode)
The system includes an isolated sandbox simulation mode to facilitate offline verification of physical hardware without active database dependencies.

Open `database.py`.

Toggle the evaluation flag to active at the top of the file:

```python
MOCK_MODE = True
```

Initialize the core script (`python main.py`).

Broadcast a test payload containing the exact string token: `HR-FRIDGE-001`.

The middleware will automatically bypass database socket pools, synthesize a static data package ("Haier Refrigerator Pro"), and dispatch the print matrix to the target hardware.

⚠️ **CRITICAL PRE-FLIGHT GUARDRAIL**: The `MOCK_MODE` flag must be set to `False` in staging environments before deploying changes to live factory floor segments!
