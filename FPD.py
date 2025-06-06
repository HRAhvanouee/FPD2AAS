from basyx.aas import model
import FPD2AAS_Functions as func
from datetime import datetime

# -------------------------------
# Extract project, process, and elements from FPD data
# -------------------------------
def extract_data(fpd_data):
    """
    Extracts project, process, and element information from FPD JSON data.
    """
    project = fpd_data[0]
    info = fpd_data[1]
    process = info["process"]
    elements = info["elementDataInformation"]
    return project, process, elements

# -------------------------------
# Add project information to submodel
# -------------------------------
def add_project_info(project):
    """
    Creates a project information collection for the AAS submodel.
    """
    smc_project_information = func.create_project_information_collection(
        project["name"], project["targetNamespace"], project["entryPoint"]
    )
    return smc_project_information

# -------------------------------
# Helper function to filter elements by type
# -------------------------------
def get_elements_by_type(elements, t):
    """
    Helper function to filter elements by their $type suffix.
    """
    return [el for el in elements if el["$type"].endswith(t)]

# -------------------------------
# Add state information (Product, Energy, Information) to process collection
# -------------------------------
def add_state_info(elements, smc_process):
    """
    Adds state information (Product, Energy, Information) to the process collection.
    """
    for state_type in ["Product", "Energy", "Information"]:
        for el in get_elements_by_type(elements, state_type):
            assigned_to = el.get("isAssignedTo", [])
            assigned_to_str = ",".join(assigned_to) if assigned_to else None
            characs = el.get("characteristics", [])
            if characs:
                ch = characs[0]  # Use only the first characteristic
                category = ch.get("category", {})
                desc = ch.get("descriptiveElement", {})
                rel = ch.get("relationalElement", {})
                validity = desc.get("validityLimits", [{}])[0]

                smc_state = func.create_state_collection(
                    id_short_smc=el["name"],
                    unique_ident_ident=el["id"],
                    long_name_ident=el["identification"].get("longName", ""),
                    short_name_ident=el["identification"].get("shortName", ""),
                    version_ident=el["identification"].get("versionNumber", ""),
                    revision_ident=el["identification"].get("revisionNumber", ""),

                    unique_ident=category.get("uniqueIdent", ""),
                    long_name=category.get("longName", ""),
                    short_name=category.get("shortName", ""),
                    version=category.get("versionNumber", ""),
                    revision=category.get("revisionNumber", ""),

                    prop_view=rel.get("view", ""),
                    prop_model=rel.get("model", ""),
                    prop_regulation=rel.get("regulationsForRelationalGeneration", ""),

                    value_determination_process=desc.get("valueDeterminationProcess", ""),
                    representivity=desc.get("representivity", ""),

                    value_actual_value=float(desc.get("actualValues", {}).get("value", 0)),
                    unit_actual_value=desc.get("actualValues", {}).get("unit", ""),
                    value_setpoint=float(desc.get("setpointValue", {}).get("value", 0)),
                    unit_setpoint=desc.get("setpointValue", {}).get("unit", ""),

                    limit_type=desc.get("validityLimits", [{}])[0].get("limitType", ""),
                    from_date=parse_datetime(validity.get("from")),
                    to_date=parse_datetime(validity.get("to")),
                    assignment=assigned_to_str
                )
            else:
                # If no characteristics, create state collection with basic info
                smc_state = func.create_state_collection(
                    id_short_smc=el["name"],
                    unique_ident_ident=el["id"],
                    long_name_ident=el["identification"].get("longName", ""),
                    short_name_ident=el["identification"].get("shortName", ""),
                    version_ident=el["identification"].get("versionNumber", ""),
                    revision_ident=el["identification"].get("revisionNumber", ""),
                    assignment=assigned_to_str
                )

            # Explicitly set the stateType property after creation
            for elem in smc_state.value:
                if isinstance(elem, model.Property) and elem.id_short == "stateType":
                    elem.value = state_type
                    break

            smc_process.add_referable(smc_state)

# -------------------------------
# Add process operator information to process collection
# -------------------------------
def add_process_operator_info(elements, smc_process):
    """
    Adds process operator information to the process collection.
    """
    for op in get_elements_by_type(elements, "ProcessOperator"):
        assigned_to = op.get("isAssignedTo", [])
        assigned_to_str = ",".join(assigned_to) if assigned_to else None
        characteristics = op.get("characteristics", [])
        if characteristics:
            ch = characteristics[0]
            cat = ch.get("category", {})
            desc = ch.get("descriptiveElement", {})
            rel = ch.get("relationalElement", {})
            validity = desc.get("validityLimits", [{}])[0]
        else:
            ch = {}
            cat = {}
            desc = {}
            rel = {}
            validity = {}

        smc_op = func.create_process_operator_collection(
            id_short_smc=op["name"].strip(),
            unique_ident_ident=op["id"],
            long_name_ident=op["identification"].get("longName", ""),
            short_name_ident=op["identification"].get("shortName", "").strip(),
            version_ident=op["identification"].get("versionNumber", ""),
            revision_ident=op["identification"].get("revisionNumber", ""),

            unique_ident=cat.get("uniqueIdent", ""),
            long_name=cat.get("longName", ""),
            short_name=cat.get("shortName", ""),
            version=cat.get("versionNumber", ""),
            revision=cat.get("revisionNumber", ""),

            prop_view=rel.get("view", ""),
            prop_model=rel.get("model", ""),
            prop_regulation=rel.get("regulationsForRelationalGeneration", ""),

            value_determination_process=desc.get("valueDeterminationProcess", ""),
            representivity=desc.get("representivity", ""),

            value_actual_value=float(desc.get("actualValues", {}).get("value", 0)),
            unit_actual_value=desc.get("actualValues", {}).get("unit", ""),
            value_setpoint=float(desc.get("setpointValue", {}).get("value", 0)),
            unit_setpoint=desc.get("setpointValue", {}).get("unit", ""),

            limit_type=validity.get("limitType", ""),
            from_date=parse_datetime(validity.get("from")),
            to_date=parse_datetime(validity.get("to")),
            assignment=assigned_to_str
        )
        smc_process.add_referable(smc_op)


# -------------------------------
# Add technical resource information to process collection
# -------------------------------
def add_technical_resource_info(elements, smc_process):
    """
    Adds technical resource information to the process collection.
    """
    for tr in get_elements_by_type(elements, "TechnicalResource"):
        assigned_to = tr.get("isAssignedTo", [])
        assigned_to_str = ",".join(assigned_to) if assigned_to else None
        characteristics = tr.get("characteristics", [])
        if characteristics:
            ch = characteristics[0]
            cat = ch.get("category", {})
            desc = ch.get("descriptiveElement", {})
            rel = ch.get("relationalElement", {})
            validity = desc.get("validityLimits", [{}])[0]
        else:
            ch = {}
            cat = {}
            desc = {}
            rel = {}
            validity = {}

        smc_tr = func.create_technical_resource_collection(
            id_short_smc=tr["name"],
            unique_ident_ident=tr["id"],
            long_name_ident=tr["identification"].get("longName", ""),
            short_name_ident=tr["identification"].get("shortName", ""),
            version_ident=tr["identification"].get("versionNumber", ""),
            revision_ident=tr["identification"].get("revisionNumber", ""),

            unique_ident=cat.get("uniqueIdent", ""),
            long_name=cat.get("longName", ""),
            short_name=cat.get("shortName", ""),
            version=cat.get("versionNumber", ""),
            revision=cat.get("revisionNumber", ""),

            prop_view=rel.get("view", ""),
            prop_model=rel.get("model", ""),
            prop_regulation=rel.get("regulationsForRelationalGeneration", ""),

            value_determination_process=desc.get("valueDeterminationProcess", ""),
            representivity=desc.get("representivity", ""),

            value_actual_value=float(desc.get("actualValues", {}).get("value", 0)),
            unit_actual_value=desc.get("actualValues", {}).get("unit", ""),
            value_setpoint=float(desc.get("setpointValue", {}).get("value", 0)),
            unit_setpoint=desc.get("setpointValue", {}).get("unit", ""),

            limit_type=validity.get("limitType", ""),
            from_date=parse_datetime(validity.get("from")),
            to_date=parse_datetime(validity.get("to")),
            assignment=assigned_to_str
        )
        smc_process.add_referable(smc_tr)


# -------------------------------
# Add flow connections between process elements
# -------------------------------
def add_flows(elements, sml_flows):
    """
    Adds flow connections between process elements to the flows list.
    """
    for flow in get_elements_by_type(elements, "Flow"):
        # Find source and target element names by their IDs
        src = next((el["name"] for el in elements if el["id"] == flow["sourceRef"]), None)
        tgt = next((el["name"] for el in elements if el["id"] == flow["targetRef"]), None)
        if src and tgt:
            flow_col = func.add_flow("FPD", src, tgt)
            sml_flows.add_referable(flow_col)
            
            
# -------------------------------
# Add usage connections between process elements
# -------------------------------
def add_usages(elements, sml_usages):
    """
    Adds usage connections between process elements to the usages list.
    """
    for usage in get_elements_by_type(elements, "Usage"):
        # Find source and target element names by their IDs
        src = next((el["name"] for el in elements if el["id"] == usage["sourceRef"]), None)
        tgt = next((el["name"] for el in elements if el["id"] == usage["targetRef"]), None)
        if src and tgt:
            usage_col = func.add_usage("FPD", src, tgt)
            sml_usages.add_referable(usage_col)

# -------------------------------
# Parse a datetime string or timestamp to a datetime object
# -------------------------------
def parse_datetime(value):
    """
    Parses a datetime string or timestamp to a datetime object.
    Returns None if parsing fails.
    """
    try:
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        elif isinstance(value, int) or isinstance(value, float):
            # Optionally interpret int/float as Unix timestamp
            return datetime.fromtimestamp(value)
    except Exception:
        return None
    return None