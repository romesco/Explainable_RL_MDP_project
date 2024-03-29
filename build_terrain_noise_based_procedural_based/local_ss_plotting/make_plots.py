#!/usr/bin/env python
import numpy
import matplotlib.pyplot as plt
from ss_plotting import plot_utils
import ss_plotting.colors as colors

def plot_bar_graph(series, series_colors,
                   series_labels=None,
                   series_color_emphasis=None, 
                   series_errs = None,
                   series_err_colors = None,
                   series_padding=0.0,
                   series_use_labels=False,
                   series_style=None,
                   plot_xlabel = None,
                   plot_ylabel = None, 
                   plot_yinvert = False,
                   plot_title = None,
                   category_labels = None,
                   category_ticks= True,
                   category_padding = 0.25,
                   barwidth=0.35,
                   xpadding=0.,
                   stacked=False,
                   fontsize=8,
                   legend_fontsize=8,
                   legend_location='best',
                   savefile = None,
                   savefile_size = (3.4, 1.5),
                   horizontal = False,
                   show_plot = True):
    """
    Plot a bar graph 
    @param series List of data for each series - each of these will be plotted in a different color
      Each series should have the same number of elements. 
    @param series_labels List of labels for each series - same length as series
    @param series_colors List of colors for each series - same length as series
    @param series_color_emphasis List of booleans, one for each series, indicating whether the series
       color should be bold - if None no series is bold
    @param series_errs The error values for each series - if None no error bars are plotted
    @param series_err_colors The colors for the error bars for each series, if None black is used
    @param plot_xlabel The label for the x-axis - if None no label is printed
    @param plot_ylabel The label for the y-axis - if None no label is printed
    @param plot_title A title for the plot - if None no title is printed
    @param category_labels The labels for each particular category in the histogram
    @param category_ticks If true, also place a tick at each category
    @param category_padding Fraction of barwidth (0 - 1) - distance between categories
    @param barwidth The width of each bar
    @param xpadding The padding between the first bar and the left axis and the last bar and the right axis
    @param stacked If true, stack the data in each category
    @param fontsize The size of font for all labels
    @param legend_fontsize The size of font for the legend labels
    @param legend_location The location of the legend, if None no legend is included
    @param savefile The path to save the plot to, if None plot is not saved
    @param savefile_size The size of the saved plot
    @param horizontal Plot bars horizontally instead of vertically
    @param show_plot If True, display the plot on the screen via a call to plt.show()
    @return fig, ax The figure and axis the plot was created in
    """

    # Validate
    if series is None or len(series) == 0:
        raise ValueError('No data series')
    num_series = len(series)

    if len(series_colors) != num_series:
        raise ValueError('You must define a color for every series')
        
    if series_labels is None:
        series_labels = [None for l in range(num_series)]
    if len(series_labels) != num_series:
        raise ValueError('You must define a label for every series')

    if series_errs is None:
        series_errs = [None for _ in series]
    if len(series_errs) != num_series:
        raise ValueError('series_errs is not None. Must provide error value for every series.')

    if series_err_colors is None:
        series_err_colors = ['black' for _ in series]
    if len(series_err_colors) != num_series:
        raise ValueError('Must provide an error bar color for every series')

    if series_color_emphasis is None:
        series_color_emphasis = [False for _ in series]
    if len(series_color_emphasis) != num_series:
        raise ValueError('The emphasis list must be the same length as the series_colors list')

    if series_use_labels and len(series[0]) > 1:
        raise ValueError('Only series containing one category may be labeled.')

    if series_style is None:
        series_style = [dict() for _ in series]

    fig, ax = plt.subplots()
    plot_utils.configure_fonts(fontsize=fontsize, legend_fontsize=legend_fontsize)

    if plot_yinvert:
      ax.invert_yaxis()

    spacing = category_padding*barwidth
    num_categories = len(series[0])
    category_width = spacing + num_series*barwidth 
    if stacked:
        category_width = spacing+barwidth 
    index = numpy.array(range(num_categories)) * category_width + xpadding

    for idx in range(num_series):
        offset = idx * (barwidth + series_padding)
        if stacked:
            offset = 0.

        style = dict(
            label = series_labels[idx],
            color = colors.get_plot_color(
                series_colors[idx], emphasis=series_color_emphasis[idx]),
            ecolor = colors.get_plot_color(series_err_colors[idx]),
            linewidth = 0,
        )
        style.update(series_style[idx])

        if horizontal:
            r = ax.barh(
                bottom = index + offset, 
                #left = index + offset,
                height = barwidth, #series[idx],
                width = series[idx],# barwidth,
                xerr = series_errs[idx],
                **style
            )
        else:
            r = ax.bar(
                left = index + offset,
                height = series[idx],
                width = barwidth,
                yerr = series_errs[idx],
                **style
            )
    
    # Label the plot
    if plot_ylabel is not None:
        ax.set_ylabel(plot_ylabel)
    if plot_xlabel is not None:
        ax.set_xlabel(plot_xlabel)
    if plot_title is not None:
        ax.set_title(plot_title)
    
    # Add category tick marks
    if series_use_labels:
        indices = numpy.arange(num_series)
        ticks = xpadding + indices * (barwidth + series_padding) + 0.5 * barwidth
        if horizontal:
            ax.set_yticks(ticks)
        else:
            ax.set_xticks(ticks)

        if series_labels is not None:
            if horizontal:
                ax.set_yticklabels(series_labels)
            else:
                ax.set_xticklabels(series_labels)
    elif category_ticks:
        if not stacked:
            ticks = index + (num_series/2.)*barwidth
        else:
            ticks = index + .5*barwidth

        if horizontal:
            ax.set_yticks(ticks)
        else:
            ax.set_xticks(ticks)

        if category_labels is not None:
            if horizontal:
                ax.set_yticklabels(category_labels)
            else:
                ax.set_xticklabels(category_labels)
    else:
        if horizontal:
            ax.set_yticks([])
        else:
            ax.set_xticks([])

    # Set the x-axis limits
    lims = [ 0,
             2 * xpadding
             + num_categories * (category_width + (num_series - 1) * series_padding)
             - spacing
    ]
    if horizontal:
        ax.set_ylim(lims)
    else:
        ax.set_xlim(lims)

    # Legend
    if legend_location is not None:
        ax.legend(loc=legend_location, frameon=False)

    # Make the axis pretty
    plot_utils.simplify_axis(ax)

    # Save the file
    if savefile is not None:
        plot_utils.output(fig, savefile, savefile_size,
                          fontsize=fontsize, 
                          legend_fontsize=legend_fontsize
                          )
        
    # Show
    if show_plot:
        plt.show()

    return fig, ax


