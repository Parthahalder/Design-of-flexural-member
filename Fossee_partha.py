import math

# Constants based on IS:800:2007
E = 2.1e5  # Modulus of Elasticity for steel (in MPa)
gamma_mo = 1.10  # Partial safety factor for steel as per IS 800

# Function to read input data from a file
def input_data(file_name='input.txt'):
    with open(file_name, 'r') as file:
        data = file.readlines()
        inputs = {line.split(":")[0].strip(): float(line.split(":")[1].strip()) for line in data}
    return inputs

# Function to write results to a file
def export_results(output, file_name='output.txt'):
    with open(file_name, 'w') as file:
        file.write(output)

# Moment capacity calculation
def moment_capacity(Z_p, fy):
    phi_m_d = (Z_p * fy) / (gamma_mo * 1e3)  # in kNm
    return phi_m_d

# Shear capacity calculation
def shear_capacity(A_v, fy):
    phi_v_d = (0.6 * fy * A_v) / (gamma_mo * 10)  # in kN
    return phi_v_d

# Deflection check (for simply supported beam with UDL)
def deflection_check(I, W, L):
    delta = ((5 * W * L**4)* 1e8) / (384 * E * I)  # deflection in mm
    return delta

# Main design check function
def design_flexural_member():
    inputs = input_data()

    # Inputs from file
    M = inputs["Applied Moment (kNm)"]
    V = inputs["Applied Shear Force (kN)"]
    L = inputs["Effective Span (m)"]
    B = inputs["Width of beam(cm)"]
    H = inputs["Height of beam(cm)"]
    fy = inputs["Yield Strength of Steel (MPa)"]
    delta_max = inputs["Allowable Deflection (mm)"]

    # UDL assumption for deflection check
    w = 2*(V / L)  # Load per unit length (kN/m)
    Z_p = (B*H*H)/4 #Plastic section modulus
    A_v = 1.2 * (B*H) # shear correction factor = 1.2 multiplied with cross sectional area to get effective shear area
    I = (B*H*H*H)/12 # Moment of inertia

    # Design Checks
    phi_m_d = moment_capacity(Z_p, fy)
    moment_check = "Pass" if phi_m_d >= M else "Fail"

    phi_v_d = shear_capacity(A_v, fy)
    shear_check = "Pass" if phi_v_d >= V else "Fail"

    delta = deflection_check(I, w, L)
    deflection_check_result = "Pass" if delta <= delta_max else "Fail"

    # Report generation
    output = f"""
    Flexural Member Design Report (Simply Supported Beam):
    -----------------------------------------------------
    Input Data:
    - Moment (M): {M:.2f} kNm
    - Shear Force (V): {V:.2f} kN
    - Effective Span (L): {L:.2f} m
    - Section Modulus (Zp): {Z_p:.2f} cm^3
    - Shear Area (Av): {A_v:.2f} cm^2
    - Moment of Inertia (I): {I:.2f} cm^4
    - Yield Strength of Steel (fy): {fy:.2f} MPa

    Design Check Results:
    ---------------------
    1. Moment Capacity (phi_Md): {phi_m_d:.2f} kNm
       - Applied Moment: {M:.2f} kNm
       - Moment Check: {moment_check}

    2. Shear Capacity (phi_Vd): {phi_v_d:.2f} kN
       - Applied Shear Force: {V:.2f} kN
       - Shear Check: {shear_check}

    3. Deflection Check:
       - Deflection (delta): {delta:.2f} mm
       - Allowable Deflection: {delta_max:.2f} mm
       - Deflection Check: {deflection_check_result}

    Conclusion: The flexural member design is {("safe" if moment_check == "Pass" and shear_check == "Pass" and deflection_check_result == "Pass" else "unsafe")}.
    """

    print(output)
    export_results(output)

# Run the design function
design_flexural_member()
