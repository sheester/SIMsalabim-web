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
        plot_funcs(data=data, x='x', y=y_var, ax=ax, label=labels[i], color=color[i],linewidth=1)
        i+=1
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
    data['Jext']=data['Jext']/1e1
    plot_funcs(data=data, x='Vext', y="Jext", ax=ax, label='Simulated')
    ax.axvline(choice_voltage, color='k', linestyle='--')
    ax.set_xlabel('V$\mathrm{_{ext}}$ [V]')
    ax.set_ylabel('J$\mathrm{_{ext}}$ [mAcm$^{-2}$]')
    ax.set_title('Current-voltage characteristic')
    if exp == True:
        data_exp['J'] = data_exp['J']/1e1
        plot_funcs(data=data_exp, x='V', y='J', ax=ax, label='Experimental')
        ax.legend()
    if exp == False:
        ax.get_legend().remove()
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
    ax = create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax,'x [nm]','V [V]','linear', color)
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
    labels = ['E$_{\mathrm{vac}}$','E$_{\mathrm{c}}$','E$_{\mathrm{v}}$','E$_{\mathrm{Fn}}$','E$_{\mathrm{Fp}}$']
    ax = create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, 'x [nm]','Energy level [eV]','linear', color)
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
    labels = ['n','p','n$_{\mathrm{ion}}$','p$_{\mathrm{ion}}$']
    create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, 'x [nm]', 'Carrier density [ m$^{-3}$ ]','log',color)
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
    labels = ['ft$_{\mathrm{b1}}$','ft$_{\mathrm{i1}}$']
    create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, 'x [nm]', 'Filling level [ - ]','linear', color)
    ax.set_title('Filling levels')
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
    labels = ['$\mathrm{\mu_{n}}$','$\mathrm{\mu_{p}}$']
    create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, 'x [nm]', 'Transport [ m$^{-2}$V$^{-1}$s$^{-1}$ ]','linear', color)
    ax.set_title('Transport')
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
    labels=['G$_{\mathrm{ehp}}$', 'G$_{\mathrm{free}}$', 'R$_{\mathrm{dir}}$', 'BulkSRH$_{\mathrm{n}}$', 'BulkSRH$_{\mathrm{p}}$', 'IntSRH$_{\mathrm{n}}$', 'IntSRH$_{\mathrm{p}}$']
    create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, 'x [nm]', 'Generation/Recombination Rate [ m$^{-3}$s$^{-1}$ ]','linear', color)
    ax.set_title('Generation and Recombination Rates')
    return ax

# Currents [Am-3]
def plot_currents(data_var, choice_voltage, plot_funcs, ax, color):
    """Make a plot with the Current parameters

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
    par=['Jn','Jp','Jtot']
    labels = ['J$_{\mathrm{n}}$', 'J$_{\mathrm{p}}$', 'J$_{\mathrm{tot}}$']
    for item in par:
        data_var[item]=data_var[item]/1e1
    create_output_plot(data_var, choice_voltage, plot_funcs, par, labels, ax, 'x [nm]', 'Current density [mAcm$^{-2}$]','linear', color)
    ax.set_title('Currents')
    return ax