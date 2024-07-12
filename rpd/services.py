import os.path
from builtins import enumerate
from datetime import datetime
from itertools import groupby

import requests
from django.conf import settings
from urllib.parse import unquote

from django.db.models import Q
from lxml import etree
import re

from rpd.models import PlanData, LinesData, Disciplines, SemesterData, LinesIndicators, ExceptionNames, AllowedNames, \
    PlanDocuments
from rpd.serializer import PlanDataSerializer, DisciplinesSerializer, LinesDataSerializer, SemesterDataSerializer, \
    LinesIndicatorsSerializer, PlanDocumentsSerializer

from app.utils import cache_function


class PLXParser:

    XMLNS = ""
    path = ""

    fileNameRegex = r"([А-я]*)-(\d*)"
    parser = etree.XMLParser(encoding='UTF-8')

    semesteroncource = None
    studylevel = None

    fileId = None

    def __init__(self, filePath, file_id):
        self.data = {}
        with open((os.path.join(settings.BASE_DIR)) + unquote(filePath), "r", encoding="utf-16") as f:
            self.parseXML(etree.parse(f, parser=self.parser), file_id)

    def get_result_data(self):
        return self.data
    def parseXML(self, tree, file_id):
        self.fileId = file_id
        root = tree.getroot()

        XHTML_NAMESPACE = root[0][0].nsmap[None]
        self.XMLNS = "{%s}" % XHTML_NAMESPACE
        self.path = ".//%s" % self.XMLNS

        planData_result = []
        plnData = self.get_plan_data(root)
        planData = self.insert_plan_data(plnData)
        planData_result.append(planData)

        self.data['plan'] = planData_result

        if self.studylevel not in [4,5]:
            competences_data = self.get_competences_data(root)

        indikators_data = self.get_indicators_data(root)

        lnsdata = self.get_lines_data(root, planData['id'], indikators_data)
        tmp = self.insert_lines_data(lnsdata)

        list_id = []
        list_keys = []
        for key, items in tmp.items():
            if items['id'] not in list_id:
                list_id.append(items['id'])
                list_keys.append(key)

        lines_data = {}
        for i in list_keys:
            lines_data[i] = tmp[i]

        lines_data_result = []
        for key, items in lines_data.items():
            lines_data_result.append(items)
        self.data['lines'] = lines_data_result

        lines_indicators = self.get_lines_ind_comp_bind_data(root)
        semester_data = self.get_semester_data(root)

        for key, items in lines_data.items():
            for v, value in lines_indicators.items():
                if value['КодСтроки'] == key:
                    value['planlineid_id'] = items['id']
                    value['find'] = True

            for v, value in semester_data.items():
                if value['planlineid_id'] == key:
                    value['planlineid_id'] = items['id']
                    value['find'] = True

        lines_indicators = {key: item for key, item in lines_indicators.items() if item['find']}
        semester_data = {key: item for key, item in semester_data.items() if item['find']}

        sorted_lines_indicators = sorted(lines_indicators.items(), key=lambda item: item[1]['КодСтроки'])
        group_lines_indicators = {key: list(items) for key, items in groupby(sorted_lines_indicators, key=lambda item: item[1]['КодСтроки'])}

        sorted_semester_data = sorted(semester_data.items(), key=lambda item: (item[1]['planlineid_id'], item[1]['num']))
        group_semester_data = {key: list(items) for key, items in groupby(sorted_semester_data, key=lambda  item: (item[1]['planlineid_id'], item[1]['num']))}

        semester_data_res = []
        for key, items in group_semester_data.items():
            temp = {**items[0][1]}
            for item in items:
                temp.update({k: v for k, v in item[1].items() if v is not None})
            semester_data_res.append(temp)

        semester_data_result = self.insert_semester_data(semester_data_res)
        self.data['semester'] = semester_data_result


        lines_indicators_res = []
        for key, items in group_lines_indicators.items():
            for item in items:
                tmp_obj = {}
                for v, value in indikators_data.items():
                    if item[1]['КодКомпетенции'] == v:
                        if self.studylevel in [4, 5]:
                            tmp_obj = {
                                'planlineid_id': item[1]['planlineid_id'],
                                'indicator_index': value['index'],
                                'indicator': value['content'],
                            }
                        else:
                            tmp_obj = {
                                'planlineid_id': item[1]['planlineid_id'],
                                'indicator_index': value['index'],
                                'indicator': value['content'],
                                'competence_index': competences_data[value['КодРодителя']]['index'],
                                'competence': competences_data[value['КодРодителя']]['content'],
                            }

                        break
                lines_indicators_res.append(tmp_obj)


        lines_indicators_result = self.insert_lines_indicators(lines_indicators_res)
        self.data['indicators'] = lines_indicators_result

        plan_files = self.get_documents_plan(lines_data, planData['id'])
        self.data['documents'] = plan_files

    study_prog = {
        1: 'подготовка специалистов',
        2: 'подготовка бакалавров',
        3: 'подготовка магистров',
        4: 'подготовка СПО',
        5: 'подготовка СПО',
        7: 'подготовка аспирантов',
    }

    def get_plan_data(self, root):

        planData = {}

        planData['subtype'] = "Рабочий учебный план"
        planData['shifr'] = "SKYF"
        planData['studyform'] = root.attrib['КодФормыОбучения']  # модифицировать
        planData['studylevel'] = root.attrib.get('КодУровняОбразования')  # модифицировать
        self.studylevel = int(root.attrib.get('КодУровняОбразования'))
        planData['studyprog'] = self.study_prog[int(root.attrib.get('КодУровняОбразования'))]
        planData['elementsinweek'] = int(root.attrib['ЭлементовВНеделе'])
        planData['faculty'] = ''

        for child in root.findall(self.path + 'Планы'):
            # print(child.tag.strip(self.XMLNS), child.attrib)

            planData['species'] = child.attrib.get('Титул').rstrip().replace("\r\n", " ")
            planData['usernum'] = int(child.attrib.get('НомерПользователя'))
            planData['whoratif'] = child.attrib.get('ПланОдобрен')

            planData['planname'] = child.attrib.get('ИмяФайла')
            planData['kafcode'] = int(child.attrib.get('КодПрофКафедры')) if child.attrib.get('КодПрофКафедры') else None
            planData['startyear'] = int(child.attrib.get('ГодНачалаПодготовки'))
            planData['dviga'] = True if child.attrib.get('ДвИГА') == 'true' else False
            planData['gviga'] = True if child.attrib.get('ГвИГА') == 'true' else False
            planData['igazetweek'] = float(child.attrib.get('ЧасовВКредите'))
            planData['igahourzet'] = float(child.attrib.get('ЗЕТвНеделю'))
            planData['semesteroncource'] = int(child.attrib.get('СеместровНаКурсе'))
            self.semesteroncource = int(child.attrib.get('СеместровНаКурсе'))
            planData['gosdate'] = datetime.fromisoformat((child.attrib.get('ДатаГОСа'))).strftime(
                "%Y-%m-%d") if child.attrib.get('ДатаГОСа') else None
            planData['gostype'] = float(child.attrib.get('ТипГОСа'))
            planData['napr_t'] = child.attrib.get('Титул').rstrip().replace("\r\n", " ")
            planData['abbrprofile'] = re.search(self.fileNameRegex, child.attrib.get('ИмяФайла').replace("_", "-"))[1]

        for child in root.findall(self.path + 'ООП'):
            planData['gosdocument'] = int(child.attrib.get('НомерДокумента') if child.attrib.get('НомерДокумента') else None)
            planData['lastshifr'] = child.attrib.get('Шифр')
            planData['naprcode'] = child.attrib.get('Шифр')
            planData['napr_e'] = child.attrib.get('Название')

        for child in root.findall(self.path + 'Филиалы'):
            planData['vuzname'] = child.attrib['Полное_название']
            planData['head'] = child.attrib['Директор']

        for child in root.findall(self.path + 'Факультеты'):
            planData['faculty'] = child.attrib['Факультет']

        for child in root.findall(self.path + 'ФормаОбучения'):
            if child.attrib.get('Код') == planData['studyform']:
                planData['studyform'] = child.attrib.get('ФормаОбучения')
                break

        for child in root.findall(self.path + 'Уровень_образования'):
            if child.attrib.get('Код_записи') == planData['studylevel']:
                planData['studylevel'] = child.attrib.get('Уровень')
                break

        for child in root.findall(self.path + 'УровеньОбразования'):
            if child.attrib.get('Код') == planData['studyprog']:
                planData['studyprog'] = child.attrib.get('Уровень')
                break

        return planData

    def insert_plan_data(self, data):
        data['file_id'] = self.fileId
        try:
            obj = PlanData.objects.values().get(file_id=self.fileId)
            data = obj
        except:
            obj = PlanDataSerializer(data=data)

            obj.is_valid(raise_exception=True)
            obj.save()

            data['id'] = obj.data['id']

        return data

    def get_lines_data(self, root, plan_id, indicators):

        lines_data = {}

        for child in root.findall(self.path + 'ПланыСтроки'):
            temp_dict = {}
            temp_dict['plan_id'] = plan_id

            temp_dict['dis'] = child.attrib.get('Дисциплина')
            temp_dict['newdisid'] = child.attrib.get('ДисциплинаКод')
            temp_dict['mustbesdudied'] = int(child.attrib.get('ПодлежитИзучениюЧасов')) if child.attrib.get('ПодлежитИзучениюЧасов') else None
            temp_dict['hoursinzet'] = int(child.attrib.get('ЧасовВЗЕТ')) if child.attrib.get('ЧасовВЗЕТ') else None
            temp_dict['caf'] = int(child.attrib.get('КодКафедры')) if child.attrib.get('КодКафедры') else None
            temp_dict['nocalccontrol'] = True if child.attrib.get('НеСчитатьКонтроль') == 'true' else False
            temp_dict['type'] = int(child.attrib.get('ТипОбъекта')) if child.attrib.get('ТипОбъекта') else None
            temp_dict['viewpract'] = int(child.attrib.get('ВидПрактики')) if child.attrib.get('ВидПрактики') else None
            temp_dict['viewobject'] = int(child.attrib.get('ВидОбъекта')) if child.attrib.get('ВидОбъекта') else None

            lines_code = int(child.attrib.get('Код'))

            tmp = []
            for deep in root.findall(self.path + 'ПланыКомпетенцииДисциплины'):
                indicators_code = abs(int(deep.attrib.get('КодКомпетенции')))

                if lines_code == int(deep.attrib.get('КодСтроки')):
                    tmp.append(indicators[indicators_code]['index'])

            temp_dict['kompetences'] = ','.join(tmp)

            lines_data[abs(lines_code)] = {}
            lines_data[abs(lines_code)].update(temp_dict)

        return lines_data

    def insert_lines_data(self, data):
        disciplines = Disciplines.objects.filter(name__in=[i['dis'] for i in data.values()])
        disciplines = {i.name: i.id for i in disciplines}

        query = Q()
        for i in data.values():
            query |= Q(plan_id=i['plan_id'], dis=i['dis'])

        lines = LinesData.objects.filter(query)
        lines = {f"{i['plan_id']}_{i['dis']}": i for i in lines.values()}

        for key, item in data.items():
            if not disciplines.get(item['dis']):
                obj = DisciplinesSerializer(data={'name': item['dis']})

                obj.is_valid(raise_exception=True)
                obj.save()

                item['disid_id'] = obj.data['id']
            else:
                item['disid_id'] = disciplines.get(item['dis'])

            if not lines.get(f"{item['plan_id']}_{item['dis']}"):
                obj = LinesDataSerializer(data=item)

                obj.is_valid(raise_exception=True)
                obj.save()

                item['id'] = obj.data['id']
            else:
                data[key] = lines.get(f"{item['plan_id']}_{item['dis']}")

        return data

    def get_semester_data(self, root):

        data = {}

        for child in root.findall(self.path + 'ПланыНовыеЧасы'):
            num = 0

            if int(child.attrib.get('Семестр')) == 0:
                continue
            if int(child.attrib.get('Курс')) == 0:
                continue

            if abs(int(child.attrib.get('КодТипаЧасов'))) != 3:
                num = 0
                if int(child.attrib.get('Семестр')) > 0:
                    num = (int(child.attrib.get('Курс')) - 1) * self.semesteroncource + int(child.attrib.get('Семестр'))

                data[abs(int(child.attrib.get('Код')))] = {
                    'planlineid_id': abs(int(child.attrib.get('КодОбъекта'))),
                    'find': False,
                    'code': abs(int(child.attrib.get('Код'))),
                    'num': num,
                    'lekc': int(child.attrib.get('Количество')) if child.attrib.get('КодВидаРаботы') == '101' else None,
                    'lab': int(child.attrib.get('Количество')) if child.attrib.get('КодВидаРаботы') == '102' else None,
                    'pr': int(child.attrib.get('Количество')) if child.attrib.get('КодВидаРаботы') == '103' else None,
                    'srs': int(child.attrib.get('Количество')) if child.attrib.get('КодВидаРаботы') == '107' else None,
                    'ekzhour': int(child.attrib.get('Количество')) if child.attrib.get('КодВидаРаботы') == '108' else None,
                    'zet': int(child.attrib.get('Количество')) if child.attrib.get('КодВидаРаботы') == '50' else None,
                    'ekz': True if child.attrib.get('КодВидаРаботы') == '1' else None,
                    'zach': True if child.attrib.get('КодВидаРаботы') == '2' else None,
                    'kp_hour': int(child.attrib.get('Количество')) if child.attrib.get('КодВидаРаботы') == '4' else None,
                    'kp': True if child.attrib.get('КодВидаРаботы') == '4' else None,
                    'kr_hour': int(child.attrib.get('Количество')) if child.attrib.get('КодВидаРаботы') == '5' else None,
                    'kr': True if child.attrib.get('КодВидаРаботы') == '5' else None,
                    'zacho': 1 if child.attrib.get('КодВидаРаботы') == '3' else None,
                    'eios': int(child.attrib.get('Количество')) if child.attrib.get('КодВидаРаботы') == '143' else None,
                }

        return data

    def insert_semester_data(self, data):

        query = Q()
        for item in data:
            query |= Q(planlineid_id=item['planlineid_id'], num=item['num'])

        semester = SemesterData.objects.filter(query)
        semester = {f"{i['planlineid_id']}_{i['num']}": i for i in semester.values()}

        result = []
        for item in data:
            if not semester.get(f"{item['planlineid_id']}_{item['num']}"):
                obj = SemesterDataSerializer(data=item)

                obj.is_valid(raise_exception=True)
                obj.save()

                result.append(obj.data)
            else:
                result.append(semester.get(f"{item['planlineid_id']}_{item['num']}"))

        return result

    def get_competences_data(self, root):
        competences_data = {}

        for child in root.findall(self.path + 'ПланыКомпетенции'):
            if self.studylevel in [4, 5]:
                competences_data[abs(int(child.attrib.get('Код')))] = {"code": child.attrib.get('Код'),
                                                                          "content": child.attrib.get('Наименование'),
                                                                          "index": child.attrib.get(
                                                                              'ШифрКомпетенции')}
            else:
                if not child.attrib.get('КодРодителя'):
                    competences_data[abs(int(child.attrib.get('Код')))] = {"code": child.attrib.get('Код'),
                                                                              "content": child.attrib.get(
                                                                                  'Наименование'),
                                                                              "index": child.attrib.get(
                                                                                  'ШифрКомпетенции')}

        return competences_data

    def get_indicators_data(self, root):
        indicators_data = {}

        for child in root.findall(self.path + 'ПланыКомпетенции'):
            if self.studylevel in [4, 5]:
                indicators_data[abs(int(child.attrib.get('Код')))] = {"code": child.attrib.get('Код'),
                                                                      "content": child.attrib.get('Наименование'),
                                                                      "index": child.attrib.get('ШифрКомпетенции'),
                                                                      }
            else:
                if child.attrib.get('КодРодителя'):
                    indicators_data[abs(int(child.attrib.get('Код')))] = {"code": child.attrib.get('Код'),
                                                                          "content": child.attrib.get('Наименование'),
                                                                          "index": child.attrib.get('ШифрКомпетенции'),
                                                                          "КодРодителя": abs(int(child.attrib.get('КодРодителя')))}

        return indicators_data

    def get_lines_ind_comp_bind_data(self, root):
        ind_comp_bind_data = {}

        for child in root.findall(self.path + 'ПланыКомпетенцииДисциплины'):
            ind_comp_bind_data[abs(int(child.attrib.get('Код')))] = {
                "КодКомпетенции": abs(int(child.attrib.get('КодКомпетенции'))),
                "КодСтроки": abs(int(child.attrib.get('КодСтроки'))),
                "find": False}

        return ind_comp_bind_data

    def insert_lines_indicators(self, data):

        query = Q()

        for item in data:
            if self.studylevel in [4, 5]:
                query |= Q(planlineid_id=item['planlineid_id'], indicator_index=item['indicator_index'])
            else:
                query |= Q(planlineid_id=item['planlineid_id'], indicator_index=item['indicator_index'], competence_index=item['competence_index'])

        indicators = LinesIndicators.objects.filter(query)
        indicators = {f"{i['planlineid_id']}_{i['indicator_index']}": i for i in indicators.values()}

        result = []
        for item in data:
            if not indicators.get(f"{item['planlineid_id']}_{item['indicator_index']}"):
                obj = LinesIndicatorsSerializer(data=item)

                obj.is_valid(raise_exception=True)
                obj.save()

                result.append(obj.data)
            else:
                result.append(indicators.get(f"{item['planlineid_id']}_{item['indicator_index']}"))

        return result

    def get_documents_plan(self, data, plan_id):
        allwd_names = AllowedNames.objects.values_list('name', flat=True)
        allowed_names = [i.lower() for i in allwd_names]

        documents_data = []
        for key, items in data.items():
            for name in allowed_names:
                if items['dis'].lower().find(name) != -1:
                    continue

            if items['dis'].lower().find('практика') != -1:
                documents_data.append({
                    'name': items['dis'].capitalize(),
                    'type': items['type'],
                })

        documents_data.append({
            'name': 'Учебный план',
            'type': 5,
        })
        documents_data.append({
            'name': 'Адаптивный учебный план',
            'type': 8,
        })
        documents_data.append({
            'name': 'Календарный учебный план',
            'type': 6,
        })
        documents_data.append({
            'name': 'Программа ГИА',
            'type': 1,
        })
        documents_data.append({
            'name': 'ФОС ГИА',
            'type': 2,
        })
        documents_data.append({
            'name': 'ООП',
            'type': 7,
        })

        if self.studylevel in [1, 2, 4, 5]:
            documents_data.append({
                'name': 'Рабочая программа воспитания',
                'type': 7,
            })
            documents_data.append({
                'name': 'Образовательный стандарт ФГОС',
                'type': 10,
            })
            documents_data.append({
                'name': 'Календарный план воспитательной работы',
                'type': 7,
            })

        if self.studylevel in [3]:
            documents_data.append({
                'name': 'Образовательный стандарт ФГОС',
                'type': 10,
            })

        if self.studylevel not in [4, 5]:
            documents_data.append({
                'name': 'АОП',
                'type': 7,
            })

        if self.studylevel in [7]:
            documents_data.append({
                'name': 'Федеральные государственные требования ФГТ',
                'type': 21,
            })
            documents_data.append({
                'name': 'План научной деятельности',
                'type': 19,
            })


        query = Q()

        result = []
        for item in documents_data:
            query |= Q(plan_id=plan_id, name=item['name'])

        documents = PlanDocuments.objects.filter(query)
        documents = {f"{plan_id}_{i['name']}": i for i in documents.values()}

        for item in documents_data:
            item['plan_id'] = plan_id
            if not documents.get(f"{item['plan_id']}_{item['name']}"):
                obj = PlanDocumentsSerializer(data=item)

                obj.is_valid(raise_exception=True)
                obj.save()

                result.append(obj.data)
            else:
                result.append(documents.get(f"{item['plan_id']}_{item['name']}"))

        return result


class AISServices(object):

    @staticmethod
    @cache_function(timeout=60 * 1)
    def get_kaf_codes():
        q = """
	        SELECT ckaf2rpgen as value, name2rpgen as label FROM dbo.uchplan_kaf
	        """

        r = requests.get(f"{settings.ARIM_URL}/wizard.sql", {
            "q": q
        }, proxies={
            "http": "",
            "https": "",
        })

        data = r.json()['RecordSet']

        return data
