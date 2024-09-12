# coding:utf-8 #
import requests
import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

pcmid_file = r'./PMC/id.txt'
output_file = r'./PMC/article.txt'


def get_lable_string(root, label):
    try:
        xx = root.find(label)
        xx_s = ''.join(xx.itertext()).strip()
    except:
        xx_s = ''
    return xx_s


def write_to_txt(ss):
    with open(output_file, 'a') as f:
        f.write(ss)

with open(pcmid_file, 'r',  encoding='utf-8') as file:
    for line in file:
        columns = line.strip().split('PMC')
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={columns[1]}&retmode=xml"
        # https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC6691464&retmode=xml
        
        # 请求全文XML
        response = requests.get(url)
        text = response.text

        if text is None or len(text)==0:
            continue
        
        

        # 开始写入
        write_to_txt('Start\n')

        # 解析xml
        root = ET.fromstring(text)

        # 查找标题
        write_to_txt('[标题] ')
        try:
            title_groups = root.findall('.//title-group')
            full_text = ''.join(title_groups[0].itertext())
            article_title = full_text.strip()
        except:
            article_title = ''
        write_to_txt(article_title + '\n')


        # 作者
        write_to_txt('[作者] ')
        try:
            author_content = ''
            name_list = root.findall('.//contrib-group')
            author_groups = name_list[0].findall('.//name')
            for iq, name in enumerate(author_groups):
                surname = get_lable_string(name,'.//surname')
                given_names = get_lable_string(name,'.//given-names')
                author_content = author_content + str(iq+1) + ' ' + surname + ' ' + given_names + ', '

        except:
            author_content = ''
        write_to_txt(author_content + '\n')

        
        
        # 摘要
        write_to_txt('[摘要] ')
        try:
            abstract_element = root.find('.//abstract')
            abstract_content = ''.join(abstract_element.itertext())
        except:
            abstract_content = ''
        write_to_txt(abstract_content + '\n')


        # 关键词
        write_to_txt('[关键词] ')
        try:
            kwd_content = ''
            kwd_elements = root.findall('.//kwd-group/kwd')
            for kwd in kwd_elements:
                kwd_content = kwd_content + kwd.text + ', '
            kwd_content = kwd_content[:-2]
        except:
            kwd_content = ''
        write_to_txt(kwd_content + '\n')
        

        # PubMed ID
        write_to_txt('[PubMed ID] ')
        try:
            pmid_element = root.find('.//article-id[@pub-id-type="pmid"]')
            pmid_content = ''.join(pmid_element.itertext()).strip()
        except:
            pmid_content = ''
        write_to_txt(pmid_content + '\n')


        # 全文
        write_to_txt('[全文]\n')
        p_elements_with_xref = root.findall('.//p[xref]')
        combined_content = ''
        for p in p_elements_with_xref:
            try:
                combined_content += ''.join(p.itertext()) + ' '
                combined_content = combined_content.replace('\n', '')
                write_to_txt(combined_content + '\n\n')
            except:
                pass
        
        # 引文
        write_to_txt('[引文]\n')
    
        ref_elements = root.findall('.//ref-list/ref')
        ref_list = []
        for iq, ref in enumerate(ref_elements):
            ref_s = ''
            name_elements = ref.findall('.//name')

            try:
                if len(name_elements) != 0:
                    for name in name_elements:
                        surname = get_lable_string(name,'.//surname')
                        given_names = get_lable_string(name,'.//given-names')
                        ref_s = ref_s + surname + ' ' + given_names + ', '
                    
                    ref_s = ref_s[:-2]

                    ref_article_title = get_lable_string(ref,'.//article-title')
                    ref_source = get_lable_string(ref,'.//source')
                    ref_year = get_lable_string(ref,'.//year')
                    ref_volume = get_lable_string(ref,'.//volume')
                    ref_fpage = get_lable_string(ref,'.//fpage')
                    ref_lpage = get_lable_string(ref,'.//lpage')
                    ref_pmid = get_lable_string(ref,'.//pub-id[@pub-id-type="pmid"]')

                    ref_s = ref_pmid + '. ' + ref_s + '. ' + ref_article_title + '. ' + ref_source + '. ' + ref_year + ';' \
                        + ref_volume + ':' + ref_fpage + '-' + ref_lpage 
                
                else:
                    ref_s = ''.join(ref.itertext())
                    ref_s = ref_s.replace('\n', '')
                    ref_s = re.sub(r'\s{2,}', ',', ref_s)[3:]
                
                ref_list.append('[{0}] {1} \n'.format(iq,ref_s))       
            except:
                pass
        
        list(map(write_to_txt, ref_list))
            
        # 结束写入
        write_to_txt('END\n\n\n')     


        vv = 1
        