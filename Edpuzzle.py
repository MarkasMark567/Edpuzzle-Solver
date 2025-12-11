import importlib.util, os, time
print("\033cEnsuring dependencies ... ",end="",flush=True)
for module in ["google.generativeai","pyautogui","PIL"]:
    if not importlib.util.find_spec(module):
        os.system(f"pip install -U -q {module if module!='PIL' else 'pillow'}")
print("done\nImporting modules ... ",end="",flush=True)
import google.generativeai as genai
from PIL import ImageGrab
import pyautogui as gui
gui.useImageNotFoundException(False)
print("done")
API_KEY = "" ### SET THIS VARIABLE TO YOUR API KEY! ###
if not API_KEY:
    print("A Google Gemini API key is required for this program to function. You can get a free one at https://aistudio.google.com/api-keys.")
    print("NOTE: you can skip this step when running this program by setting the variable API_KEY to your own key.")
    API_KEY=input("Paste API key: ")
print("Verifying API key ... ",end="",flush=True)
genai.configure(api_key=API_KEY)
print("done")
chat = genai.GenerativeModel('gemini-2.5-flash',system_instruction = """
    You are an automated grading engine. Your task is to analyze the provided image of a multiple-choice question or problem.
    1. Identify the correct answer(s) based on the content of the image.
    2. Output strictly the number(s) corresponding to the correct option(s).
    3. If there are multiple correct answers, separate them with commas (e.g., "1,3,4").
    4. Do NOT provide explanations, introduction text, periods, or markdown formatting. Output ONLY the numbers.
    """).start_chat(history=[])

images = ['Checkbox.png','Question-Icon.png','Next-Question.png','Submit.png','Topleft-Corner.png','Bottomright-Corner.png','Continue.png','Final.png']
images = ['imgs\\'+i for i in images]
print("The program has started. Make sure all possible answer choices can be seen when a question appears.")

def isOnScreen(*images: str): return any([bool(gui.locateOnScreen(i,confidence=0.8)) for i in images])

time.sleep(3)

while True:
    if isOnScreen(images[1],images[6]):
        if not isOnScreen(images[2],images[3],images[6]):
            print('here')
            btmr=sorted([gui.center(loc) for loc in gui.locateAllOnScreen(images[5])],key=lambda c:c[0])[-1]
            img=ImageGrab.grab((*gui.locateCenterOnScreen(images[4]),*btmr))
            answerCoords = sorted([gui.center(loc) for loc in gui.locateAllOnScreen(images[0],confidence=0.8)],key=lambda c:c[1])
            for num in chat.send_message(img).text.split(","): gui.leftClick(answerCoords[int(num)-1])
        gui.leftClick(next((coord for coord in [gui.locateCenterOnScreen(images[x],confidence=0.8) for x in [2,3,6]] if coord is not None),(None,None)))
    elif isOnScreen(images[7]):
        gui.leftClick(gui.locateCenterOnScreen(images[7],confidence=0.8))

        break
