from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .forms import UserForm
from keras.models import Sequential
import h5py 
import numpy as np
import random
import pandas as pd
import dill
import time

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
def pred_out_to_midi(pred_output, initial_ts, initial_tempo):
    
    #generate new score                  
    midi_stream = stream.Stream()
    rounded_durations = ['0.1', '0.3', '1.25', '2'] 
    
    ts_numerator, ts_denominator = initial_ts.split('/')
    new_ts = meter.TimeSignature(f'{ts_numerator}/{ts_denominator}')
    midi_stream.insert(0, new_ts)
    midi_stream.insert(0, tempo.MetronomeMark(number = initial_tempo))
    
    count=0
    for i in range(0, len(pred_output)):
        #print(pred_output[i])
        j=0
        if pred_output[i] == '<SOC>':
            i = i+1
            new_chord = []
            while((len(pred_output) > i ) and pred_output[i] != '<EOC>' and j<3):
                #print(pred_output[i])
                if (not pred_output[i][0].isdigit()): 
                    new_chord.append(pred_output[i])
                    i= i+1
                    j=j+1
            #out of while loop i.e end of one chord:
            # Parse and add a chord to the stream
           
            #to see if there exists the duration:
            if ((len(pred_output) > i+1 ) and '.' in pred_output[i +1]):
                d = duration.Duration(float(pred_output[i+1]))
                i= i+1
            else:
                d= duration.Duration(float(random.choice(rounded_durations)))
                
            try:
                c = chord.Chord(new_chord)
                c.duration = d
                midi_stream.append(c)
            except:
                print(f'o-o{new_chord}')
        
        
        elif ((len(pred_output) > i ) and pred_output[i] ==  '<EOC>'):
            continue

        elif((len(pred_output)>i ) and '.' not in pred_output[i]):
            # Parse and add a note to the stream
             #to see if there exists the duration:
            try:
                n = note.Note(pred_output[i])
                if( (len(pred_output) > i + 1)):

                    if ('.' in pred_output[i +1]):
                        d = duration.Duration(float(pred_output[i+1]))
                        i= i+1
                    else:
                        d= duration.Duration(float(random.choice(rounded_durations)))
                else:
                        d= duration.Duration(float(random.choice(rounded_durations)))
            except:
                continue
            
            n.duration = d
            midi_stream.append(n)
        
        else : #else it is digit
            print(f"c{count}\t {pred_output[i]}")
            count = count+1
    # Save the stream to a MIDI file
    timestr = time.strftime("%Y%m%d-%H%M%S")
    new_file = 'media/output/output' + '.mid'
    return midi_stream.write('midi', fp=new_file) 
    

# for loadiing models:
from keras import backend as K

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


#############################################################

def index(request):
    return render(request, 'login.html')

def forgot_password(request):
    pass

def register(request):
    form = UserForm()
    context = {} 
    if request.method == "POST":
        username = request.POST['username']
        #request.session['username'] = username
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            print("yess")
            return render(request, 'login.html', context)
    
    context = {'form':form}

    return render(request, 'register.html', context)



def login(request):

    if request.method == "POST":
        Username = request.POST['username']
        Password=request.POST['password']
        user_detail = User.objects.all()

        print(user_detail[0].username)
        for user in user_detail:
            
            if user.username == Username and user.password == Password:
                #set session:
                request.session['username'] = user.username
                return render(request, 'main-v2.html')
            
    context = {}
    return render(request, 'login.html', context)


