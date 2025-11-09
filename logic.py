import datetime
import json
from data import *

# --- 3. HELPER FUNCTIONS & ANALYSIS LOGIC ---
# This file stores all the functions that "do" things.

def get_key_from_score(options_dict, score):
    """Helper to find the text key (e.g., 'Stable') for a given score (e.g., 2)."""
    for key, data in options_dict.items():
        if data['score'] == score:
            return key
    return "Unknown"

def format_option(option_key, options_dict):
    """Helper function for formatting selectbox options"""
    return f"{option_key} ({options_dict[option_key]['desc']})"

def check_suitability(site_details, project_name):
    """
    Checks a single project against the site details.
    Returns a list of issues. If the list is empty, the project is suitable.
    """
    if project_name not in CONSTRUCTION_RULES:
        return ["Invalid project name selected."]
        
    rules = CONSTRUCTION_RULES[project_name]
    issues = []
    
    # --- Check Legal, Survey & Site ---
    if 'zoning_allowed' in rules and site_details['zoning'] not in rules['zoning_allowed']:
        issues.append(f"**Zoning Violation:** Site is '{site_details['zoning']}', but project requires one of `[{', '.join(rules['zoning_allowed'])}]`.")
    if 'min_fsi' in rules and site_details['fsi_available'] < rules['min_fsi']:
        issues.append(f"**FSI Violation:** Site FSI is `{site_details['fsi_available']}`, but project requires a minimum of `{rules['min_fsi']}`.")
    if 'min_envelope_width_ft' in rules and site_details['envelope_width'] < rules['min_envelope_width_ft']:
        issues.append(f"**Size Violation:** Site envelope width is `{site_details['envelope_width']}ft`, but project requires a minimum of `{rules['min_envelope_width_ft']}ft`.")
    if 'min_envelope_depth_ft' in rules and site_details['envelope_depth'] < rules['min_envelope_depth_ft']:
        issues.append(f"**Size Violation:** Site envelope depth is `{site_details['envelope_depth']}ft`, but project requires a minimum of `{rules['min_envelope_depth_ft']}ft`.")
    if 'max_slope_pct' in rules and site_details['slope_pct'] > rules['max_slope_pct']:
        issues.append(f"**Topography Violation:** Site slope is `{site_details['slope_pct']}%`, but project requires a maximum of `{rules['max_slope_pct']}%`.")
    if 'max_protected_trees_count' in rules and site_details['protected_trees_count'] > rules['max_protected_trees_count']:
        issues.append(f"**Vegetation Violation:** Site has `{site_details['protected_trees_count']}` protected trees, but project allows a maximum of `{rules['max_protected_trees_count']}`.")

    # --- Check Geotechnical (Soil Properties) ---
    if 'min_spt_n' in rules and site_details['spt_n'] < rules['min_spt_n']:
        issues.append(f"**SPT Violation:** Site SPT N-value is `{site_details['spt_n']}`, but project requires a minimum of `{rules['min_spt_n']}`.")
    if 'min_bearing_capacity_kpa' in rules and site_details['bearing_capacity'] < rules['min_bearing_capacity_kpa']:
        issues.append(f"**Bearing Capacity Violation:** Site capacity is `{site_details['bearing_capacity']} kPa`, but project requires a minimum of `{rules['min_bearing_capacity_kpa']} kPa`.")
    if 'min_cbr_pct' in rules and site_details['cbr_pct'] < rules['min_cbr_pct']:
        issues.append(f"**CBR Violation:** Site CBR is `{site_details['cbr_pct']}%`, but project requires a minimum of `{rules['min_cbr_pct']}%`.")
    if 'max_plate_load_settlement_mm' in rules and site_details['plate_load_settlement_mm'] > rules['max_plate_load_settlement_mm']:
        issues.append(f"**Plate Load Violation:** Site settlement is `{site_details['plate_load_settlement_mm']}mm`, but project allows a maximum of `{rules['max_plate_load_settlement_mm']}mm`.")
    if 'min_proctor_compaction_pct' in rules and site_details['proctor_compaction'] < rules['min_proctor_compaction_pct']:
        issues.append(f"**Compaction Violation:** Site compaction is `{site_details['proctor_compaction']}%`, but project requires a minimum of `{rules['min_proctor_compaction_pct']}%`.")
    if 'max_plasticity_index' in rules and site_details['plasticity_index'] > rules['max_plasticity_index']:
        issues.append(f"**Atterberg Violation:** Site Plasticity Index is `{site_details['plasticity_index']}`, but project requires a maximum of `{rules['max_plasticity_index']}` (less is better).")
    if 'min_ucs_kpa' in rules and site_details['ucs_kpa'] < rules['min_ucs_kpa']:
        issues.append(f"**UCS Violation:** Site UCS is `{site_details['ucs_kpa']} kPa`, but project requires a minimum of `{rules['min_ucs_kpa']} kPa`.")
    if 'min_soil_texture_score' in rules and site_details['soil_texture_score'] < rules['min_soil_texture_score']:
        req_texture = get_key_from_score(SOIL_TEXTURE_OPTIONS, rules['min_soil_texture_score'])
        issues.append(f"**Soil Texture Violation:** Site soil is '{site_details['soil_texture_key']}', but project requires at least '{req_texture}'.")
    if 'min_cohesion_kpa' in rules and site_details['cohesion_kpa'] < rules['min_cohesion_kpa']:
        issues.append(f"**Cohesion Violation:** Site cohesion is `{site_details['cohesion_kpa']} kPa`, but project requires a minimum of `{rules['min_cohesion_kpa']} kPa`.")
    if 'min_friction_angle_deg' in rules and site_details['friction_angle_deg'] < rules['min_friction_angle_deg']:
        issues.append(f"**Friction Angle Violation:** Site friction angle is `{site_details['friction_angle_deg']}°`, but project requires a minimum of `{rules['min_friction_angle_deg']}°`.")
    if ('min_soil_ph' in rules and site_details['soil_ph'] < rules['min_soil_ph']) or \
       ('max_soil_ph' in rules and site_details['soil_ph'] > rules['max_soil_ph']):
        issues.append(f"**Soil pH Violation:** Site pH is `{site_details['soil_ph']}`, but project requires it to be between `{rules['min_soil_ph']}` and `{rules['max_soil_ph']}`.")
    
    # --- Check Geotechnical (Water & Contaminants) ---
    if 'min_groundwater_depth_ft' in rules and site_details['groundwater_depth'] < rules['min_groundwater_depth_ft']:
        issues.append(f"**Groundwater Violation:** Water table is at `{site_details['groundwater_depth']} ft`, but project requires it to be deeper than `{rules['min_groundwater_depth_ft']} ft`.")
    if 'max_percolation_rate_min_inch' in rules and site_details['percolation_rate_min_inch'] > rules['max_percolation_rate_min_inch']:
        issues.append(f"**Percolation Violation:** Site percolation rate is `{site_details['percolation_rate_min_inch']} min/inch`, but project requires a maximum of `{rules['max_percolation_rate_min_inch']} min/inch` (faster is better).")
    if 'min_soil_resistivity_ohm_m' in rules and site_details['soil_resistivity_ohm_m'] < rules['min_soil_resistivity_ohm_m']:
        issues.append(f"**Resistivity Violation:** Site resistivity is `{site_details['soil_resistivity_ohm_m']} Ohm-m`, but project requires a minimum of `{rules['min_soil_resistivity_ohm_m']} Ohm-m` (higher is less corrosive).")
    if 'max_contaminant_score' in rules and site_details['contaminant_score'] > rules['max_contaminant_score']:
        req_contaminant = get_key_from_score(SOIL_CONTAMINANT_OPTIONS, rules['max_contaminant_score'])
        issues.append(f"**Contaminant Violation:** Site has '{site_details['contaminant_key']}' contaminants, but project allows a maximum of '{req_contaminant}'.")
    if 'max_water_quality_score' in rules and site_details['water_quality_score'] > rules['max_water_quality_score']:
        req_water = get_key_from_score(WATER_QUALITY_OPTIONS, rules['max_water_quality_score'])
        issues.append(f"**Water Quality Violation:** Site water is '{site_details['water_quality_key']}', but project allows a maximum of '{req_water}'.")

    # --- Check Environmental & Risk ---
    if 'min_eia_status_score' in rules and site_details['eia_score'] < rules['min_eia_status_score']:
        req_eia = get_key_from_score(EIA_STATUS_OPTIONS, rules['min_eia_status_score'])
        issues.append(f"**EIA Violation:** Site EIA status is '{site_details['eia_key']}', but project requires at least '{req_eia}'.")
    if 'min_phase1_score' in rules and site_details['phase1_score'] < rules['min_phase1_score']:
        req_phase1 = get_key_from_score(PHASE1_ESA_OPTIONS, rules['min_phase1_score'])
        issues.append(f"**Phase I ESA Violation:** Site status is '{site_details['phase1_key']}', but project requires at least '{req_phase1}'.")
    if 'min_phase2_score' in rules and site_details['phase2_score'] < rules['min_phase2_score']:
        req_phase2 = get_key_from_score(PHASE2_ESA_OPTIONS, rules['min_phase2_score'])
        issues.append(f"**Phase II ESA Violation:** Site status is '{site_details['phase2_key']}', but project requires at least '{req_phase2}'.")
    if 'max_biodiversity_impact_score' in rules and site_details['biodiversity_score'] > rules['max_biodiversity_impact_score']:
        req_bio = get_key_from_score(BIODIVERSITY_IMPACT_OPTIONS, rules['max_biodiversity_impact_score'])
        issues.append(f"**Biodiversity Violation:** Site impact is '{site_details['biodiversity_key']}', but project allows a maximum of '{req_bio}'.")
    if 'max_wetland_percentage' in rules and site_details['wetland_percentage'] > rules['max_wetland_percentage']:
        issues.append(f"**Wetland Violation:** Site is `{site_details['wetland_percentage']}%` wetland, but project allows a maximum of `{rules['max_wetland_percentage']}%`.")
    if 'max_flood_risk_score' in rules and site_details['flood_score'] > rules['max_flood_risk_score']:
        req_flood = get_key_from_score(FLOOD_RISK_OPTIONS, rules['max_flood_risk_score'])
        issues.append(f"**Flood Risk Violation:** Site is in '{site_details['flood_key']}', but project allows a maximum of '{req_flood}'.")
    if 'max_drainage_score' in rules and site_details['drainage_score'] > rules['max_drainage_score']:
        req_drainage = get_key_from_score(DRAINAGE_OPTIONS, rules['max_drainage_score'])
        issues.append(f"**Drainage Violation:** Site drainage is '{site_details['drainage_key']}', but project allows a maximum of '{req_drainage}'.")
    if 'max_seismic_zone_score' in rules and site_details['seismic_score'] > rules['max_seismic_zone_score']:
        req_seismic = get_key_from_score(SEISMIC_ZONE_OPTIONS, rules['max_seismic_zone_score'])
        issues.append(f"**Seismic Violation:** Site is in '{site_details['seismic_key']}', but project allows a maximum of '{req_seismic}'.")
    if 'max_air_quality_aqi' in rules and site_details['air_quality_aqi'] > rules['max_air_quality_aqi']:
        issues.append(f"**Air Quality Violation:** Local AQI is `{site_details['air_quality_aqi']}`, but project requires a maximum of `{rules['max_air_quality_aqi']}`.")
    if 'max_noise_level_dba' in rules and site_details['noise_level_dba'] > rules['max_noise_level_dba']:
        issues.append(f"**Noise Violation:** Average noise is `{site_details['noise_level_dba']} dBA`, but project requires a maximum of `{rules['max_noise_level_dba']} dBA`.")
    if 'min_hazardous_site_proximity_ft' in rules and site_details['hazardous_site_proximity_ft'] < rules['min_hazardous_site_proximity_ft']:
        issues.append(f"**Hazardous Site Violation:** Site is `{site_details['hazardous_site_proximity_ft']} ft` from a known hazard, but project requires a minimum of `{rules['min_hazardous_site_proximity_ft']} ft`.")

    # --- Check Infrastructure & Community ---
    if 'min_utility_level' in rules and site_details['utility_level'] < rules['min_utility_level']:
        required_utility = get_key_from_score(UTILITY_OPTIONS, rules['min_utility_level'])
        issues.append(f"**Utility Violation:** Project requires '{required_utility}', but site is '{site_details['utility_key']}'.")
    if ('max_pop_density_per_sq_km' in rules and site_details['pop_density_per_sq_km'] > rules['max_pop_density_per_sq_km']) or \
       ('min_pop_density_per_sq_km' in rules and site_details['pop_density_per_sq_km'] < rules['min_pop_density_per_sq_km']):
        issues.append(f"**Population Density Violation:** Site density is `{site_details['pop_density_per_sq_km']}/km²`, which is outside the project's allowed range.")
    if 'max_traffic_impact_score' in rules and site_details['traffic_score'] > rules['max_traffic_impact_score']:
        req_traffic = get_key_from_score(TRAFFIC_IMPACT_OPTIONS, rules['max_traffic_impact_score'])
        issues.append(f"**Traffic Violation:** Site traffic impact is '{site_details['traffic_key']}', but project allows a maximum of '{req_traffic}'.")

    return issues

