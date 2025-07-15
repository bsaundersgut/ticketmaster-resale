# 🎫 Ticketmaster Resale Ticket Checker

A Python script using Selenium that continuously checks a specific Ticketmaster event page for **resale tickets** containing `"Weekend Camping"` in their name. When such tickets appear, it alerts you with a sound and **pauses for manual intervention**.

## ✅ Features

- Automatically navigates to the Ticketmaster event page
- Continuously searches for resale tickets
- Plays a beep sound when tickets are found
- Stops when tickets are detected and **waits for you to buy them manually**
- Robust error handling and wait timing

---

## 🖥️ Requirements

- Python 3.7+
- Google Chrome installed (script uses ChromeDriver)
- Windows OS (for `winsound` module – you can swap for `playsound` or alerts for macOS/Linux)

---

## 📦 Installation

1. **Clone the repository or save the script**
   ```bash
   git clone https://github.com/yourname/ticketmaster-resale-checker.git
   cd ticketmaster-resale-checker

