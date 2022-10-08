# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 04:47:29 2022

@author: bryan
"""

import random
import math
import distances

diffi = "insane"
if diffi == "insane":
    dist = round(random.random()*10+20)*10
if diffi == "hard":
    dist = round(random.random()*10+10)*10
if diffi == "normal":
    dist = round(random.random()*5+10)*10
if diffi == "easy":
    dist = round(random.random()*3+10)*10
bpm = 75
slider_distance = 200
time_difference = 800
slider_velocity = round((bpm * -0.006153846153846 + 2.03076923076923)*10)*10
def generate_pos(x,y,jump, rad, diff, last_note_slider, current_note_slider, consec_same):
    #jump = distances.randn_skew(1, 1.11949787979379)[0]
    jump = distances.randn_skew(1, 0.977931864550102)[0]
    if jump < 0:
        jump = 0
    jump *= diff
    if consec_same < 2 and False:
        if random.random() <= .25:
            return x, y, rad, consec_same+1
        if diff == time_difference:
            if random.random() <= .125:
                return x, y, rad, consec_same+1
        if diff == 2 * time_difference:
            if random.random() <= .0625:
                return x, y, rad, consec_same+1
    else:
        consec_same = 0
    start = True
    cand_x, cand_y = x, y
    attempts = 0
    while cand_x < 0 or cand_y < 0 or cand_x > 500 or cand_y > 375 or start:
        if diff <= time_difference / 4 or last_note_slider or current_note_slider:
            rand = random.random()*math.pi+rad-math.pi/2
        else:
            rand = random.random()*2*math.pi
        cand_x = x+jump*math.cos(rand)
        cand_y = y+jump*math.sin(rand)
        start = False
        attempts += 1
        if attempts >= 100:
            attempts = 0
            no_choice = False
            screwed = False
            while cand_x < 0 or cand_y < 0 or cand_x > 500 or cand_y > 375 or start:
                if diffi == "insane":
                    dist = round(random.random()*10+20)*10
                if diffi == "hard":
                    dist = round(random.random()*10+10)*10
                if diffi == "normal":
                    dist = round(random.random()*5+10)*10
                if diffi == "easy":
                    dist = round(random.random()*3+10)*10
                
                jump = diff/time_difference*dist*100/140 
                #jump = distances.randn_skew(1, 1.11949787979379)[0]
                jump = distances.randn_skew(1, 0.977931864550102)[0]
                jump *= diff
                if jump < 0:
                    jump = 0
                if (4 * diff <= time_difference or last_note_slider or current_note_slider) and not no_choice and not screwed: 
                    rand = random.random()*math.pi+rad-math.pi/2
                elif screwed:
                    rand = random.random()*2*math.pi    
                elif no_choice:
                     rand = random.random()*3/2*math.pi+rad-3*math.pi/4   
                else:
                    rand = random.random()*2*math.pi
                cand_x = x+jump*math.cos(rand)
                cand_y = y+jump*math.sin(rand)
                start = False
                attempts += 1
                if attempts >= 100: 
                    if diff == time_difference:
                        no_choice = True
                    else:
                        return round(random.random()*500), round(random.random()*375), 0, consec_same
                if attempts >= 200:
                    if diff < time_difference:
                        screwed = True
                    else:
                        return round(random.random()*500), round(random.random()*375), 0, consec_same
                if attempts >= 300:    
                    print(diff)
                    return round(random.random()*500), round(random.random()*375), 0, consec_same
    if cand_x == x:
        print(jump, x, y)
    return round(cand_x),round(cand_y), rand, consec_same

def generate_slider(x, y, dist, rad, diff, vel):
    duration = diff/time_difference*slider_distance
    if str(duration)[-2:] == ".0":
        duration = int(str(duration)[:-2])

    travel = duration/vel*dist
    start = True
    cand_x, cand_y = x, y
    attempts = 0
    no_choice = False
    while cand_x < 10 or cand_y < 10 or cand_x > 490 or cand_y > 365 or start:
        if no_choice:
            rand = random.random()*2*math.pi
        elif attempts >= 200:          
            rand = random.random()*3/2*math.pi+rad-3*math.pi/4
        else:
            rand = random.random()*math.pi+rad-math.pi/2          
        cand_x = x+travel*math.cos(rand)
        cand_y = y+travel*math.sin(rand)
        start = False
        attempts += 1
        if attempts >= 100:          
            no_choice = True        
        if attempts >= 300:
            print("oops")
            return round(random.random()*500), round(random.random()*375), 0, duration

    return round(cand_x),round(cand_y), rand, duration 
cleaned = True

with open("notes.txt") as f:
    notes = f.readlines()

times = set()    
if not cleaned:
   i = 0
   while i < len(notes):
        first = notes[i].find(",")+1
        second = notes[i][first:].find(",")       
        pos = notes[i][:first+second]
        comma = pos.find(",")
        pos = pos[:comma], pos[comma+1:]
        time = notes[i][first+second+1:]
        time = time[:time.find(",")]
        
        if time not in times:
            notes[i] = pos[0]+","+pos[1]+","+time+",1,0,0:0:0:0:"
            times.add(time)
            i += 1
        else:
            notes.pop(i)


first = notes[0].find(",")+1
second = notes[0][first:].find(",")

prev_pos = notes[0][:first+second]
comma = prev_pos.find(",")
prev_pos = int(prev_pos[:comma]), int(prev_pos[comma+1:])
prev_time = notes[0][first+second+1:]
prev_time = int(prev_time[:prev_time.find(",")])
first_time = prev_time

rad = 0
circles = 0
sliders = 0
riders = 0
i = 1
consec = 0
csame = 0
last_note_slider = False
current_note_slider = False

while i < len(notes):
    
    rider = False
    
        
    
    
    #coordinates of previous note
    x, y = prev_pos
    
    #determine timing of current note and ending portion
    first_= notes[i].find(",")+1
    second_ = notes[i][first_:].find(",")
    end = notes[i][first_+second_:]
    end_parsed = end.split(",")
    color = int(end_parsed[2])
    if color == 12:
        i += 1
        continue
    time = notes[i][first_+second_+1:]
    time = int(time[:time.find(",")])

 
    diff = time - prev_time 


    #remove quickies on easier maps
    if diffi == "normal":
        if round((diff)/time_difference)*time_difference <= 2*time_difference:
            if random.random() < .5:
                notes.pop(i)
                continue
    if diffi == "easy":
        if round((diff)/time_difference)*time_difference <= 2 * time_difference:
            if random.random() < .85:
                notes.pop(i)
                continue
    
    
    #determine time of next note
    start_again = True
    while start_again:
        flag = True
        if i == len(notes) - 1:
            flag = False
        else:
            _first_= notes[i+1].find(",")+1
            _second_ = notes[i+1][_first_:].find(",")
            _time = notes[i+1][_first_+_second_+1:]
            _time = int(_time[:_time.find(",")])
            _diff = _time - time
            
            flag = _diff <= time_difference and "12" not in notes[i+1].split(",")
        if False:
            if time >= 138750 and _diff >= 600:
                print(_diff)
                if diffi == "insane" and random.random() < 1: 
                    to_add = notes[i].split(",")
                    to_add[2] = str(int(to_add[2])+int(_diff/2))
                    note = ""
                    note += to_add[0]
                    for part in to_add[1:]:
                        note += ","+part
                    notes.insert(i+1, note)
                    #print(notes[i], notes[i+1], notes[i+2])
            elif time >= 138750 and _diff >= 300:
                #print(_diff, i)
                if diffi == "insane" and random.random() < .5: 
                    to_add = notes[i].split(",")
                    to_add[2] = str(int(to_add[2])+int(_diff/2))
                    note = ""
                    note += to_add[0]
                    for part in to_add[1:]:
                        note += ","+part
                    print(len(notes))
                    notes.insert(i+1, note)
                    print(len(notes))
                    #print(notes[i], notes[i+1], notes[i+2])
        else:
            start_again = False

    #determine time of next next note
    _flag = True
    if i >= len(notes) - 2:
        _flag = False
    else:
        __first_= notes[i+2].find(",")+1
        __second_ = notes[i+2][__first_:].find(",")
        __time = notes[i+2][__first_+__second_+1:]
        __time = int(__time[:__time.find(",")])
        __diff = __time - _time
        _flag = _diff == __diff and "12" not in notes[i+2].split(",")
  
    

    
    
    #randomly change color
    changed = False
    if color <= 2 and (diff > time_difference or random.random() < 0.1) and consec >= 2:
        color += 4
        changed = True
        
    #track consecutive number of notes with the same color
    if color <= 2:
        consec += 1
    else:
        consec = 0
    
    #automatically change color if 9 straight and not stream
    if not changed and consec >= 9 and diff > time_difference / 8:
        color += 4
        consec = 0
        
    #randomly change snap    
    if random.random() < 0.1:
        if diffi == "insane":
            dist = round(random.random()*10+20)*10
        if diffi == "hard":
            dist = round(random.random()*10+10)*10
        if diffi == "normal":
            dist = round(random.random()*5+10)*10
        if diffi == "easy":
            dist = round(random.random()*3+10)*10
        
    
        
    #determine if slider
    if False and round(diff/time_difference)*time_difference == time_difference or round(_diff/time_difference)*time_difference == time_difference or round(__diff/time_difference)*time_difference == time_difference:
        mult = .25
    else:
        mult = 1
    if diffi == "easy":
        mult *= 4/3
    if diffi == "normal":
        mult *= 6/5
    if diffi == "insane":
        mult *= 2/3
    if (random.random() < .447 and flag) or _diff <= 100:  
        current_note_slider = True
        #determine new snapped position of current note and its direction

        pos = generate_pos(x, y, diff/time_difference*dist*100/140, rad, diff, last_note_slider, current_note_slider, csame)
        new_pos = pos[0:2]
        csame = pos[3]
        slider = generate_slider(x, y, slider_distance, rad, _diff, slider_velocity)      
        new_end = ","+end_parsed[1]+","+str(color+1)+",0,L|"+str(slider[0])+":"
        notes.pop(i+1)
        if diffi == "normal" or diffi == "easy":
            mult = 1/2
        else:
            mult = 1
        #determine if rider
        if False and random.random() < 1/2 * mult and _flag: 
            rider = True
            rad = slider[2]-math.pi/2
            new_end += str(slider[1])+",2,"+str(slider[3])
            prev_time = __time
            notes.pop(i+1)
            riders += 1
        else: 
            rad = slider[2]
            new_end += str(slider[1])+",1,"+str(slider[3])
            prev_pos = slider[0:2]
            prev_time = _time
            sliders += 1 
            
        notes[i] = str(new_pos[0])+","+str(new_pos[1])+new_end
        last_note_slider = True

    else: 
        #determine new snapped position of current note and its direction
        current_note_slider = False
        pos = generate_pos(x, y, diff/time_difference*dist/100*140 , rad, diff, last_note_slider, current_note_slider, csame)
        new_pos = pos[0:2]
        rad = pos[2]
        csame = pos[3]
        new_end = ","+end_parsed[1]+","+str(color)+",0,0:0:0:0:"        
        notes[i] = str(new_pos[0])+","+str(new_pos[1])+new_end
        prev_pos = new_pos
        prev_time = time
        last_note_slider = False
        circles += 1
     

    #clap sound
    beats_away = round(diff/time_difference*2)/2
    if False and time % 600 == 0 and not current_note_slider:
        to_add = notes[i].split(",")
        if random.random() < .5:
            to_add[4] = "8"
        else:
            to_add[4] = "6"
        note = ""
        note += to_add[0]
        for part in to_add[1:]:
            note += ","+part
        notes[i] = note
        
    #finish
    if i == len(notes) - 1:
        to_add = notes[i].split(",")
        to_add[4] = "6"
        note = ""
        note += to_add[0]
        for part in to_add[1:]:
            note += ","+part
        notes[i] = note
        
        
    #increment counter
    i += 1
"""
first = notes[0].find(",")+1
second = notes[0][first:].find(",")