def plot(series, series_colors,
         series_color_emphasis = None,
         series_labels = None,
         series_errs = None,
         series_err_colors = None,
         fill_error=True,
         plot_xlabel = None, 
         plot_xlim = None,
         plot_ylabel = None, 
         plot_ylim = None,
         plot_title = None,
         fontsize=8, legend_fontsize=8,
         linewidth = 2,
         legend_location = 'best',
         savefile = None,
         savefile_size = (3.4, 1.5),
         show_plot = True,
         jitter_x = -1.,
         jitter_y = -1.,
         jitter_alpha = 1.,
         marker_size = 5,
         x_scale = 'linear',
         y_scale = 'linear',
         plot_markers = None,
         line_styles = None,
         mark_every=1):
    """
    Plot yvals as a function of xvals
    @param series List of (xvals, yvals) for each series- each of these will be plotted in a different color
    @param series_labels List of labels for each series - same length as series
    @param series_colors List of colors for each series - same length as series
    @param series_color_emphasis List of booleans, one for each series, indicating whether the series
       color should be bold - if None no series is bold
    @param series_errs The error values for each series - if None no error bars are plotted
    @param series_err_colors The colors for the error bars for each series, if None black is used
-   @param fill_error If true, shade the area to show error bars, if not, draw actual error bars
    @param plot_xlabel The label for the x-axis - if None no label is printed
    @param plot_xlim The limits for the x-axis - if None these limits are selected automatically
    @param plot_ylabel The label for the y-axis - if None no label is printed
    @param plot_ylim The limits for the y-axis - if None these limits are selected automatically
    @param plot_title A title for the plot - if None no title is printed
    @param fontsize The size of font for all labels
    @param legend_fontsize The size of font for the legend labels
    @param linewidth The width of the lines in the plot
    @param legend_location The location of the legend, if None no legend is included
    @param savefile The path to save the plot to, if None plot is not saved
    @param savefile_size The size of the saved plot
    @param show_plot If True, display the plot on the screen via a call to plt.show()
    @param x_scale set to log or linear for the x axis
    @param y_scale set to log or linear for the y axis
    @param plot_markers if not None, a list of line marker symbols
    @param line_styles if not None, a list of line style symbols
    
    @param marker_size 
    @param jitter_x the scale of the normal distribution for jitter along x direction, if -1., then no jitter along x 
    @param jitter_y the scale of the normal distribution for jitter along y direction, if -1., then no jitter along y 
    @param jitter_alpha the alpha value for jittered scatter points
    @return fig, ax The figure and axis the plot was created in
    """

    # Validate
    if series is None or len(series) == 0:
        raise ValueError('No data series')
    num_series = len(series)

    if len(series_colors) != num_series:
        raise ValueError('You must define a color for every series')
        
    if series_labels is None:
        series_labels = [None for s in series]
    if len(series_labels) != num_series:
        raise ValueError('You must define a label for every series')

    if series_errs is None:
        series_errs = [None for s in series]
    if len(series_errs) != num_series:
        raise ValueError('series_errs is not None. Must provide error value for every series.')

    if series_err_colors is None:
        series_err_colors = ['black' for s in series]
    if len(series_err_colors) != num_series:
        raise ValueError('Must provide an error bar color for every series')

    if series_color_emphasis is None:
        series_color_emphasis = [False for s in series]
    if len(series_color_emphasis) != num_series:
        raise ValueError('The emphasis list must be the same length as the series_colors list')

    if plot_markers is None:
        plot_markers = ['None' for s in series]
    if len(plot_markers ) != num_series:
        raise ValueError('The marker list must contain all series')

    if line_styles is None:
        line_styles  = ['-' for s in series]
    if len(line_styles) != num_series:
        raise ValueError('The line style list must contain all series')

    fig, ax = plt.subplots()
    plot_utils.configure_fonts(fontsize=fontsize, legend_fontsize=legend_fontsize)

    num_series = len(series)
    for idx in range(num_series):
        xvals = series[idx][0]
        yvals = numpy.array(series[idx][1])
        
        # by Shen Li
        if jitter_x != -1. and jitter_y == -1.:
            # http://nbviewer.jupyter.org/gist/fonnesbeck/5850463
            # Add some random "jitter" to the x-axis
            xvals = numpy.random.normal(xvals, jitter_x, size=len(yvals))
        elif jitter_x == -1. and jitter_y != -1.:
            # http://nbviewer.jupyter.org/gist/fonnesbeck/5850463
            # Add some random "jitter" to the x-axis
            yvals = numpy.random.normal(yvals, jitter_y, size=len(xvals))
        elif jitter_x != -1. and jitter_y != -1.:
            xs = list(numpy.random.normal(xvals, jitter_x, size=len(yvals)))
            ys = list(numpy.random.normal(yvals, jitter_y, size=len(xvals)))
            xvals = xs
            yvals = ys

        r = ax.plot(xvals, yvals,
            label = series_labels[idx],
            color = colors.get_plot_color(series_colors[idx], emphasis=series_color_emphasis[idx]),
            marker = plot_markers[idx],
            linestyle = line_styles[idx],
            lw = linewidth,
            markersize=marker_size,
            markevery=mark_every,
            alpha=jitter_alpha)

        errs = series_errs[idx]
        if errs is not None:
            shade_color = colors.get_plot_color(color = series_err_colors[idx])
            if fill_error:
                plot_utils.shaded_error(ax, xvals, yvals, numpy.array(errs), color=shade_color)
            else:
                ax.errorbar(xvals, yvals, yerr=errs, linestyle='None', ecolor=shade_color)
        
    
    # Label the plot
    if plot_ylabel is not None:
        ax.set_ylabel(plot_ylabel)
    if plot_xlabel is not None:
        ax.set_xlabel(plot_xlabel)
    if plot_title is not None:
        ax.set_title(plot_title)
    if plot_xlim is not None:
        ax.set_xlim(plot_xlim)
    if plot_ylim is not None:
        ax.set_ylim(plot_ylim)
    
    ax.set_yscale(y_scale)
    ax.set_xscale(x_scale)

    # Legend
    if legend_location is not None:
        ax.legend(loc=legend_location, frameon=False)

    # Make the axis pretty
    plot_utils.simplify_axis(ax)

    # Save the file
    if savefile is not None:
        plot_utils.output(fig, savefile, savefile_size,
                          fontsize=fontsize,
                          legend_fontsize=legend_fontsize)

    # Show
    if show_plot:
        plt.show()

    return fig, ax
    
