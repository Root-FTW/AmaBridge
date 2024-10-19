# AmaBridge

**AmaBridge** is a Python-based automation tool that serves as a bridge between users and the powerful [OWASP Amass](https://github.com/OWASP/Amass) framework. Designed to simplify and enhance DNS enumeration and subdomain discovery, AmaBridge offers an intuitive interface, organized result management, and flexible configuration options without the need for extensive command-line interactions.

## Table of Contents

- [Why AmaBridge?](#why-amabridge)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Script](#running-the-script)
  - [Scanning Multiple Domains](#scanning-multiple-domains)
  - [Using a Wordlist](#using-a-wordlist)
  - [Reviewing Results](#reviewing-results)
- [Automating Scans](#automating-scans)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

## Why AmaBridge?

While **Amass** is a robust and versatile tool for DNS enumeration, it often requires users to navigate complex command-line options to perform scans effectively. **AmaBridge** streamlines this process by providing a user-friendly Python interface that manages multiple domains, organizes scan results systematically, and offers flexibility in configuration—making it ideal for both beginners and seasoned professionals.

**AmaBridge** offers:

- **Simplified Usage:** No need to memorize or input lengthy command-line arguments.
- **Organized Results:** Each domain scanned has its dedicated result files, preventing data overlap and confusion.
- **Flexible Wordlist Integration:** Optionally incorporate wordlists for enhanced brute-force capabilities without mandatory dependencies.
- **Automated Scan Differentiation:** Easily identify and compare results from multiple scans with clear separators and timestamps.
- **Extensible Architecture:** Easily modify or extend functionality according to specific needs.

## Features

- **Multiple Domain Support:** Scan one or multiple domains in a single execution.
- **Optional Wordlist Usage:** Incorporate a custom wordlist if available, or proceed with passive enumeration.
- **Organized Output:** Results are neatly segregated into individual files within a designated `Result` directory.
- **Scan History Separation:** Previous and new scan results are separated with timestamps for easy comparison.
- **User-Friendly Prompts:** Interactive prompts guide users through the scanning process.
- **Error Handling:** Gracefully manages errors during execution, ensuring continuous operation across multiple domains.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/AmaBridge.git
   ```

2. **Navigate to the Directory:**

   ```bash
   cd AmaBridge
   ```

3. **Ensure Python is Installed:**

   AmaBridge requires Python 3.6 or higher. You can download Python from the [official website](https://www.python.org/downloads/).

4. **Install Amass:**

   - **Download Amass:**
     Visit the [Amass GitHub Releases](https://github.com/OWASP/Amass/releases) page and download the appropriate binary for your operating system.

   - **Add Amass to PATH:**
     Extract the binary and add its directory to your system's PATH environment variable to access it from any command prompt.

   - **Verify Installation:**

     ```cmd
     amass -version
     ```

## Usage

### Running the Script

1. **Navigate to the AmaBridge Directory:**

   ```cmd
   cd C:\AmaBridge
   ```

2. **Execute the Script:**

   ```cmd
   python ama_bridge.py
   ```

### Scanning Multiple Domains

During execution, when prompted, enter multiple domains separated by commas. For example:

```
Enter domain(s) to scan, separated by commas: example.com, testsite.org, sample.net
```

### Using a Wordlist

1. **When Prompted for a Wordlist:**

   ```
   Do you have a wordlist? (yes/no): yes
   ```

2. **Provide the Path:**

   - **Local Path Example:**
     ```
     Please enter the local path or URL of your wordlist: C:\Wordlists\my_wordlist.txt
     ```

   - **URL Example:**
     ```
     Please enter the local path or URL of your wordlist: https://example.com/wordlist.txt
     ```
     *The script will download the wordlist and save it locally for use.*

### Reviewing Results

1. **Navigate to the `Result` Directory:**

   ```cmd
   cd C:\AmaBridge\Result
   ```

2. **Locate Individual Result Files:**

   - Each domain has its own set of result files:
     - `domain_name.txt`: Contains records of the scan.
     - `domain_name.json`: Structured data with subdomain details.
     - `domain_name.csv`: Comma-separated values for easier analysis.

3. **Understanding Scan Separations:**

   - Within each `.txt` file, scans are separated by clear timestamps, allowing users to differentiate between multiple scans for the same domain.

## Automating Scans

To schedule periodic scans using AmaBridge, utilize the **Task Scheduler** in Windows:

1. **Open Task Scheduler:**
   - Press `Win + R`, type `taskschd.msc`, and press Enter.

2. **Create a New Task:**
   - Click on **"Create Task..."** in the Actions pane.

3. **Configure General Settings:**
   - Name the task (e.g., "AmaBridge Weekly Scan").
   - Set security options as needed.

4. **Set Triggers:**
   - Define when the task should run (e.g., weekly at a specific time).

5. **Define Actions:**
   - Action: **Start a program**
   - Program/script: `python`
   - Add arguments: `C:\AmaBridge\ama_bridge.py`
   - Start in: `C:\AmaBridge\`

6. **Finalize and Save:**
   - Review settings and save the task.

*AmaBridge will now execute automatically based on the defined schedule, ensuring continuous monitoring of your specified domains.*

## Technical Details

### Script Workflow

1. **User Inputs:**
   - **Domains:** Users input one or multiple domains separated by commas.
   - **Wordlist:** Users indicate if they have a wordlist and provide its path or URL.

2. **Wordlist Handling:**
   - **URL:** Downloads the wordlist and saves it locally.
   - **Local Path:** Verifies existence and uses it for brute-force enumeration.

3. **Result Management:**
   - **Directory Structure:** Creates a `Result` directory if it doesn't exist.
   - **Per-Domain Files:** Each domain has its own `.txt`, `.json`, and `.csv` files.
   - **Scan Separation:** Appends a timestamped separator in `.txt` files for repeated scans.

4. **Amass Execution:**
   - Constructs and executes the Amass command with appropriate flags.
   - Handles execution success or failure per domain.

5. **Result Processing:**
   - **Text Files (`.txt`):** Extracts and lists subdomains discovered through `node -->` records.
   - **JSON Files (`.json`):** Parses and displays subdomain details along with their IP addresses.
   - **CSV Files (`.csv`):** Available for further analysis in spreadsheet applications.

### Key Components

- **Subprocess Module:** Executes Amass commands within the Python script.
- **JSON Handling:** Parses Amass's structured JSON output for detailed insights.
- **User Prompts:** Interactive inputs guide users through scanning and configuration steps.
- **Error Handling:** Ensures the script continues running even if certain scans fail.

### Benefits Over Direct Amass Usage

- **Ease of Use:** Reduces the complexity of Amass commands by handling flags and options internally.
- **Organized Output:** Automatically segregates results per domain, enhancing readability and management.
- **Automated Wordlist Handling:** Simplifies the incorporation of wordlists without manual command adjustments.
- **Scalability:** Efficiently manages multiple domains in a single execution without user intervention.
- **Repeatable Scans:** Clearly separates multiple scans for the same domain, aiding in tracking changes over time.

## Contributing

Contributions are welcome! If you'd like to enhance AmaBridge, please follow these steps:

1. **Fork the Repository:**
   - Click the **"Fork"** button at the top-right of this page.

2. **Create a New Branch:**
   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes:**
   ```bash
   git commit -m "Add Your Feature Description"
   ```

4. **Push to the Branch:**
   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open a Pull Request:**
   - Navigate to your forked repository and click **"New Pull Request"**.

## License

This project is licensed under the [MIT License](LICENSE).
