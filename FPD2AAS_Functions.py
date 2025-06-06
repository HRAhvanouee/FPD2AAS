# Import necessary classes from the BaSyx AAS Python SDK
from basyx.aas import model
from basyx.aas.adapter import aasx  # Required if you later want to read/write AASX files

############################################################################################################
# ID Management Functions for AAS and Submodel
############################################################################################################

def get_id_management_aas(id_short_aas='FPD'):
    """Generate a unique IRI for the Asset Administration Shell (AAS)."""
    return f"https://www.aut.ruhr-uni-bochum.de/{id_short_aas}_AAS"

def get_global_id_management_aas(id_short_aas='FPD'):
    """Generate a global asset ID for the AAS."""
    return f"https://www.aut.ruhr-uni-bochum.de/{id_short_aas}_Asset"

def get_id_management_submodel(id_short_submodel='FPD'):
    """Generate a unique IRI for the Submodel."""
    return f"https://www.aut.ruhr-uni-bochum.de/{id_short_submodel}_Submodel"

############################################################################################################
# AAS and Submodel Creation Functions
############################################################################################################

def create_fpd_aas(id_short_aas='FPD'):
    """
    Create and return an Asset Administration Shell (AAS) for a Functional Product Description (FPD).
    """
    aas = model.AssetAdministrationShell(
        id_=get_id_management_aas(id_short_aas),
        id_short=id_short_aas,
        asset_information=model.AssetInformation(
            asset_kind=model.AssetKind.INSTANCE,
            global_asset_id=get_global_id_management_aas(id_short_aas)
        )
    )
    return aas

def create_fpd_submodel(id_short_submodel='FPD'):
    """
    Create and return a Submodel for a Functional Product Description (FPD).
    """
    submodel = model.Submodel(
        id_=get_id_management_submodel(id_short_submodel),
        id_short=id_short_submodel
    )
    return submodel

############################################################################################################
# SubmodelElementCollection for Project Information
############################################################################################################

def create_project_information_collection(name_project='project name', target_namespace='namespace', entry_point='entry point'):
    """
    Create a SubmodelElementCollection for general project information.
    """
    prop_name_project = model.Property(
        id_short="name",
        value_type=model.datatypes.String,
        value=name_project,
        category='CONSTANT'
    )
    prop_target_namespace = model.Property(
        id_short="targetNamespace",
        value_type=model.datatypes.String,
        value=target_namespace,
        category='CONSTANT'
    )
    prop_entry_point = model.Property(
        id_short="entryPoint",
        value_type=model.datatypes.String,
        value=entry_point,
        category='CONSTANT'
    )
    smc_project_information = model.SubmodelElementCollection(
        id_short='projectInformation',
        value=(prop_name_project, prop_target_namespace, prop_entry_point),
        category='PARAMETER'
    )
    return smc_project_information

############################################################################################################
# SubmodelElementCollection for Process
############################################################################################################

def create_process_collection(id_short_process='process'):
    """
    Create a SubmodelElementCollection named 'process' for FPD.
    """
    smc_process = model.SubmodelElementCollection(
        id_short=id_short_process,
        category='PARAMETER'
    )
    return smc_process

############################################################################################################
# SubmodelElementList for Flows and Flow Collection
############################################################################################################

def create_flows_list():
    """
    Create a SubmodelElementList for flows.
    """
    sml_flows = model.SubmodelElementList(
        id_short='flows',
        type_value_list_element=model.SubmodelElementCollection
    )
    return sml_flows

def add_flow(id_short_submodel='FPD', incoming_id_short='state_incoming', outcoming_id_short='state_outcoming'):
    """
    Create a flow SubmodelElementCollection with incoming and outgoing references.
    """
    # Reference to incoming state
    ref_incoming = model.ReferenceElement(
        id_short='incoming',
        value=model.ModelReference((
            model.Key(type_=model.KeyTypes.SUBMODEL, value=get_id_management_submodel(id_short_submodel)),
            model.Key(type_=model.KeyTypes.SUBMODEL_ELEMENT_COLLECTION, value='process'),
            model.Key(type_=model.KeyTypes.SUBMODEL_ELEMENT_COLLECTION, value=incoming_id_short),
        ), model.SubmodelElementCollection),
        category='PARAMETER'
    )
    # Reference to outgoing state
    ref_outcoming = model.ReferenceElement(
        id_short='outcoming',
        value=model.ModelReference((
            model.Key(type_=model.KeyTypes.SUBMODEL, value=get_id_management_submodel(id_short_submodel)),
            model.Key(type_=model.KeyTypes.SUBMODEL_ELEMENT_COLLECTION, value='process'),
            model.Key(type_=model.KeyTypes.SUBMODEL_ELEMENT_COLLECTION, value=outcoming_id_short),
        ), model.SubmodelElementCollection),
        category='PARAMETER'
    )
    # Flow collection
    smc_flow = model.SubmodelElementCollection(
        id_short=None,  # Should be set uniquely if needed
        category='PARAMETER',
        value=(ref_incoming, ref_outcoming)
    )
    return smc_flow

############################################################################################################
# SubmodelElementList for Usages and Usage Collection
############################################################################################################

def create_usages_list():
    """
    Create a SubmodelElementList for usages.
    """
    sml_usages = model.SubmodelElementList(
        id_short='usages',
        type_value_list_element=model.SubmodelElementCollection
    )
    return sml_usages

def add_usage(id_short_submodel='FPD', source_id_short='source', target_id_short='target'):
    """
    Create a flow SubmodelElementCollection with incoming and outgoing references.
    """
    # Reference to source
    ref_source = model.ReferenceElement(
        id_short='source',
        value=model.ModelReference((
            model.Key(type_=model.KeyTypes.SUBMODEL, value=get_id_management_submodel(id_short_submodel)),
            model.Key(type_=model.KeyTypes.SUBMODEL_ELEMENT_COLLECTION, value='process'),
            model.Key(type_=model.KeyTypes.SUBMODEL_ELEMENT_COLLECTION, value=source_id_short),
        ), model.SubmodelElementCollection),
        category='PARAMETER'
    )
    # Reference to target
    ref_target = model.ReferenceElement(
        id_short='target',
        value=model.ModelReference((
            model.Key(type_=model.KeyTypes.SUBMODEL, value=get_id_management_submodel(id_short_submodel)),
            model.Key(type_=model.KeyTypes.SUBMODEL_ELEMENT_COLLECTION, value='process'),
            model.Key(type_=model.KeyTypes.SUBMODEL_ELEMENT_COLLECTION, value=target_id_short),
        ), model.SubmodelElementCollection),
        category='PARAMETER'
    )
    # Usage collection
    smc_usage = model.SubmodelElementCollection(
        id_short=None,  # Should be set uniquely if needed
        category='PARAMETER',
        value=(ref_source, ref_target)
    )
    return smc_usage

############################################################################################################
# SubmodelElementCollection for State
############################################################################################################

def create_state_collection(
    id_short_smc='state',
    unique_ident_ident=None, long_name_ident=None, short_name_ident=None, version_ident=None, revision_ident=None,
    unique_ident=None, long_name=None, short_name=None, version=None, revision=None,
    prop_view=None, prop_model=None, prop_regulation=None,
    value_determination_process=None, representivity=None,
    value_actual_value=None, unit_actual_value=None,
    value_setpoint=None, unit_setpoint=None,
    limit_type=None, from_date=None, to_date=None, assignment=None
):
    """
    Create a SubmodelElementCollection for a state, including identification and characteristics.
    """
    prop_stateType = model.Property(
        id_short='stateType',
        value_type=model.datatypes.String,
        value=None,
        category='CONSTANT'
    )
    smc_identification = create_identification_collection(
        unique_ident_ident, long_name_ident, short_name_ident, version_ident, revision_ident
    )
    smc_characteristics = create_characteristics_collection(
        unique_ident, long_name, short_name, version, revision,
        prop_view, prop_model, prop_regulation,
        value_determination_process, representivity,
        value_actual_value, unit_actual_value,
        value_setpoint, unit_setpoint,
        limit_type, from_date, to_date
    )
    prop_assignment = model.Property(
        id_short='assignment',
        value_type=model.datatypes.String,
        value=assignment,
        category='CONSTANT'
    )
    smc_state = model.SubmodelElementCollection(
        id_short=id_short_smc,
        category='PARAMETER',
        value=(prop_stateType, smc_identification, smc_characteristics, prop_assignment)
    )
    return smc_state

