import re

filenames = ['M001_S02_audio_M_C', 'M001_S05_audio_M_C', 'M001_S09_audio_M_C', 
             'M001_S10_audio_M_C', 'M001_S11_audio_M_C', 'M002_S07_audio_M_C',
             'M002_S08_audio_M_C', 'M003_S13_audio_M_C', 'M003_S17_audio_M_C',
             'M003_S18_audio_M_C', 'M003_S20_audio_M_C', 'M003_S21_audio_M_C',
             'M003_S22_audio_M_C', 'M003_S23_audio_M_C']

file_in = list()
new_word=""

for filename in filenames:
    print(filename)
    with open(filename+'.txt', "r") as file:
        words = file.readline().split()
        for word in words:
            word=re.sub('[ ,.?!+]',"", word.upper())
            if new_word=="":
                new_word=word
            elif word == 'HMM'or word == 'MHMM' or word == 'HM' or word=='UHUH' or word=='CU' or word=='SH' or word=='AHM' or word=='UMHM' or word=='EHM':
                new_word=new_word
            elif word=="IT'S":
                word="ITS"
                new_word=new_word+" " +word
            elif word=="THAT'S":
                word="THATS"
                new_word=new_word+" " +word
            elif word=="DOCTOR'S":
                word="DOCTORS'"
                new_word=new_word+" " +word
            elif word=="PATIENT'S":
                word="PATIENTS'"
                new_word=new_word+" " +word
            elif word=="LET'S":
                word="LETS"
                new_word=new_word+" " +word
            elif word=="WHAT'S":
                word="WHATS"
                new_word=new_word+" " +word
            elif word=="WAHT":
                word="WHAT"
                new_word=new_word+" " +word
            elif word=="ITA":
                word="ITS"
                new_word=new_word+" " +word
            elif word=="AHM":
                word="A"
                new_word=new_word+" " +word
            else:
                new_word=new_word+" " +word
    
    with open(filename+'.lab', "w") as write_file:
        write_file.write(new_word)
