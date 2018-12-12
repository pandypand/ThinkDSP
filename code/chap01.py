#!/usr/bin/env python
# coding: utf-8

# ## ThinkDSP
# 
# This notebook contains code examples from Chapter 1: Sounds and Signals
# 
# Copyright 2015 Allen Downey
# 
# License: [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/)
# 

# ### Signals
# 
# Here are the modules we'll need.
# 
# * `thinkdsp` is a module that accompanies _Think DSP_ and provides classes and functions for working with signals.
# 
# * `thinkplot` is a wrapper around matplotlib.
# 
# [Documentation of the thinkdsp module is here](http://greenteapress.com/thinkdsp.html). 

# In[1]:


from __future__ import print_function, division

#%matplotlib inline

import thinkdsp
import thinkplot

import numpy as np

from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets
from IPython.display import display


# Instantiate cosine and sine signals.

# In[2]:


cos_sig = thinkdsp.CosSignal(freq=440, amp=1.0, offset=0)
sin_sig = thinkdsp.SinSignal(freq=880, amp=0.5, offset=0)


# Plot the sine and cosine signals.  By default, `plot` plots three periods.  

# In[3]:


cos_sig.plot()
thinkplot.config(xlabel='Time (s)')


# Notice that the frequency of the sine signal is doubled, so the period is halved.

# In[5]:


sin_sig.plot()
thinkplot.config(xlabel='Time (s)')


# The sum of two signals is a SumSignal.

# In[6]:


mix = sin_sig + cos_sig
mix


# Here's the documentation for `thinkdsp.py`: http://greenteapress.com/thinkdsp/thinkdsp.html

# ### Waves
# 
# A Signal represents a mathematical function defined for all values of time.  If you evaluate a signal at a sequence of equally-spaced times, the result is a Wave.  `framerate` is the number of samples per second.

# In[7]:


wave = mix.make_wave(duration=0.5, start=0, framerate=11025)
wave


# IPython provides an Audio widget that can play a wave.

# In[8]:


from IPython.display import Audio
audio = Audio(data=wave.ys, rate=wave.framerate)
audio


# Wave also provides `make_audio()`, which does the same thing:

# In[9]:


wave.make_audio()


# The `ys` attribute is a NumPy array that contains the values from the signal.  The interval between samples is the inverse of the framerate.

# In[10]:


print('Number of samples', len(wave.ys))
print('Timestep in ms', 1 / wave.framerate * 1000)


# Signal objects that represent periodic signals have a `period` attribute.
# 
# Wave provides `segment`, which creates a new wave.  So we can pull out a 3 period segment of this wave.

# In[11]:


period = mix.period
segment = wave.segment(start=0, duration=period*3)
period


# Wave provides `plot`

# In[12]:


segment.plot()
thinkplot.config(xlabel='Time (s)')


# `normalize` scales a wave so the range doesn't exceed -1 to 1.
# 
# `apodize` tapers the beginning and end of the wave so it doesn't click when you play it.

# In[14]:


wave.normalize()
wave.apodize()
wave.plot()
thinkplot.config(xlabel='Time (s)')


# You can write a wave to a WAV file.

# In[15]:


wave.write('temp.wav')


# `wave.write` writes the wave to a file so it can be used by an exernal player.

# In[16]:


thinkdsp.play_wave(filename='temp.wav', player='aplay')


# `read_wave` reads WAV files.  The WAV examples in the book are from freesound.org.  In the contributors section of the book, I list and thank the people who uploaded the sounds I use.

# In[21]:


wave = thinkdsp.read_wave('92002__jcveliz__violin-origional.wav')


# In[22]:


wave.make_audio()


# I pulled out a segment of this recording where the pitch is constant.  When we plot the segment, we can't see the waveform clearly, but we can see the "envelope", which tracks the change in amplitude during the segment.

# In[23]:


start = 1.2
duration = 0.6
segment = wave.segment(start, duration)
segment.plot()
thinkplot.config(xlabel='Time (s)')


# ### Spectrums
# 
# Wave provides `make_spectrum`, which computes the spectrum of the wave.

# In[24]:


spectrum = segment.make_spectrum()


# Spectrum provides `plot`

# In[25]:


spectrum.plot()
thinkplot.config(xlabel='Frequency (Hz)')


# The frequency components above 10 kHz are small.  We can see the lower frequencies more clearly by providing an upper bound:

# In[26]:


spectrum.plot(high=10000)
thinkplot.config(xlabel='Frequency (Hz)')


# Spectrum provides `low_pass`, which applies a low pass filter; that is, it attenuates all frequency components above a cutoff frequency.

# In[27]:


spectrum.low_pass(3000)


# The result is a spectrum with fewer components.

# In[28]:


spectrum.plot(high=10000)
thinkplot.config(xlabel='Frequency (Hz)')


# We can convert the filtered spectrum back to a wave:

# In[29]:


filtered = spectrum.make_wave()


# And then normalize it to the range -1 to 1.

# In[30]:


filtered.normalize()


# Before playing it back, I'll apodize it (to avoid clicks).

# In[31]:


filtered.apodize()
filtered.plot()
thinkplot.config(xlabel='Time (s)')


# And I'll do the same with the original segment.

# In[32]:


segment.normalize()
segment.apodize()
segment.plot()
thinkplot.config(xlabel='Time (s)')


# Finally, we can listen to the original segment and the filtered version.

# In[33]:


segment.make_audio()


# In[34]:


filtered.make_audio()


# The original sounds more complex, with some high-frequency components that sound buzzy.
# The filtered version sounds more like a pure tone, with a more muffled quality.  The cutoff frequency I chose, 3000 Hz, is similar to the quality of a telephone line, so this example simulates the sound of a violin recording played over a telephone.

# **Exercise 1:** Run the code in the following cells to create a `Signal` with two frequency components, and then create a `Wave` that contains a half-second sample from the `Signal`.
# 
# Add code to compute and plot the `Spectrum` of this `Wave`.
# 
# Then add another `Signal` to the mix, recompute the `Wave` and look at the `Spectrum`.

# In[37]:


cos_sig = thinkdsp.CosSignal(freq=440, amp=1.0, offset=0)
sin_sig = thinkdsp.SinSignal(freq=880, amp=0.5, offset=0)
mix = cos_sig + sin_sig
mix.plot()


# In[40]:


wave = mix.make_wave(duration=0.5, start=0, framerate=11025)
wave.plot()


# ### Interaction
# 
# The following example shows how to use interactive IPython widgets.

# In[42]:


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

    spectrum.plot(color='0.7')
    spectrum.low_pass(cutoff)
    spectrum.plot(color='#045a8d')
    thinkplot.show(xlabel='Frequency (Hz)')
    
    audio = spectrum.make_wave().make_audio()
    display(audio)


# Adjust the sliders to control the start and duration of the segment and the cutoff frequency applied to the spectrum.

# In[43]:


wave = thinkdsp.read_wave('92002__jcveliz__violin-origional.wav')
interact(filter_wave, wave=fixed(wave), 
         start=(0, 5, 0.1), duration=(0, 5, 0.1), cutoff=(0, 10000, 100));


# In[44]:





# In[44]:





# In[44]:





# In[44]:





# In[44]:





# In[ ]:




