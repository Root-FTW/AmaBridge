**AmaBridge** is a powerful Python-based automation tool designed to streamline and enhance DNS enumeration and subdomain discovery using [OWASP Amass](https://github.com/OWASP/Amass). Acting as a bridge between users and Amass, AmaBridge offers a user-friendly interface, organized result management, and flexible configuration options, eliminating the need for complex command-line interactions.

---

## Table of Contents

- [Why AmaBridge?](#why-amabridge)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Script](#running-the-script)
  - [Scanning Multiple Domains](#scanning-multiple-domains)
  - [Using a Wordlist](#using-a-wordlist)
  - [Reviewing Results](#reviewing-results)
- [Automation](#automation)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Why AmaBridge?

While **Amass** is an exceptionally robust tool for DNS enumeration, it can often be daunting for users, especially those new to DNS reconnaissance, due to its extensive command-line options and configurations. **AmaBridge** simplifies this process by providing an intuitive Python interface that handles the complexities of Amass, allowing users to focus on analyzing the results rather than configuring options.

**AmaBridge** offers:

- **Simplified Usage:** No need to memorize or input lengthy command-line arguments.
- **Organized Output:** Each domain scanned has its dedicated result files, preventing data overlap and confusion.
- **Flexible Wordlist Integration:** Optionally incorporate wordlists for enhanced brute-force capabilities without mandatory dependencies.
- **Automated Scan Differentiation:** Easily identify and compare results from multiple scans with clear separators and timestamps.
- **Extensible Architecture:** Easily modify or extend functionality according to specific needs.

---

## Features

- **Multiple Domain Support:** Scan one or multiple domains in a single execution.
- **Optional Wordlist Usage:** Incorporate a custom wordlist if available, or proceed with passive enumeration.
- **Organized Output:** Results are neatly segregated into individual files within a designated `Result` directory.
- **Scan History Separation:** Previous and new scan results are separated with timestamps for easy comparison.
- **User-Friendly Prompts:** Interactive prompts guide users through the scanning process.
- **Colorful Console Output:** Enhanced readability with color-coded messages and stylish ASCII art.
- **Error Handling:** Gracefully manages errors during execution, ensuring continuous operation across multiple domains.
- **Detailed Reporting:** Extracts and displays subdomains along with their associated IP addresses for comprehensive analysis.

---

## Installation

### Prerequisites

1. **Python 3.6 or Higher:**
   - Download and install Python from the [official website](https://www.python.org/downloads/).
   - During installation, ensure you check the option to **Add Python to PATH**.

2. **Amass:**
   - **Download Amass:**
     - Visit the [Amass GitHub Releases](https://github.com/OWASP/Amass/releases) page.
     - Download the appropriate binary for your operating system.
   - **Install Amass:**
     - Extract the downloaded archive.
     - Move the `amass` executable to a directory that's included in your system's PATH, or add its directory to the PATH environment variable.
   - **Verify Installation:**
     ```cmd
     amass -version
     ```
     *You should see the Amass version information.*

3. **Python Libraries:**
   - Install the required Python libraries using pip:
     ```cmd
     pip install colorama pyfiglet
     ```

### Clone the Repository

```cmd
git clone https://github.com/Root-FTW/AmaBridge.git
cd AmaBridge
```

---

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

   *Upon execution, you'll see a stylish ASCII banner and be prompted to input your domains and wordlist options.*

### Scanning Multiple Domains

During execution, when prompted, enter one or multiple domains separated by commas. For example:

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

   *If you choose not to use a wordlist, simply respond with `no`, and the script will proceed with passive enumeration.*

### Reviewing Results

1. **Navigate to the `Result` Directory:**

   ```cmd
   cd C:\AmaBridge\Result
   ```

2. **Locate Individual Result Files:**

   - **Per Domain Files:**
     - `example_com.txt`: Contains records of the scan.
     - `example_com.json`: Structured data with subdomain details.
     - `example_com.csv`: Comma-separated values for easier analysis.

3. **Understanding Scan Separations:**

   - Within each `.txt` file, scans are separated by clear timestamps, allowing users to differentiate between multiple scans for the same domain.

   **Example of Separator:**
   ```
   ----- Scan on 2023-10-05 14:30:00 -----
   ```

4. **Console Output:**
   - The script will display a list of found subdomains and their associated IP addresses directly in the console with color-coded formatting for enhanced readability.

---

## Automation

To schedule periodic scans using **AmaBridge**, leverage the **Task Scheduler** in Windows:

1. **Open Task Scheduler:**
   - Press `Win + R`, type `taskschd.msc`, and press Enter.

2. **Create a New Task:**
   - Click on **"Create Task..."** in the Actions pane.

3. **Configure General Settings:**
   - **Name:** AmaBridge Weekly Scan
   - **Description:** Automates weekly DNS enumeration using AmaBridge.
   - **Security Options:** Choose **"Run whether user is logged on or not"** for unattended scans.

4. **Set Triggers:**
   - **Trigger:** Weekly
   - **Start:** Choose your preferred start date and time.
   - **Repeat Task Every:** Select the desired frequency.

5. **Define Actions:**
   - **Action:** Start a program
   - **Program/script:** `python`
   - **Add arguments:** `C:\AmaBridge\ama_bridge.py`
   - **Start in:** `C:\AmaBridge\`

6. **Configure Conditions and Settings:**
   - Adjust conditions such as running the task only if the computer is on AC power, waking the computer to run the task, etc.

7. **Finalize and Save:**
   - Click **"OK"** and provide your user credentials if prompted.

**AmaBridge** will now execute automatically based on the defined schedule, ensuring continuous monitoring of your specified domains.

---

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

- **Colorama:** Enhances console output with color-coded messages for better readability and user experience.
- **Pyfiglet:** Generates stylish ASCII art for the project title, giving a modern and professional look.
- **Subprocess Module:** Executes Amass commands within the Python script, capturing output and handling errors.
- **JSON Handling:** Parses Amass's structured JSON output for detailed insights into subdomain discovery.
- **User Prompts:** Interactive inputs guide users through scanning and configuration steps.
- **Error Handling:** Ensures the script continues running even if certain scans fail, providing clear feedback on issues.

### Benefits Over Direct Amass Usage

- **Ease of Use:** Reduces the complexity of Amass commands by handling flags and options internally.
- **Organized Output:** Automatically segregates results per domain, enhancing readability and management.
- **Automated Wordlist Handling:** Simplifies the incorporation of wordlists without manual command adjustments.
- **Scalability:** Efficiently manages multiple domains in a single execution without user intervention.
- **Visual Enhancements:** Color-coded messages and ASCII art make the tool more engaging and easier to follow.
- **Repeatable Scans:** Clearly separates multiple scans for the same domain, aiding in tracking changes over time.

---

## Contributing

Contributions are welcome! If you'd like to enhance **AmaBridge**, please follow these steps:

1. **Fork the Repository:**
   - Click the **"Fork"** button at the top-right of this page.

2. **Clone Your Fork:**
   ```bash
   git clone https://github.com/Root-FTW/AmaBridge.git
   cd AmaBridge
   ```

3. **Create a New Branch:**
   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes:**
   - Commit your changes with clear and descriptive messages.
   ```bash
   git commit -m "Add Your Feature Description"
   ```

5. **Push to the Branch:**
   ```bash
   git push origin feature/YourFeatureName
   ```

6. **Open a Pull Request:**
   - Navigate to your forked repository on GitHub and click **"New Pull Request"**.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For any questions, suggestions, or support, feel free to reach out via [GitHub Issues](https://github.com/Root-FTW/AmaBridge/issues) or contact me directly through my GitHub profile.

---

**Stay secure and keep hacking responsibly with AmaBridge!**

```
