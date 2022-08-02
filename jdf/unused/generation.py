import random

for x in range(32) :
    s = random.randint(0,60)
    if(x<10):
        strx = '0'+str(x)
        
    else:
        strx = str(x)
    
    if(s<10):
        strs = '0'+str(s)
    else:
        strs = str(s)
    co2 = str(random.randint(400,500))
    voc = str(random.randint(0,200))
    spm1 = str(random.randint(0,3))
    spm25 = str(random.randint(0,2))
    spm10 = str(random.randint(0,1))
    aec1 =str(random.randint(0,2))
    aec25 = str(random.randint(0,3))
    aec10 = str(random.randint(0,1))
    print("Time: 2022-07-" + strx + " 12:50:"+ strs + " VOC: "+ voc + " CO2: " + co2 +" SPM1.0: "+ spm1 +" SPM2.5: "+spm25+ " SPM10: "+spm10+" AEC1: "+aec1+" AEC2.5: "+aec25+" AEC1.0: "+aec10+"")
