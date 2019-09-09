#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import pyaudio
import matplotlib.pyplot as plt


# In[2]:


def frequency(steps):
    #where steps 
    #-57 is C0, -48 is A0, 50 is B8
    #positive is number of half steps up from A4
    #negative is number of halfsteps down from A4
    #12 halfsteps are an octave
    f = np.power(2, steps/12)*440 
    # 440hz A4
    # see https://en.wikipedia.org/wiki/Music_and_mathematics
    return f

def amplitude(frequency, x, fs = 44100):
    #fs is the sample rate
    
    amplitude = np.sin(2*np.pi*frequency * (x/fs))
    return amplitude

def chordSignal(stepsFromA4toTonic, chordType, amplitudeScalar = 0.25, fs = 44100):
    #fs is the sample rate
    
    # the frequency of the signal 
    tonic = frequency(stepsFromA4toTonic) 
    majThird = frequency(stepsFromA4toTonic+4-chordType)
    fifth = frequency(stepsFromA4toTonic+7)  
    majSeven = frequency(stepsFromA4toTonic+11-chordType) 
    majNine = frequency(stepsFromA4toTonic+14) 

        
    # the points on the x axis for the signal
    x = np.arange(fs) 
    
    #making attack and decay
    section1 = np.arange(fs*.1)
    section2 = np.arange(fs*.4)
    section3 = np.arange(fs*.5)

    amplitude1 = (1/len(section1))*section1
    amplitude2 = (section2*0)+1
    amplitude3 = (-(1/len(section3)*section3))+1
    amplitudeAttackDecay= np.append(amplitude1, amplitude2)
    amplitudeAttackDecay= np.append(amplitudeAttackDecay,amplitude3)
    
    #amplitudeAttack = (1/4410)*attack
    #amplitudeDecay = (-(1/39690)*decay) +1
    #amplitudeAttackDecay  = np.append(amplitudeAttack,amplitudeDecay)
    
    # compute the value (amplitude) of the sin wave at the for each sample
    note1 = amplitude(tonic, x)
    note2 = amplitude(majThird, x)
    note3 = amplitude(fifth, x)
    note4 = amplitude(majSeven, x) 
    note5 = amplitude(majNine, x) 

    signal = (note1+note2+note3+note4+note5)*amplitudeScalar*amplitudeAttackDecay 

    return signal

def chordWithHarmonic(chordType, rootNote=-9, rate=44100):
    signal = chordSignal(rootNote, chordType, fs = rate)+ chordSignal(rootNote+12, chordType, amplitudeScalar= 0.10, fs = rate)
    return signal


# In[3]:


def playChordAudio(rootNote, chordType):
    rate =44100
    data = chordWithHarmonic(chordType, rootNote=rootNote, rate=rate)

    ''' Send audio array to pyaudio for playback
    '''

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=1)
    stream.write(data.astype(np.float32).tostring())
    stream.close()
    p.terminate()


# In[4]:


def playChordProgression(progressionHalfSteps,majorMinor):
    
    for counter,rootNote in enumerate(progressionHalfSteps):
        chordType = majorMinor[counter]
        playChordAudio(rootNote,chordType)


# In[6]:


#progressionHalfSteps = np.array([-8., -5., -9., -9.])
#majorMinor = np.array([1., 0., 0., 0.])
#playChordProgression(progressionHalfSteps, majorMinor)


# In[ ]:




