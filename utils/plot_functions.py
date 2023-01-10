"""Functions for page: Simulation_results"""

def create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, xlabel, ylabel, yscale, color):
    """Create a pyplot for a set of variables for a given Vext.

    Parameters
    ----------
    data_var : DataFrame
        All output data from the Var.dat file
    choice_voltage : float
        The Vext potential for which to show the data
    plot_funcs : Any
        Type of plot
    par : List
        List of parameter to plot
    labels : List
        List of parameter labels to plot
    ax : axes
        Axes object for the plot
    xlabel : string
        Label for the x-axis. Format: parameter [unit]
    ylabel : string
        Label for the y-axis. Format: parameter [unit]
    yscale : string
        Scale of the y-axis. E.g linear or log
    color : List
        List of standard colors

    Returns
    -------
    axes
        Updated Axes object for the plot
    """
    i=0
    data = data_var[data_var['Vext'] == choice_voltage]
    for y_var in par:
        if (sum(data[y_var]) != 0):
            plot_funcs(data['x'], data[y_var], label=labels[i], color=color[i],linewidth=1)
        i+=1
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yscale(yscale)
    return ax

# JV-curve
def plot_jv_curve(data, choice_voltage, plot_funcs, ax, exp, data_exp='' ):
    """Make a plot of the JV curve

    Parameters
    ----------
    data : DataFrame
        All output data from the JV.dat file
    choice_voltage : float
        The Vext potential for which the data in Var.dat is shown
    plot_funcs : Any
        Type of plot
    ax : axes
        Axes object for the plot
    exp : boolean
        True if experimental JV curve needs to be plotted.
    data_exp : DataFrame
        Optional argument when an experimental JV curve is supplied
    Returns
    -------
    axes
        Updated Axes object for the plot
    """
    plot_funcs(data['Vext'], data['Jext'], label='Simulated')
    ax.axvline(choice_voltage, color='k', linestyle='--')
    ax.set_xlabel('$V_{ext}$ [V]')
    ax.set_ylabel('$J_{ext}$ [Am$^{-2}$]')

    ax.set_title('Current-voltage characteristic')
    if exp is True:
        plot_funcs(data_exp['V'], data_exp['J'], label='Experimental')
        ax.legend()
    if exp is False:
        legend = ax.legend()
        legend.remove()
        # ax.get_legend().remove()
    ax.axhline(y=0, color='gray', linewidth=0.5)
    ax.axvline(x=0, color='gray', linewidth=0.5)
    return ax


# Potential [V]
def plot_potential(data_var, choice_voltage, plot_funcs, ax, color):
    """Make a plot of the Potential

    Parameters
    ----------
    data_var : DataFrame
        All output data from the Var.dat file
    choice_voltage : float
        The Vext potential for which to show the data
    plot_funcs : Any
        Type of plot
    ax : axes
        Axes object for the plot
    color : List
        List of standard colors

    Returns
    -------
    axes
        Updated Axes object for the plot
    """
    par = ['V']
    labels = ['V']
    ax = create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax,'$x$ [nm]','$V$ [V]','linear', color)
    ax.set_title('Potential')
    return ax

# Energy [eV]
def plot_energy(data_var, choice_voltage, plot_funcs, ax, color):
    """Make a plot with the Energy parameters (Band diagram)

    Parameters
    ----------
    data_var : DataFrame
        All output data from the Var.dat file
    choice_voltage : float
        The Vext potential for which to show the data
    plot_funcs : Any
        Type of plot
    ax : axes
        Axes object for the plot
    color : List
        List of standard colors

    Returns
    -------
    axes
        Updated Axes object for the plot
    """
    par = ['Evac','Ec', 'Ev', 'phin', 'phip']
    labels = ['$E_{vac}$','$E_{c}$','$E_{v}$','$E_{Fn}$','$E_{Fp}$']
    ax = create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, '$x$ [nm]','Energy level [eV]','linear', color)
    ax.set_title('Energy Band Diagram')
    return ax

