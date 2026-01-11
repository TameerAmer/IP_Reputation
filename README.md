# IP Reputation Checker

A Python application to check the reputation of IP addresses using the [AbuseIPDB](https://www.abuseipdb.com/) API. This tool helps identify potentially malicious IP addresses by checking their abuse confidence scores and reporting history.

## 📋 Table of Contents

- [What Does This Do?](#what-does-this-do)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Quick Start (For Reviewers)](#quick-start-for-reviewers)
- [Getting Your API Key](#getting-your-api-key)
- [How to Use](#how-to-use)
- [Running Tests](#running-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [Docker Setup (Optional)](#docker-setup-optional)
- [Troubleshooting](#troubleshooting)
- [Known Limitations & Performance Considerations](#known-limitations--performance-considerations)
- [Project Structure](#project-structure)
- [Support](#support)
- [Credits](#credits)

---

## What Does This Do?

This application checks IP addresses against the AbuseIPDB database to determine if they have been reported for malicious activity. It provides:

- **Single IP Check** (`check_ip`): Check one IP address at a time
- **Batch IP Check** (`check_ip_batch`): Check multiple IP addresses in one run
- **Risk Assessment**: Categorizes IPs as HIGH, MEDIUM, or LOW risk
- **Detailed Reports**: Returns abuse confidence scores, total reports, country codes, and ISP information

---

## Prerequisites

Before you start, you need:

1. **A Computer** running Windows, macOS, or Linux
2. **Python 3.8 or newer** installed on your computer
3. **An AbuseIPDB API Key** (free - see instructions below)
4. **Internet Connection** to communicate with the AbuseIPDB API

### Check if Python is Installed

Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux) and type:

```bash
python --version
```

or

```bash
python3 --version
```

You should see something like `Python 3.12.0`. If you see an error, you need to install Python first from [python.org](https://www.python.org/downloads/).

---

## Installation Guide

### Step 1: Download the Code

If you have the code as a ZIP file, extract it to a folder on your computer.

If you're using Git:

```bash
git clone https://github.com/TameerAmer/IP_Reputation.git
cd IP_Reputation
```

### Step 2: Create a Virtual Environment

A virtual environment keeps this project's dependencies separate from your other Python projects.

**On Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

You'll see `(.venv)` appear at the beginning of your command line when it's activated.

### Step 3: Install Required Packages

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This installs all the necessary libraries the application needs.

---
## Quick Start (For Reviewers)

**Want to test the application immediately?** Use this test API key created specifically for assignment evaluation:

> ✅ **If you're using this Quick Start guide, you can skip ahead to [How to Use](#how-to-use) once you've tested the commands below. ** You only need to follow [Getting Your API Key](#getting-your-api-key) if you want to set up your own account for regular use.

### Test with Single IP Check
```bash
# Set the test API key
export ABUSEIPDB_API_KEY="0f638e87fce7988030b6c1b860511a80f5b534498ef9b1ee918bed878ff45de164a45fe64b9c9a56"

# Check a single IP
export IP_ADDRESS="8.8.8.8"
python -m check_ip.main
```

### Test with Batch IP Check
```bash
# Set the test API key  
export ABUSEIPDB_API_KEY="0f638e87fce7988030b6c1b860511a80f5b534498ef9b1ee918bed878ff45de164a45fe64b9c9a56"

# Check multiple IPs
export IP_ADDRESSES="118.25.6.39,8.8.8.8,1.1.1.1,185.220.101.1"
python -m check_ip_batch.main
```

### Docker Quick Test
```bash
# Single IP
docker build -t check-ip -f check_ip/Dockerfile .
docker run --rm -e ABUSEIPDB_API_KEY="0f638e87fce7988030b6c1b860511a80f5b534498ef9b1ee918bed878ff45de164a45fe64b9c9a56" \
           -e IP_ADDRESS="8.8.8.8" check-ip

# Batch
docker build -t check-ip-batch -f check_ip_batch/Dockerfile .
docker run --rm -e ABUSEIPDB_API_KEY="0f638e87fce7988030b6c1b860511a80f5b534498ef9b1ee918bed878ff45de164a45fe64b9c9a56" \
           -e IP_ADDRESSES="118.25.6.39,8.8.8.8" check-ip-batch
```

> **Note for Reviewers:**  
> This test account uses the free tier (1,000 requests/day). If you encounter rate limits,  
> you can create your own account in 5 minutes - see [Getting Your API Key](#getting-your-api-key).


---

## Getting Your API Key

1. **Sign Up** for a free account at [AbuseIPDB](https://www.abuseipdb.com/register)
2. **Verify** your email address
3. **Get Your API Key**:
   - Log in to your AbuseIPDB account
   - Go to your [API page](https://www.abuseipdb.com/account/api)
   - Copy your API key (it looks like a long string of letters and numbers)

### Set Up Your API Key

You need to tell the application your API key. There are two ways:

#### Option 1: Environment Variable (Recommended)

**On Windows (PowerShell):**

```powershell
$env:ABUSEIPDB_API_KEY="your-api-key-here"
```

**On Windows (Command Prompt):**

```cmd
set ABUSEIPDB_API_KEY=your-api-key-here
```

**On macOS/Linux:**

```bash
export ABUSEIPDB_API_KEY="your-api-key-here"
```

Replace `your-api-key-here` with your actual API key.

#### Option 2: Create a `.env` file

Create a file named `.env` in the project root directory with this content:

```
ABUSEIPDB_API_KEY=your-api-key-here
```

---

## How to Use

### Check a Single IP Address

1. **Set the IP address** you want to check:

   **Windows (PowerShell):**
   ```powershell
   $env:IP_ADDRESS="118.25.6.39"
   ```

   **Windows (Command Prompt):**
   ```cmd
   set IP_ADDRESS=118.25.6.39
   ```

   **macOS/Linux:**
   ```bash
   export IP_ADDRESS="118.25.6.39"
   ```

2. **Run the check:**

   ```bash
   python -m check_ip.main
   ```

3. **View the results** - you'll see JSON output with:
   - Abuse confidence score (0-100)
   - Risk level (HIGH/MEDIUM/LOW)
   - Total reports
   - Country code
   - ISP information

### Check Multiple IP Addresses (Batch)

1. **Set multiple IP addresses** (comma-separated):

   **Windows (PowerShell):**
   ```powershell
   $env:IP_ADDRESSES="118.25.6.39, 185.220.101.1, 8.8.8.8"
   ```

   **Windows (Command Prompt):**
   ```cmd
   set IP_ADDRESSES=118.25.6.39, 185.220.101.1, 8.8.8.8
   ```

   **macOS/Linux:**
   ```bash
   export IP_ADDRESSES="118.25.6.39, 185.220.101.1, 8.8.8.8"
   ```

2. **Run the batch check:**

   ```bash
   python -m check_ip_batch.main
   ```

3. **View the results** - you'll see a summary including:
   - Total IPs checked
   - Successful vs failed checks
   - Risk level distribution
   - Detailed results for each IP

### Customize Risk Thresholds (Optional)

By default, an abuse confidence score of 70 or higher is considered HIGH risk. To change this:

**Windows (PowerShell):**
```powershell
$env:CONFIDENCE_THRESHOLD="80"
```

**macOS/Linux:**
```bash
export CONFIDENCE_THRESHOLD="80"
```

---

## Running Tests

To make sure everything is working correctly, you can run the test suite.

### Make sure you're in the virtual environment

You should see `(.venv)` at the start of your command prompt. If not, activate it again:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Run specific test modules

**Test AbuseIPDB API functions:**
```bash
python -m unittest abuseipdb/tests/test_api_call.py 
```

**Test single IP checker:**
```bash
python -m unittest check_ip/tests/test_main.py
```

**Test batch IP checker:**
```bash
python -m unittest check_ip_batch/tests/test_main.py
```

If all tests pass, you'll see `OK` at the end. If any fail, you'll see detailed error messages.

---
## CI/CD Pipeline

This project includes automated testing and Docker image building through GitHub Actions.

### Automated Testing

Every pull request triggers automated tests to ensure code quality:

- Runs all unit tests across the project
- Uses Python 3.12
- Must pass all tests before merging to `main`

### Docker Image Building & Publishing (Production)

The workflow includes a commented-out section for building and pushing Docker images to a registry. This is intended for production deployment and requires additional setup.

#### To Enable Image Building:

1. **Choose a Docker Registry**:
   - [Docker Hub](https://hub.docker.com/) (free tier available)
   - [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) (free)
   - Or your preferred registry

2. **Create Docker Repositories** (if using Docker Hub):
    - Create two repositories with these exact names:
       - `check-ip`
       - `check-ip-batch`
    - Keep your Docker Hub username handy for the next step

3. **Set Up Registry Credentials** in your GitHub repository:
   - Go to Settings → Secrets and variables → Actions
   - Add your registry credentials:
       - `DOCKER_USERNAME`: Your Docker Hub username
       - `DOCKER_PASSWORD`: Your Docker Hub access token (from Account Settings → Security)

4. **Update the Workflow File** (`.github/workflows/auto_tests.yml`):
   - Uncomment the `build-and-push-images` section
   - Configure the image registry and repository names
   - Update the Docker image push commands with your registry details

5. **Images are built only when**:
   - All tests pass
   - Workflow is manually triggered or on pull request/push events (depending on configuration)

---

## Docker Setup (Optional)

If you prefer to use Docker instead of installing Python directly:

### Prerequisites for Docker

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Make sure Docker is running

### Run with Docker

**For single IP check:**

```bash
docker build -t check-ip -f check_ip/Dockerfile .
docker run -e ABUSEIPDB_API_KEY="your-api-key" -e IP_ADDRESS="118.25.6.39" check-ip
```

**For batch IP check:**

```bash
docker build -t check-ip-batch -f check_ip_batch/Dockerfile .
docker run -e ABUSEIPDB_API_KEY="your-api-key" -e IP_ADDRESSES="118.25.6.39, 8.8.8.8" check-ip-batch
```

---

## Troubleshooting

### "Python is not recognized" error

- **Problem**: Python is not installed or not in your PATH
- **Solution**: Download and install Python from [python.org](https://www.python.org/downloads/). During installation, make sure to check "Add Python to PATH"

### "No module named 'requests'" error

- **Problem**: Required packages are not installed or virtual environment is not activated
- **Solution**: 
  1. **First**, activate your virtual environment (if you haven't already):
     - **Windows**: `.venv\Scripts\activate`
     - **macOS/Linux**: `source .venv/bin/activate`
  2. **Then**, install the required packages: `pip install -r requirements.txt`

### "Invalid API key" error

- **Problem**: Your API key is incorrect or not set
- **Solution**: 
  1. Double-check your API key on the AbuseIPDB website
  2. Make sure you've set the `ABUSEIPDB_API_KEY` environment variable correctly
  3. Try setting it again (copy-paste to avoid typos)

### "Command not found" error on macOS/Linux

- **Problem**: You might need to use `python3` instead of `python`
- **Solution**: Replace `python` with `python3` in all commands


### Tests are failing

1. Make sure your virtual environment is activated
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Check that you have an internet connection (some tests mock API calls, but imports still need to work)

---
## Known Limitations & Performance Considerations

#### API Rate Limits

The free tier of AbuseIPDB has the following limitations:

- **1,000 requests per day** (resets at midnight UTC)
- **No per-second rate limit** (but we implement a 0.1-second delay to be respectful to the API)

#### Performance with Large Batches

The batch IP checker implements a 0.1-second delay between requests to:

- Avoid overwhelming the API with rapid-fire requests
- Be a good API citizen (even though there's no enforced limit)
- Reduce the chance of triggering any undocumented rate limiting

Expected processing times:

| Number of IPs | Estimated Time | API Calls Used | Remaining (Free Tier) |
|--------------|----------------|----------------|----------------------|
| 10 IPs       | ~1 second      | 10/1000        | 990                  |
| 50 IPs       | ~5 seconds     | 50/1000        | 950                  |
| 100 IPs      | ~10 seconds    | 100/1000       | 900                  |
| 500 IPs      | ~50 seconds    | 500/1000       | 500                  |
| 1,000 IPs    | ~1.7 minutes   | 1000/1000      | 0 (limit reached)    |

#### What Happens When You Hit the Daily Limit

When you exceed 1,000 requests in a day, the API will return an error:

- The tool will report status code 2 (API error)
- Individual IPs that failed will appear in the `errors` object
- If you're running a batch and hit the limit mid-way, you'll get partial results

Example output when limit is hit:

```json
{
  "step_status": {
    "code": 0,
    "message": "partial_success"
  },
  "api_object": {
    "summary": {
      "total": 100,
      "successful": 47,
      "failed": 53,
      "risk_counts": {"HIGH": 5, "MEDIUM": 12, "LOW": 30}
    },
    "results": { ... },
    "errors": {
      "192.168.1.50": "API request failed",
      "192.168.1.51": "API request failed",
      ...
    }
  }
}
```
---

## Project Structure

```
IP_Reputation/
├── abuseipdb/              # Core API interaction module
│   ├── api_call.py         # API functions
│   └── tests/              # Unit tests
├── check_ip/               # Single IP checker
│   ├── main.py             # Single IP entry point
│   ├── Dockerfile          # Docker configuration
│   └── tests/              # Unit tests
├── check_ip_batch/         # Batch IP checker
│   ├── main.py             # Batch entry point
│   ├── Dockerfile          # Docker configuration
│   └── tests/              # Unit tests
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Support

If you encounter any issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review the error message carefully - it often tells you what's wrong
3. Make sure you followed all installation steps in order
4. Open an issue on the GitHub repository with:
   - The exact error message
   - What you were trying to do
   - Your operating system (Windows/macOS/Linux)

---

## Credits

- Uses the [AbuseIPDB API](https://www.abuseipdb.com/)
- Built with Python and the `requests` library
