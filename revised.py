"""
Created on Wed May 20 12:35:57 2020
@author: Kowe
"""
#importing appropriate libraries
import speech_recognition as sr
import pandas as pd
import nltk
from math import *
from bokeh import *

def getData():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
       print("Please wait. Calibrating microphone...")  
       # listen for 5 seconds and create the ambient noise energy level  
       r.adjust_for_ambient_noise(source, duration=5)  
       print("Say something!")
       audio = r.listen(source)
       
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said: " + r.recognize_google(audio) + '\n')
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    tuples = nltk.pos_tag(nltk.word_tokenize(r.recognize_google(audio)))
    sentence = r.recognize_google(audio)
    return tuples, sentence
 
def organizeData(tuples):
    #dictionary with the pos
    posDict = { 'CC': 0,'CD': 0,'DT': 0,'EX': 0, 'FW': 0,    
                'IN': 0,'JJ': 0,'JJR': 0,    'JJS': 0,    'LS': 0,    
                'MD': 0,'NN': 0,'NNS': 0,    'NNP': 0,    'NNPS': 0,    
                'PDT': 0,'POS': 0,'PRP': 0,'PRP$': 0,'RB': 0,    
                'RBR': 0,'RBS': 0,'RP': 0,'TO': 0,'UH': 0,    
                'VB': 0,'VBD': 0,'VBG': 0,'VBN': 0,'VBP': 0,    
                'VBZ': 0,    'WDT': 0,    'WP': 0, 'WP$': 0,'WRB': 0,    
                }
    #adding entries to the dictionary  
    for groups in tuples: 
        for words in groups:
            if words in posDict:
                posDict[words]+=1
                
    #removing empty entries
    for words in list(posDict):
        if posDict[words] == 0:
            posDict.pop(words)
     
    data = pd.Series(posDict).reset_index(name='value').rename(columns={'index':'part of speech'})
    return data

def createGraph(data,sentence):
    #graphing the results
    output_file("results.html")
    
    #Creating the colors for the pie chart
    total = len(data['value'])
    divisor = int(245/total)
    options = Viridis256[0:245:divisor] #gives colors to correspond with data
    if 245%divisor != 0: #if there is an additional item, removes it from the color options
        options.pop()
    
    #Determinging the angle of each slice and the color of each slice
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = options
    
    #Determining the percentage of each slice
    percent = data['value']/data['value'].sum()*100
    percent = percent.astype(int)
    data['percent'] = percent
    
    #Creating the figure
    name= "Sentence: "+sentence
    p = figure(plot_height=350, title=name, toolbar_location=None,
           tools="hover", tooltips="@percent%, Total words:@value", x_range=(-0.5, 1.0))
   
    #Creating the wedge
    p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white",fill_color = 'color',legend='part of speech', source=data)
    
    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    
    show(p)

#Main program
pos,sent = getData()
array = organizeData(pos)   
createGraph(array,sent)