# Carrier densities [m-3]
def plot_carrier_densities(data_var, choice_voltage, plot_funcs, ax, color):
    """Make a plot with the Carrier Density parameters

    Parameters
    ----------
    data_var : DataFrame
        All output data from the Var.dat file
    choice_voltage : float
        The Vext potential for which to show the data
    plot_funcs : Any
        Type of plot
    ax : axes
        Axes object for the plot
    color : List
        List of standard colors

    Returns
    -------
    axes
        Updated Axes object for the plot
    """
    par = ['n','p','nion','pion']
    labels = ['$n$','$p$','$n_{ion}$','$p_{ion}$']
    create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, '$x$ [nm]', 'Carrier density [m$^{-3}$]','log',color)
    ax.set_title('Carrier Densities')
    return ax

# Filling Level [a.u.]
def plot_filling_levels(data_var, choice_voltage, plot_funcs, ax, color):
    """Make a plot with the Filling level parameters

    Parameters
    ----------
    data_var : DataFrame
        All output data from the Var.dat file
    choice_voltage : float
        The Vext potential for which to show the data
    plot_funcs : Any
        Type of plot
    ax : axes
        Axes object for the plot
    color : List
        List of standard colors

    Returns
    -------
    axes
        Updated Axes object for the plot
    """
    par = ['ftb1','fti1']
    labels = ['$ft_{b1}$','$ft_{i1}$']
    create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, '$x$ [nm]', 'Filling of traps [ ]','linear', color)
    ax.set_title('Filling of traps')
    return ax

# Transport [m2V-1s-1]
def plot_transport(data_var, choice_voltage, plot_funcs, ax, color):
    """Make a plot with the Transport parameters

    Parameters
    ----------
    data_var : DataFrame
        All output data from the Var.dat file
    choice_voltage : float
        The Vext potential for which to show the data
    plot_funcs : Any
        Type of plot
    ax : axes
        Axes object for the plot
    color : List
        List of standard colors

    Returns
    -------
    axes
        Updated Axes object for the plot
    """
    par = ['mun','mup']
    labels = ['$\mu_{n}$','$\mu_{p}$']
    create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, '$x$ [nm]', 'Mobility [m$^{-2}$V$^{-1}$s$^{-1}$]','log', color)
    ax.set_title('Mobilities')
    return ax

# Generation and Recombination [m-3s-1]
def plot_generation_recombination(data_var, choice_voltage, plot_funcs, ax, color):
    """Make a plot with the Generation and Recombination parameters

    Parameters
    ----------
    data_var : DataFrame
        All output data from the Var.dat file
    choice_voltage : float
        The Vext potential for which to show the data
    plot_funcs : Any
        Type of plot
    ax : axes
        Axes object for the plot
    color : List
        List of standard colors

    Returns
    -------
    axes
        Updated Axes object for the plot
    """
    par=['Gehp', 'Gfree', 'Rdir','BulkSRHn', 'BulkSRHp', 'IntSRHn', 'IntSRHp']
    labels=['$G_{ehp}$', '$G_{free}$', '$R_{dir}$', '$BulkSRH_{n}$', '$BulkSRH_{p}$', '$IntSRH_{n}$', '$IntSRH_{p}$']
    create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, 'x [nm]', 'Generation/Recombination Rate [m$^{-3}$s$^{-1}$]','linear', color)
    ax.set_title('Generation and Recombination Rates')
    return ax

# Currents [Am-2]
def plot_currents(data_var, choice_voltage, plot_funcs, ax, color):
    """Make a plot with the Current parameters
float
        All output data from the Var.dat file
    choice_voltage : float
        The Vext potential for which to show the data
    plot_funcs : Any
        Type of plot
    ax : axes
        Axes object for the plot
    color : List
        List of standard colors

    Returns
    -------
    axes
        Updated Axes object for the plot
    """
    par=['Jn','Jp','Jtot']
    labels = ['$J_{n}$', '$J_{p}$', '$J_{tot}$']

    create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, '$x$ [nm]', 'Current density [Am$^{-2}$]','linear', color)
    ax.set_title('Current densities')
    return ax
