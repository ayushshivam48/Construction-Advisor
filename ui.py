import streamlit as st
import datetime
from data import *
from logic import *

def render_input_tab():
    """
    Renders all the Streamlit widgets for the input form.
    """

    # --- Get Lists for Dropdowns ---
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

    st.header("Enter Your Site's Details")
    st.markdown("Fill out the details from your site reports below. The form is organized into sections.")

    with st.form(key="site_details_form"):

        # --- Section 0: Report Heading ---
        st.subheader("Report Details")
        # Use `key` to link to st.session_state and maintain value
        st.text_input(
            "Site Name or Address (for Report Heading)",
            key="project_heading" # Links to st.session_state.project_heading
        )
        st.divider()

        # --- Section 1: Legal, Survey & Site ---
        with st.expander("1. Legal, Survey & Site", expanded=True):
            col1_form, col2_form = st.columns(2)
            with col1_form:
                st.selectbox(
                    "Land Use and Zoning Verification",
                    zoning_list,
                    index=zoning_list.index(st.session_state.zoning_choice), # Set index from state
                    format_func=lambda x: format_option(x, ZONING_OPTIONS),
                    key="zoning_choice" # Link to st.session_state.zoning_choice
                )
                st.number_input(
                    "Available Floor Space Index (FSI)",
                    min_value=0.0, step=0.1,
                    key="fsi_available" # Link to st.session_state.fsi_available
                )
                st.number_input(
                    "Topographical Survey (Average Slope %)",
                    min_value=0.0, step=0.5,
                    help="The average slope of the buildable area. 10% is 10ft of drop over 100ft.",
                    key="slope_pct"
                )
            with col2_form:
                st.number_input(
                    "Available Building Envelope WIDTH (ft) (after setbacks)",
                    min_value=0.0, step=1.0,
                    key="envelope_width"
                )
                st.number_input(
                    "Available Building Envelope DEPTH (ft) (after setbacks)",
                    min_value=0.0, step=1.0,
                    key="envelope_depth"
                )
                st.number_input(
                    "Vegetation and Tree Survey (Protected Trees Count)",
                    min_value=0, step=1,
                    key="vegetation_survey"
                )

        # --- Section 2: Geotechnical (Soil Properties) ---
        with st.expander("2. Geotechnical (Soil Properties)", expanded=False):
            col1_form, col2_form = st.columns(2)
            with col1_form:
                st.number_input(
                    "Standard Penetration Test (SPT N-value)",
                    min_value=0, step=1,
                    help="Average N-value from soil borings. Represents soil strength.",
                    key="spt_n_value"
                )
                st.number_input(
                    "Soil Bearing Capacity Test (kPa)",
                    min_value=0.0, step=10.0,
                    help="KiloPascals (kPa). 100 kPa ≈ 10.2 tons/m²",
                    key="bearing_capacity_kpa"
                )
                st.number_input(
                    "California Bearing Ratio (CBR) Test (%)",
                    min_value=0.0, step=1.0,
                    help="Strength of subgrade, crucial for roads/foundations.",
                    key="cbr_pct"
                )
                st.number_input(
                    "Plate Load Test (Settlement in mm @ 100kPa)",
                    min_value=0.0, step=0.1,
                    help="Enter settlement in mm. Lower is better.",
                    key="plate_load_settlement_mm"
                )
                st.number_input(
                    "Proctor Compaction Test (%)",
                    min_value=0.0, max_value=200.0, step=1.0,
                    help="Optimal compaction percentage for the soil/fill.",
                    key="proctor_compaction_pct"
                )
                st.number_input(
                    "Atterberg Limits Test (Plasticity Index, PI)",
                    min_value=0, step=1,
                    help="A high PI (e.g., > 25) indicates expansive clay.",
                    key="plasticity_index"
                )
                st.number_input(
                    "Unconfined Compression Test (UCS) (kPa)",
                    min_value=0.0, step=10.0,
                    help="Strength of cohesive soil (clay).",
                    key="ucs_kpa"
                )
            with col2_form:
                st.selectbox(
                    "Soil Texture and Classification",
                    soil_texture_list,
                    index=soil_texture_list.index(st.session_state.soil_texture_choice),
                    format_func=lambda x: format_option(x, SOIL_TEXTURE_OPTIONS),
                    key="soil_texture_choice"
                )
                st.number_input(
                    "Triaxial Shear Test (Cohesion in kPa)",
                    min_value=0.0, step=1.0,
                    key="cohesion_kpa"
                )
                st.number_input(
                    "Direct Shear Test (Friction Angle in °)",
                    min_value=0.0, step=1.0,
                    key="friction_angle_deg"
                )
                st.number_input(
                    "Permeability Test (cm/sec)",
                    step=0.00001, format="%.6f",
                    help="e.g., Clay is 1.0E-7, Sand is 1.0E-3",
                    key="permeability_cm_sec"
                )
                st.number_input(
                    "Grain Size Distribution (% Fines)",
                    min_value=0.0, max_value=100.0, step=1.0,
                    help="Percent of soil passing 0.075mm sieve (silt/clay).",
                    key="percent_fines"
                )
                st.number_input(
                    "Core Cutter Test (Dry Density kg/m³)",
                    min_value=0.0, step=50.0,
                    key="core_cutter_density"
                )
                st.number_input(
                    "Soil pH Test",
                    min_value=0.0, max_value=14.0, step=0.1,
                    help="Very high or low pH can corrode foundations.",
                    key="soil_ph"
                )

        # --- Section 3: Geotechnical (Water & Contaminants) ---
        with st.expander("3. Geotechnical (Water & Contaminants)", expanded=False):
            col1_form, col2_form = st.columns(2)
            with col1_form:
                st.number_input(
                    "Groundwater Table Test (Depth in ft)",
                    min_value=0.0, step=1.0,
                    help="Depth from surface to the water table (in feet).",
                    key="groundwater_depth_ft"
                )
                st.number_input(
                    "Soil Percolation Test (min/inch)",
                    min_value=0.0, step=1.0,
                    help="Time for water to drop 1 inch. Crucial for septic.",
                    key="percolation_rate_min_inch"
                )
                st.number_input(
                    "Soil Resistivity Test (Ohm-m)",
                    min_value=0.0, step=5.0,
                    help="Low resistivity (< 20) indicates high corrosivity.",
                    key="soil_resistivity_ohm_m"
                )
            with col2_form:
                st.selectbox(
                    "Chemical Analysis of Soil",
                    contaminant_list,
                    index=contaminant_list.index(st.session_state.contaminant_choice),
                    format_func=lambda x: format_option(x, SOIL_CONTAMINANT_OPTIONS),
                    key="contaminant_choice"
                )
                st.selectbox(
                    "Water Quality Test (for foundation)",
                    water_quality_list,
                    index=water_quality_list.index(st.session_state.water_quality_choice),
                    format_func=lambda x: format_option(x, WATER_QUALITY_OPTIONS),
                    key="water_quality_choice"
                )

        # --- Section 4: Environmental & Risk ---
        with st.expander("4. Environmental & Risk", expanded=False):
            col1_form, col2_form = st.columns(2)
            with col1_form:
                st.selectbox(
                    "Environmental Impact Assessment (EIA)",
                    eia_list,
                    index=eia_list.index(st.session_state.eia_choice),
                    format_func=lambda x: format_option(x, EIA_STATUS_OPTIONS),
                    key="eia_choice"
                )
                st.selectbox(
                    "Phase I Environmental Site Assessment",
                    phase1_list,
                    index=phase1_list.index(st.session_state.phase1_choice),
                    format_func=lambda x: format_option(x, PHASE1_ESA_OPTIONS),
                    key="phase1_choice"
                )
                st.selectbox(
                    "Phase II Environmental Site Assessment",
                    phase2_list,
                    index=phase2_list.index(st.session_state.phase2_choice),
                    format_func=lambda x: format_option(x, PHASE2_ESA_OPTIONS),
                    key="phase2_choice"
                )
                st.selectbox(
                    "Biodiversity Impact Assessment",
                    biodiversity_list,
                    index=biodiversity_list.index(st.session_state.biodiversity_choice),
                    format_func=lambda x: format_option(x, BIODIVERSITY_IMPACT_OPTIONS),
                    key="biodiversity_choice"
                )
                st.number_input(
                    "Wetland Delineation (% of site)",
                    min_value=0.0, max_value=100.0, step=1.0,
                    key="wetland_percentage"
                )
            with col2_form:
                st.selectbox(
                    "Flood Risk Assessment",
                    flood_list,
                    index=flood_list.index(st.session_state.flood_choice),
                    format_func=lambda x: format_option(x, FLOOD_RISK_OPTIONS),
                    key="flood_choice"
                )
                st.selectbox(
                    "Drainage Pattern Analysis",
                    drainage_list,
                    index=drainage_list.index(st.session_state.drainage_choice),
                    format_func=lambda x: format_option(x, DRAINAGE_OPTIONS),
                    key="drainage_choice"
                )
                st.selectbox(
                    "Seismic Hazard Assessment",
                    seismic_list,
                    index=seismic_list.index(st.session_state.seismic_choice),
                    format_func=lambda x: format_option(x, SEISMIC_ZONE_OPTIONS),
                    key="seismic_choice"
                )
                st.number_input(
                    "Air Quality Test (Local AQI)",
                    min_value=0, step=5,
                    key="air_quality_aqi"
                )
                st.number_input(
                    "Noise Level Survey (Avg dBA)",
                    min_value=0.0, step=1.0,
                    help="e.g., 50 is quiet suburb, 70 is busy traffic.",
                    key="noise_level_dba"
                )
                st.number_input(
                    "Hazardous Waste Site Screening (Proximity in ft)",
                    min_value=0.0, step=100.0,
                    help="Distance to nearest known site. 0 if on-site.",
                    key="hazardous_site_proximity_ft"
                )

        # --- Section 5: Infrastructure & Community ---
        with st.expander("5. Infrastructure & Community", expanded=False):
            col1_form, col2_form = st.columns(2)
            with col1_form:
                st.selectbox(
                    "Utility Availability",
                    utility_list,
                    index=utility_list.index(st.session_state.utility_choice),
                    format_func=lambda x: format_option(x, UTILITY_OPTIONS),
                    key="utility_choice"
                )
                st.number_input(
                    "Population Density Survey (people/km²)",
                    min_value=0, step=100,
                    key="pop_density_per_sq_km"
                )
            with col2_form:
                st.selectbox(
                    "Traffic Impact Assessment",
                    traffic_list,
                    index=traffic_list.index(st.session_state.traffic_choice),
                    format_func=lambda x: format_option(x, TRAFFIC_IMPACT_OPTIONS),
                    key="traffic_choice"
                )

        st.divider()

        # --- Section 6: Desired Project ---
        st.subheader("6. Your Desired Project")
        st.selectbox(
            "Select your desired construction project",
            project_list,
            index=project_list.index(st.session_state.desired_project_choice),
            key="desired_project_choice"
        )

        st.markdown("---")

        # --- Action Button ---
        submitted = st.form_submit_button("Analyze Suitability", type="primary", use_container_width=True)

        if submitted:
            # Collate all details into session state from the widget keys
            st.session_state.site_details = {
                'project_heading': st.session_state.project_heading or "Untitled Site",
                # Legal & Survey
                'zoning': st.session_state.zoning_choice,
                'fsi_available': st.session_state.fsi_available,
                'envelope_width': st.session_state.envelope_width,
                'envelope_depth': st.session_state.envelope_depth,
                'slope_pct': st.session_state.slope_pct,
                'protected_trees_count': st.session_state.vegetation_survey,

                # Geotechnical (Soil)
                'spt_n': st.session_state.spt_n_value,
                'bearing_capacity': st.session_state.bearing_capacity_kpa,
                'cbr_pct': st.session_state.cbr_pct,
                'plate_load_settlement_mm': st.session_state.plate_load_settlement_mm,
                'proctor_compaction': st.session_state.proctor_compaction_pct,
                'plasticity_index': st.session_state.plasticity_index,
                'ucs_kpa': st.session_state.ucs_kpa,
                'soil_texture_key': st.session_state.soil_texture_choice,
                'soil_texture_score': SOIL_TEXTURE_OPTIONS[st.session_state.soil_texture_choice]['score'],
                'cohesion_kpa': st.session_state.cohesion_kpa,
                'friction_angle_deg': st.session_state.friction_angle_deg,
                'permeability_cm_sec': st.session_state.permeability_cm_sec,
                'percent_fines': st.session_state.percent_fines,
                'core_cutter_density': st.session_state.core_cutter_density,
                'soil_ph': st.session_state.soil_ph,

                # Geotechnical (Water & Contaminants)
                'groundwater_depth': st.session_state.groundwater_depth_ft,
                'percolation_rate_min_inch': st.session_state.percolation_rate_min_inch,
                'soil_resistivity_ohm_m': st.session_state.soil_resistivity_ohm_m,
                'contaminant_key': st.session_state.contaminant_choice,
                'contaminant_score': SOIL_CONTAMINANT_OPTIONS[st.session_state.contaminant_choice]['score'],
                'water_quality_key': st.session_state.water_quality_choice,
                'water_quality_score': WATER_QUALITY_OPTIONS[st.session_state.water_quality_choice]['score'],

                # Environmental & Risk
                'eia_key': st.session_state.eia_choice,
                'eia_score': EIA_STATUS_OPTIONS[st.session_state.eia_choice]['score'],
                'phase1_key': st.session_state.phase1_choice,
                'phase1_score': PHASE1_ESA_OPTIONS[st.session_state.phase1_choice]['score'],
                'phase2_key': st.session_state.phase2_choice,
                'phase2_score': PHASE2_ESA_OPTIONS[st.session_state.phase2_choice]['score'],
                'biodiversity_key': st.session_state.biodiversity_choice,
                'biodiversity_score': BIODIVERSITY_IMPACT_OPTIONS[st.session_state.biodiversity_choice]['score'],
                'wetland_percentage': st.session_state.wetland_percentage,
                'flood_key': st.session_state.flood_choice,
                'flood_score': FLOOD_RISK_OPTIONS[st.session_state.flood_choice]['score'],
                'drainage_key': st.session_state.drainage_choice,
                'drainage_score': DRAINAGE_OPTIONS[st.session_state.drainage_choice]['score'],
                'seismic_key': st.session_state.seismic_choice,
                'seismic_score': SEISMIC_ZONE_OPTIONS[st.session_state.seismic_choice]['score'],
                'air_quality_aqi': st.session_state.air_quality_aqi,
                'noise_level_dba': st.session_state.noise_level_dba,
                'hazardous_site_proximity_ft': st.session_state.hazardous_site_proximity_ft,

                # Infrastructure & Community
                'utility_key': st.session_state.utility_choice,
                'utility_level': UTILITY_OPTIONS[st.session_state.utility_choice]['score'],
                'pop_density_per_sq_km': st.session_state.pop_density_per_sq_km,
                'traffic_key': st.session_state.traffic_choice,
                'traffic_score': TRAFFIC_IMPACT_OPTIONS[st.session_state.traffic_choice]['score'],
            }
            st.session_state.desired_project = st.session_state.desired_project_choice

            # --- Run Analysis and store results in session state ---
            st.session_state.project_issues = check_suitability(
                st.session_state.site_details,
                st.session_state.desired_project
            )

            # "Other Suitable Projects" has been removed
            # st.session_state.suitable_projects = suitable_projects_list

    # After the form, show a success message to guide the user to the next tab
    if submitted:
        st.success("Analysis Complete! Click the 'View Analysis Report' tab to see your results.")


