import time
from langchain.tools import tool
import webbrowser
import os
# import pyautogui
import wikipedia
import pywhatkit
import psutil
import winshell
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
from modules.voice import speak
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

SMTP_MAIL_ID = os.getenv("SMTP_MAIL_ID") 
SMTP_MAIL_PASSWORD = os.getenv("SMTP_MAIL_PASSWORD") 


def validate_site(site: str) -> str:
    """
    Validate and format the website name into a proper domain.
    
    Args:
        site (str): The name or URL of the website.
    
    Returns:
        str: A valid domain name or URL-ready string.
    """
    site = site.strip().lower()
    known_sites = {
        "google": "www.google.com",
        "youtube": "www.youtube.com",
        "facebook": "www.facebook.com",
        "twitter": "www.twitter.com",
        "instagram": "www.instagram.com",
        "linkedin": "www.linkedin.com",
        "github": "www.github.com",
        "reddit": "www.reddit.com",
        "wikipedia": "www.wikipedia.org",
        "stackoverflow": "www.stackoverflow.com",
        "amazon": "www.amazon.com",
        "netflix": "www.netflix.com",
        "spotify": "www.spotify.com",
        "twitch": "www.twitch.tv",
        "discord": "www.discord.com",
        "whatsapp": "www.whatsapp.com",
        "gmail": "www.gmail.com",
        "yahoo": "www.yahoo.com",
        "bing": "www.bing.com",
        "duckduckgo": "www.duckduckgo.com",
        "quora": "www.quora.com",
        "pinterest": "www.pinterest.com",
        "leetcode": "www.leetcode.com",
        "medium": "www.medium.com",
        "slack": "www.slack.com",
        "zoom": "www.zoom.us",
        "microsoft": "www.microsoft.com",
        "apple": "www.apple.com",
    }
    if site.startswith("http"):
        site = site.split("//")[-1]
    else:
        site = known_sites.get(site, site)
    return site


@tool
def open_website(site: str) -> None:
    """
    Opens a website in the default browser.

    Args:
        site (str): Name or URL of the website to open.

    Returns:
        None
    """
    site = validate_site(site)
    speak(f"Opening in your browser.")
    webbrowser.open(f"https://{site}")

# @tool
# def increase_volume(value=5) -> None:
#     """
#     Increases the system volume by value or default 5 steps.

#     Args:
#         value (int): steps of volumen.

#     Returns:
#         None
#     """
#     for _ in range(value):
#         pyautogui.press("volumeup")
#     speak(f"Volume increased by {value} steps.")

# @tool
# def decrease_volume(value=5) -> None:
#     """
#     Decreases the system volume by value or default 5 steps.
    
#     Args:
#         value (int): steps of volumen.

#     Returns:
#         None
#     """
#     for _ in range(value):
#         pyautogui.press("volumedown")
#     speak(f"Volume decreased by {value} steps.")

# @tool
# def mute_volume() -> None:
#     """
#     Mutes the system volume.

#     Returns:
#         None
#     """
#     pyautogui.press("volumemute")


# @tool
# def unmute_volume() -> None:
#     """
#     Unmutes the system volume.

#     Returns:
#         None
#     """
#     pyautogui.press("volumemute")


@tool
def shutdown_system() -> None:
    """
    Shuts down the system immediately.

    Returns:
        None
    """
    os.system("shutdown /s /t 1")


@tool
def restart_system() -> None:
    """
    Restarts the system immediately.

    Returns:
        None
    """
    os.system("shutdown /r /t 1")


@tool
def get_battery_status() -> str:
    """
    Retrieves the current battery status.

    Returns:
        str: Battery percentage and charging status.
    """
    battery = psutil.sensors_battery()
    if battery is None:
        return "Battery status not available on this system."
    speak(f"{battery.percent}% & {'charging' if battery.power_plugged else 'not charging'}.")
    return f"Battery is at {battery.percent}%, {'charging' if battery.power_plugged else 'not charging'}."


@tool
def empty_recycle_bin() -> None:
    """
    Empties the system recycle bin.

    Returns:
        None
    """
    winshell.recycle_bin().empty(confirm=True, show_progress=True, sound=True)
    speak("Recycle bin emptied successfully!")

# @tool
# def take_screenshot() -> str:
#     """
#     Takes a screenshot and saves it to the 'captures' directory.

#     Returns:
#         str: File path where the screenshot was saved.
#     """
#     os.makedirs("captures", exist_ok=True)
#     screenshot = pyautogui.screenshot()
#     random_filename = f"screenshot_{int(time.time())}.png"
#     path = f"captures/{random_filename}"
#     screenshot.save(path)
#     speak("Screenshot taken successfully!")
#     return f"Screenshot taken and saved as {path}."


@tool
def search_wikipedia(query: str) -> str:
    """
    Searches Wikipedia and returns a 2-sentence summary.

    Args:
        query (str): The search term.

    Returns:
        str: Summary text or error message.
    """
    try:
        response = wikipedia.search(query,sentences=2)
        speak(f"{response}")
        return response
    except Exception:
        return "Sorry, I couldn't find that on Wikipedia."


@tool
def play_on_youtube(song: str) -> None:
    """
    Plays a song or video on YouTube in the browser.

    Args:
        song (str): Name of the song or search term.

    Returns:
        None
    """
    pywhatkit.playonyt(song)
    speak(f"Playing {song} on YouTube.")


@tool
def send_email(to: str, 
               subject: str = "Drink Water",
               body: str = "Hey, You are doing great, this is a just reminder to drink water and stay hydrated!"
               ) -> None:
    """
    Sends an email using SMTP.

    Args:
        to (str): Recipient email address.
        subject (str): Subject of the email.
        body (str): Message body.

    Returns:
        None
    """
    msg = EmailMessage()
    msg["From"] = SMTP_MAIL_ID
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SMTP_MAIL_ID, SMTP_MAIL_PASSWORD)
        smtp.send_message(msg)

    speak("Email sent successfully! to " + to.split('@')[0])


@tool
def run_python_script(script_name: str) -> None:
    """
    Executes a local Python script by filename.

    Args:
        script_name (str): Filename of the script (e.g. 'script.py').

    Returns:
        None
    """
    try:
        os.system(f"python {script_name}")
        speak(f"Running {script_name}")
    except Exception:
        speak("Failed to run script")

from langchain_community.tools import DuckDuckGoSearchRun

tools = [
    open_website,
    send_email,
    run_python_script,
    # increase_volume,
    # decrease_volume,
    # mute_volume,
    # unmute_volume,
    shutdown_system,
    restart_system,
    get_battery_status,
    empty_recycle_bin,
    # take_screenshot,
    search_wikipedia,
    play_on_youtube,
    DuckDuckGoSearchRun().as_tool()
]
