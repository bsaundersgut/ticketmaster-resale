# Ticket Checker Script

A Selenium-based script to monitor Ticketmaster resale tickets and alert you when tickets become available. The browser stays open for manual intervention to complete the purchase.

---

## ⚙️ Setup

### 1. Install required Python packages

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install selenium webdriver-manager
```

---

## 📜 Usage

1. Open `ticket_checker.py` and ensure the URL is correct for your event:

```python
url = "https://www.ticketmaster.ie/all-together-now-weekend-camping-portlaw-31-07-2025/event/18006117864E1B03"
```

2. Run the script:

```bash
python ticket_checker.py
```

3. When a matching ticket is found:

- You’ll hear a beep
- The browser will stay on the page for manual ticket purchase

---

## 🔔 Optional: Custom Alerts

To make the alert louder or longer, change the beep line in the script:

```python
winsound.Beep(1000, 1500)  # frequency (Hz), duration (ms)
```

> **Note:** On macOS/Linux, `winsound` is not available. Instead, install `playsound`:

```bash
pip install playsound
```

Then use in Python:

```python
from playsound import playsound
playsound("alert.mp3")
```

---

## 🛑 Stop the Script

Press **Ctrl + C** in your terminal to stop at any time.

---

## ⚠️ Disclaimer

This script is provided for educational and personal use. Use responsibly and at your own risk. Ticketmaster may change their website structure at any time, which can break the script.

---

## 🛠 Troubleshooting

- **ChromeDriver version mismatch?**  
  Make sure your Chrome browser is up-to-date. `webdriver-manager` automatically handles ChromeDriver versions.

- **Page loads too slowly?**  
  Increase the `time.sleep()` delays slightly in the script.

---

## 📄 License

MIT License — free to use and modify.
