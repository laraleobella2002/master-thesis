from psychopy import visual, event, core, monitors
import random
import csv

crowdCount = 4
spacing = 0.35
start_value_right= .2
start_value_left= -.2
step_size = .05
min_value= 0.03
num_trials = 20
lineHight= 1.5
lineThickness = 1
eccentricity1 = 10
eccentricity2 = -10


fileName = 'data.csv'
data_file = open(fileName, 'w', newline='')
writer = csv.writer(data_file)
writer.writerow(['trials', 'offset', 'keys', 'direction', 'response_time', 'statement'])

mon = monitors.Monitor('tempMonitor')
mon.setWidth(53)
mon.setDistance(57.9)
mon.setSizePix([1920, 1080])

win = visual.Window(fullscr=True, color='white', units='deg', monitor=mon)
rt_clock = core.Clock()

for trials in range(num_trials):
    staircase = random.choice(['left', 'right'])
    eccentricity = random.choice([ eccentricity1, eccentricity2])
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
        start=(eccentricity+ (offset/2), lineHight),
        end=(eccentricity+ (offset/2), 0)
        )

    vernier2 = visual.Line(
        win=win,
        lineColor='black',
        lineWidth=lineThickness,
        start=(eccentricity- (offset/2), 0),
        end=(eccentricity- (offset/2), -lineHight)
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
    for i in range(-crowdCount, crowdCount + 1):
        if i == 0:
            continue
        x_pos = eccentricity + (i * spacing)
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
    core.wait(1)
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
    writer.writerow([trials, offset, keys, direction, response_time, statement ])

data_file.close()
win.close()
core.quit()