def generate_report_text(site_details, desired_project, project_issues):
    """
    Generates a text string for the download button.
    (Removed suitable_projects)
    """
    today = datetime.date.today().isoformat()
    report = f"CONSTRUCTION SUITABILITY ANALYSIS REPORT\n"
    report += f"Report Date: {today}\n"
    report += f"Project Site: {site_details.get('project_heading', 'N/A')}\n"
    report += f"=========================================\n\n"
    
    report += f"--- ANALYSIS FOR: {desired_project} ---\n"
    
    if not project_issues:
        report += f"SUCCESS: Your project '{desired_project}' is suitable for this site!\n\n"
    else:
        report += f"FAILURE: Your project '{desired_project}' is NOT suitable for this site.\n"
        report += "Issues Found:\n"
        for issue in project_issues:
            report += f"- {issue.replace('**', '')}\n" # Remove markdown
        report += "\n"

    # "Other Suitable Projects" section has been removed.
            
    report += f"=========================================\n"
    report += "--- SITE DETAILS SUMMARY ---\n"
    
    report += f"\nLegal, Survey & Site:\n"
    report += f"- Zoning: {site_details['zoning']} ({ZONING_OPTIONS[site_details['zoning']]['desc']})\n"
    report += f"- Slope: {site_details['slope_pct']}%\n"
    report += f"- FSI: {site_details['fsi_available']}\n"
    report += f"- Envelope: {site_details['envelope_width']} ft (Width) x {site_details['envelope_depth']} ft (Depth)\n"
    report += f"- Protected Trees: {site_details['protected_trees_count']}\n"

    report += f"\nGeotechnical (Soil Properties):\n"
    report += f"- SPT N-value: {site_details['spt_n']}\n"
    report += f"- Bearing Capacity: {site_details['bearing_capacity']} kPa\n"
    report += f"- CBR: {site_details['cbr_pct']}%\n"
    report += f"- Plate Load Settlement: {site_details['plate_load_settlement_mm']} mm\n"
    report += f"- Proctor Compaction: {site_details['proctor_compaction']}%\n"
    report += f"- Plasticity Index: {site_details['plasticity_index']}\n"
    report += f"- UCS: {site_details['ucs_kpa']} kPa\n"
    report += f"- Soil Texture: {site_details['soil_texture_key']} ({SOIL_TEXTURE_OPTIONS[site_details['soil_texture_key']]['desc']})\n"
    report += f"- Cohesion: {site_details['cohesion_kpa']} kPa\n"
    report += f"- Friction Angle: {site_details['friction_angle_deg']}°\n"
    report += f"- Permeability: {site_details['permeability_cm_sec']} cm/sec\n"
    report += f"- Percent Fines: {site_details['percent_fines']}%\n"
    report += f"- Dry Density: {site_details['core_cutter_density']} kg/m³\n"
    report += f"- Soil pH: {site_details['soil_ph']}\n"

    report += f"\nGeotechnical (Water & Contaminants):\n"
    report += f"- Groundwater Depth: {site_details['groundwater_depth']} ft\n"
    report += f"- Percolation Rate: {site_details['percolation_rate_min_inch']} min/inch\n"
    report += f"- Soil Resistivity: {site_details['soil_resistivity_ohm_m']} Ohm-m\n"
    report += f"- Contaminants: {site_details['contaminant_key']} ({SOIL_CONTAMINANT_OPTIONS[site_details['contaminant_key']]['desc']})\n"
    report += f"- Water Quality: {site_details['water_quality_key']} ({WATER_QUALITY_OPTIONS[site_details['water_quality_key']]['desc']})\n"
    
    report += f"\nEnvironmental & Risk:\n"
    report += f"- EIA: {site_details['eia_key']} ({EIA_STATUS_OPTIONS[site_details['eia_key']]['desc']})\n"
    report += f"- Phase I ESA: {site_details['phase1_key']} ({PHASE1_ESA_OPTIONS[site_details['phase1_key']]['desc']})\n"
    report += f"- Phase II ESA: {site_details['phase2_key']} ({PHASE2_ESA_OPTIONS[site_details['phase2_key']]['desc']})\n"
    report += f"- Biodiversity Impact: {site_details['biodiversity_key']} ({BIODIVERSITY_IMPACT_OPTIONS[site_details['biodiversity_key']]['desc']})\n"
    report += f"- Wetland %: {site_details['wetland_percentage']}%\n"
    report += f"- Flood Risk: {site_details['flood_key']} ({FLOOD_RISK_OPTIONS[site_details['flood_key']]['desc']})\n"
    report += f"- Drainage: {site_details['drainage_key']} ({DRAINAGE_OPTIONS[site_details['drainage_key']]['desc']})\n"
    report += f"- Seismic: {site_details['seismic_key']} ({SEISMIC_ZONE_OPTIONS[site_details['seismic_key']]['desc']})\n"
    report += f"- Air Quality (AQI): {site_details['air_quality_aqi']}\n"
    report += f"- Noise Level (dBA): {site_details['noise_level_dba']}\n"
    report += f"- Hazardous Site Proximity: {site_details['hazardous_site_proximity_ft']} ft\n"
    
    report += f"\nInfrastructure & Community:\n"
    report += f"- Utilities: {site_details['utility_key']} ({UTILITY_OPTIONS[site_details['utility_key']]['desc']})\n"
    report += f"- Population Density: {site_details['pop_density_per_sq_km']} people/km²\n"
    report += f"- Traffic Impact: {site_details['traffic_key']} ({TRAFFIC_IMPACT_OPTIONS[site_details['traffic_key']]['desc']})\n\n"
    
    return report

