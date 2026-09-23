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
    {'label':'Block 1: Binocular_Standard', 'spacing': 0, 'crowdCount': 0, 'eccentricity': 0},
    {'label':'Block 2: Binocular_Crowded', 'spacing': spacing , 'crowdCount': 1, 'eccentricity': 0},
    {'label':'Block 3: Binocular_Standard', 'spacing': 0, 'crowdCount': 0, 'eccentricity': 0},
    {'label':'Block 4: Binocular_Crowded', 'spacing': spacing , 'crowdCount': 1, 'eccentricity': 0},
]

expInfo = {'participantID': '', 'session': '', 'amblyopic_eye':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title='Vernier Experiment')
participant_name = expInfo['participantID']
session_num = expInfo['session']
amblyopic_eye = expInfo['amblyopic_eye']
start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

fileName = f'amblyopia_data_{participant_name}_binocular.csv'
data_file = open(fileName, 'w', newline='')
writer = csv.writer(data_file)
writer.writerow(['label', 'trials', 'offset', 'trial_spacing', 'keys', 'direction', 'response_time', 'accuracy','response_numeric'])

fileName2 = f'amblyopia_data_{participant_name}_binocular_parameters.csv'
data_file2 = open(fileName2, 'w', newline='')
writer_para= csv.writer(data_file2)
writer_para.writerow(['participant_name', 'session_num', 'amblyopic_eye', 'contrast', 'screen_width', 'screen_height', 'step_size', 'max_value', 'num_trials', 'lineHight', 'lineThickness', 'stim_time', 'spacing', 'start_time', 'end_time'])

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
    writer_para.writerow([participant_name, session_num, amblyopic_eye, contrast, SCREEN_WIDTH, SCREEN_HEIGHT, step_size, max_value, num_trials, lineHeight, lineThickness, stim_time, spacing, start_time, end_time])
    data_file.close()
    data_file2.close()
    win.close()
    core.quit()


# # Color calibration
# def calibrate_single_color(color_name, initial_color):

#     color = list(initial_color)
#     mouse = event.Mouse(win=win)
#     patch = visual.Rect(
#         win=win,
#         width=8,
#         height=8,
#         fillColor=color,
#         lineColor=color,
#         pos=(0, 0)
#     )

#     instructions = visual.TextStim(
#         win=win,
#         text=(
#             f"{color_name} CALIBRATION\n\n"
#             f"Look through the {color_name} filter.\n\n"
#             f"The {color_name} stimulus should be just not visible.\n\n"
#             "Press SPACE when finished."
#         ),
#         color='black',
#         height=0.7,
#         wrapWidth=35,
#         pos=(0, 13),
#         alignText='left'
#     )

#     slider_x_min = -8
#     slider_x_max = 8
#     slider_width = slider_x_max - slider_x_min
#     slider_y = [-7, -5.5, -7]
#     slider_names = ['R', 'G', 'B']

#     slider_backgrounds = []
#     slider_handles = []
#     slider_labels = []
#     value_texts = []

#     for i in range(3):

#         background = visual.Rect(
#             win=win,
#             width=slider_width,
#             height=0.35,
#             pos=(0, slider_y[i]),
#             fillColor='lightgray',
#             lineColor='black'
#         )

#         handle = visual.Rect(
#             win=win,
#             width=0.45,
#             height=0.8,
#             pos=(0, slider_y[i]),
#             fillColor='black',
#             lineColor='black'
#         )

#         label = visual.TextStim(
#             win=win,
#             text=slider_names[i],
#             color='black',
#             height=0.45,
#             pos=(-9.5, slider_y[i])
#         )

#         # Numeric value
#         value_display = visual.TextStim(
#             win=win,
#             text=f"{color[i]:.2f}",
#             color='black',
#             height=0.4,
#             pos=(9.5, slider_y[i])
#         )

#         slider_backgrounds.append(background)
#         slider_handles.append(handle)
#         slider_labels.append(label)
#         value_texts.append(value_display)

#     finish_button = visual.Rect(
#         win=win,
#         width=5,
#         height=1.2,
#         pos=(0, -10),
#         fillColor='lightgray',
#         lineColor='black'
#     )

