import numpy as np
import matplotlib.pyplot as plt

class Visualize():
    fig = None
    n_evaluations = None
    scroll_cid = None

    def __init__(self, players, games, map):
        self.players = players
        self.games = games
        self.map = map

    def show(self, n_evaluations=1):
        self.fig = plt.figure()
        self.n_evaluations = n_evaluations
        self.draw()
        plt.show()

    def refresh(self):
        self.fig.clf()
        self.draw()
        plt.draw()

    def draw(self):
        axis = self.fig.add_subplot(111)
        cmap = 'magma_r'
        edgecolors = 'black'

        minx = 99999
        miny = 99999
        maxx = -99999
        maxy = -99999

        axis.set_title('n_evaluations: '+str(self.n_evaluations))

        # get plot size
        for g in self.games:
            minx = np.min((g.x.min(), minx))
            miny = np.min((g.y.min(), miny))
            maxx = np.max((g.x.max(), maxx))
            maxy = np.max((g.y.max(), maxy))

        # game map
        xscale = (maxx-minx)*0.1
        yscale = (maxy-miny)*0.1
        xlim = [minx-xscale, maxx+xscale]
        ylim = [miny-yscale, maxy+yscale]
        xpoints = np.linspace(start=xlim[0], stop=xlim[1], num=50)
        ypoints = np.linspace(start=ylim[0], stop=ylim[1], num=50)
        x, y = np.meshgrid(xpoints, ypoints)
        r = self.map.reward(x, y)
        axis.contourf(x, y, r, 20, cmap='RdGy')

        # show path
        for (g, p) in zip(self.games, self.players):
            minx = np.min((g.x.min(), minx))
            miny = np.min((g.y.min(), miny))
            maxx = np.max((g.x.max(), maxx))
            maxy = np.max((g.y.max(), maxy))

            i = np.min((self.n_evaluations, len(g.r)))
            axis.scatter(g.x[:i], g.y[:i], edgecolors=edgecolors, label=p.title)
            axis.plot(g.x[:i], g.y[:i], c=(0,0,0,0.5), ls='--', lw=1)

        legend = axis.legend()

        if self.scroll_cid is not None:
            self.fig.canvas.mpl_disconnect(self.scroll_cid)
        self.scroll_cid = self.fig.canvas.mpl_connect('scroll_event', self.onscroll)

    def onscroll(self, event):
        if event.button == 'up':
            self.n_evaluations += 1
        elif event.button == 'down':
            self.n_evaluations -= 1
        self.refresh()