def render_report_tab():
    """
    Renders all the Streamlit widgets for the report page.
    """
    st.header("Analysis Report")

    # Check if an analysis has been run
    if not st.session_state.site_details:
        st.info("Your report will appear here after you fill out the form on the 'Enter Site Details' tab and click 'Analyze'.")
    else:
        # --- Get data from session state ---
        site_details = st.session_state.site_details
        desired_project = st.session_state.desired_project
        project_heading = site_details.get('project_heading', 'Untitled Site')
        today_str = datetime.date.today().isoformat()
        project_issues = st.session_state.project_issues
        # suitable_projects = st.session_state.suitable_projects (Removed)

        # --- PART 1: Check the user's desired project ---
        st.subheader(f"Analysis for: {desired_project}")

        if not project_issues:
            st.success(f"✅ SUCCESS: Your project '{desired_project}' is suitable for this site!")
        else:
            st.error(f"❌ FAILURE: Your project '{desired_project}' is NOT suitable for this site.")
            st.markdown("**Issues Found:**")
            for issue in project_issues:
                st.markdown(f"- {issue}")

        st.divider()

        # --- PART 2: "Other Suitable Projects" section has been removed ---

        # --- Display Summary Expander ---
        expander_title = f"Details for '{project_heading}' (Report Date: {today_str}) - Click to Expand & Download"
        with st.expander(expander_title, expanded=False):

            # Generate report text without suitable_projects
            report_data = generate_report_text(site_details, desired_project, project_issues)

            st.subheader("Site Details Summary")

            st.markdown(f"**Legal, Survey & Site:**")
            st.json({
                'Zoning': f"{site_details['zoning']} ({ZONING_OPTIONS[site_details['zoning']]['desc']})",
                'Slope': f"{site_details['slope_pct']}%",
                'FSI': site_details['fsi_available'],
                'Envelope': f"{site_details['envelope_width']} ft (Width) x {site_details['envelope_depth']} ft (Depth)",
                'Protected Trees': site_details['protected_trees_count']
            })

            st.markdown(f"**Geotechnical (Soil Properties):**")
            st.json({
                'SPT N-value': site_details['spt_n'],
                'Bearing Capacity': f"{site_details['bearing_capacity']} kPa",
                'CBR': f"{site_details['cbr_pct']}%",
                'Plate Load Settlement': f"{site_details['plate_load_settlement_mm']} mm",
                'Proctor Compaction': f"{site_details['proctor_compaction']}%",
                'Plasticity Index': site_details['plasticity_index'],
                'UCS': f"{site_details['ucs_kpa']} kPa",
                'Soil Texture': f"{site_details['soil_texture_key']} ({SOIL_TEXTURE_OPTIONS[site_details['soil_texture_key']]['desc']})",
                'Cohesion': f"{site_details['cohesion_kpa']} kPa",
                'Friction Angle': f"{site_details['friction_angle_deg']}°",
                'Permeability': f"{site_details['permeability_cm_sec']} cm/sec",
                'Percent Fines': f"{site_details['percent_fines']}%",
                'Dry Density': f"{site_details['core_cutter_density']} kg/m³",
                'Soil pH': site_details['soil_ph']
            })

            st.markdown(f"**Geotechnical (Water & Contaminants):**")
            st.json({
                'Groundwater Depth': f"{site_details['groundwater_depth']} ft",
                'Percolation Rate': f"{site_details['percolation_rate_min_inch']} min/inch",
                'Soil Resistivity': f"{site_details['soil_resistivity_ohm_m']} Ohm-m",
                'Contaminants': f"{site_details['contaminant_key']} ({SOIL_CONTAMINANT_OPTIONS[site_details['contaminant_key']]['desc']})",
                'Water Quality': f"{site_details['water_quality_key']} ({WATER_QUALITY_OPTIONS[site_details['water_quality_key']]['desc']})"
            })

            st.markdown(f"**Environmental & Risk:**")
            st.json({
                'EIA': f"{site_details['eia_key']} ({EIA_STATUS_OPTIONS[site_details['eia_key']]['desc']})",
                'Phase I ESA': f"{site_details['phase1_key']} ({PHASE1_ESA_OPTIONS[site_details['phase1_key']]['desc']})",
                'Phase II ESA': f"{site_details['phase2_key']} ({PHASE2_ESA_OPTIONS[site_details['phase2_key']]['desc']})",
                'Biodiversity Impact': f"{site_details['biodiversity_key']} ({BIODIVERSITY_IMPACT_OPTIONS[site_details['biodiversity_key']]['desc']})",
                'Wetland %': f"{site_details['wetland_percentage']}%",
                'Flood Risk': f"{site_details['flood_key']} ({FLOOD_RISK_OPTIONS[site_details['flood_key']]['desc']})",
                'Drainage': f"{site_details['drainage_key']} ({DRAINAGE_OPTIONS[site_details['drainage_key']]['desc']})",
                'Seismic': f"{site_details['seismic_key']} ({SEISMIC_ZONE_OPTIONS[site_details['seismic_key']]['desc']})",
                'Air Quality (AQI)': site_details['air_quality_aqi'],
                'Noise Level (dBA)': site_details['noise_level_dba'],
                'Hazardous Site Proximity': f"{site_details['hazardous_site_proximity_ft']} ft"
            })

            st.markdown(f"**Infrastructure & Community:**")
            st.json({
                'Utilities': f"{site_details['utility_key']} ({UTILITY_OPTIONS[site_details['utility_key']]['desc']})",
                'Population Density': f"{site_details['pop_density_per_sq_km']} people/km²",
                'Traffic Impact': f"{site_details['traffic_key']} ({TRAFFIC_IMPACT_OPTIONS[site_details['traffic_key']]['desc']})"
            })

            st.divider()

            st.download_button(
                label="Download Full Report (.txt)",
                data=report_data,
                file_name=f"Construction_Analysis_{datetime.date.today().isoformat()}.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.divider()

def render_requirements_tab():
    """
    Renders the "Check Project Requirements" tool in its own tab.
    """
    st.header("Check Project Requirements")
    st.markdown("Select any project from the database to see its minimum requirements.")

    project_list = list(CONSTRUCTION_RULES.keys())
    project_list_with_placeholder = ["Select a project..."] + project_list

    # The selectbox is the only widget needed here
    st.selectbox(
        "Select Project to Check",
        project_list_with_placeholder,
        key="check_project_rules" # Link to session state
    )

    # "Clear Selection" button was removed per user request.
    # User can re-select "Select a project..." to clear.

    # If a project is selected, show its details
    selected_project_to_check = st.session_state.check_project_rules
    if selected_project_to_check != "Select a project...":

        # Get the formatted rules
        rules_display = format_rules_for_display(selected_project_to_check)
        st.json(rules_display)

        # Generate text for download
        rules_text = generate_rules_text(selected_project_to_check)

        st.download_button(
            label=f"Download Requirements for {selected_project_to_check} (.txt)",
            data=rules_text,
            file_name=f"Requirements_{selected_project_to_check}.txt",
            mime="text/plain",
            use_container_width=True
        )