############################################################################################################
# SubmodelElementCollection for Identification
############################################################################################################

def create_identification_collection(
    unique_ident_ident=None, long_name_ident=None, short_name_ident=None, version_ident=None, revision_ident=None
):
    """
    Create a SubmodelElementCollection for identification properties.
    """
    prop_unique_ident = model.Property(
        id_short='uniqueIdent',
        value_type=model.datatypes.String,
        value=unique_ident_ident,
        category='CONSTANT'
    )
    prop_long_name = model.Property(
        id_short='longName',
        value_type=model.datatypes.String,
        value=long_name_ident,
        category='CONSTANT'
    )
    prop_short_name = model.Property(
        id_short='shortName',
        value_type=model.datatypes.String,
        value=short_name_ident,
        category='CONSTANT'
    )
    prop_version_number = model.Property(
        id_short='versionNumber',
        value_type=model.datatypes.String,
        value=version_ident,
        category='CONSTANT'
    )
    prop_revision_number = model.Property(
        id_short='revisionNumber',
        value_type=model.datatypes.String,
        value=revision_ident,
        category='CONSTANT'
    )
    smc_identification = model.SubmodelElementCollection(
        id_short='identification',
        category='PARAMETER',
        value=(prop_unique_ident, prop_long_name, prop_short_name, prop_version_number, prop_revision_number)
    )
    return smc_identification

############################################################################################################
# SubmodelElementCollection for Characteristics
############################################################################################################

def create_characteristics_collection(
    unique_ident=None, long_name=None, short_name=None, version=None, revision=None,
    prop_view=None, prop_model=None, prop_regulation=None,
    value_determination_process=None, representivity=None,
    value_actual_value=None, unit_actual_value=None,
    value_setpoint=None, unit_setpoint=None,
    limit_type=None, from_date=None, to_date=None
):
    """
    Create a SubmodelElementCollection for characteristics, including descriptive and relational elements.
    """
    prop_unique_ident = model.Property(
        id_short='uniqueIdent',
        value_type=model.datatypes.String,
        value=unique_ident,
        category='CONSTANT'
    )
    prop_long_name = model.Property(
        id_short='longName',
        value_type=model.datatypes.String,
        value=long_name,
        category='CONSTANT'
    )
    prop_short_name = model.Property(
        id_short='shortName',
        value_type=model.datatypes.String,
        value=short_name,
        category='CONSTANT'
    )
    prop_version_number = model.Property(
        id_short='versionNumber',
        value_type=model.datatypes.String,
        value=version,
        category='CONSTANT'
    )
    prop_revision_number = model.Property(
        id_short='revisionNumber',
        value_type=model.datatypes.String,
        value=revision,
        category='CONSTANT'
    )
    smc_descriptive_element = create_descriptive_element_collection(
        value_determination_process, representivity,
        value_actual_value, unit_actual_value,
        value_setpoint, unit_setpoint,
        limit_type, from_date, to_date
    )
    smc_relational_element = create_relational_element_collection(
        prop_view, prop_model, prop_regulation
    )
    smc_characteristics = model.SubmodelElementCollection(
        id_short='characteristics',
        category='PARAMETER',
        value=(
            prop_unique_ident, prop_long_name, prop_short_name,
            prop_version_number, prop_revision_number,
            smc_descriptive_element, smc_relational_element
        )
    )
    return smc_characteristics