def format_rules_for_display(project_name):
    """
    Takes a project name and formats its rules from CONSTRUCTION_RULES 
    into a cleaner dictionary for st.json display.
    """
    if project_name not in CONSTRUCTION_RULES:
        return {"Error": "Project not found."}
    
    rules = CONSTRUCTION_RULES[project_name]
    formatted = {
        "Project": project_name,
        "Legal & Survey": {
            "Zoning Allowed": rules.get('zoning_allowed', 'N/A'),
            "Min FSI": rules.get('min_fsi', 'N/A'),
            "Min Envelope (W x D)": f"{rules.get('min_envelope_width_ft', 'N/A')} ft x {rules.get('min_envelope_depth_ft', 'N/A')} ft",
            "Max Slope": f"{rules.get('max_slope_pct', 'N/A')}%",
            "Max Protected Trees": rules.get('max_protected_trees_count', 'N/A')
        },
        "Geotechnical (Soil)": {
            "Min SPT N-Value": rules.get('min_spt_n', 'N/A'),
            "Min Bearing Capacity": f"{rules.get('min_bearing_capacity_kpa', 'N/A')} kPa",
            "Min CBR": f"{rules.get('min_cbr_pct', 'N/A')}%",
            "Max Plate Load Settlement": f"{rules.get('max_plate_load_settlement_mm', 'N/A')} mm",
            "Min Proctor Compaction": f"{rules.get('min_proctor_compaction_pct', 'N/A')}%",
            "Max Plasticity Index": rules.get('max_plasticity_index', 'N/A'),
            "Min UCS": f"{rules.get('min_ucs_kpa', 'N/A')} kPa",
            "Min Soil Texture": f"Score {rules.get('min_soil_texture_score', 'N/A')}",
            "Min Cohesion": f"{rules.get('min_cohesion_kpa', 'N/A')} kPa",
            "Min Friction Angle": f"{rules.get('min_friction_angle_deg', 'N/A')}°",
            "Soil pH Range": f"{rules.get('min_soil_ph', 'N/A')} - {rules.get('max_soil_ph', 'N/A')}"
        },
        "Geotechnical (Water)": {
            "Min Groundwater Depth": f"{rules.get('min_groundwater_depth_ft', 'N/L/A')} ft",
            "Max Percolation Rate": f"{rules.get('max_percolation_rate_min_inch', 'N/A')} min/inch",
            "Min Soil Resistivity": f"{rules.get('min_soil_resistivity_ohm_m', 'N/A')} Ohm-m",
            "Max Contaminant Level": f"Score {rules.get('max_contaminant_score', 'N/A')}",
            "Max Water Aggressiveness": f"Score {rules.get('max_water_quality_score', 'N/A')}"
        },
        "Environmental & Risk": {
            "Min EIA Status": f"Score {rules.get('min_eia_status_score', 'N/A')}",
            "Min Phase I ESA": f"Score {rules.get('min_phase1_score', 'N/A')}",
            "Min Phase II ESA": f"Score {rules.get('min_phase2_score', 'N/A')}",
            "Max Biodiversity Impact": f"Score {rules.get('max_biodiversity_impact_score', 'N/A')}",
            "Max Wetland %": f"{rules.get('max_wetland_percentage', 'N/A')}%",
            "Max Flood Risk": f"Score {rules.get('max_flood_risk_score', 'N/A')}",
            "Max Drainage Issues": f"Score {rules.get('max_drainage_score', 'N/A')}",
            "Max Seismic Zone": f"Score {rules.get('max_seismic_zone_score', 'N/A')}",
            "Max Air Quality (AQI)": rules.get('max_air_quality_aqi', 'N/A'),
            "Max Noise Level (dBA)": rules.get('max_noise_level_dba', 'N/A'),
            "Min Hazard Proximity": f"{rules.get('min_hazardous_site_proximity_ft', 'N/A')} ft"
        },
        "Infrastructure & Community": {
            "Min Utility Level": f"Score {rules.get('min_utility_level', 'N/A')}",
            "Population Density": f"{rules.get('min_pop_density_per_sq_km', 'N/A')} - {rules.get('max_pop_density_per_sq_km', 'N/A')}",
            "Max Traffic Impact": f"Score {rules.get('max_traffic_impact_score', 'N/A')}"
        }
    }
    # Clean up 'N/A - N/A' or 'N/A' scores
    formatted["Infrastructure & Community"]["Population Density"] = formatted["Infrastructure & Community"]["Population Density"].replace('N/A - N/A', 'N/A')
    return formatted

def generate_rules_text(project_name):
    """
    Generates a simple text file string for downloading a project's rules.
    """
    rules_dict = format_rules_for_display(project_name)
    report = f"MINIMUM REQUIREMENTS FOR: {project_name}\n"
    report += f"=========================================\n\n"
    
    # Use json.dumps for a clean, indented text representation
    report += json.dumps(rules_dict, indent=2)
    
    return report