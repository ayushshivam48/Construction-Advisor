import streamlit as st
from data import * # Import data to get default list values

def initialize_state():
    """
    Initializes all required keys in st.session_state on the first run.
    This prevents the form from resetting its values on submission.
    """
    
    # --- Lists for dropdowns ---
    zoning_list = list(ZONING_OPTIONS.keys())
    eia_list = list(EIA_STATUS_OPTIONS.keys())
    phase1_list = list(PHASE1_ESA_OPTIONS.keys())
    phase2_list = list(PHASE2_ESA_OPTIONS.keys())
    biodiversity_list = list(BIODIVERSITY_IMPACT_OPTIONS.keys())
    flood_list = list(FLOOD_RISK_OPTIONS.keys())
    drainage_list = list(DRAINAGE_OPTIONS.keys())
    seismic_list = list(SEISMIC_ZONE_OPTIONS.keys())
    contaminant_list = list(SOIL_CONTAMINANT_OPTIONS.keys())
    water_quality_list = list(WATER_QUALITY_OPTIONS.keys())
    utility_list = list(UTILITY_OPTIONS.keys())
    traffic_list = list(TRAFFIC_IMPACT_OPTIONS.keys())
    soil_texture_list = list(SOIL_TEXTURE_OPTIONS.keys())
    project_list = list(CONSTRUCTION_RULES.keys())

    # --- Report Data State ---
    if 'site_details' not in st.session_state:
        st.session_state.site_details = None # None means no report has been run
    if 'desired_project' not in st.session_state:
        st.session_state.desired_project = ""
    if 'project_issues' not in st.session_state:
        st.session_state.project_issues = []
    # 'suitable_projects' has been removed.
    
    # --- "Check Rules" Tool State ---
    if 'check_project_rules' not in st.session_state:
        st.session_state.check_project_rules = "Select a project..." 

    # --- Form Input State ---
    # We define all form keys here with their defaults.
    # This is the "fix" for the reset bug.
    default_inputs = {
        'project_heading': "Untitled Site",
        'zoning_choice': zoning_list[0],
        'fsi_available': 1.0,
        'slope_pct': 5.0,
        'envelope_width': 50.0,
        'envelope_depth': 50.0,
        'vegetation_survey': 0,
        'spt_n_value': 15,
        'bearing_capacity_kpa': 150.0,
        'cbr_pct': 10.0,
        'plate_load_settlement_mm': 2.0,
        'proctor_compaction_pct': 95.0,
        'plasticity_index': 10,
        'ucs_kpa': 100.0,
        'soil_texture_choice': soil_texture_list[0],
        'cohesion_kpa': 10.0,
        'friction_angle_deg': 30.0,
        'permeability_cm_sec': 0.0001,
        'percent_fines': 20.0,
        'core_cutter_density': 1800.0,
        'soil_ph': 7.0,
        'groundwater_depth_ft': 20.0,
        'percolation_rate_min_inch': 30.0,
        'soil_resistivity_ohm_m': 50.0,
        'contaminant_choice': contaminant_list[0],
        'water_quality_choice': water_quality_list[0],
        'eia_choice': eia_list[0],
        'phase1_choice': phase1_list[0],
        'phase2_choice': phase2_list[0],
        'biodiversity_choice': biodiversity_list[0],
        'wetland_percentage': 0.0,
        'flood_choice': flood_list[0],
        'drainage_choice': drainage_list[0],
        'seismic_choice': seismic_list[0],
        'air_quality_aqi': 50,
        'noise_level_dba': 55.0,
        'hazardous_site_proximity_ft': 10000.0,
        'utility_choice': utility_list[0],
        'pop_density_per_sq_km': 1000,
        'traffic_choice': traffic_list[0],
        'desired_project_choice': project_list[0]
    }

    # Loop and set defaults ONLY if not already in session_state
    for key, value in default_inputs.items():
        if key not in st.session_state:
            st.session_state[key] = value