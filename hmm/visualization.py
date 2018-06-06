import matplotlib as mpl
from matplotlib import pyplot


def visualization(a):
    fig = pyplot.figure(2)
    cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_colormap',
                                           ['white','grey','black'],
                                           256)

    img2 = pyplot.imshow(a,interpolation='nearest',
                    cmap = cmap2,
                    origin='lower')

    fig.savefig("image5.png")