import numpy as np
from scipy.signal import butter, sosfilt, sosfiltfilt
from scipy.io import wavfile
SR=48000; DUR=9.44; t=np.arange(int(SR*DUR))/SR; N=len(t)
rng=np.random.default_rng(7)
def lp(x,fc,o=4): return sosfilt(butter(o,fc,'low',fs=SR,output='sos'),x)
def hp(x,fc,o=4): return sosfilt(butter(o,fc,'high',fs=SR,output='sos'),x)
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],'band',fs=SR,output='sos'),x)
def saw(f,ph=0): return 2*((f*t+ph)%1)-1
def env(a,b,attack=0.01,release=0.3):
    e=np.zeros(N); i0,i1=int(a*SR),min(N,int(b*SR))
    seg=np.arange(i1-i0)/SR; e[i0:i1]=np.minimum(1,seg/attack)*np.exp(-seg/release); return e
# Pad: D-Moll add9, verstimmte Sägezähne, langsam öffnender Filter (blockweise)
notes=[73.42,110.0,174.61,220.0,329.63]
padL=np.zeros(N); padR=np.zeros(N)
for f in notes:
    for d,side in [(-0.12,0),(0.0,1),(0.13,2)]:
        s=saw(f*(1+d/100),rng.random())
        if side!=1: padL+=s
        if side!=0: padR+=s
blk=2400; outL=np.zeros(N); outR=np.zeros(N)
for i in range(0,N,blk):
    tc=i/SR; fc=350+1500*min(1,tc/6)*(0.85+0.15*np.sin(2*np.pi*0.25*tc))
    sos=butter(2,fc,'low',fs=SR,output='sos')
    outL[i:i+blk]=sosfilt(sos,padL[max(0,i-4800):i+blk])[-(min(blk,N-i)):]
    outR[i:i+blk]=sosfilt(sos,padR[max(0,i-4800):i+blk])[-(min(blk,N-i)):]
pad=np.stack([outL,outR])/12
# Riser 1.8 -> 3.0 s (gefiltertes Rauschen)
noise=rng.standard_normal(N); r=np.clip((t-1.8)/1.2,0,1)*(t<3.0)
riser=bp(noise,1500,9000)*r**2*0.18
# Impact bei 3.0 s (Sub-Sinus mit Pitch-Drop + Rauschschlag)
imp=np.zeros(N); m=t>=3.0; tt=t[m]-3.0
imp[m]=np.sin(2*np.pi*(55*tt+ (90/6)*(1-np.exp(-6*tt))))*np.exp(-tt/0.9)*0.55
imp+=lp(noise,2500)*env(3.0,4.5,0.002,0.25)*0.25
# Puls ab 3.0 s: 145 BPM, weiche Kick + Offbeat-Hats
bpm=145; beat=60/bpm; kick=np.zeros(N); hat=np.zeros(N)
k=3.0+beat
while k<DUR-0.5:
    i=int(k*SR); L=min(N-i,int(0.35*SR)); kt=np.arange(L)/SR
    kick[i:i+L]+=np.sin(2*np.pi*(48*kt+(110/30)*(1-np.exp(-30*kt))))*np.exp(-kt/0.16)*0.45
    j=int((k+beat/2)*SR); Lh=min(N-j,int(0.06*SR))
    if Lh>0: hat[j:j+Lh]+=hp(noise[j:j+Lh],7000,2)*np.exp(-np.arange(Lh)/SR/0.015)*0.10
    k+=beat
# Sidechain-Ducking der Fläche durch die Kick
duck=1-0.45*np.convolve(np.abs(kick)>0.05,np.ones(int(0.12*SR))/int(0.12*SR),'same').clip(0,1)
mix=pad*duck + np.stack([riser*0.9,riser]) + imp + kick + np.stack([hat*0.8,hat])
# Ein- und Ausblenden
fade=np.ones(N); fade[:int(0.15*SR)]=np.linspace(0,1,int(0.15*SR)); n2=int(0.9*SR); fade[-n2:]=np.linspace(1,0,n2)**1.5
mix*=fade
mix=np.tanh(mix*1.2)/np.tanh(1.2)
mix=mix/np.max(np.abs(mix))*0.89
wavfile.write("bed.wav",SR,(mix.T*32767).astype(np.int16))
print("ok",mix.shape)
