import csv
import random
from datetime import datetime
from psychopy import visual, event, core, monitors, gui

# Initialization
num_trials = 170
stim_time = 0.1

offset_init = 0.15
step_size = 0.01
max_value = 0.25

spacing = 0.3
spacing_jitter = 0.02 

block_conditions = [
    {'label':'Block 1: Monocular_Standard', 'spacing': 0, 'crowdCount': 0, 'eccentricity': 0},
    {'label':'Block 2: Monocular_Crowded', 'spacing': spacing , 'crowdCount': 1, 'eccentricity': 0},
    {'label':'Block 3: Monocular_Standard', 'spacing': 0, 'crowdCount': 0, 'eccentricity': 0},
    {'label':'Block 4: Monocular_Crowded', 'spacing': spacing , 'crowdCount': 1, 'eccentricity': 0},
]

expInfo = {'participantID': '', 'session': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title='Vernier Experiment')
participant_name = expInfo['participantID']
session_num = expInfo['session']
start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

fileName = f'amblyopia_data_{participant_name}_amblyopic_eye.csv'
data_file = open(fileName, 'w', newline='')
writer = csv.writer(data_file)
writer.writerow(['label', 'trials', 'offset', 'trial_spacing', 'keys', 'direction', 'response_time', 'accuracy','response_numeric'])

fileName2 = f'amblyopia_data_{participant_name}_amblyopic_eye_parameters.csv'
data_file2 = open(fileName2, 'w', newline='')
writer_para= csv.writer(data_file2)
writer_para.writerow(['participant_name', 'session_num', 'amblyopic_eye', 'contrast', 'screen_width', 'screen_height', 'step_size', 'max_value', 'num_trials', 'lineHight', 'lineThickness', 'stim_time', 'spacing', 'start_time', 'end_time'])

binocular_param_file = f'amblyopia_data_{participant_name}_binocular_parameters.csv'


with open(binocular_param_file, 'r', newline='') as f:
    reader = csv.DictReader(f)
    params = next(reader)
amblyopic_eye = params['amblyopic_eye']
matched_contrast = float(params['contrast'])

# win = visual.Window(fullscr=True, color='white', units='pix')
# SCREEN_WIDTH, SCREEN_HEIGHT = map(int, win.size) # retrieve screen resolution automatically
SCREEN_WIDTH = 3200
SCREEN_HEIGHT = 2000
mon = monitors.Monitor('tempMonitor')
mon.setWidth(58.5)
mon.setDistance(54.5)
mon.setSizePix([SCREEN_WIDTH, SCREEN_HEIGHT])

win = visual.Window(fullscr=True, color='white', units='deg', monitor=mon)
win.mouseVisible = False
rt_clock = core.Clock()

def stop_experiment():
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    writer_para.writerow([participant_name, session_num, amblyopic_eye, matched_contrast, SCREEN_WIDTH, SCREEN_HEIGHT, step_size, max_value, num_trials, lineHeight, lineThickness, stim_time, spacing, start_time, end_time])
    data_file.close()
    data_file2.close()
    win.close()
    core.quit()


# Stimuli
dichoptic_offset = 0.05

lineHeight = 1.5
lineThickness = 2

cross_size = 0.4
cross_width = 4

red_color = [1, 0, 1]
blue_color = [0, 1, 1]

if amblyopic_eye == 'left' or amblyopic_eye == 'l':
    amblyopic_eye_color = blue_color
elif amblyopic_eye == 'right' or amblyopic_eye == 'r':
    amblyopic_eye_color = red_color

circle_amb = visual.Circle(
    win=win,
    radius=cross_size,
    lineColor=amblyopic_eye_color,
    fillColor=None,
    lineWidth=cross_width,
    opacity=0.7
)

square_amb = visual.Rect(
    win=win,
    width=cross_size * 2,
    height=cross_size * 2,
    lineColor=amblyopic_eye_color,
    fillColor=None,
    lineWidth=cross_width,
    opacity=0.7
)


# Display experiment
first_page = visual.TextStim(
    win,
    text='Hello!\n\n'
         '1. Please keep looking at the black cross during the trials.\n\n'
         '2. If the upper line is to the right, press the RIGHT arrow key.\n\n'
         '3. If the upper line is to the left, press the LEFT arrow key.\n\n'
         '\n\n'
         'Press SPACE to continue.',
    color='black',
    height=1.5, # front size
    wrapWidth=45,
    alignText='left'
)
first_page.draw()
win.flip()

event.clearEvents()
first_keys = []
while not first_keys:
    first_keys = event.getKeys(keyList=['space', 'escape'])
    core.wait(0.05)
if 'escape' in first_keys:
    win.close()
    core.quit()

for condition in block_conditions:

    # Condition parameters
    streak = 0
    vernier_offset = offset_init
    
    current_spacing = condition['spacing']
    current_crowdCount = condition['crowdCount']
    current_eccentricity = condition['eccentricity']
    block_label = condition['label']


    # Instructions
    msg = visual.TextStim(
        win,
        text=f'Starting {block_label}\n\n'
            '\n\n'
            'Press SPACE to continue.',
        color='black',
        height=1.5, # front size
        wrapWidth=45,
        alignText='left'
    )
    msg.draw()
    win.flip()

    event.clearEvents()
    block_keys = []
    while not block_keys:
        block_keys = event.getKeys(keyList=['space', 'escape'])
        core.wait(0.05)
    if 'escape' in block_keys:
        stop_experiment()

    
    # Trials
    trial_list = ['left'] * int(num_trials / 2) + ['right'] * int(num_trials / 2)
    random.shuffle(trial_list)
    
    for trials in range(num_trials):
        staircase = trial_list[trials]

        if staircase == 'left':
            offset = -vernier_offset
            direction = 'left'
        else:
            offset = vernier_offset
            direction = 'right'
            
        if current_crowdCount > 0:
            trial_spacing = current_spacing + random.uniform(-spacing_jitter, spacing_jitter)
        else:
            trial_spacing = 0

        trial_successful = False  
        while not trial_successful:

            # Amblyopic eye display
            vernier1_amb = visual.Line(
                win=win,
                lineColor=amblyopic_eye_color,
                lineWidth=lineThickness,
                start=(current_eccentricity + offset, lineHeight),
                end=(current_eccentricity + offset, 0)
            )
    
            vernier2_amb = visual.Line(
                win=win,
                lineColor=amblyopic_eye_color,
                lineWidth=lineThickness,
                start=(current_eccentricity, 0),
                end=(current_eccentricity, -lineHeight)
            )

            vertical_cross_amb = visual.Line(
                win=win,
                lineColor=amblyopic_eye_color,
                lineWidth=cross_width,
                opacity=0.7,
                start=(0, -cross_size),
                end=(0, cross_size)
            )

            horizontal_cross_amb = visual.Line(
                win=win,
                lineColor=amblyopic_eye_color,
                lineWidth=cross_width,
                opacity=0.7,
                start=(-cross_size, 0),
                end=(cross_size, 0)
            )

            # Crowding
            flankers_amb = []        
            for i in range(-current_crowdCount, current_crowdCount + 1):
                if i == 0:
                    continue
        
                x_pos = current_eccentricity + (i * trial_spacing)
        
                flanker_amb = visual.Line(
                    win=win,
                    lineColor=amblyopic_eye_color,
                    lineWidth=lineThickness,
                    start=(x_pos, -lineHeight),
                    end=(x_pos, lineHeight)
                )
        
                flankers_amb.append(flanker_amb)

            vernier1_amb.draw()
            vernier2_amb.draw()
            for flanker in flankers_amb:
                flanker.draw()

            win.flip()
            core.wait(stim_time) 


            # Decision
            vertical_cross_amb.draw()
            horizontal_cross_amb.draw()
            square_amb.draw()
            win.flip()
            core.wait(0.05)

            event.clearEvents()
            rt_clock.reset()

            keys = []
            while not keys:
                keys = event.getKeys(keyList=['right', 'left', 'escape'])
                core.wait(0.01)
            response_time = rt_clock.getTime()
            
            if 'escape' in keys:
                stop_experiment()

            key_pressed = keys[0]
            if key_pressed == direction:
                statement = 'correct'
                correct_response = True
                circle_amb.draw()

                streak += 1
                if streak == 2:
                    vernier_offset -= step_size  
                    streak = 0
                    if vernier_offset < 0:
                        vernier_offset = 0 
            
            else:
                statement = 'false'
                correct_response = False
                vernier_offset += step_size  
                square_amb.draw()

                streak = 0
                if vernier_offset > max_value:
                    vernier_offset = max_value
            
            win.flip()
            core.wait(0.5)

            writer.writerow([block_label, trials, offset, trial_spacing, key_pressed, direction, response_time, statement, correct_response])
            trial_successful = True

last_page = visual.TextStim(win, text='Thank you, press escape to exit', color='black')
last_page.draw()
win.flip()

event.clearEvents()
last_keys = []
while not last_keys:
    last_keys = event.getKeys(keyList=['escape'])
    core.wait(0.05)

stop_experiment()