# Flow-Log-Processor-Kubernetes

This project contains two components for processing network flow log data based on a lookup table:
- **Standalone Python Script**:
  - A simple script that processes the flow log data, maps each log entry to a tag using a lookup table, and generates summary reports.
  - File name - Flow_Log_Processor.py
  - Generated output files - tag_count.csv and port_protocol_count.csv
- **Flask Web Application**:
  - A web interface that allows users to upload a lookup table and flow log file, processes the data, and displays the results in a tabulated form. Also allows you to used previously uploaded files.
  - Public URL - https://trialwebsite.pythonanywhere.com/

## Assumptions
- **Log Format and Log Version**: The program supports the default log format (version 2) as described in the problem statement. The fields in the log file are space-separated, with destination port and protocol fields in the expected positions (7th and 8th, respectively).
- **File Types For the Flask App**: The lookup table must be a CSV/TXT file, and the flow logs must be in a TXT file format. The program includes validation to ensure that only these file types are processed.
- Port/Protocol count is updated for all combinations of Destination Port/Protocol. This includes combinations that are not a part of some specific tag.
- The standalone Flow_Log_Processor.py script expects the log file to be called 'flow_logs.txt' and the lookup table to be called 'lookup_table.txt'. Both these files must be placed in the Test_Files folder.

## Directory Structure
```
FLOW-LOG-PROCESSOR/
│
├── Flask_App/
│   ├── templates/
│   │   ├── home.html
│   │   ├── results.html
│   ├── uploads/
│       ├── look_up.html
│       └── flow_log.html
│   └── app.py
│   └── deployment.yaml
│   └── Dockerfile
│
├── Test_Files/
│   ├── flow_logs.txt
│   └── lookup_table.txt
│
├── Flow_Log_Processor.py
├── protocol_lookup.py
└── protocols_code_master.csv   
```
- `Flow_Log_Processor.py/`: Standalone Python script for processing logs
- `protocols_code_master.csv /`: CSV defining the protocol code and the associated protocol
- `protocol_lookup.py/`: Standalone Python script for creating the dictionary mapping the protocol code with the protocol (6-TCP, 17-UDP)
- `Flask_App/app.py`: Flask application providing a web interface
- `Flask_App/templates /`: HTML template for the web interface
- `Flask_App/uploads /`: The directory for storing files uploaded while using the web interface.
- `Test_Files/`: Consists of the lookup table and flow logs used for testing.

## Requirements
- **Python 3.9**
- **Flask**: Only required if running the web interface

## Setup Instructions

### Running the Standalone Script
- Clone the Repository:
  ```
  git clone <repository_url>
  cd Flow-Log-Processor
  ```
- Run the Script:
   Ensure your lookup_table.csv and flow_logs.txt files are in the Test_Files directory.
   Run the script using Python:
   ```
   python Flow_Log_Processor.py
   ```
- The script will output tag_count.csv and port_protocol_count.csv files in the same directory.

### Running the Flask Web Application
- Install Flask
  ```
  pip install flask
  ```
- Start the Flask Server:
  ```
  cd Flask_App
  python app.py
  ```
- Access the Web Interface:
  - Open a web browser and navigate to http://127.0.0.1:5000/.
  - Use the interface to upload your lookup_table.csv and flow_logs.txt files.
  - The results will be displayed in a tabulated form on the results page.

### Creating the Docker Image and running 5 pods on Kubernetes

#### Prerequisites
- Docker
- Minikube
- Kubectl

#### Build the Docker Image
- docker build --no-cache -t flowlog-kubernetes .

#### Build the Docker Image
- Start Minikube

#### Load the Docker Image into Minikube
- minikube image load flowlog-kubernetes

#### Deploy the Kubernetes Resources
- kubectl apply -f deployment.yaml

#### Deploy the Kubernetes Resources
- kubectl apply -f deployment.yaml

#### Access the Flask Application
- minikube service flowlog-test-service

### Tests and Validation

- File Type Validation: The Flask app includes checks to ensure that only .csv/txt files are uploaded for the lookup table and .txt files for the flow logs. If incorrect file types are uploaded, they are rejected with an appropriate error message.
- Performance Test: Created large flow_logs.txt file and a lookup_table.csv with many entries.
- Made sure the entries in the flow_log are valid. If not, they are ignored.

