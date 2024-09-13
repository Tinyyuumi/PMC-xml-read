该仓库用于从PMC网站论文的xml中提取作者、标题、摘要、引文位置、引文等信息。  
This repository is used to extract information from paper XML in website PMC, which includes author, title, abstract, reference location and reference.


https://www.ncbi.nlm.nih.gov/pmc  

1、先从网站上导出搜索列表，放在pmc_result.txt文件中  

![](pcmid.png)

2、运行 extract_pcmid.py，从pmc_result.txt文件提取PCMID并保存在id.txt中
```
python extract_pcmid.py
```

3、运行 article.py，从id.txt文件根据PCMID提取文章信息
```
python article.py
```
