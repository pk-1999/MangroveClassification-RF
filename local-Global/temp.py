import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

plt.close('all')

a = sorted([f.name for f in font_manager.fontManager.ttflist])

for i in a:
    print(i)
