from rdkit.Chem import MolFromSmiles, rdMolDescriptors, Descriptors

"""
Validates data by comparing the extracted formula and molecular mass with the by rdkit calculated formula and mass.
- "validated" : true, if the extracted and calculated informations are very close
- "validated" : false, if the extracted and calculated informations are far apart
- "validated" : None, if not yet validated or unable to validate because of missing smiles

returns nothing, saves the result within the dictionary
"""
def validate_data(data):
    if data["smiles"] == "":
        data["validated"] = None
        return
    
    # Calculate Informations with rdkit package
    mol = MolFromSmiles(data["smiles"])
    calculated_formula = rdMolDescriptors.CalcMolFormula(mol)
    calculated_mw = Descriptors.MolWt(mol)
    
    # Compare and validate
    same_formula = calculated_formula == data["formula"]
    nearly_same_mass = abs(data["molecular_mass"] - calculated_mw) < 0.1

    data["validated"] = same_formula and nearly_same_mass


if __name__ == "__main__":
    # Unit Test
    import incremental_loading
    import pathmanagement

    JSON_PATH = pathmanagement.create_file_paths()[0]

    data_collection = incremental_loading.load_json(JSON_PATH)
    
    for data in data_collection:
        data["validated"] = None
        print("Data before valiation:")
        print(f"{data["source"]["url"]}\n{data["smiles"]}\n{data["validated"]}")

        validate_data(data)

        print("\nData after:")
        print(f"{data["validated"]}\n")
        