############################################################################################################
# SubmodelElementCollection for Relational Element
############################################################################################################

def create_relational_element_collection(prop_view=None, prop_model=None, prop_regulation=None):
    """
    Create a SubmodelElementCollection for relational elements.
    """
    prop_view = model.Property(
        id_short='view',
        value_type=model.datatypes.String,
        value=prop_view,
        category='PARAMETER'
    )
    prop_model = model.Property(
        id_short='model',
        value_type=model.datatypes.String,
        value=prop_model,
        category='PARAMETER'
    )
    prop_regulation = model.Property(
        id_short='regulationsForRelationalGeneration',
        value_type=model.datatypes.String,
        value=prop_regulation,
        category='PARAMETER'
    )
    smc_relational_element = model.SubmodelElementCollection(
        id_short='relationalElement',
        category='PARAMETER',
        value=(prop_view, prop_model, prop_regulation)
    )
    return smc_relational_element

############################################################################################################
# SubmodelElementCollection for Descriptive Element
############################################################################################################

def create_descriptive_element_collection(
    value_determination_process=None, representivity=None,
    value_actual_value=None, unit_actual_value=None,
    value_setpoint=None, unit_setpoint=None,
    limit_type=None, from_date=None, to_date=None
):
    """
    Create a SubmodelElementCollection for descriptive elements.
    """
    prop_value_determination_process = model.Property(
        id_short='valueDeterminationProcess',
        value_type=model.datatypes.String,
        value=value_determination_process,
        category='CONSTANT'
    )
    prop_representivity = model.Property(
        id_short='representivity',
        value_type=model.datatypes.String,
        value=representivity,
        category='CONSTANT'
    )
    smc_setpoint_value = create_setpoint_value_collection(value_setpoint, unit_setpoint)
    smc_validity_limits = create_validity_limits_collection(limit_type, from_date, to_date)
    smc_actual_values = create_actual_values_collection(value_actual_value, unit_actual_value)
    smc_descriptive_element = model.SubmodelElementCollection(
        id_short='descriptiveElement',
        category='PARAMETER',
        value=(
            prop_value_determination_process,
            prop_representivity,
            smc_setpoint_value,
            smc_validity_limits,
            smc_actual_values
        )
    )
    return smc_descriptive_element

############################################################################################################
# SubmodelElementCollections for Actual Values, Setpoint Values, and Validity Limits
############################################################################################################

def create_actual_values_collection(value_actual_value=None, unit_actual_value=None):
    """
    Create a SubmodelElementCollection for actual values.
    """
    prop_value = model.Property(
        id_short='valueActualValue',
        value_type=model.datatypes.Double,
        value=value_actual_value,
        category='CONSTANT'
    )
    prop_unit = model.Property(
        id_short='unitActualValue',
        value_type=model.datatypes.String,
        value=unit_actual_value,
        category='CONSTANT'
    )
    smc_actual_values = model.SubmodelElementCollection(
        id_short='actualValues',
        category='PARAMETER',
        value=(prop_value, prop_unit)
    )
    return smc_actual_values

def create_setpoint_value_collection(value_setpoint=None, unit_setpoint=None):
    """
    Create a SubmodelElementCollection for setpoint values.
    """
    prop_value = model.Property(
        id_short='valueSetpoint',
        value_type=model.datatypes.Double,
        value=value_setpoint,
        category='CONSTANT'
    )
    prop_unit = model.Property(
        id_short='unitSetpoint',
        value_type=model.datatypes.String,
        value=unit_setpoint,
        category='CONSTANT'
    )
    smc_setpoint_value = model.SubmodelElementCollection(
        id_short='setpointValue',
        category='PARAMETER',
        value=(prop_value, prop_unit)
    )
    return smc_setpoint_value

def create_validity_limits_collection(limit_type=None, from_date=None, to_date=None):
    """
    Create a SubmodelElementCollection for validity limits.
    """
    prop_limit_type = model.Property(
        id_short='limitType',
        value_type=model.datatypes.String,
        value=limit_type,
        category='CONSTANT'
    )
    prop_from = model.Property(
        id_short='from',
        value_type=model.datatypes.DateTime,
        value=from_date,
        category='CONSTANT'
    )
    prop_to = model.Property(
        id_short='to',
        value_type=model.datatypes.DateTime,
        value=to_date,
        category='CONSTANT'
    )
    smc_validity_limits = model.SubmodelElementCollection(
        id_short='validityLimits',
        category='PARAMETER',
        value=(prop_limit_type, prop_from, prop_to)
    )
    return smc_validity_limits

############################################################################################################
# SubmodelElementCollection for Process Operator
############################################################################################################

def create_process_operator_collection(
    id_short_smc='processOperator',
    unique_ident_ident=None, long_name_ident=None, short_name_ident=None, version_ident=None, revision_ident=None,
    unique_ident=None, long_name=None, short_name=None, version=None, revision=None,
    prop_view=None, prop_model=None, prop_regulation=None,
    value_determination_process=None, representivity=None,
    value_actual_value=None, unit_actual_value=None,
    value_setpoint=None, unit_setpoint=None,
    limit_type=None, from_date=None, to_date=None, assignment=None
):
    """
    Create a SubmodelElementCollection for a process operator.
    """
    smc_identification = create_identification_collection(
        unique_ident_ident, long_name_ident, short_name_ident, version_ident, revision_ident
    )
    smc_characteristics = create_characteristics_collection(
        unique_ident, long_name, short_name, version, revision,
        prop_view, prop_model, prop_regulation,
        value_determination_process, representivity,
        value_actual_value, unit_actual_value,
        value_setpoint, unit_setpoint,
        limit_type, from_date, to_date
    )
    prop_assignment = model.Property(
        id_short='assignment',
        value_type=model.datatypes.String,
        value=assignment,
        category='CONSTANT'
    )
    smc_process_operator = model.SubmodelElementCollection(
        id_short=id_short_smc,
        category='PARAMETER',
        value=(smc_identification, smc_characteristics, prop_assignment)
    )
    return smc_process_operator

############################################################################################################
# SubmodelElementCollection for Technical Resource
############################################################################################################

def create_technical_resource_collection(
    id_short_smc='technicalResource',
    unique_ident_ident=None, long_name_ident=None, short_name_ident=None, version_ident=None, revision_ident=None,
    unique_ident=None, long_name=None, short_name=None, version=None, revision=None,
    prop_view=None, prop_model=None, prop_regulation=None,
    value_determination_process=None, representivity=None,
    value_actual_value=None, unit_actual_value=None,
    value_setpoint=None, unit_setpoint=None,
    limit_type=None, from_date=None, to_date=None, assignment=None
):
    """
    Create a SubmodelElementCollection for a technical resource.
    """
    smc_identification = create_identification_collection(
        unique_ident_ident, long_name_ident, short_name_ident, version_ident, revision_ident
    )
    smc_characteristics = create_characteristics_collection(
        unique_ident, long_name, short_name, version, revision,
        prop_view, prop_model, prop_regulation,
        value_determination_process, representivity,
        value_actual_value, unit_actual_value,
        value_setpoint, unit_setpoint,
        limit_type, from_date, to_date
    )
    prop_assignment = model.Property(
        id_short='assignment',
        value_type=model.datatypes.String,
        value=assignment,
        category='CONSTANT'
    )
    smc_technical_resource = model.SubmodelElementCollection(
        id_short=id_short_smc,
        category='PARAMETER',
        value=(smc_identification, smc_characteristics, prop_assignment)
    )
    return smc_technical_resource