
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import map
import time

class MapExplorer():

    x = np.array([])
    y = np.array([])
    r = np.array([])
    n_evaluations = 0

    onclick_cid = None
    keypress_cid = None
    scroll_cid = None
    scale = 1

    def __init__(self, map, x0, y0):
        self.map = map
        self.explore(x0, y0)

    def play(self):
        
        self.fig = plt.figure()

        def draw():
            self.fig.clf()
            self.plot_exploration(onclick, onzoom)
            plt.draw()

        def onclick(x, y):
            self.explore(x, y)
            draw()

        def onzoom(up):
            if up:
                self.scale = self.scale*0.8
            else:
                self.scale = self.scale*1.2
            draw()
        
        draw()
        plt.show()

    def explore(self, x, y):
        self.x = np.append(self.x, x)
        self.y = np.append(self.y, y)
        self.r = np.append(self.r, self.map.reward(x, y))
        self.n_evaluations += 1

    def plot_exploration(self, onclick, onzoom):

        xlim = [self.x[-1]-self.scale, self.x[-1]+self.scale]
        ylim = [self.y[-1]-self.scale, self.y[-1]+self.scale]
        xpoints = np.linspace(start=xlim[0], stop=xlim[1], num=50)
        ypoints = np.linspace(start=ylim[0], stop=ylim[1], num=50)
        x, y = np.meshgrid(xpoints, ypoints)
        r = self.map.reward(x, y)

        cmap = 'magma_r'
        edgecolors = 'black'
        # xy gamemap
        self.gamemap_ax = self.fig.add_subplot(223)
        self.gamemap_ax.set_title('Game map (above)')
        self.gamemap_ax.set_xlabel('x')
        self.gamemap_ax.set_ylabel('y')
        self.gamemap_ax.set_xlim(xlim)
        self.gamemap_ax.set_ylim(ylim)
        self.gamemap_ax.contourf(x,y,r, 20, cmap='RdGy')
        s = self.gamemap_ax.scatter(self.x, self.y, c=self.r, cmap=cmap, edgecolors=edgecolors)
        self.gamemap_ax.plot(self.x, self.y, c=(0,0,0,0.5), ls='--', lw=1)

        # x sideview
        self.x_sideview_ax = self.fig.add_subplot(221)
        self.x_sideview_ax.set_title('Sideview x')
        self.x_sideview_ax.set_xlabel('x')
        self.x_sideview_ax.set_ylabel('Reward')
        self.x_sideview_ax.set_xlim(xlim)
        self.x_sideview_ax.plot(xpoints, self.map.reward(xpoints, self.y[-1]), c=(0,0,0,0.5), lw=1)
        self.x_sideview_ax.scatter(self.x, self.r, c=self.r, cmap=cmap, edgecolors=edgecolors)
        self.x_sideview_ax.plot(self.x, self.r, c=(0,0,0,0.5), ls='--', lw=1)

        # y sideview
        self.y_sideview_ax = self.fig.add_subplot(224)
        self.y_sideview_ax.set_title('Sideview y')
        self.y_sideview_ax.set_xlabel('Reward')
        self.y_sideview_ax.set_ylabel('y')
        self.y_sideview_ax.set_ylim(ylim)
        self.y_sideview_ax.plot(self.map.reward(self.x[-1], ypoints), ypoints, c=(0,0,0,0.5), lw=1)
        self.y_sideview_ax.scatter(self.r, self.y, c=self.r, cmap=cmap, edgecolors=edgecolors)
        self.y_sideview_ax.plot(self.r, self.y, c=(0,0,0,0.5), ls='--', lw=1)

        # 3d
        self.rotation_ax = self.fig.add_subplot(222, projection='3d')
        self.rotation_ax.set_title('Rotating view')
        self.rotation_ax.set_xlabel('x')
        self.rotation_ax.set_ylabel('y')
        self.rotation_ax.set_zlabel('Reward')
        self.rotation_ax.set_xlim(xlim)
        self.rotation_ax.set_ylim(ylim)
        self.rotation_ax.plot_surface(x, y, r, cmap='RdGy')
        self.rotation_ax.plot(self.x, self.y, self.r, c=(0,0,0,0.5), ls='--', lw=1)
        self.rotation_ax.scatter(self.x, self.y, self.r, c=self.r, cmap=cmap, edgecolors=edgecolors)
        
        self.fig.subplots_adjust(right=0.8)
        cbar_ax = self.fig.add_axes([0.85, 0.15, 0.05, 0.7])
        self.fig.colorbar(s, cax=cbar_ax)

        def _onclick(event):
            if self.gamemap_ax == event.inaxes:
                print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                ('double' if event.dblclick else 'single', event.button,
                event.x, event.y, event.xdata, event.ydata))
                onclick(event.xdata, event.ydata)

        if self.onclick_cid is not None:
            self.fig.canvas.mpl_disconnect(self.onclick_cid)
        self.onclick_cid = self.fig.canvas.mpl_connect('button_press_event', _onclick)

        def keypress(event):
            if event.key == '+' or event.key == 'up':
                onzoom(up=True)
            elif event.key == '-' or event.key == 'down':
                onzoom(up=False)

        if self.keypress_cid is not None:
            self.fig.canvas.mpl_disconnect(self.keypress_cid)
        self.keypress_cid = self.fig.canvas.mpl_connect('key_release_event', keypress)

        def scroll(event):
            if event.button == 'up':
                onzoom(up=True)
            elif event.button == 'down':
                onzoom(up=False)

        if self.scroll_cid is not None:
            self.fig.canvas.mpl_disconnect(self.scroll_cid)
        self.scroll_cid = self.fig.canvas.mpl_connect('scroll_event', scroll)


h = map.HomelyHill()
# h.plot()
# plt.show()

m = MapExplorer(map=h, x0=0, y0=0)


# m.plot_exploration(lambda x,y: None)
# plt.show()


m.play()