
from pylab import xlim, ylim


def funci(x):
    """Here is something new
    Hallo hallo.
    I am a docstring! 
    
    You can represent code blocks fairly easily::

       import numpy as np
       x = np.random.rand(12)
       print x

    .. math::
        \int f(x)~dx 
    .. note::
       Michse beautiful
       you too
    .. seealso:: This is a simple **seealso** note.
    .. warning::
       never use me!
    .. todo:: 
       This is a todo!
       
       
    .. plot:: pyplots/scatter_tooltip.py
       :include-source:
    
    Full path: 
    
    .. raw:: html
    
        <div style="margin-top:10px;">
        <iframe width="700" height="500"scrolling="no" frameborder="0" src="E:/IPython2/141007 Sphinx and ShapelyChipDesigns/try4/docs/pyplots/img/scatter_plot.html"></iframe>
        </div>
        
    "pyplots/img/scatter_plot.html" 
    
    .. raw:: html

        <div style="margin-top:10px;">
        <iframe width="700" height="500"scrolling="no" frameborder="0" src="pyplots/img/scatter_plot.html"></iframe>
        </div>
        
    "../pyplots/img/scatter_plot.html" 
    
    .. raw:: html

        <div style="margin-top:10px;">
        <iframe width="700" height="500"scrolling="no" frameborder="0" src="../pyplots/img/scatter_plot.html"></iframe>
        </div>
        
    "../../pyplots/img/scatter_plot.html
    
    .. raw:: html

        <div style="margin-top:10px;">
        <iframe width="700" height="500"scrolling="no" frameborder="0" src="../../pyplots/img/scatter_plot.html"></iframe>
        </div>

    "../../../src/_img/scatter_plot.html
    
    .. raw:: html

        <div style="margin-top:10px;">
        <iframe width="700" height="500"scrolling="no" frameborder="0" src="../../../src/_img/scatter_plot.html"></iframe>
        </div>
       
    .. raw:: html

        <div style="margin-top:10px;">
          <iframe width="560" height="315" src="http://www.youtube.com/embed/_EjisXtMy_Y" frameborder="0" allowfullscreen></iframe>
        </div>
    
    .. doctest::

        >>> import math
        >>> print math.sqrt(2.)
        1.41421356237
       
    .. plot:: pyplots/ellipses.py
       :include-source:
       
    .. plot:: pyplots/test_mpld3.py
       :include-source:
       
    .. image:: pyplots/img/scatter_plot.png

    .. _ipython-highlighting:
    .. sourcecode:: ipython

        In [69]: lines = plot([1,2,3])

        In [70]: setp(lines)
          alpha: float
          animated: [True | False]
          antialiased or aa: [True | False]
          ...snip
    
    You can also inline code for plots directly, and the code will be
    executed at documentation build time and the figure inserted into your
    docs; the following code::

       .. plot::

          import matplotlib.pyplot as plt
          import numpy as np
          x = np.random.randn(1000)
          plt.hist( x, 20)
          plt.grid()
          plt.title(r'Normal: $\mu=%.2f, \sigma=%.2f$'%(x.mean(), x.std()))
          plt.show()

    Produces this output: 
    
    .. plot::
    
        import matplotlib.pyplot as plt
        import numpy as np
        x = np.random.randn(1000)
        plt.hist( x, 20)
        plt.grid()
        plt.title(r'Normal: $\mu=%.2f, \sigma=%.2f$'%(x.mean(), x.std()))
        plt.show()
       
    Lalal: 
       import matplotlib.pyplot as plt
        import numpy as np
        x = np.random.randn(1000)
        plt.hist( x, 20)
        plt.grid()
        plt.title(r'Normal: $\mu=%.2f, \sigma=%.2f$'%(x.mean(), x.std()))
        plt.show()
    """
    return 0