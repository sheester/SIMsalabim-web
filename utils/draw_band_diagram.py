"""Draw the energy band diagram"""
import matplotlib.pyplot as plt

def create_energy_label(x_left, x_right, y, band_type, position, ax):
    """Create and place the label for an energy level (in eV) of a layer

    Parameters
    ----------
    x_left : float
        Left x position of the layer [m]
    x_right : float
        right x position of the layer [m]
    y : float
        Energy of the band [eV]
    band_type : string
        Type of band (CB, VB, Electrode)
    position : float
        Full length of the device
    ax : axes
        Axes object for the plot
    """

    # If the layer covers over 20% of the figure size, move the label to the x middle of the figure. Else align oit to the left side pf the layer.
    if 'VB' in band_type:
        offset = 0.035
    else:
        offset = -0.01

    if (x_right - x_left) > 0.2*position:
        ax.text((x_left+x_right)/2,y+offset*y,y)
    else:
        ax.text(x_left,y+offset*y,y)

def create_width_label(x_left, x_right, value, y_min, ax, color):
    """ Create the label to displaythe width of a layer on the width bar

    Parameters
    ----------
    x_left : float
        Left x position of the layer [m]
    x_right : float
        right x position of the layer [m]
    value : float
        Width of the layer [m]
    y_max : float
        Lowest energy level of the device [eV]
    ax : axes
        Axes object for the plot
    color : string
        Color of the label
    """
    ax.text((x_left+x_right)/2,y_min-0.7,round(value*1e9),color=color)


def plot_device_widths(ax, y_min, L, LLTL, LRTL, L_original):
    """Plot a width bar below the band energy diagram with the thickness of each layer.

    Parameters
    ----------
    ax : axes
        Axes object for the plot
    y_max : float
        Lowest energy level [eV]
    L : float
        Full width of the device
    LLTL : float
        Width of the Left Transport Layer [m]
    LRTL : float
        Width of the Right Transport Layer
    L_original : List
        List with the layer widths before scaling
    """
    # Horizontal line below the band diagram
    ax.hlines(y_min-0.75,0,L,color='k')
    # Small vertical line on each layer interface
    ax.vlines([0,LLTL,L-LRTL,L],y_min-0.85,y_min-0.65,color='k')
    # Label for each segment
    create_width_label(0,LLTL-0.05*L,L_original[1],y_min,ax,'k')
    create_width_label(LLTL,L-LRTL-0.05*L,L_original[0]-L_original[1]-L_original[2],y_min,ax,'k')
    create_width_label(L-LRTL,L-0.05*L,L_original[2],y_min,ax,'k')
    # Label for the unit [nm]
    ax.text(1.05*L,y_min-0.7,'[nm]',color='k')

def create_band_energy_diagram(param):
    """Create and plot the band energy diagram for the device based on the input parameters

    Parameters
    ----------
    param : dict
        Dictionary with the relevant parameters from the device parameters file

    Returns
    -------
    Figure
        Figure object with the band energy diagram
    """

    fig, ax = plt.subplots()

    # Read parameters
    L = float(param["L"])
    LLTL = float(param["L_LTL"])
    LRTL = float(param["L_RTL"])
    CB = -float(param["CB"])
    VB = -float(param["VB"])
    WL = -float(param["W_L"])
    WR = -float(param["W_R"])
    CBLTL = -float(param["CB_LTL"])
    CBRTL = -float(param["CB_RTL"])
    VBLTL = -float(param["VB_LTL"])
    VBRTL = -float(param["VB_RTL"])

    E_low = min([CB,VB,WL,WR,CBLTL,CBRTL,VBLTL,VBRTL])

    # Save original values for width bar
    L_original = [L,LLTL,LRTL]
    # Set a threshold width for bands to remain visible. Threshold is 10% of the total device width. Only when Transport Layer are defined. 
    if LLTL != 0 and LRTL != 0:
        if LLTL < 0.1*L:
            LLTL = 0.1*L
        if LRTL < 0.1*L:
            LRTL=0.1*L
        if (L-LLTL-LRTL) < 0.1*L:
            frac=LLTL/LRTL
            L_diff = 0.1*L-(L-LLTL-LRTL)
            LLTL = LLTL - L_diff*frac
            LRTL = LRTL - L_diff*(1/frac)

    # Left Transport Layer
    if LLTL > 0:
        ax.fill_between([0, LLTL],[CBLTL,CBLTL],y2=[VBLTL,VBLTL],color='#AF312E')
        create_energy_label(0,LLTL,CBLTL,'CBLTL',L,ax)
        create_energy_label(0,LLTL,VBLTL,'VBLTL',L,ax)

    # Layer 1
    ax.fill_between([LLTL, L-LRTL],[CB,CB],y2=[VB,VB],color='#C7D5A0')
    create_energy_label(LLTL,L-LRTL,CB,'CB',L,ax)
    create_energy_label(LLTL,L-LRTL,VB,'VB',L,ax)

    # Right Transport Layer
    if LRTL > 0:
        ax.fill_between([L-LRTL,L],[CBRTL,CBRTL],y2=[VBRTL,VBRTL],color='#95B2DA')
        create_energy_label(L-LRTL,L,CBRTL,'CBRTL',L,ax)
        create_energy_label(L-LRTL,L,VBRTL,'VBRTL',L,ax)

    # Left Electrode
    ax.plot([-0.1*L,0],[WL,WL],color='k')
    create_energy_label(-0.1*L,0,WL,'WL',L,ax)

    # Right Electrode
    ax.plot([L,L+0.1*L],[WR,WR],color='k')
    create_energy_label(L,L+0.1*L,WR,'WR',L,ax)

    # Hide the figure axis
    ax.axis('off')

    # Add a horizontal bar to the figure width the layer widths
    plot_device_widths(ax, E_low, L, LLTL, LRTL, L_original)

    # plt.show()
    return fig

if __name__ == '__main__':
    # TEMP parameters for testing
    param = {
        "L": 300e-9,
        "L_LTL": 30e-9,
        "L_RTL": 30e-9,
        "CB": 3.0,
        "VB": 5.0,
        "W_L": 3.0,
        "W_R": 5.0,
        "CB_LTL": 3.0,
        "CB_RTL": 2.5,
        "VB_LTL": 5.5,
        "VB_RTL": 5.0}
    create_band_energy_diagram(param)
