import json
from datasets import load_dataset
import re

class RareDataLoader():
    def __init__(self, dataset_path=None) -> None:
        self.dataset_path = dataset_path
        self.data = {}
        if dataset_path is None:
            for dataset_name in ["RAMEDIS", "MME", "HMS", "LIRICAL", "PUMCH_ADM"]:
                self.data[dataset_name] = load_dataset('chenxz/RareBench', dataset_name, split='test')
        else:
            with open(dataset_path, "r", encoding="utf-8-sig") as f:
                self.data = json.load(f)


    def get_symptoms_formatted(self, patient):
        symptom_list = patient['Phenotype']
        phenotype_mapping = json.load(open("mapping/phenotype_mapping.json", "r", encoding="utf-8-sig"))
        sym_word_list = []

        for i in symptom_list:
            if i in phenotype_mapping:
                sym_word_list.append(phenotype_mapping[i])
        
        return (", ").join(sym_word_list)


    def get_diseases_formatted(self, patient):
        disease_list = patient['RareDisease']
        disease_mapping = json.load(open("mapping/disease_mapping.json", "r", encoding="utf-8-sig"))
        disease_word_list = []

        for i in disease_list:
            if i in disease_mapping:
                word = disease_mapping[i]
                #remove chinese characters
                word = word.encode("ascii", "ignore").decode()
                words = word.replace(";", "/").split("/")

                disease_word_list.extend(words)
                print(disease_word_list)

        
        return (", ").join(set(disease_word_list))
    
    def get_full_dataset(self):
        self.patient_list = []
        for dataset_name in ["RAMEDIS", "MME", "HMS", "LIRICAL", "PUMCH_ADM"]:
            relevant_dataset = self.data[dataset_name]
            for i in range(len(relevant_dataset)):
                pt = relevant_dataset[i]
                new_dict = {}
                new_dict["input"] = self.get_symptoms_formatted(pt)
                new_dict["output"] = self.get_diseases_formatted(pt)
                self.patient_list.append(new_dict)
        return self.patient_list
    
    def get_full_json_list(self):
        self.patient_list = self.get_full_dataset()
        return json.dumps(self.patient_list)



