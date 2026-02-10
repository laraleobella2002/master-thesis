from psychopy import visual, event, core, monitors
import random
import csv

crowdCount = 4
spacing = 0.35
offsets = [-0.3, -0.2, -0.1, 0.1, 0.2, 0.3]
num_trials = 10
lineHight= 1.5
lineThickness = 1

fileName = 'data.csv'
data_file = open(fileName, 'w', newline='')
writer = csv.writer(data_file)
writer.writerow(['trials', 'offset', 'keys', 'direction', 'response_time', 'statement'])

mon = monitors.Monitor('tempMonitor')
mon.setWidth(53)
mon.setDistance(57.9)
mon.setSizePix([1920, 1080])

win = visual.Window(size=[900, 900], color='white', units='deg', monitor=mon)
rt_clock = core.Clock()

for trials in range(num_trials):
    offset = random.choice(offsets)
    vernier1 = visual.Line(
        win=win,
        lineColor='black',
        lineWidth=lineThickness,
        start=(offset/2, lineHight),
        end=(offset/2, 0)
        )

    vernier2 = visual.Line(
        win=win,
        lineColor='black',
        lineWidth=lineThickness,
        start=(0, 0),
        end=(0, -lineHight)
        )

    flankers = []
    for i in range(-crowdCount, crowdCount + 1):
        if i == 0:
            continue
        x_pos = i * spacing
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
    win.flip()
    core.wait(0.25)
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
    else:
        statement = 'false'  
    writer.writerow([trials, offset, keys, direction, response_time, statement ])

data_file.close()
win.close()
core.quit()