#     finish_text = visual.TextStim(
#         win=win,
#         text="FINISHED",
#         color='black',
#         height=0.45,
#         pos=(0, -10)
#     )

#     dragging = None

#     while True:

#         mouse_x, mouse_y = mouse.getPos()

#         if mouse.getPressed()[0]:
#             if dragging is None:

#                 for i in range(3):
#                     if (slider_y[i] - 0.6 <= mouse_y <= slider_y[i] + 0.6 and slider_x_min <= mouse_x <= slider_x_max):
#                         dragging = i

#                 if (-4.5 <= mouse_x <= 4.5 and -11.6 <= mouse_y <= -10.4):
#                     break

#             if dragging is not None:
#                 x = max(slider_x_min, min(slider_x_max, mouse_x))
#                 value = ((x - slider_x_min)/slider_width) * 2 - 1
#                 color[dragging] = value
#         else:
#             dragging = None

#         patch.fillColor = color
#         patch.lineColor = color

#         for i in range(3):
#             handle_x = slider_x_min + ((color[i] + 1) / 2) * slider_width
#             slider_handles[i].pos = handle_x, slider_y[i]
#             value_texts[i].text = f"{color[i]:.2f}"

#         instructions.draw()
#         patch.draw()

#         for i in range(3):
#             slider_backgrounds[i].draw()
#             slider_handles[i].draw()
#             slider_labels[i].draw()
#             value_texts[i].draw()

#         finish_button.draw()
#         finish_text.draw()

#         win.flip()

#     return color

# step = 0.01

# instruction = visual.TextStim(
#     win=win,
#     text=(
#         "COLOR CALIBRATION\n\n"
#         "Put on the glasses.\n\n"
#         "The goal is to make the red and blue stimuli equally visible.\n\n"
#         "Use the arrows to adjust intensity.\n\n"
#         "Press SPACE to continue."
#     ),
#     color='black',
#     height=0.8,
#     wrapWidth=35,
#     alignText='left'
# )
# instruction.draw()
# win.flip()

# keys = event.waitKeys(keyList=['space', 'escape'])
# if 'escape' in keys:
#     win.close()
#     core.quit()

# win.mouseVisible = True
# red_color = calibrate_single_color(color_name='RED', initial_color=[1.0, -1.0, -1.0])
# blue_color = calibrate_single_color(color_name='BLUE', initial_color=[-1.0, -1.0, 1.0])

# instruction = visual.TextStim(
#     win=win,
#     text=(
#         "You should now see the two colors look equally strong.\n\n"
#         "Press SPACE to continue.\n\n"
#     ),
#     color='black',
#     height=0.7,
#     wrapWidth=35,
#     pos=(0, 6)
# )

# red_patch = visual.Rect(
#     win=win,
#     width=5,
#     height=5,
#     fillColor=red_color,
#     lineColor=red_color,
#     pos=(-6, -2)
# )

# blue_patch = visual.Rect(
#     win=win,
#     width=5,
#     height=5,
#     fillColor=blue_color,
#     lineColor=blue_color,
#     pos=(6, -2)
# )

# instruction.draw()
# red_patch.draw()
# blue_patch.draw()
# win.flip()

# keys = event.waitKeys(keyList=['space', 'escape'])
# if 'escape' in keys:
#     win.close()
#     core.quit()


# Stimuli
lineHeight = 1.5
lineThickness = 2

cross_size = 0.3
cross_width = 4

red_color = [1, -1, -1]
blue_color = [-1, 1, 1]

if amblyopic_eye == 'left' or amblyopic_eye == 'l':
    amblyopic_eye_color = red_color
    healthy_eye_color = blue_color
elif amblyopic_eye == 'right' or amblyopic_eye == 'r':
    amblyopic_eye_color = blue_color
    healthy_eye_color = red_color

circle = visual.Circle(
    win=win,
    radius=cross_size,
    lineColor='black',
    fillColor=None,
    lineWidth=cross_width
)

square = visual.Rect(
    win=win,
    width=cross_size * 2,
    height=cross_size * 2,
    lineColor='black',
    fillColor=None,
    lineWidth=cross_width
)


# Interocular contrast matching
matched_contrast = 0.2
contrast_step = 0.02
min_contrast = 0.01
max_contrast = 1.00

instruction = visual.TextStim(
    win,
    text=(
        'Contrast matching\n\n'
        'Adjust the contrast until both cubes appear with the same intensity.\n\n'
        'RIGHT arrow: increase contrast\n'
        'LEFT arrow: decrease contrast\n\n'
        'Press SPACE when they look matched.'
    ),
    color='black',
    height=1.5,
    wrapWidth=45,
    alignText='left'
)
instruction.draw()
win.flip()

event.clearEvents()
instruction_keys = []
while not instruction_keys:
    instruction_keys = event.getKeys(keyList=['space', 'escape'])
    core.wait(0.05)
if 'escape' in instruction_keys:
    stop_experiment()

left_cube_pos = (-5, 0)
right_cube_pos = (5, 0)
cube_size = 3

healthy_cube_color = visual.Rect(
    win=win,
    width=cube_size,
    height=cube_size,
    fillColor=healthy_eye_color,
    opacity=matched_contrast,
    pos=left_cube_pos
)

amblyopic_cube_color = visual.Rect(
    win=win,
    width=cube_size,
    height=cube_size,
    fillColor=amblyopic_eye_color,
    opacity=1.0,
    pos=right_cube_pos
)

matching_done = False
while not matching_done:

    healthy_cube_color.opacity = matched_contrast
    healthy_cube_color.draw()
    amblyopic_cube_color.draw()
    win.flip()

    keys = event.waitKeys(keyList=['left', 'right', 'space', 'escape'])
    if 'escape' in keys:
        stop_experiment()
    key_pressed = keys[0]

    # Decrease contrast
    if key_pressed == 'left':
        matched_contrast -= contrast_step
        if matched_contrast < min_contrast:
            matched_contrast = min_contrast

    # Increase contrast
    elif key_pressed == 'right':
        matched_contrast += contrast_step
        if matched_contrast > max_contrast:
            matched_contrast = max_contrast

    # Accept match
    elif key_pressed == 'space':
        matching_done = True


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
                start=(0, -cross_size),
                end=(0, 0)
            )

            horizontal_cross_amb = visual.Line(
                win=win,
                lineColor=amblyopic_eye_color,
                lineWidth=cross_width,
                start=(0, 0),
                end=(cross_size, 0)
            )


            # Crowding
            flankers_amb = []
            flankers_healthy = []
        
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
        
                flanker_healthy = visual.Line(
                    win=win,
                    lineColor=healthy_eye_color,
                    lineWidth=lineThickness,
                    start=(x_pos, -lineHeight),
                    end=(x_pos, lineHeight)
                )
        
                flankers_amb.append(flanker_amb)
                flankers_healthy.append(flanker_healthy)

            vernier1_amb.draw()
            vernier2_amb.draw()
            for flanker in flankers_amb:
                flanker.draw()


            # Healthy eye display
            vernier1_healthy = visual.Line(
                win=win,
                lineColor=healthy_eye_color,
                lineWidth=lineThickness,
                opacity=matched_contrast,
                start=(current_eccentricity + offset, lineHeight),
                end=(current_eccentricity + offset, 0)
            )

            vernier2_healthy = visual.Line(
                win=win,
                lineColor=healthy_eye_color,
                lineWidth=lineThickness,
                opacity=matched_contrast,
                start=(current_eccentricity, 0),
                end=(current_eccentricity, -lineHeight)
            )
            
            vertical_cross_healthy = visual.Line(
                win=win,
                lineColor=healthy_eye_color,
                lineWidth=cross_width,
                opacity=matched_contrast,
                start=(0, 0),
                end=(0, cross_size)
            )

            horizontal_cross_healthy = visual.Line(
                win=win,
                lineColor=healthy_eye_color,
                lineWidth=cross_width,
                opacity=matched_contrast,
                start=(-cross_size, 0),
                end=(0, 0)
            )

            vernier1_healthy.draw()
            vernier2_healthy.draw()
            for flanker in flankers_healthy:
                flanker.draw()

            win.flip()
            core.wait(stim_time) 


            # Decision
            vertical_cross_amb.draw()
            horizontal_cross_amb.draw()
            vertical_cross_healthy.draw()
            horizontal_cross_healthy.draw()
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
                circle.draw()

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
                square.draw()

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