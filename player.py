import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.optimize

class Player():
    @property
    def title(self):
        return type(self).__name__

    def play(self, game):
        raise NotImplementedError

class NaturalSelection(Player):
    @property
    def title(self):
        return super().title + ' ' + str(self.sigma)

    def __init__(self, mu=[0, 0], sigma=[1, 1]):
        self.mu = mu
        self.sigma = sigma
        self.best_reward = None

    def play(self, game):
        for _ in range(100):
            guess = self.mu + np.random.randn(2)*self.sigma
            r = game.explore(x=guess[0], y=guess[1])
            if self.best_reward is None or r > self.best_reward:
                self.mu = guess
                self.best_reward = r
        
class NaturalEvolutionSGD(Player):
    @property
    def title(self):
        return super().title + r' $\sigma:$' + str(self.sigma) + ', npop:' + str(self.npop) + r' $\alpha:$' + str(self.alpha)

    def __init__(self, mu=[0, 0], sigma=np.array([1, 1]), npop=2, alpha=1):
        self.mu = mu
        self.sigma = sigma
        self.npop = npop
        self.alpha = alpha

    def play(self, game):
        for _ in range(100):
            N = np.random.randn(self.npop, 2)
            w_try = self.mu + N*self.sigma
            r = game.explore(x=w_try[:,0], y=w_try[:,1])
            A = (r - np.mean(r))/np.std(r)
            self.mu = self.mu + self.alpha/(self.npop*self.sigma)*np.dot(N.T, A)

class FiniteDifferences(Player):
    @property
    def title(self):
        return super().title + r' $\alpha:$' + str(self.alpha)

    def __init__(self, mu=[0, 0], alpha=0.1):
        self.alpha = alpha
        self.mu = np.array(mu)

    def play(self, game):
        eps = 1E-2
        for _ in range(100):
            r0 = game.explore(x=self.mu[0], y=self.mu[1])
            N = np.eye(2)
            w_try = self.mu + N*eps
            r = game.explore(x=w_try[:,0], y=w_try[:,1])
            A = r - r0
            self.mu = self.mu + self.alpha*np.dot(N.T, A)/eps

class ScipyOptimizer(Player):
    @property
    def title(self):
        return self.method

    def __init__(self, method):
        self.method = method

    def play(self, game):
        x0 = np.array([0, 0])
        scipy.optimize.minimize(fun=lambda x: -game.explore(x=x[0], y=x[1]), x0=x0, method=self.method)

class Human(Player):
    
    x = np.array([])
    y = np.array([])
    r = np.array([])

    onclick_cid = None
    keypress_cid = None
    scroll_cid = None
    scale = 1

    def play(self, game):
        # visualize, wait for human, ends when human presses space or enter?

        self.fig = plt.figure()

        def draw():
            self.fig.clf()
            self.plot_exploration(game, onclick, onzoom, onend)
            plt.draw()

        def onclick(x, y):
            self.x = np.append(self.x, x)
            self.y = np.append(self.y, y)
            self.r = np.append(self.r, game.explore(x, y))
            
            draw()

        def onzoom(up):
            if up:
                self.scale = self.scale*0.8
            else:
                self.scale = self.scale*1.2
            draw()

        def onend():
            plt.close(self.fig)
        
        draw()
        plt.show()

    def plot_exploration(self, game, onclick, onzoom, onend):
    
        if len(self.r) == 0:
            xlim = [-self.scale, self.scale]
            ylim = [-self.scale, self.scale]
        else:
            xlim = [self.x[-1]-self.scale, self.x[-1]+self.scale]
            ylim = [self.y[-1]-self.scale, self.y[-1]+self.scale]

        cmap = 'magma_r'
        edgecolors = 'black'
        # xy gamemap
        self.gamemap_ax = self.fig.add_subplot(121)
        self.gamemap_ax.set_title('Game map (above)')
        self.gamemap_ax.set_xlabel('x')
        self.gamemap_ax.set_ylabel('y')
        self.gamemap_ax.set_xlim(xlim)
        self.gamemap_ax.set_ylim(ylim)
        s = self.gamemap_ax.scatter(self.x, self.y, c=self.r, cmap=cmap, edgecolors=edgecolors)
        self.gamemap_ax.plot(self.x, self.y, c=(0,0,0,0.5), ls='--', lw=1)

        # 3d
        self.rotation_ax = self.fig.add_subplot(122, projection='3d')
        self.rotation_ax.set_title('Rotating view')
        self.rotation_ax.set_xlabel('x')
        self.rotation_ax.set_ylabel('y')
        self.rotation_ax.set_zlabel('Reward')
        self.rotation_ax.set_xlim(xlim)
        self.rotation_ax.set_ylim(ylim)
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
            print(event.key)
            if event.key == '+' or event.key == 'up':
                onzoom(up=True)
            elif event.key == '-' or event.key == 'down':
                onzoom(up=False)
            elif event.key == 'enter' or event.key == ' ':
                onend()

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


