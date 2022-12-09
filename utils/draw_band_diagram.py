import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_rectangle_patch(
        CB,
        VB,
        energy_offset,
        energy_step_size,
        p_origin,
        width,
        total_width_step_size,
        color,
        size,
        ax):
    # Description:  Draw a rectangle box representing a device layer.
    # Arguments:    CB (float) -                    Conduction band edge or Work function for electrodes
    #               VB (float) -                    Valence band edge or Work function for electrodes
    #               energy_offset (float) -         Energy offset to shift diagram in place (=maximum energy)
    #               energy_step_size (float) -      Amount of eV per grid point
    #               p_origin (float) -              x location of the previous layer
    #               width (float) -                 Width of the layer
    #               total_width_step_size (float) - Amount of m per grid point
    #               color (string) -                Outline color of layer
    #               size (number) -                 Number of grid points
    #               ax (ax) -                       Figure
    # Returns:      rect (Rectangle) -              Rectangle patches object.
    #               p_right (float) -               x value of right border of current layer to be used as input for x position of the next layer
    e_CB = (CB-energy_offset)/energy_step_size
    e_VB = (VB-energy_offset)/energy_step_size
    e_delta = e_VB-e_CB
    p_left = p_origin
    p_right = p_left + width/total_width_step_size
    p_delta = p_right-p_left
    if CB==VB:
        rect = patches.Rectangle((p_left, e_CB-0.005*size), p_delta, e_delta+0.01*size,
                                linewidth=0, edgecolor='none', facecolor=color)
    else:
        rect = patches.Rectangle((p_left, e_CB), p_delta, e_delta,
                                linewidth=0, edgecolor='none', facecolor=color)

    # Add the Energy label to the figure. For electrodes, only one label has to be added.
    create_energy_label(p_left+0.01*size, p_right, e_CB, 0.05/energy_step_size, CB, size, ax)
    if not CB == VB:
        create_energy_label(p_left+0.01*size, p_right, e_VB, -0.12/energy_step_size, VB, size, ax)

    return (rect, p_right)

def create_energy_label(x_left, x_right, y, offset, value, size, ax):
    # If the layer covers over 20% of the figure size, move the label to the x middle of the figure. Else align oit to the left side pf the layer.
    if (x_right - x_left) > 0.2*size:
        ax.text((x_left+x_right)/2,y+offset,value)
    else:
        ax.text(x_left,y + offset,value)

def create_band_energy_diagram(param):
    fig, ax = plt.subplots()

    size = 1000000  # set number of grid points
    ax.set_xlim(-0.01*size, size+0.01*size)  # Add extra whitespace to x-axis
    ax.set_ylim(-size-0.01*size, 0.01*size)  # Add extra whitespace to y-axis

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

    energy = [CB, VB, WL, WR, CBLTL, CBRTL, VBLTL, VBRTL]

    # Set a threshold width for bands to remain visible. Threshold is 10% of the total device width
    if LLTL < 0.1*L:
        LLTL = 0.1*L
    if LRTL < 0.1*L:
        LRTL=0.1*L
    if (L-LLTL-LRTL) < 0.1*L:
        frac=LLTL/LRTL
        L_diff = 0.1*L-(L-LLTL-LRTL)
        LLTL = LLTL - L_diff*frac
        LRTL = LRTL - L_diff*(1/frac)

    # Electrode width configuration
    electrode_width_fraction = 0.1  # Added fraction of the total device width
    electrode_width = electrode_width_fraction*L  # Set the width of a electrode

    # Width configuration
    total_width = L+2*electrode_width
    total_width_step_size = total_width/size  # m/gridpoint

    # Energy configuration
    max_energy = max(energy)
    min_energy = min(energy)
    energy_step_size = abs((max_energy-min_energy))/size  # ev/gridpoint
    # Offset in energy compared to 0eV to shift the band diagram in view.
    energy_offset = max_energy

    # Left Electrode
    left_electrode, p_origin_ltl = create_rectangle_patch(
        WL, WL, energy_offset, energy_step_size, 0, electrode_width_fraction*size*total_width_step_size, total_width_step_size, 'k', size, ax)
    ax.add_patch(left_electrode)

    # Left Transport Layer
    if LLTL != 0:
        left_transport_layer, p_origin_layer = create_rectangle_patch(
            CBLTL, VBLTL, energy_offset,  energy_step_size, p_origin_ltl, LLTL, total_width_step_size, '#AF312E', size, ax)
        ax.add_patch(left_transport_layer)

    # Layer 1
    layer_1, p_origin_rtl = create_rectangle_patch(
        CB, VB, energy_offset, energy_step_size, p_origin_layer, L-LLTL-LRTL, total_width_step_size, '#C7D5A0', size, ax)
    ax.add_patch(layer_1)

    # Right Transport Layer
    if LRTL != 0:
        right_transport_layer, p_origin_right_electrode = create_rectangle_patch(
            CBRTL, VBRTL, energy_offset, energy_step_size, p_origin_rtl, LRTL, total_width_step_size, '#95B2DA', size, ax)
        ax.add_patch(right_transport_layer)

    # Right Electrode
    right_electrode, p_end = create_rectangle_patch(
        WR, WR, energy_offset, energy_step_size, p_origin_right_electrode, electrode_width_fraction*size*total_width_step_size, total_width_step_size, 'k', size, ax)
    ax.add_patch(right_electrode)

    ax.axis('off')
    # plt.show()
    # plt.savefig('./figures/band_diagram.png')
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
