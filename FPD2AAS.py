# FPD to AAS Conversion Script
# ---------------------------------------------
# Automated/JSON-driven version below
# ---------------------------------------------

import json
from basyx.aas import model
from basyx.aas.adapter import aasx
import FPD2AAS_Functions as func  # Custom module for AAS functions
import FPD                      # Custom module for FPD data extraction

# -------------------------------
# Define file paths for input/output
# -------------------------------
path_json = r"C:\Users\Rezaee\Desktop\Files\RUB\Paper\5 - ONCON 2025\code\FPD.json"
path_aasx = r"C:\Users\Rezaee\Desktop\Files\RUB\Paper\5 - ONCON 2025\code\AAS.aasx"

# -------------------------------
# Load FPD data from JSON file
# -------------------------------
with open(path_json, 'r', encoding='utf-8') as f:
    fpd_data = json.load(f)

# -------------------------------
# Extract project, process, and elements from FPD data
# -------------------------------
project, process, elements = FPD.extract_data(fpd_data)

# -------------------------------
# Create AAS and Submodel
# -------------------------------
aas = func.create_fpd_aas('FPD_AAS')              # Create Asset Administration Shell
submodel = func.create_fpd_submodel('FPD')        # Create main Submodel

# -------------------------------
# Add project information to submodel
# -------------------------------
smc_project_information = FPD.add_project_info(project)

# -------------------------------
# Create process collection and add state, operator, and resource info
# -------------------------------
smc_process = func.create_process_collection('process')
FPD.add_state_info(elements, smc_process)             # Add state info to process
FPD.add_process_operator_info(elements, smc_process)  # Add operator info to process
FPD.add_technical_resource_info(elements, smc_process) # Add technical resource info

# -------------------------------
# Add flows between process elements
# -------------------------------
sml_flows = func.create_flows_list()              # Create flows list
FPD.add_flows(elements, sml_flows)                # Add flows to the list

# -------------------------------
# Add usages between process elements
# -------------------------------
sml_usages = func.create_usages_list()              # Create usages list
FPD.add_usages(elements, sml_usages)                # Add usages to the list

# -------------------------------
# Add all elements to submodel and link to AAS
# -------------------------------
submodel.submodel_element.add(smc_project_information)
submodel.submodel_element.add(smc_process)
submodel.submodel_element.add(sml_flows)
submodel.submodel_element.add(sml_usages)
aas.submodel.add(model.ModelReference.from_referable(submodel))

# -------------------------------
# Save the AAS and Submodel to AASX file
# -------------------------------
object_store = model.DictObjectStore([submodel, aas])          # Create object store
file_store = aasx.DictSupplementaryFileContainer()             # Create empty file store

with aasx.AASXWriter(path_aasx) as writer:
    writer.write_aas(
        aas_ids=aas.id, 
        object_store=object_store, 
        file_store=file_store
    )