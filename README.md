# AWS Captcha Automation

Automating AWS CAPTCHA solving using Python and Selenium.
This project is intended for research, test automation, and integration into custom pipelines.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: Selenium](https://img.shields.io/badge/Framework-Selenium-green.svg)](https://www.selenium.dev/)

## 🎬 Demo

<img src="aws_catcha.gif" width="600">

---

## 🚀 Features

* **Class-based architecture** — modular design for easy integration
* **Intelligent iframe handling** — automatic discovery of AWS security containers
* **Request and session synchronization** — prevents 403 Forbidden errors
* **Advanced logging** — based on loguru with colorized output
* **Automatic cleanup** — automatically removes temporary captcha files
* **Human-like interaction** — realistic input and latency
* **Continuous monitoring mode** — optional loop resolution

---

## 🛠 Installation

Clone the repository:

```bash
git clone https://github.com/rtf-labs-studio/aws-captcha-automation.git
cd aws-captcha-automation
```

Create Virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Installing dependencies:

```bash
pip install -r requirements.txt
```

---

## 📖 Usage

The `CaptchaHandler` class manages the entire security check lifecycle.

```python
from selenium import webdriver
from captcha_handler import CaptchaHandler

# Driver initialization
driver = webdriver.Chrome()

# Handler setup
API_KEY = "YOUR_2CAPTCHA_API_KEY"
handler = CaptchaHandler(driver, API_KEY)

# Navigate to a secure AWS page
driver.get("https://target-website-with-aws.com")

# Captcha solving
handler.solve_security_check(single_run=True)
```

---

## ⚙️ How it works

The module follows a structured execution flow:

1. **Detection**
Scans the DOM for *security check* elements

2. **Isolation**

Finds the AWS container and switches to iframe

3. **Capture**

Waits for a captcha image and loads it

4. **Solve**
Submits the image to the 2Captcha API

5. **Submit**
Enters the solution and submits the form

6. **Restore**
Returns the driver to `default_content`

---

## 🔧 Configuration

Available parameters:

* `single_run=True` — single run or continuous monitoring

---

## 🧠 Use Cases

* Web scraping behind AWS WAF
* Automated bots
* Testing secure endpoints
* High-load distributed crawlers

---

## ⚠️ Disclaimer

This project is intended for:

* research Purposes
* Automated testing
* Educational purposes

Use responsibly and comply with the target website's terms of service.

---

## 🤝 Contribution

Pull requests are welcome.

For significant changes, please first create an issue.

---

## ⭐ Support

If you find this project useful, please rate it.

Our channel: https://t.me/rtf_labs_studio