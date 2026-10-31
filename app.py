# ==============================================================================
# EndoCore: 3D Bio-Shield AI Simulator (Filter 2 MVP)
# Framework: Plotly Dash (Python)
# ==============================================================================

# 1. IMPORT REQUIRED LIBRARIES
# We use 'dash' to build the interactive web dashboard.
# We use 'plotly' to build the 3D visual environment.
# We use 'numpy' to generate the 3D dots (cells) mathematically.
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

# 2. INITIALIZE THE WEB APPLICATION
app = dash.Dash(__name__)

# 3. BUILD THE DASHBOARD LAYOUT (The User Interface)
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#111111', 'color': 'white'}, children=[
    
    # Dashboard Header
    html.H1("EndoCore: 3D Bio-Shield AI Simulator", style={'textAlign': 'center', 'color': '#00ffcc'}),
    html.P("Filter 2 MVP - Interactive AI Cytokine Detection & Peptide Release", style={'textAlign': 'center'}),
    
    # Create a 3-column layout
    html.Div(style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'marginTop': '30px'}, children=[
        
        # ==========================================
        # LEFT PANEL: THE CONTROL DECK (Sliders)
        # ==========================================
        html.Div(style={'width': '25%', 'padding': '20px', 'backgroundColor': '#222222', 'borderRadius': '10px'}, children=[
            html.H3("Simulate Microenvironment", style={'color': '#ffaa00'}),
            html.P("Drag sliders to simulate a CD8+ T-Cell Attack:"),
            
            # Slider 1: IL-6 (Pro-inflammatory Cytokine)
            html.Label("IL-6 Concentration (pg/mL)"),
            dcc.Slider(id='slider-il6', min=0, max=100, step=1, value=5, 
                       marks={0: '0', 50: '50', 100: '100'}, tooltip={"placement": "bottom", "always_visible": True}),
            html.Br(),
            
            # Slider 2: IFN-gamma (Pro-inflammatory Cytokine)
            html.Label("IFN-γ Concentration (pg/mL)"),
            dcc.Slider(id='slider-ifn', min=0, max=100, step=1, value=2, 
                       marks={0: '0', 50: '50', 100: '100'}, tooltip={"placement": "bottom", "always_visible": True}),
            html.Br(),
            
            # Slider 3: Interstitial pH
            html.Label("Interstitial pH (Drop simulates inflammation)"),
            dcc.Slider(id='slider-ph', min=6.0, max=7.5, step=0.1, value=7.4, 
                       marks={6.0: '6.0', 6.8: '6.8', 7.4: '7.4'}, tooltip={"placement": "bottom", "always_visible": True}),
        ]),
        
        # ==========================================
        # CENTER PANEL: THE 3D BIO-SIMULATION
        # ==========================================
        html.Div(style={'width': '45%', 'padding': '10px'}, children=[
            html.H3("3D Nanochip Environment", style={'textAlign': 'center'}),
            # This is where the 3D Plotly graph will appear
            dcc.Graph(id='3d-bio-sim', style={'height': '500px'})
        ]),
        
        # ==========================================
        # RIGHT PANEL: THE AI COMMAND TERMINAL
        # ==========================================
        html.Div(style={'width': '25%', 'padding': '20px', 'backgroundColor': '#000000', 'border': '1px solid #333', 'borderRadius': '10px', 'fontFamily': 'monospace'}, children=[
            html.H3("AI Logic Terminal", style={'color': '#00ffcc'}),
            # This text box will update automatically based on the AI's decision
            html.Div(id='ai-terminal-output', style={'whiteSpace': 'pre-line', 'color': '#00ff00', 'lineHeight': '1.5'})
        ])
    ])
])

