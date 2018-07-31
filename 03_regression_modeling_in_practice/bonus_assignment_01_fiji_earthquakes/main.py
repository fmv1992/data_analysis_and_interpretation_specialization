"""
This work creates all the data needed for the analyzes on the pdf.

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
# pylama:ignore=C901,W0611,R0914
# Too complex and import not used
import os
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import scipy
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from mpl_toolkits.basemap import Basemap


def main():
    u"""Main function."""
    # Data reading and managing.
    db = pd.read_csv('quakes.csv')
    db.drop('index', axis=1, inplace=True)
    print('original head:')
    print(db.head())
    # Depth should be in meters to honor de SI.
    db['depth'] *= 1e3
    # Lets create a low ('l'), medium ('m') and high ('h') categories for the
    # earthquakes considering the cutoff values of 4.75 and 5.25

    # Creation of qualitative variables
    def mag_quali(x):
        u"""Map a magnitude to a qualitative variable."""
        if x <= 4.75:
            return 'l'
        elif x <= 5.25:
            return 'm'
        else:
            return 'h'

    def depth_quali(x):
        u"""Map a depth to a categorical variable."""
        if x <= 1 * 700e3 / 3:
            return 'l'
        elif x <= 2 * 700e3 / 3:
            return 'm'
        else:
            return 'h'

    db['mag_quali'] = db['mag'].apply(mag_quali).astype('category')
    db['depth_quali'] = db['depth'].apply(depth_quali).astype('category')

    # Now it is time for some plotting: the lat and long
    # Lets improve it with a map of the world
    for qualitative_variable in ['mag_quali', 'depth_quali']:
        OFFSET = 50
        MINLAT = db.lat.min() - OFFSET
        MAXLAT = db.lat.max() + OFFSET
        MINLONG = db.long.min() - OFFSET
        MAXLONG = db.long.max() + OFFSET
        fig, ax1 = plt.subplots()
        themap = Basemap(
            projection='gall',
            llcrnrlon=MINLONG,    # lower-left corner longitude
            llcrnrlat=MINLAT,     # lower-left corner latitude
            urcrnrlon=MAXLONG,    # upper-right corner longitude
            urcrnrlat=MAXLAT,     # upper-right corner latitude
            resolution='i',
            area_thresh=100000.0)
        themap.drawcoastlines()
        themap.drawcountries()
        themap.fillcontinents(color='gainsboro')
        themap.drawmapboundary(fill_color='steelblue')
        x, y = themap(
            db.long.tolist(),
            db.lat.tolist())
        x = pd.Series(x, index=list(range(1000)))
        y = pd.Series(y)

        for color, category in zip(['white', 'yellow', 'red'],
                                   ['l', 'm', 'h']):
            if qualitative_variable == 'mag_quali':
                full_sentence_for_category = {
                    'l': 'low intensity earthquake.',
                    'm': 'medium intensity earthquake.',
                    'h': 'high intensity earthquake.'}
            else:
                full_sentence_for_category = {
                    'l': 'low depth earthquake.',
                    'm': 'medium depth earthquake.',
                    'h': 'high depth earthquake.'}

            mask = db[qualitative_variable] == category
            themap.plot(x[mask].tolist(),
                        y[mask].tolist(),
                        'o',                     # marker shape
                        color=color,             # marker colour
                        markersize=4,            # marker size
                        label=str.capitalize(
                            full_sentence_for_category[category]))
        # Now add the legend with some customizations.
        legend = ax1.legend(loc='best', frameon=True, fancybox=True,
                            shadow=True, markerscale=1.7)

        # The frame is matplotlib.patches.Rectangle instance surrounding the
        # legend.
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
        if qualitative_variable == 'mag_quali':
            plt.title('Latitude and Longitude plotting of earthquakes '
                      'by magnitude.'
                      '\nNorth of New Zealand.')
        else:
            plt.title('Latitude and Longitude plotting of earthquakes '
                      'by depth.'
                      '\nNorth of New Zealand.')
        plt.tight_layout()
        plt.savefig(
            os.path.join(
                'images', 'lat_long_earthquakes_{}.png'.format(
                    qualitative_variable)), dpi=500)
        plt.close('all')
        del ax1, fig

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
        plt.savefig(
            os.path.join(
                'images', 'histogram_for_{}.png'.format(col)),
            dpi=500)
        plt.close('all')

    # Now it is time to find correlation among variables.
    # The three meaningful quantitative variables are 'mag', 'stations' and
    # 'depth'.
    # Lets start with a linear regression:

    def linear_regression(v1, v2):
        u"""Create a linear regression."""
        plt.scatter(db[v1], db[v2])
        plt.title(
            '{0} versus {1} scatter plot.'.format(
                histogram_vars[v1].capitalize(),
                histogram_vars[v2].capitalize()))
        print('Regression for {0} versus {1}:'.format(
            histogram_vars[v1].capitalize(),
            histogram_vars[v2].capitalize()))
        reg1 = smf.ols('db[v1] ~ db[v2]', data=db).fit()
        print(reg1.summary(), '\n' * 3)
        plt.tight_layout()
        plt.savefig(
            os.path.join('images', 'scatter_{0}_{1}'.format(v1, v2)),
            dpi=500)
        plt.close('all')

    for var1, var2 in [
            ['mag', 'depth'],
            ['mag', 'stations'],
            ['depth', 'stations']
    ]:
        linear_regression(var1, var2)

    print('final processed data head:')
    print(db.head())


if __name__ == '__main__':
    main()
