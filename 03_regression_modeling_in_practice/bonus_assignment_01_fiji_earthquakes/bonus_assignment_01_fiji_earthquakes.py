u"""
From the description:
    Locations of Earthquakes off Fiji
    Description

    The data set give the locations of 1000 seismic events of MB > 4.0. The
    events occurred in a cube near Fiji since 1964.
    Usage

    quakes

    Format

    A data frame with 1000 observations on 5 variables.
    [,1] 	lat 	numeric 	Latitude of event
    [,2] 	long 	numeric 	Longitude
    [,3] 	depth 	numeric 	Depth (km)
    [,4] 	mag 	numeric 	Richter Magnitude
    [,5] 	stations 	numeric 	Number of stations reporting

"""
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import scipy
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from mpl_toolkits.basemap import Basemap

def main():
    # Data reading and managing.
    db = pd.read_csv('quakes.csv', index_col='index')
    # Depth should be in meters to honor de SI.
    db['depth'] *= 1e3
    # Lets create a low ('l'), medium ('m') and high ('h') categories for the
    # earthquakes considering the cutoff values of 4.75 and 5.25


    def mag_quali(x):
        u"""Maps a magnitude to a qualitative variable."""
        if x <= 4.75:
            return 'l'
        elif x <= 5.25:
            return 'm'
        else:
            return 'h'
    serie = db['mag'].apply(mag_quali).astype('category')
    db.insert(4, 'mag_quali', serie)


    # Now it is time for some plotting: the lat and long
    # Lets improve it with a map of the world
    OFFSET = 50
    MINLAT = db.lat.min() - OFFSET
    MAXLAT = db.lat.max() + OFFSET
    MINLONG = db.long.min() - OFFSET
    MAXLONG = db.long.max() + OFFSET
    fig, ax1 = plt.subplots()
    themap = Basemap(projection='gall',
                     llcrnrlon=MINLONG,             # lower-left corner longitude
                     llcrnrlat=MINLAT,              # lower-left corner latitude
                     urcrnrlon=MAXLONG,             # upper-right corner longitude
                     urcrnrlat=MAXLAT,              # upper-right corner latitude
                     resolution='i',
                     area_thresh=100000.0,
                     )
    themap.drawcoastlines()
    themap.drawcountries()
    themap.fillcontinents(color='gainsboro')
    themap.drawmapboundary(fill_color='steelblue')
    map_colors_intensity = {
        'white': 'l',
        'yellow': 'm',
        'red': 'h'}

    for color, category in zip(['white', 'yellow', 'red'],
                               ['l', 'm', 'h']):
        full_sentence_for_category = {
            'l': 'low intensity earthquake.',
            'm': 'medium intensity earthquake.',
            'h': 'high intensity earthquake.'}
        x, y = themap(db[db.mag_quali == category].long.tolist(),
                      db[db.mag_quali == category].lat.tolist())
        themap.plot(x, y,
                    'o',                    # marker shape
                    color=color,         # marker colour
                    markersize=4,            # marker size
                    label=str.capitalize(full_sentence_for_category[category])
                    )

    # Now add the legend with some customizations.
    legend = ax1.legend(loc='best', frameon=True, fancybox=True,
                        shadow=True, markerscale=1.7)

    # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.5')

    # Set the fontsize
    for label in legend.get_texts():
        label.set_fontsize('medium')

    for label in legend.get_lines():
        label.set_linewidth(1.5)  # the legend line width

    OFFSET = 0.05
    MINLAT = min(y) * (1 - OFFSET)
    MAXLAT = max(y) * (1 + OFFSET)
    MINLONG = min(x) * (1 - OFFSET)
    MAXLONG = max(x) * (1 + OFFSET)
    ax1.set_xlim([MINLONG, MAXLONG])
    ax1.set_ylim([MINLAT, MAXLAT])
    plt.title('Latitude and Longitude plotting of earthquakes.'
              '\nNorth of New Zealand.')
    plt.tight_layout()
    plt.savefig('lat_long_earthquakes.png', dpi=500)
    plt.close('all')
    # A bunch of histograms would also be nice to better understand the
    # distribution of our variables
    histogram_vars = {'mag': 'earthquake\'s magnitude',
                      'depth': 'depth of the earthquake',
                      'stations': 'number of stations that detected the '
                      'eartquake'}
    for col in histogram_vars.keys():
        plt.hist(db[col], bins=12)
        plt.title('Histogram for {0}.'.format(histogram_vars[col]))
        plt.tight_layout()
        plt.savefig('histogram_for_{}.png'.format(col), dpi=500)
        plt.close('all')

    # Now it is time to find correlation among variables.
    # The three meaningful quantitative variables are 'mag', 'stations' and
    # 'depth'.
    # Lets start with a linear regression:


    def linear_regression(v1, v2):
        plt.scatter(db[v1], db[v2])
        plt.title(
            '{0} versus {1} scatter plot.'.format(
                histogram_vars[v1].capitalize(),
                histogram_vars[v2].capitalize()))
        print('Regression for {0} versus {1}:'.format(
                histogram_vars[v1].capitalize(),
                histogram_vars[v2].capitalize()))
        reg1 = smf.ols('db[v1] ~ db[v2]', data=db).fit()
        print(reg1.summary(), '\n'*3)
        plt.tight_layout()
        plt.savefig('scatter_{0}_{1}'.format(v1, v2), dpi=500)
        plt.close('all')


    for var1, var2 in [
        ['mag', 'depth'],
        ['mag', 'stations'],
        ['depth', 'stations']
    ]:
        linear_regression(var1, var2)


if __name__ == '__main__':
    main()
