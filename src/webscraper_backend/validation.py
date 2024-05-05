from rdkit.Chem import MolFromSmiles, rdMolDescriptors, Descriptors

"""
Validates data by comparing the extracted formula and molecular mass with the by rdkit calculated formula and mass.
- "valid" : true, if the extracted and calculated informations are very close
- "valid" : false, if the extracted and calculated informations are far apart
- "valid" : None, if not yet validated or unable to validate because of missing smiles

returns nothing, saves the result within the dictionary
"""
def validate_data(data):
    if data["smiles"] == "":
        data["valid"] = None
        return
    
    # Calculate Informations with rdkit package
    mol = MolFromSmiles(data["smiles"])
    calculated_formula = rdMolDescriptors.CalcMolFormula(mol)
    calculated_mw = Descriptors.MolWt(mol)
    
    # Compare and validate
    same_formula = calculated_formula == data["formula"]
    nearly_same_mass = abs(float(data["molecular_mass"]) - calculated_mw) < 0.1

    data["valid"] = same_formula and nearly_same_mass


if __name__ == "__main__":
    # Unit Test
    import incremental_loading

    data_collection = incremental_loading.load_existing_data()
    
    for data in data_collection:
        data["valid"] = None
        print("Data before valiation:")
        print(f"{data["source_url"]}\n{data["smiles"]}\n{data["valid"]}")

        validate_data(data)

        print("\nData after:")
        print(f"{data["valid"]}\n")
        