# 4. THE AI LOGIC & 3D RENDERING FUNCTION (The "Brain")
# This function runs automatically every time you move a slider.
@app.callback(
    [Output('3d-bio-sim', 'figure'),
     Output('ai-terminal-output', 'children')],
    [Input('slider-il6', 'value'),
     Input('slider-ifn', 'value'),
     Input('slider-ph', 'value')]
)
def update_simulation(il6_val, ifn_val, ph_val):
    
    # --- STEP A: THE AI DECISION ALGORITHM ---
    # We define the threshold for an autoimmune attack based on your research.
    # High cytokines OR low pH indicates an attack.
    is_attack = (il6_val > 40) or (ifn_val > 40) or (ph_val < 6.9)
    
    # --- STEP B: BUILD THE 3D VISUALIZATION ---
    fig = go.Figure()
    
    # 1. Draw the EndoCore Beta Cells (Always a stable blue core in the center)
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers+text',
        marker=dict(size=40, color='#00aaff', opacity=0.8, symbol='circle'),
        text=["EndoCore<br>Beta Cells"], textposition="bottom center",
        name='CRISPR Beta Cells'
    ))
    
    # 2. Draw the surrounding Immune Cells (using random math to place dots in a sphere)
    # Generate 150 random dots around the core
    theta = np.random.uniform(0, 2*np.pi, 150)
    phi = np.random.uniform(0, np.pi, 150)
    r = np.random.uniform(5, 10, 150) # Distance from the center
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    
    # 3. Determine the color of the immune cells based on the AI decision
    if not is_attack:
        # NORMAL STATE: Immune cells are neutral grey, Terminal shows normal status.
        cell_color = 'rgba(150, 150, 150, 0.5)' 
        cell_name = 'Neutral Tissue Cells'
        
        terminal_text = f"""
        [SYSTEM] Sensors Active...
        IL-6: {il6_val} pg/mL
        IFN-γ: {ifn_val} pg/mL
        pH: {ph_val}
        
        [AI_MODEL] Status: Normal Homeostasis.
        [OUTPUT] Beta-Cell Insulin Output: 100%.
        Micro-valves: CLOSED.
        """
        
    else:
        # ATTACK DETECTED: AI triggers the defense! 
        # The visual instantly turns the attacking red dots into green Tregs.
        cell_color = '#00ff00' # Bright Green
        cell_name = 'Tolerogenic Peptides / Tregs'
        
        terminal_text = f"""
        [SYSTEM] WARNING: Cytokine Spike Detected!
        IL-6: {il6_val} pg/mL  (HIGH)
        IFN-γ: {ifn_val} pg/mL (HIGH)
        pH: {ph_val} (ACIDIC)
        
        [AI_MODEL] THRESHOLD BREACHED. 
        CD8+ T-Cell Autoimmune Attack Classified.
        
        [ACTUATION] Triggering Defense Sequence...
        [ACTUATION] Opening Micro-valves...
        [ACTUATION] Releasing IL-10 & TGF-β Peptides!
        
        [STATUS] Attack Neutralized. 
        T-Cells converting to Tregs (Green).
        Beta Cells Secure.
        """
        
        # Draw the aggressive red T-cells slightly further out to show the attack was stopped
        r_red = np.random.uniform(12, 15, 50)
        x_red = r_red * np.sin(phi[:50]) * np.cos(theta[:50])
        y_red = r_red * np.sin(phi[:50]) * np.sin(theta[:50])
        z_red = r_red * np.cos(phi[:50])
        
        fig.add_trace(go.Scatter3d(
            x=x_red, y=y_red, z=z_red,
            mode='markers',
            marker=dict(size=6, color='#ff0000', opacity=0.9),
            name='Repelled CD8+ T-Cells'
        ))

    # Add the primary immune cells (Grey if normal, Green if defended) to the 3D plot
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(size=8, color=cell_color, opacity=0.9),
        name=cell_name
    ))
    
    # Clean up the 3D layout to make it look like a sleek medical interface
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='#111111',
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='#111111'
        ),
        legend=dict(font=dict(color="white"))
    )
    
    # Return the updated 3D graph and the updated Terminal text to the web page
    return fig, terminal_text

# 5. RUN THE SERVER
if __name__ == '__main__':
    app.run_server(debug=True)
