from psychopy import visual, event, core, monitors, gui
import random
import csv
import os

step_size = 0.05
min_value= 0.02
num_trials = 10
lineHight= 1.5
lineThickness = 2
stim_time= 1

block_conditions = [
    {'label':'Block 1: Binocular_UC', 'spacing': 0, 'crowdCount': 0, 'eccentricity': 8},
    {'label':'Block 2: Binocular_C', 'spacing': 0.5, 'crowdCount': 2, 'eccentricity': -8},
    {'label':'Block 3: Monocular_UC', 'spacing': 0, 'crowdCount': 0, 'eccentricity': 5},
    {'label':'Block 4: Monocular_C', 'spacing': 0.5, 'crowdCount': 2, 'eccentricity': -5},
]

expInfo={ 'participantID': ''} 
dlg = gui.DlgFromDict(dictionary=expInfo, title='Vernier Experiment')
participant_name = expInfo['participantID']


fileName= f'data_{participant_name}.csv'
data_file = open(fileName, 'w', newline='')
writer = csv.writer(data_file)
writer.writerow(['label', 'trials', 'offset', 'keys', 'direction', 'response_time', 'statement'])

mon = monitors.Monitor('tempMonitor')
mon.setWidth(53)
mon.setDistance(57.9)
mon.setSizePix([1920, 1080])

win = visual.Window(fullscr=True, color='white', units='deg', monitor=mon)
rt_clock = core.Clock()

first_page= visual.TextStim(win, text= 'Hello\n 1.Please keep looking at the black cross during the trails\n 2.If the upper line is to the right press →\n 3.If to the left press ← \n Now please press SPACE to start :)', color='black')
first_page.draw()
win.flip()
event.waitKeys(keyList=['space'])

for condition in block_conditions: 
    current_spacing = condition['spacing']
    current_crowdCount = condition['crowdCount']
    current_eccentricity = condition['eccentricity']
    block_label = condition['label'] 
    start_value_right = 0.2
    start_value_left = -0.2
    msg = f"Starting {block_label}\n Press SPACE to continue."
    block_msg = visual.TextStim(win, text=msg, color='black')
    block_msg.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
    for trials in range(num_trials):
        staircase = random.choice(['left', 'right'])
        if staircase == 'left':
            offset = start_value_left
            direction = 'left' 
        else:
            offset = start_value_right
            direction = 'right'
            
        vernier1 = visual.Line(
            win=win,
            lineColor='black',
            lineWidth=lineThickness,
            start=(current_eccentricity+ (offset/2), lineHight),
            end=(current_eccentricity+ (offset/2), 0)
            )

        vernier2 = visual.Line(
            win=win,
            lineColor='black',
            lineWidth=lineThickness,
            start=(current_eccentricity- (offset/2), 0),
            end=(current_eccentricity- (offset/2), -lineHight)
            )
           
        cross1 = visual.Line(
            win=win,
            lineColor='black',
            lineWidth=4,
            start=(0,-0.3),
            end=(0,0.3)
            )
           
        cross2= visual.Line(
            win=win,
            lineColor='black',
            lineWidth=4,
            start=(-0.3, 0),
            end=(0.3,0)
            )

        flankers = []
        for i in range(-current_crowdCount, current_crowdCount + 1):
            if i == 0:
                continue
            x_pos = current_eccentricity + (i * current_spacing)
            if x_pos==offset:  
                continue
               
            if offset<0:
                direction='left'
            else:
                direction='right'

            flanker = visual.Line(
                win=win,
                lineColor='black',
                lineWidth=lineThickness,
                start=(x_pos, -lineHight),
                end=(x_pos, lineHight)
                )
            flankers.append(flanker)


        for flanker in flankers:
            flanker.draw()

        vernier1.draw()
        vernier2.draw()
        cross1.draw()
        cross2.draw()
        win.flip()
        core.wait(stim_time)
        win.flip()
        rt_clock.reset()
        keys = event.waitKeys(keyList=['right', 'left','escape'])
        response_time = rt_clock.getTime()

        if 'escape' in keys:
            win.close()
            core.quit()

        key_pressed = keys[0]
        
        if key_pressed == direction:
            statement = 'correct'
            if staircase == 'left':
                start_value_left += step_size 
                if start_value_left > -min_value: 
                    start_value_left = -min_value
            else:
                start_value_right -= step_size 
                if start_value_right < min_value: 
                    start_value_right = min_value
                
        else:
            statement = 'false'  
            if staircase == 'left':
                start_value_left -= step_size 
            else:
                start_value_right += step_size
        writer.writerow([block_label, trials, offset, keys, direction, response_time, statement ])

last_page= visual.TextStim(win, text= 'Thank you, press escape to exit' , color='black')
last_page.draw()
win.flip()
event.waitKeys(keyList=['escape'])
data_file.close()
win.close()
core.quit()