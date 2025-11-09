# --- 1. DATA DICTIONARIES (The "Indexes") ---
# This file stores all data structures (options and rules).

# --- Legal, Survey & Site ---
ZONING_OPTIONS = {
    'R-1': {'desc': 'Single-Family Residential'},
    'R-M': {'desc': 'Multi-Family Residential'},
    'C-1': {'desc': 'Commercial (Offices, Retail)'},
    'I-1': {'desc': 'Industrial (Warehouses, Manufacturing)'},
    'AG':  {'desc': 'Agricultural (Farms, Barns)'}
}

# --- Geotechnical (Soil Properties) ---
SOIL_TEXTURE_OPTIONS = {
    'GW/GP/SW/SP': {'score': 3, 'desc': 'Gravel/Sand (Excellent)'},
    'GM/GC/SM/SC': {'score': 2, 'desc': 'Silty/Clayey Gravels/Sands (Good)'},
    'ML/CL': {'score': 1, 'desc': 'Silt/Low-Plasticity Clay (Fair to Poor)'},
    'MH/CH/OL/OH/Pt': {'score': 0, 'desc': 'High-Plasticity Silt/Clay, Organic, Peat (Very Poor)'}
}

# --- Geotechnical (Water & Contaminants) ---
SOIL_CONTAMINANT_OPTIONS = {
    'None': {'score': 0, 'desc': 'No harmful contaminants found.'},
    'Low': {'score': 1, 'desc': 'Low levels, requires minor soil remediation.'},
    'High': {'score': 2, 'desc': 'High levels, requires significant remediation.'}
}
WATER_QUALITY_OPTIONS = {
    'Good': {'score': 0, 'desc': 'Low sulfates/chlorides. Not aggressive.'},
    'Aggressive': {'score': 1, 'desc': 'High sulfates/chlorides. Requires special concrete.'},
    'Contaminated': {'score': 2, 'desc': 'Biologically or chemically contaminated.'}
}

# --- Environmental & Risk ---
EIA_STATUS_OPTIONS = {
    'Pass': {'score': 2, 'desc': 'EIA Passed, no issues.'},
    'Pass w/ Mitigation': {'score': 1, 'desc': 'EIA Passed, but requires mitigation.'},
    'Fail': {'score': 0, 'desc': 'EIA Failed, construction not advised.'},
    'Not Required': {'score': 3, 'desc': 'Project scale does not require an EIA.'}
}
PHASE1_ESA_OPTIONS = {
    'Pass': {'score': 2, 'desc': 'No Recognized Environmental Conditions (RECs).'},
    'RECs Identified': {'score': 1, 'desc': 'RECs identified, Phase II recommended.'},
    'Fail': {'score': 0, 'desc': 'Significant contamination obvious.'}
}
PHASE2_ESA_OPTIONS = {
    'Pass': {'score': 3, 'desc': 'No contamination found.'},
    'Remediation Req': {'score': 1, 'desc': 'Contamination found, remediation required.'},
    'Monitoring Req': {'score': 2, 'desc': 'Low levels found, monitoring required.'},
    'Fail': {'score': 0, 'desc': 'Site unviable due to contamination.'},
    'N/A': {'score': 4, 'desc': 'Phase II was not required.'}
}
BIODIVERSITY_IMPACT_OPTIONS = {
    'Low': {'score': 0, 'desc': 'Negligible impact on local flora/fauna.'},
    'Medium': {'score': 1, 'desc': 'Some impact, requires mitigation/offsets.'},
    'High': {'score': 2, 'desc': 'Significant impact on protected species/habitat.'}
}
FLOOD_RISK_OPTIONS = {
    'Zone X (Low)': {'score': 0, 'desc': 'Low risk. (0.2% annual chance)'},
    'Zone A (High)': {'score': 1, 'desc': 'High risk, no base elevation. (1% annual chance)'},
    'Zone AE (High)': {'score': 2, 'desc': 'High risk, with base elevation. (1% annual chance)'},
    'Zone V (Coastal)': {'score': 3, 'desc': 'High risk coastal, storm surge.'}
}
DRAINAGE_OPTIONS = {
    'Good': {'score': 0, 'desc': 'Well-drained, minimal surface water pooling.'},
    'Average': {'score': 1, 'desc': 'Some pooling, requires standard grading/drainage.'},
    'Poor': {'score': 2, 'desc': 'Poorly drained, high water table, requires significant engineering.'}
}
SEISMIC_ZONE_OPTIONS = {
    'Zone I (Low)': {'score': 1, 'desc': 'Low risk'},
    'Zone II (Low-Mod)': {'score': 2, 'desc': 'Low-Moderate risk'},
    'Zone III (Moderate)': {'score': 3, 'desc': 'Moderate risk'},
    'Zone IV (High)': {'score': 4, 'desc': 'High risk'},
    'Zone V (Very High)': {'score': 5, 'desc': 'Very High risk (severe)'}
}

