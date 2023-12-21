import pyautogui as ag
import matplotlib.pyplot as mplt


class UILocatorModel():
    def capture_desktop(self):
        return ag.screenshot()

    def change_color_of_label(self, num_of_matches_found) -> str:
        if(num_of_matches_found == 1):
            return 'green'
        else:
            return 'red'

    def plot_result(self, needle_img, haystack_img, needle_img_edges, haystack_img_edges, peakmap, title, coord):
        fig, axs = mplt.subplots(2, 3)
        sp_haystack_img = axs[0, 0]
        sp_needle_img = axs[0, 1]
        sp_invisible = axs[0, 2]
        sp_haystack_img_edges = axs[1, 0]
        sp_needle_img_edges = axs[1, 1]
        sp_peakmap = axs[1, 2]
        
        # ROW 1 ================================
        sp_needle_img.set_title('Needle')
        sp_needle_img.imshow(needle_img, cmap=mplt.cm.gray)
        sp_haystack_img.set_title('Haystack')
        sp_haystack_img.imshow(haystack_img, cmap=mplt.cm.gray)
        sp_haystack_img.sharex(sp_haystack_img_edges)
        sp_haystack_img.sharey(sp_haystack_img_edges)

        sp_invisible.set_visible(False)

        # ROW 2 ================================
        sp_needle_img_edges.set_title('Needle (edge d.)')
        sp_needle_img_edges.imshow(needle_img_edges, cmap=mplt.cm.gray)    

        sp_haystack_img_edges.set_title('Haystack (edge d.)')
        sp_haystack_img_edges.imshow(haystack_img_edges, cmap=mplt.cm.gray)

        sp_peakmap.set_title('Peakmap')
        sp_peakmap.imshow(peakmap)
        sp_peakmap.sharex(sp_haystack_img_edges)
        sp_peakmap.sharey(sp_haystack_img_edges)
        
        for loc in coord:
            rect = mplt.Rectangle((loc[0], loc[1]), loc[2], loc[3], edgecolor='r', facecolor='none')
            sp_haystack_img_edges.add_patch(rect)
        
        sp_peakmap.autoscale(False)    
        fig.suptitle(title, fontsize=14, fontweight='bold')
        
        mplt.show()