# coding:utf-8 #
with open('./PMC/pmc_result.txt', 'r',  encoding='utf-8') as file:
    for line in file:
        if line.startswith('PMCID:'):
            columns = line.strip().split(' ')
            with open('./PMC/id.txt', 'a') as file1:
                file1.writelines(columns[1])
                file1.writelines('\n')

