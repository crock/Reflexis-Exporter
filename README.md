# Reflexis-Exporter

With this little tool, you can export your work schedule to the standard vCalendar format for easy import into your calendar application of choice.

To use, you will need to run the Python 3 installer. You can download that from [here](https://python.org/download). Be sure to tick the checkbox `Add Python to environment variables` during the installation process.

After Python is installed, open your default terminal application. This will be `Command Prompt.exe` (CMD) on Windows or `Terminal.app` on macOS. You now need to install the dependencies that the application requires in order to run.
Simply type this command in the window and it should install all of them automatically.
```
pip install requests bs4 icalendar
```

Open `main.py` in a text editor and fill in your Reflexis username and password on lines 9 & 10 inside the quotation marks. If done right, it should look like this...

```python
USERNAME = "YourUsernameHere"
PASSWORD = "passw0rd123"
```

Now you are ready to run the application!

Type the word `python` followed by a space in the terminal window and then drag and drop the `main.py` you downloaded into the window. It should pre-fill the path to the file for you. Now just hit the enter or return key. 

Once the script has finished running, you should see a file called `work_calendar.ics` in the same directory as `main.py`. This will be the file you import into your calendar application.