# --- Infrastructure & Community ---
UTILITY_OPTIONS = {
    'Full':    {'score': 2, 'desc': 'Connected to city water, sewer, and power.'},
    'Partial': {'score': 1, 'desc': 'e.g., Water/power available, but needs a septic system.'},
    'None':    {'score': 0, 'desc': 'Off-grid. No main utilities available.'}
}
TRAFFIC_IMPACT_OPTIONS = {
    'Low': {'score': 0, 'desc': 'Minimal impact on local roads.'},
    'Medium': {'score': 1, 'desc': 'Requires local road upgrades or traffic signals.'},
    'High': {'score': 2, 'desc': 'Requires major road infrastructure changes.'}
}


# --- 2. RULES DATABASE (Significantly expanded) ---

CONSTRUCTION_RULES = {
    'Single-Family Home': {
        # Legal & Survey
        'zoning_allowed': ['R-1', 'R-M'],
        'min_fsi': 0.4,
        'min_envelope_width_ft': 30,
        'min_envelope_depth_ft': 30,
        'max_slope_pct': 20,
        'max_protected_trees_count': 10,
        # Geotechnical (Soil)
        'min_spt_n': 10,
        'min_bearing_capacity_kpa': 100,
        'min_cbr_pct': 5,
        'max_plate_load_settlement_mm': 25,
        'min_proctor_compaction_pct': 90,
        'max_plasticity_index': 25,
        'min_ucs_kpa': 75,
        'min_soil_texture_score': 1, # Allows 'Fair to Poor'
        'min_cohesion_kpa': 5,
        'min_friction_angle_deg': 25,
        'min_soil_ph': 5.5,
        'max_soil_ph': 8.5,
        # Geotechnical (Water & Contaminants)
        'min_groundwater_depth_ft': 8,
        'max_percolation_rate_min_inch': 60, # 1-60 min/inch is acceptable for septic
        'min_soil_resistivity_ohm_m': 20, # < 20 is highly corrosive
        'max_contaminant_score': 1, # Can handle 'Low'
        'max_water_quality_score': 1, # Can't be 'Contaminated'
        # Environmental & Risk
        'min_eia_status_score': 1, # Must pass (or pass w/ mitigation)
        'min_phase1_score': 1, # Must at least review RECs
        'min_phase2_score': 1, # Can handle remediation
        'max_biodiversity_impact_score': 1, # 'Low' or 'Medium'
        'max_wetland_percentage': 5,
        'max_flood_risk_score': 2, # Can't be in Zone V (Coastal)
        'max_drainage_score': 1, # Can't be 'Poor'
        'max_seismic_zone_score': 5, # Can be built in any zone with engineering
        'max_air_quality_aqi': 150,
        'max_noise_level_dba': 70, # Can build with sound insulation
        'min_hazardous_site_proximity_ft': 500, # Not too close
        # Infrastructure
        'min_utility_level': 1, # Requires at least 'Partial'
        'max_pop_density_per_sq_km': 10000,
        'max_traffic_impact_score': 0, # Should have 'Low' impact
    },
    
    'Apartment Complex (Multi-Family)': {
        # Legal & Survey
        'zoning_allowed': ['R-M', 'C-1'],
        'min_fsi': 1.5,
        'min_envelope_width_ft': 100,
        'min_envelope_depth_ft': 100,
        'max_slope_pct': 10,
        'max_protected_trees_count': 5,
        # Geotechnical (Soil)
        'min_spt_n': 20,
        'min_bearing_capacity_kpa': 200,
        'min_cbr_pct': 10,
        'max_plate_load_settlement_mm': 20,
        'min_proctor_compaction_pct': 95,
        'max_plasticity_index': 15,
        'min_ucs_kpa': 150,
        'min_soil_texture_score': 2, # Requires 'Good'
        'min_cohesion_kpa': 20,
        'min_friction_angle_deg': 30,
        'min_soil_ph': 6.0,
        'max_soil_ph': 8.0,
        # Geotechnical (Water & Contaminants)
        'min_groundwater_depth_ft': 15, # For basements/parking
        'max_percolation_rate_min_inch': 999, # N/A, must use city sewer
        'min_soil_resistivity_ohm_m': 30,
        'max_contaminant_score': 0, # Must be 'None'
        'max_water_quality_score': 0, # Must be 'Good'
        # Environmental & Risk
        'min_eia_status_score': 2, # Must pass cleanly
        'min_phase1_score': 2, # Must 'Pass'
        'min_phase2_score': 3, # Must 'Pass' or 'N/A'
        'max_biodiversity_impact_score': 0, # 'Low' only
        'max_wetland_percentage': 0,
        'max_flood_risk_score': 1, # Must be outside 1% flood plain
        'max_drainage_score': 0, # Must be 'Good'
        'max_seismic_zone_score': 4, # Becomes very costly in Zone V
        'max_air_quality_aqi': 100,
        'max_noise_level_dba': 60, # Residential comfort
        'min_hazardous_site_proximity_ft': 2000,
        # Infrastructure
        'min_utility_level': 2, # Must have 'Full' utilities
        'min_pop_density_per_sq_km': 1000,
        'max_traffic_impact_score': 1, # 'Medium' is max
    },
    
    'Warehouse (Industrial)': {
        # Legal & Survey
        'zoning_allowed': ['I-1'],
        'min_fsi': 0.8,
        'min_envelope_width_ft': 150,
        'min_envelope_depth_ft': 200,
        'max_slope_pct': 10,
        'max_protected_trees_count': 20, # Less sensitive
        # Geotechnical (Soil)
        'min_spt_n': 15,
        'min_bearing_capacity_kpa': 150,
        'min_cbr_pct': 15, # Needs good subgrade for slabs/trucks
        'max_plate_load_settlement_mm': 30,
        'min_proctor_compaction_pct': 92,
        'max_plasticity_index': 30,
        'min_ucs_kpa': 100,
        'min_soil_texture_score': 1,
        'min_cohesion_kpa': 0, # Can be built on granular
        'min_friction_angle_deg': 28,
        'min_soil_ph': 5.0,
        'max_soil_ph': 9.0, # Wider range
        # Geotechnical (Water & Contaminants)
        'min_groundwater_depth_ft': 5, # Often built on slabs, less sensitive
        'max_percolation_rate_min_inch': 999, # N/A
        'min_soil_resistivity_ohm_m': 10, # Can engineer for it
        'max_contaminant_score': 1, # Can often be built on remediated land
        'max_water_quality_score': 1,
        # Environmental & Risk
        'min_eia_status_score': 1,
        'min_phase1_score': 1,
        'min_phase2_score': 1, # Can be built on remediated site
        'max_biodiversity_impact_score': 1,
        'max_wetland_percentage': 10,
        'max_flood_risk_score': 2,
        'max_drainage_score': 2, # Can engineer drainage
        'max_seismic_zone_score': 5,
        'max_air_quality_aqi': 999, # N/A (often in industrial zones)
        'max_noise_level_dba': 999, # N/A
        'min_hazardous_site_proximity_ft': 0, # Can BE the hazardous site
        # Infrastructure
        'min_utility_level': 1, # Needs power/water, maybe not sewer
        'max_traffic_impact_score': 2, # Will have high traffic
    },
    
    'Small Office Building': {
        # Legal & Survey
        'zoning_allowed': ['C-1'],
        'min_fsi': 1.0,
        'min_envelope_width_ft': 50,
        'min_envelope_depth_ft': 50,
        'max_slope_pct': 15,
        'max_protected_trees_count': 10,
        # Geotechnical (Soil)
        'min_spt_n': 15,
        'min_bearing_capacity_kpa': 150,
        'min_cbr_pct': 8,
        'max_plate_load_settlement_mm': 25,
        'min_proctor_compaction_pct': 95,
        'max_plasticity_index': 20,
        'min_ucs_kpa': 120,
        'min_soil_texture_score': 2,
        'min_cohesion_kpa': 10,
        'min_friction_angle_deg': 28,
        'min_soil_ph': 6.0,
        'max_soil_ph': 8.0,
        # Geotechnical (Water & Contaminants)
        'min_groundwater_depth_ft': 10,
        'max_percolation_rate_min_inch': 999, # N/A
        'min_soil_resistivity_ohm_m': 30,
        'max_contaminant_score': 0,
        'max_water_quality_score': 0,
        # Environmental & Risk
        'min_eia_status_score': 1,
        'min_phase1_score': 2,
        'min_phase2_score': 3,
        'max_biodiversity_impact_score': 1,
        'max_wetland_percentage': 0,
        'max_flood_risk_score': 2,
        'max_drainage_score': 1,
        'max_seismic_zone_score': 4,
        'max_air_quality_aqi': 100,
        'max_noise_level_dba': 70, # Office environment
        'min_hazardous_site_proximity_ft': 1500,
        # Infrastructure
        'min_utility_level': 2,
        'min_pop_density_per_sq_km': 500,
        'max_traffic_impact_score': 1,
    },

    'Farm Barn': {
        # Legal & Survey
        'zoning_allowed': ['AG'],
        'min_fsi': 0.2,
        'min_envelope_width_ft': 40,
        'min_envelope_depth_ft': 60,
        'max_slope_pct': 25,
        'max_protected_trees_count': 50, # N/A
        # Geotechnical (Soil)
        'min_spt_n': 5,
        'min_bearing_capacity_kpa': 50,
        'min_cbr_pct': 3,
        'max_plate_load_settlement_mm': 50,
        'min_proctor_compaction_pct': 85,
        'max_plasticity_index': 40,
        'min_ucs_kpa': 25,
        'min_soil_texture_score': 0, # Can build on anything
        'min_cohesion_kpa': 0,
        'min_friction_angle_deg': 20,
        'min_soil_ph': 4.5,
        'max_soil_ph': 9.0,
        # Geotechnical (Water & Contaminants)
        'min_groundwater_depth_ft': 3,
        'max_percolation_rate_min_inch': 120,
        'min_soil_resistivity_ohm_m': 5, # N/A
        'max_contaminant_score': 1,
        'max_water_quality_score': 1,
        # Environmental & Risk
        'min_eia_status_score': 3, # 'Not Required' is typical
        'min_phase1_score': 1,
        'min_phase2_score': 2,
        'max_biodiversity_impact_score': 2,
        'max_wetland_percentage': 20,
        'max_flood_risk_score': 2,
        'max_drainage_score': 2,
        'max_seismic_zone_score': 5,
        'max_air_quality_aqi': 999, # N/A
        'max_noise_level_dba': 999, # N/A
        'min_hazardous_site_proximity_ft': 0, # Farms use chemicals
        # Infrastructure
        'min_utility_level': 0, # Often 'None'
        'max_traffic_impact_score': 0,
    }
}