import pyautogui
import cv2
import sys
import numpy as np
import win32api
import win32gui, win32ui
from win32api import GetSystemMetrics

# np.set_printoptions(threshold=sys.maxsize)
# Specify resolution
resolution = (1920, 1080)
dc = win32gui.GetDC(0)
dcObj = win32ui.CreateDCFromHandle(dc)
hwnd = win32gui.WindowFromPoint((0, 0))
monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

# Specify frames rate. We can choose any
# value and experiment with it
fps = 60.0

# Create an Empty window
cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

# Resize this window
cv2.resizeWindow("Live", 480, 270)

stat_images = {}
stat_threshes = {}
stat_results = {}
stat_maxVal = {}
stat_maxLoc = {}
def find_max(values):
    max_value = -1
    max_key = ''
    for key in values:
        if max_value < values[key]:
            max_value = values[key]
            max_key = key

    return max_key, max_value

stat_images['hooked'] = cv2.imread("hooked.png", cv2.IMREAD_GRAYSCALE)
stat_images['dying'] = cv2.imread("dying.png", cv2.IMREAD_GRAYSCALE)
stat_images['healthy'] = cv2.imread("healthy.png", cv2.IMREAD_GRAYSCALE)
stat_images['injured'] = cv2.imread("injured.png", cv2.IMREAD_GRAYSCALE)
for key in stat_images:
    _, stat_threshes[key] = cv2.threshold(stat_images[key], 127, 255, 0)

cv2.imwrite('injuredthresh.png', stat_threshes['injured'])
while True:
    # Take screenshot using PyAutoGUI
    img = pyautogui.screenshot()

    frame = np.array(img)
    frame = frame[724:782, 220:271]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, screen_thresh = cv2.threshold(frame, 140, 255, 0)
    for key in stat_images:
        stat_results[key] = cv2.matchTemplate(screen_thresh, stat_threshes[key], cv2.TM_CCOEFF_NORMED)
        _, stat_maxVal[key], _, stat_maxLoc[key] = cv2.minMaxLoc(stat_results[key])
        x, y = stat_maxLoc[key]
        print(stat_maxVal[key])
        max_key, val = find_max(stat_maxVal)
        if val >= 0.25:
            print(max_key)
            cv2.rectangle(screen_thresh, (x, y), (x + 50, y + 50), (255, 255, 255))

    m = win32gui.GetCursorPos()
    #print(m)
    # dcObj.Rectangle((x,y,x+30,y+30))
    # win32gui.InvalidateRect(hwnd, monitor, True) # Refresh the entire monitor
    # Optional: Display the recording screen
    cv2.imshow('Live', screen_thresh)

    # Stop recording when we press 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Destroy all windows
cv2.destroyAllWindows()


