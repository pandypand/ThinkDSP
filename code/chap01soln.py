#!/usr/bin/env python
# coding: utf-8

# ## ThinkDSP
# 
# This notebook contains solutions to exercises in Chapter 1: Sounds and Signals
# 
# Copyright 2015 Allen Downey
# 
# License: [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/)

# In[2]:


from __future__ import print_function, division

get_ipython().run_line_magic('matplotlib', 'inline')

import thinkdsp
import thinkplot

import warnings
warnings.filterwarnings('ignore')

from IPython.html.widgets import interact, fixed
from IPython.display import display


# ### Exercise
# 
# Go to http://freesound.org and download a sound sample that
# includes music, speech, or other sounds that have a well-defined pitch.
# Select a roughly half-second segment where the pitch is
# constant.  Compute and plot the spectrum of the segment you selected.
# What connection can you make between the timbre of the sound and the
# harmonic structure you see in the spectrum?
# 
# Use `high_pass`, `low_pass`, and `band_stop` to
# filter out some of the harmonics.  Then convert the spectrum back
# to a wave and listen to it.  How does the sound relate to the
# changes you made in the spectrum?

# ### Solution
# 
# I chose this recording (or synthesis?) of a trumpet section http://www.freesound.org/people/Dublie/sounds/170255/
# 
# As always, thanks to the people who contributed these recordings!

# In[3]:


wave = thinkdsp.read_wave('170255__dublie__trumpet.wav')
wave.normalize()
wave.make_audio()


# Here's what the whole wave looks like:

# In[4]:


wave.plot()


# By trial and error, I selected a segment with a constant pitch (although I believe it is a chord played by at least two horns).

# In[5]:


segment = wave.segment(start=1.1, duration=0.3)
segment.make_audio()


# Here's what the segment looks like:
# 

# In[6]:


segment.plot()


# And here's an even shorter segment so you can see the waveform:

# In[7]:


segment.segment(start=1.1, duration=0.005).plot()


# Here's what the spectrum looks like:

# In[8]:


spectrum = segment.make_spectrum()
spectrum.plot(high=7000)


# It has lots of frequency components.  Let's zoom in on the fundamental and dominant frequencies:

# In[9]:


spectrum = segment.make_spectrum()
spectrum.plot(high=1000)


# `peaks` prints the highest points in the spectrum and their frequencies, in descending order:

# In[10]:


spectrum.peaks()[:30]


# The dominant peak is at 870 Hz.  It's not easy to dig out the fundamental, but with peaks at 507, 347, and 253 Hz, we can infer a fundamental at roughly 85 Hz, with harmonics at 170, 255, 340, 425, and 510 Hz.
# 
# 85 Hz is close to F2 at 87 Hz.  The pitch we perceive is usually the fundamental, even when it is not dominant.  When you listen to this segment, what pitch(es) do you perceive?
# 
# Next we can filter out the high frequencies:

# In[11]:


spectrum.low_pass(2000)


# And here's what it sounds like:

# In[12]:


spectrum.make_wave().make_audio()


# The following interaction allows you to select a segment and apply different filters.  If you set the cutoff to 3400 Hz, you can simulate what the sample would sound like over an old (not digital) phone line.

# In[13]:


def filter_wave(wave, start, duration, cutoff):
    """Selects a segment from the wave and filters it.
    
    Plots the spectrum and displays an Audio widget.
    
    wave: Wave object
    start: time in s
    duration: time in s
    cutoff: frequency in Hz
    """
    segment = wave.segment(start, duration)
    spectrum = segment.make_spectrum()

    spectrum.plot(high=5000, color='0.7')
    spectrum.low_pass(cutoff)
    spectrum.plot(high=5000, color='#045a8d')
    thinkplot.config(xlabel='Frequency (Hz)')
    
    audio = spectrum.make_wave().make_audio()
    display(audio)


# In[14]:


interact(filter_wave, wave=fixed(wave), 
         start=(0, 5, 0.1), duration=(0, 5, 0.1), cutoff=(0, 5000, 100));


# ### Exercise
# 
# Synthesize a compound signal by creating SinSignal and CosSignal
# objects and adding them up.  Evaluate the signal to get a Wave,
# and listen to it.  Compute its Spectrum and plot it.
# What happens if you add frequency
# components that are not multiples of the fundamental?

# ### Solution
# 
# Here are some arbitrary components I chose.  It makes an interesting waveform!

# In[15]:


signal = (thinkdsp.SinSignal(freq=400, amp=1.0) +
          thinkdsp.SinSignal(freq=600, amp=0.5) +
          thinkdsp.SinSignal(freq=800, amp=0.25))
signal.plot()


# We can use the signal to make a wave:

# In[16]:


wave2 = signal.make_wave(duration=1)
wave2.apodize()


# And here's what it sounds like:

# In[17]:


wave2.make_audio()


# The components are all multiples of 200 Hz, so they make a coherent sounding tone.
# 
# Here's what the spectrum looks like:

# In[18]:


spectrum = wave2.make_spectrum()
spectrum.plot(high=2000)


# If we add a component that is not a multiple of 200 Hz, we hear it as a distinct pitch.

# In[19]:


signal += thinkdsp.SinSignal(freq=450)
signal.make_wave().make_audio()


# ### Exercise
# 
# Write a function called `stretch` that takes a Wave and a stretch factor and speeds up or slows down the wave by modifying `ts` and `framerate`.  Hint: it should only take two lines of code.

# ### Solution
# 
# I'll use the trumpet example again:

# In[20]:


wave3 = thinkdsp.read_wave('170255__dublie__trumpet.wav')
wave3.normalize()
wave3.make_audio()


# Here's my implementation of `stretch`

# In[21]:


def stretch(wave, factor):
    wave.ts *= factor
    wave.framerate /= factor


# And here's what it sounds like if we speed it up by a factor of 2.

# In[22]:


stretch(wave3, 0.5)
wave3.make_audio()


# Here's what it looks like (to confirm that the `ts` got updated correctly).

# In[23]:


wave3.plot()


# I think it sounds better speeded up.  In fact, I wonder if we are playing the original at the right speed.

# In[ ]:




