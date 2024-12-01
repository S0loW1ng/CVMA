## README

### OPSEC sanitisation tool

This Flask-based application is designed to help users identify and understand their digital footprint by processing user-submitted data, querying external APIs, and generating structured JSON reports. It provides detailed insights into compromised information, such as usernames, emails, passwords, and more. Tailored for OPSEC purposes, this tool empowers users to pinpoint potential data leaks and take proactive steps to remove sensitive information from the internet, ultimately reducing their attack surface and enhancing personal security

---

### Features

1. **Form Input**:
   - Users can submit emails, usernames, first names, and last names via a web-based form.
   
2. **Integration with External APIs**:
   - Queries **LeakCheck API** for leaked credentials and other associated information.
   - Uses **ProxyNova API** to retrieve proxy-related data for given emails.
   - Executes **Sherlock** to find associated accounts for given usernames.

3. **Output JSON**:
   - Processes and consolidates data into JSON format, categorizing passwords, emails, usernames, addresses, and associated accounts.


---

### Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd project
   ```

2. **Install Dependencies**:
   Ensure you have Python 3 installed, then install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**:
   Export your API key for LeakCheck:
   ```bash
   export API=<your_leakcheck_api_key>
   ```

4. **Run the Application**:
   Start the Flask server:
   ```bash
   python app.py
   ```

5. **Access the Application**:
   Open a browser and go to:
   ```
   http://127.0.0.1:5000
   ```

---

### Usage

1. **Submit Data**:
   - Enter emails, usernames, first name, and last name into the form on the web page.

2. **Processing**:
   - The backend processes the data and queries:
     - **LeakCheck API** for leaked information.
     - **ProxyNova API** for proxy-related data.
     - **Sherlock** for social account details.

3. **View Results**:
   - The processed data is displayed as a formatted JSON file in a new browser window.

---

### Environment Variables

- `API`: API key for the LeakCheck API.
- Make sure to export this variable before running the application.

---

### Dependencies


Install using:

```bash
pip install -r requirements.txt
```

---

### Known Issues

1. **Sherlock Output Delay**:
   - Processing Sherlock output may take time for larger username lists.
   
2. **ProxyNova API**:
   - Limited responses based on free-tier usage.
   
3. **Environment Variables**:
   - Ensure the `API` variable is correctly exported; otherwise, API queries will fail.

---

### License

This project is licensed under the MIT License. See the LICENSE file for more information.

--- 

