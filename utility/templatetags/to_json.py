
# from django import template
# register = template.Library()
# from archive.serializers import FolderSerializer,FileSerializer
# import json


# from resume.serializers import ResumeSerializer
# from warehouse.serializers import WareHouseSerializer
# from accounting.serializers import AccountSerializer, FinancialBalanceSerializer,ProfileSerializer, TransactionSerializer


# @register.filter
# def to_json_warehouses(warehouses):
#     return json.dumps(WareHouseSerializer(warehouses,many=True).data)

    
# @register.filter
# def to_json_financial_balances(financial_balances):
#     return json.dumps(FinancialBalanceSerializer(financial_balances,many=True).data)

# @register.filter
# def to_json_resumes(resumes):
#     return json.dumps(ResumeSerializer(resumes,many=True).data)

# @register.filter
# def to_json_accounts(accounts):
#     return json.dumps(AccountSerializer(accounts,many=True).data)

# @register.filter
# def to_json_profiles(profiles):
#     return json.dumps(ProfileSerializer(profiles,many=True).data)
# @register.filter
# def to_json_transactions(transactions):
#     return json.dumps(TransactionSerializer(transactions,many=True).data)


# @register.filter
# def to_json_folders(folders):
#     return json.dumps(FolderSerializer(folders,many=True).data)

# @register.filter
# def to_json_folder(folder):
#     return json.dumps(FolderSerializer(folder).data)

# @register.filter
# def to_json_files(files):
#     return json.dumps(FileSerializer(files,many=True).data)
