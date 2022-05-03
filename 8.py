import numpy as np
import matplotlib.pyplot as plt
tmp = []
pred = 0
with open("settings.txt") as sett:
    for i in sett.read().split("\n"):
        p = i.split(" ")
        if len(p) ==2:
            n = float(p[1])
            tmp.append(n)
            


d_a = np.loadtxt("data.txt", dtype = float)

x_raw = d_a[:,1]
y_raw = d_a[:,0]

filter_arr = []

prev = 0
for el in y_raw:
    if abs(el-prev)<=0.1:
        filter_arr.append(True)
        prev = el
    else:
        #print(el,prev)
        filter_arr.append(False)
        
x = x_raw[filter_arr]
y = y_raw[filter_arr]

fig, axs = plt.subplots(1,1)
fig.set_figwidth(8)
fig.set_figheight(5)
axs.minorticks_on()
axs.grid(b=True,which='major',color='cadetblue',linewidth=1.3)
axs.grid(b=True,which='minor',color='gainsboro')
axs.set_title('Процесс заряда и разряда конденсатора в RC-цепочке')
axs.set_xlabel('Время, с')
axs.set_ylabel('Напряжение, В')
axs.set_path_effects(path_effects.withTickedStroke())
line, = axs.plot(x,y,color='blue', marker='o',markersize=1,label = 'V(t)')
axs.legend(handles=[line])
axs.text(60,2.6,'Время заряда = 44.33 с')
axs.text(60,2.3,'Время разряда = 85.14 с')
plt.show()