prev_pos = notes[0][:first+second]
comma = prev_pos.find(",")
prev_pos = int(prev_pos[:comma]), int(prev_pos[comma+1:])
prev_time = notes[0][first+second+1:]
prev_time = int(prev_time[:prev_time.find(",")])
first_time = prev_time
parsed_ends = []
time_diffs = []
dist_diffs = []
velocities = []
reversals = []
for i in range(1, len(notes)):   
    #coordinates of previous note
    x, y = prev_pos
    first = notes[i].find(",")+1
    second = notes[i][first:].find(",")
    pos = notes[i][:first+second]
    comma = pos.find(",")
    pos = int(pos[:comma]), int(pos[comma+1:])
    
    #determine timing of current note and ending portion
    first_= notes[i].find(",")+1
    second_ = notes[i][first_:].find(",")
    end = notes[i][first_+second_:]
    end_parsed = end.split(",")
    
   
    
    parsed_ends.append(end_parsed)
    time = notes[i][first_+second_+1:]
    time = int(time[:time.find(",")])
    time_diff = time-prev_time
    dist_diff = ((prev_pos[0]-pos[0])**2+(prev_pos[0]-pos[0]))**.5
    time_diffs.append(time_diff)
    dist_diffs.append(dist_diff)
    velocities.append(dist_diff/time_diff)
    prev_time = time 
    prev_pos = pos
    if ":" in end_parsed[4] and len(end_parsed) > 5:   
       s = end_parsed[4] 
       last_line = 0
       last_colon = 0
       for j in range(len(s)):
           if s[j] == "|":
               last_line = j
           if s[j] == ":":
               last_colon = j
       if end_parsed[5] == "1":
            prev_pos = (int(end_parsed[4][last_line+1:last_colon]), int(end_parsed[4][last_colon+1:]))
    f = open("vel.txt", "w")

for v in velocities:
    f.write(str(v)+"\n")
f.close

"""
f = open("out.txt", "w")   
for note in notes:
    f.write(note+"\n")
f.close()

