from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from keras.models import Sequential
import h5py 
import numpy as np
import random
import pandas as pd
from music21 import *
from keras.models import load_model
# Create your views here.



from music21 import midi
def play_midi_file(midi_file_name):
    mf = midi.MidiFile()

    mf.open(midi_file_name) # path='abc.midi'
    mf.read()
    mf.close()
    s = midi.translate.midiFileToStream(mf)
    s.show('midi')

# for seeing output from chords and given duration:
def get_music_midi_from_chords_and_duration(input_chords):
    midi_stream = stream.Stream()

    for note_pattern, duration_pattern in input_chords:
        notes_in_chord = note_pattern.split('.')
        
        chord_notes = []
        for current_note in notes_in_chord:
            new_note = note.Note(current_note)
            new_note.duration = duration.Duration(duration_pattern)
            new_note.storedInstrument = instrument.Violoncello()
            chord_notes.append(new_note)
        new_chord = chord.Chord(chord_notes)
        
        midi_stream.append(new_chord)

        new_tempo = tempo.MetronomeMark(number=50)
            
        midi_stream.append(new_tempo)

    midi_stream = midi_stream.chordify()
    rannum= random.randint(0, 350)
    #timestr = time.strftime("%Y%m%d-%H%M%S")
    new_file = 'media/'+ 'output11' + '.mid'
    return midi_stream.write('midi', fp=new_file)


def index(request):
    return render(request, 'main.html')


@csrf_exempt
def generate_music(request):
    

    if request.method == 'POST':

        modes = request.POST['modes']
        input_sequence = request.POST['input_sequence']
        print("Input sequence = " + input_sequence + "\n")
        str = input_sequence.replace("[", "").replace("]", "").replace("\n", "").replace(",","")
        str_list1 = str.split(" ")
        str_list2 = list(map(int, str_list1))
        input_sequence11_arr = np.array(str_list2)
        print("array hai = " , input_sequence11_arr, ' type = ', type(input_sequence11_arr))
        #print("Input sequence = " + input_sequence11 + "\n")
        random_music = input_sequence11_arr


        #loading best model (Previously trained modle)
        if (modes == 'major'):
            model = load_model('media/models/major_best_model.h5')
        else:
            model = load_model('media/models/minor_best_model.h5')

        
        
        
        

        # start = 0
        # end = 35000 - 1 
        # random_music= []
        # for i in range(32):
        #     random_music.append(random.randint(start, end))
        
        # random_music = np.array(random_music)
        
        
        
        # random_music = [42518, 22133, 19038, 22133, 42518, 22133, 18865, 5528, 24591, 2698, 22468, 5528, 24591, 3987, 25997, 5528, 24591, 2698, 22468, 5528, 24591, 2698, 22468, 5528, 24591, 3987, 25997, 5528, 24591, 2698, 22468, 42619]
        
       
        
        #ind = np.random.randint(0,len(x_val)-1)
        #random_music = x_val[ind]
        

        no_of_timesteps =32
        predictions=[]
        for i in range(30):

            random_music = random_music.reshape(1,no_of_timesteps)
            print("random music = ", random_music)
            

            prob  = model.predict(random_music)[0]
            y_pred= np.argmax(prob,axis=0)
            predictions.append(y_pred)

            random_music = np.insert(random_music[0],len(random_music[0]),y_pred)
            random_music = random_music[1:]
            
        print(predictions)


        df =pd.read_csv("media/dataset_processed/initial_dataset_major_songs_295.csv")
        x=df['32_chords_and_duration']
        y=df['target_chords_and_duration']
        x=np.array(x)
        y=np.array(y)

        
        temp_x = []
        

        for i in range(len(x)):
            str = x[i]
            # Remove square brackets and "\n" characters
            str = str.replace("[", "").replace("]", "").replace("\n", "").replace("'","")
            

            # Split the string by space to get a list of strings
            str_list = str.split(" ")
            

            # Convert the list of strings to a numpy array
            result = np.array(str_list)
            temp_x.append(result)
            
            ##############################################################
            # to calculate progress:
            total_length = len(x)
            iterative = i+1
            percent = ((i+1)/len(x)) * 100
            if (percent) % 5 ==0 :
                print( percent,"% done")
            #############################################################
            
            #print(result, "type = ", type(result))
            #np.vstack([temp_x,result])
        
        #convert list to array:
        x = np.array(temp_x)
        unique_x_CD = list(set(x.ravel()))

        unique_y_CD = list(set(y))
         

        #intergers back to notes
        unique_x_int_to_CD = dict((number, note_) for number, note_ in enumerate(unique_y_CD)) 
        predicted_CD = [unique_x_int_to_CD[i] for i in predictions]

        predicted_CD_split = []
        for each_outcome in predicted_CD:
            temp_list = []
            temp_list = each_outcome.split("@")
            temp_list[1] =float(temp_list[1])
            predicted_CD_split.append(tuple(temp_list))
        
        print("Generating music from our processed chords...")
        proccessed_chords_to_midi_sample = get_music_midi_from_chords_and_duration(predicted_CD_split)
        print(proccessed_chords_to_midi_sample)
        #play_midi_file(proccessed_chords_to_midi_sample)
        

    

    return render(request, 'index.html')


