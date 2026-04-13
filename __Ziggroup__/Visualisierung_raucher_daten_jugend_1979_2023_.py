import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from __Ziggroup__.raucher_daten_jugend_1979_2023_ import jahre, nieraucher_prozent, raucher_prozent

plt.figure(figsize=(10, 5.5))

plt.plot(jahre, nieraucher_prozent, 'o-', color='forestgreen', 
         label='Nie-Raucher (%)', linewidth=2.5, markersize=7)

plt.plot(jahre, raucher_prozent, 's-', color='firebrick', 
         label='Raucher (%)', linewidth=2.5, markersize=7)

plt.title('Raucheranteil Jugendliche Deutschland 1979–2023', fontsize=13, pad=12)
plt.xlabel('Jahr')
plt.ylabel('Anteil (%)')

plt.grid(alpha=0.35, linestyle=':')
plt.legend(frameon=True, fontsize=10)

plt.xticks(jahre, rotation=50, ha='right', fontsize=9)
plt.yticks(fontsize=9)

plt.margins(x=0.02)
plt.tight_layout()
plt.show()