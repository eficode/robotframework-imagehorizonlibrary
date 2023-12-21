import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.feature import match_template
from skimage.feature import peak_local_max
import skimage.viewer
from skimage.color import rgb2gray
import pyautogui as ag
import sys

screen = data.coins()
coin = screen[170:220, 75:130]



#coin = skimage.io.imread('..\\..\\images\\text.png', as_gray=True)
#coin = skimage.io.imread('..\\..\\images\\win_changed.png', as_gray=True)

#skimage.viewer.ImageViewer(image).show()
# ---
# result = match_template(image, coin,pad_input=True) #added the pad_input bool
# peak_min_distance = min(coin.shape)
# peak_min_distance = 1

# peaks = peak_local_max(result,min_distance=peak_min_distance,threshold_abs=1)
# # produce a plot equivalent to the one in the docs
# plt.imshow(result)
# # highlight matched regions (plural)
# plt.plot(peaks[:,1], peaks[:,0], 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)
# plt.show()
# ---


def detect_edges(img, sigma, low, high):
    edge_img = skimage.feature.canny(
        image=img,
        sigma=sigma,
        low_threshold=low,
        high_threshold=high,
    )
    return edge_img


def plot_result(what, where, what_edges, where_edges, peakmap, title, locations):   

    fig, axs = plt.subplots(2, 3)
    sp_what = axs[0, 0]
    sp_where = axs[0, 1]
    sp_invisible = axs[0, 2]
    sp_what_edges = axs[1, 0]
    sp_where_edges = axs[1, 1]
    sp_peakmap = axs[1, 2]
    
    # ROW 1 ================================
    sp_what.imshow(what, cmap=plt.cm.gray)
    sp_what.set_title('what')
    sp_where.imshow(where, cmap=plt.cm.gray)

    sp_where.set_title('where')
    sp_where.sharex(sp_where_edges)
    sp_where.sharey(sp_where_edges)

    sp_invisible.set_visible(False)

    # ROW 2 ================================
    sp_what_edges.imshow(what_edges, cmap=plt.cm.gray)    
    sp_what_edges.set_title('what_edge')

    sp_where_edges.imshow(where_edges, cmap=plt.cm.gray)
    sp_where_edges.set_title('where_edge')

    sp_peakmap.imshow(peakmap)
    sp_peakmap.set_title('peakmap')
    sp_peakmap.sharex(sp_where_edges)
    sp_peakmap.sharey(sp_where_edges)
    
    for loc in locations:
        # highlight matched region
        #hwhat, wwhat = what_edges.shape
        # TODO: 
        #rect = plt.Rectangle((x_peak-int(wwhat/2), y_peak-int(hwhat/2)), wwhat, hwhat, edgecolor='r', facecolor='none')
        rect = plt.Rectangle((loc[0], loc[1]), loc[2], loc[3], edgecolor='r', facecolor='none')
        sp_where_edges.add_patch(rect)

    
    sp_peakmap.autoscale(False)    
    fig.suptitle(title, fontsize=14, fontweight='bold')
    
    plt.show()
    pass





def try_locate(what_name, sigma=2.0, low=0.1, high=0.3, confidence=0.99, locate_all=False):
    locations = None
    what = skimage.io.imread('..\\..\\images\\' + what_name, as_gray=True)
    what_h, what_w = what.shape   
    where = rgb2gray(np.array(ag.screenshot()))
    what_edge = detect_edges(what, sigma, low, high)
    where_edges = detect_edges(where, sigma, low, high)
    peakmap = match_template(where_edges, what_edge)

    if locate_all: 
        # https://stackoverflow.com/questions/48732991/search-for-all-templates-using-scikit-image
        # peaks = peak_local_max(peakmap)
        peaks = peak_local_max(peakmap,threshold_rel=confidence) 
        peak_coords = zip(peaks[:,1], peaks[:,0])
        locations = []
        for i, pk in enumerate(peak_coords):
            locations.append((pk[0], pk[1], what_w, what_h))
        pass
        title = f"{len(locations)} matches with confidence level > {confidence}"
    else: 
        ij = np.unravel_index(np.argmax(peakmap), peakmap.shape)
        x, y = ij[::-1]
        peak = peakmap[y][x]
        if peak > confidence:                      
            locations = [(x, y, what_w, what_h)]
        matched = peak > confidence
        title = f"Match = {str(matched)} (peak at {peak} > {confidence})"

#    plot_result(what, where, peakmap, title, x,y)
    plot_result(what, where, what_edge, where_edges, peakmap, title, locations)
    

#image = skimage.io.imread('..\\..\\images\\screen.png', as_gray=True)

#try_locate('ok.png', sigma=1.4, confidence=0.8, locate_all=True)

try_locate('3.png', locate_all=True)
#try_locate('3.png', sigma=1.0, confidence=0.8, locate_all=True)
#compare('win.png')
#cProfile.run('compare()')

# confidence:            0.9999999999999
# win auf screen:        0.9999999999999992
# win auf screenshot:    0.9999999999999974
# win_ch auf screen:     0.9999999419440094
# win_ch auf screenshot: 0.9999999419440035

