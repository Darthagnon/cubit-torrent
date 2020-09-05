import json
import re  # nosec
import ipywidgets  # pylint: disable=import-error
from IPython.display import HTML, clear_output, display  # pylint: disable=import-error
from google.colab import files  # pylint: disable=import-error
from glob import glob
from sys import exit as exx


# JDownloader =================================================================

Email = ipywidgets.Text(placeholder="*Required", description="Email:")
Password = ipywidgets.Text(placeholder="*Required", description="Password:")
Device = ipywidgets.Text(placeholder="Optional", description="Name:")
SavePath = ipywidgets.Dropdown(
    value="/content/Downloads",
    options=["/content", "/content/Downloads"],
    description="Save Path:",
)


def refreshJDPath(a=1):
    if checkAvailable("/content/drive/"):
        if checkAvailable("/content/drive/Shared drives/"):
            SavePath.options = (
                ["/content", "/content/Downloads", "/content/drive/My Drive"]
                + glob("/content/drive/My Drive/*/")
                + glob("/content/drive/Shared drives/*/")
            )
        else:
            SavePath.options = [
                "/content",
                "/content/Downloads",
                "/content/drive/My Drive",
            ] + glob("/content/drive/My Drive/*/")
    else:
        SavePath.options = ["/content", "/content/Downloads"]


def exitJDWeb():
    runSh("pkill -9 -e -f java")
    clear_output(wait=True)
    createButton("Start", func=startJDService, style="info")


def confirmJDForm(a):
    clear_output(wait=True)
    action = a.description
    createButton(f"{action} Confirm?")
    if action == "Restart":
        createButton("Confirm", func=startJDService, style="danger")
    else:
        createButton("Confirm", func=exitJDWeb, style="danger")
    createButton("Cancel", func=displayJDControl, style="warning")


def displayJDControl(a=1):
    clear_output(wait=True)
    createButton("Control Panel")
    display(
        HTML(
            """
            <h3 style="font-family:Trebuchet MS;color:#4f8bd6;">
                You can login to the WebUI by clicking
                    <a href="https://my.jdownloader.org/" target="_blank">
                        here
                    </a>.
            </h3>
            """
        ),
        HTML(
            """
            <h4 style="font-family:Trebuchet MS;color:#4f8bd6;">
                If the server didn't showup in 30 sec. please re-login.
            </h4>
            """
        ),
    )
    createButton("Re-Login", func=displayJDLoginForm, style="info")
    createButton("Restart", func=confirmJDForm, style="warning")
    createButton("Exit", func=confirmJDForm, style="danger")


def startJDService(a=1):
    runSh("pkill -9 -e -f java")
    runSh(
        "java -jar /root/.JDownloader/JDownloader.jar -norestart -noerr -r &",
        shell=True,  # nosec
    )
    displayJDControl()


def displayJDLoginForm(a=1):
    clear_output(wait=True)
    Email.value = ""
    Password.value = ""
    Device.value = ""
    refreshJDPath()
    display(
        HTML(
            """
            <h3 style="font-family:Trebuchet MS;color:#4f8bd6;">
                If you don't have an account yet, please register
                    <a href="https://my.jdownloader.org/login.html#register" target="_blank">
                        here
                    </a>.
            </h3>
            """
        ),
        HTML("<br>"),
        Email,
        Password,
        Device,
        SavePath,
    )
    createButton("Refresh", func=refreshJDPath)
    createButton("Login", func=startJDFormLogin, style="info")
    if checkAvailable(
        "/root/.JDownloader/cfg/org.jdownloader.api.myjdownloader.MyJDownloaderSettings.json"
    ):
        createButton("Cancel", func=displayJDControl, style="danger")


def startJDFormLogin(a=1):
    try:
        if not Email.value.strip():
            ERROR = "Email field is empty."
            THROW_ERROR
        if not "@" in Email.value and not "." in Email.value:
            ERROR = "Email is an incorrect format."
            THROW_ERROR
        if not Password.value.strip():
            ERROR = "Password field is empty."
            THROW_ERROR
        if not bool(re.match("^[a-zA-Z0-9]+$", Device.value)) and Device.value.strip():
            ERROR = "Only alphanumeric are allowed for the device name."
            THROW_ERROR
        clear_output(wait=True)
        if SavePath.value == "/content":
            savePath = {"defaultdownloadfolder": "/content/Downloads"}
        elif SavePath.value == "/content/Downloads":
            runSh("mkdir -p -m 666 /content/Downloads")
            savePath = {"defaultdownloadfolder": "/content/Downloads"}
        else:
            savePath = {"defaultdownloadfolder": SavePath.value}

        with open(
            "/root/.JDownloader/cfg/org.jdownloader.settings.GeneralSettings.json", "w+"
        ) as outPath:
            json.dump(savePath, outPath)
        if Device.value.strip() == "":
            Device.value = Email.value
        runSh("pkill -9 -e -f java")
        data = {
            "email": Email.value,
            "password": Password.value,
            "devicename": Device.value,
            "directconnectmode": "LAN",
        }
        with open(
            "/root/.JDownloader/cfg/org.jdownloader.api.myjdownloader.MyJDownloaderSettings.json",
            "w+",
        ) as outData:
            json.dump(data, outData)
        startJDService()
    except:
        print(ERROR)


def handleJDLogin(newAccount):
    installJDownloader()
    if newAccount:
        displayJDLoginForm()
    else:
        data = {
            "email": "daniel.dungngo@gmail.com",
            "password": "ZjPNiqjL4e6ckwM",
            "devicename": "daniel.dungngo@gmail.com",
            "directconnectmode": "LAN",
        }
        with open(
            "/root/.JDownloader/cfg/org.jdownloader.api.myjdownloader.MyJDownloaderSettings.json",
            "w+",
        ) as outData:
            json.dump(data, outData)
        startJDService()


# TO DO ===
# Update MAKE BUTTON FUNCTIONS
# FINISH MAKING ICONS
#