def generate_random(request):
    if request.method == 'POST' :
        selected_mode = request.POST['modes']
        selected_key_note = request.POST['notes']
    
    combo_file_name =''
    my_custom_objects = {"f1_m": f1_m, "precision_m":precision_m, "recall_m":recall_m}
    if (selected_mode == 'Aeolian'):
        model = load_model('media/models/Aeolian_best_model_small_LSTM_2.h5' , custom_objects = my_custom_objects)
        combo_file_name = 'COMBO_Aeolian' 
    elif(selected_mode == 'Dorian'):
        model = load_model('media/models/Dorian_best_model_small_LSTM.h5', custom_objects = my_custom_objects)
        combo_file_name = 'COMBO_Dorian'
    elif(selected_mode == 'Harmonic-Minor'):
        model = load_model('media/models/Harmonic_minor_best_model_small_LSTM.h5', custom_objects = my_custom_objects)
        combo_file_name = 'COMBO_Harmonic_minor'
    elif(selected_mode == 'Ionian'):
        model = load_model('media/models/Ionian_best_model_small_LSTM.h5', custom_objects = my_custom_objects)
        combo_file_name = 'COMBO_Ionian'
    elif(selected_mode == 'Lydian'):
        model = load_model('media/models/lydian_best_model_small_LSTM.h5', custom_objects = my_custom_objects)
        combo_file_name = 'COMBO_Lydian'
    elif(selected_mode == 'Melodic-Minor'):
        model = load_model('media/models/Melodic_minor_ascend_best_model_small_LSTM.h5', custom_objects = my_custom_objects)
        combo_file_name = 'COMBO_Melodic_minor_ascend'
    elif(selected_mode == 'Mixolydian'):
        model = load_model('media/models/Mixolydian_best_model_small_LSTM.h5', custom_objects = my_custom_objects)
        combo_file_name = 'COMBO_Mixolydian'
    elif(selected_mode == 'Phrygian'):
        model = load_model('media/tester/Phrygian_MODEL.h5', custom_objects = my_custom_objects)
        combo_file_name = 'COMBO_Phrygian'
        

    with open('media/tester/Phrygian.dill', 'rb') as f:
        args = dill.load(f)
 
    x_train = args["x_train"]
    x_val = args["x_val"]
    y_train = args["y_train"]
    y_val = args["y_val"]

    mapping_dict = {}
    all_note_list0 = ["C","C#","D","D#","E","F","F#", "G","G#", "A","A#", "B" ]
    all_note_list1 = ["C","D-","D","E-","E","F","G-", "G","A-", "A","B-", "B" ]

    assigning_index = 1
    for each_octave in range(0 , 9): 
        for each_note in range (0, len(all_note_list0)):
            #print(each_note)
            
            temp_dict0 = { all_note_list0[each_note] + str(each_octave) : assigning_index }
            temp_dict1 = { all_note_list1[each_note] + str(each_octave) : assigning_index }
            mapping_dict.update(temp_dict0)
            mapping_dict.update(temp_dict1)
            assigning_index += 1

    mapping_dict.update({"<SOC>"  : assigning_index})
    mapping_dict.update({"<EOC>"  : assigning_index + 1})
    mapping_dict.update({'0': assigning_index + 2})
    mapping_dict.update({'0.1': assigning_index + 3})
    mapping_dict.update({'0.3': assigning_index + 4})
    mapping_dict.update({'1.25': assigning_index + 5})
    mapping_dict.update({'2': assigning_index + 6})

    
    ## FOR MAKING PREDICTIONS:
    ind = np.random.randint(0,len(x_val)-1)
    random_music = x_train[ind]
    no_of_timesteps = 60
    predictions=[]
    for i in range(200):
        random_music = random_music.reshape(1,no_of_timesteps)
        #print("random music = ", random_music)
        prob  = model.predict(random_music)[0]
        y_pred= np.argmax(prob,axis=0)
        predictions.append(y_pred)
        random_music = np.insert(random_music[0],len(random_music[0]),y_pred)
        random_music = random_music[1:]
    
    print(predictions)
    unique_x_int_to_CD = dict((num, note) for note, num in mapping_dict.items())
    predicted_CD = [unique_x_int_to_CD[i] for i in predictions]
    print(predicted_CD)

    predicted_CD = [unique_x_int_to_CD[i] for i in predictions]
    p =pred_out_to_midi(predicted_CD, '3/8', 90)

    
    #### FINAL END OF FUNCTION:
    return render(request, 'index-v2.html')


@csrf_exempt

def generate_music(request):
    

    if request.method == 'POST':

        modes = request.POST['modes']
        input_sequence = request.POST['input_sequence']
        print("Input sequence = " + input_sequence + "\n")
        str00 =' '.join(input_sequence.split())
        print("Input sequence = " + str00 + "\n")
        str = str00.replace("[ ", "").replace("]", "").replace("\n", "").replace(",","").replace("[", "").replace(" ]", "")
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


