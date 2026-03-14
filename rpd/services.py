import codecs
import os.path
from builtins import enumerate
from datetime import datetime
from itertools import groupby
from tempfile import NamedTemporaryFile

import requests
from django.conf import settings
from urllib.parse import unquote

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.db.models import Q
from lxml import etree
import re

from rpd.models import PlanData, LinesData, Disciplines, SemesterData, LinesIndicators, ExceptionNames, AllowedNames, \
    PlanDocuments, BaseDocuments, DocumentsTypes, RPDFile
from rpd.serializer import PlanDataSerializer, DisciplinesSerializer, LinesDataSerializer, SemesterDataSerializer, \
    LinesIndicatorsSerializer, PlanDocumentsSerializer
from competence_passport.models import Scheme, Competence
from competence_passport.serializer import SchemeSerializer, CompetenceFullSerializer
from app.utils import cache_function, RPGEN


class RPDGenSerivce:

    @staticmethod
    def get_asp_plan(id):
        query = "SELECT * FROM asp_param_value where plan_id = %s and type_id in (15, 16, 17, 18) order by type_id"

        data = RPGEN.fetch(query, [id])

        return data

    @staticmethod
    def get_current_control():
        query = "SELECT * FROM cl$current_control"

        data = RPGEN.fetch(query)

        return data

    @staticmethod
    def get_kind_srs():
        query = "SELECT * FROM cl$kindsrs"

        data = RPGEN.fetch(query)

        return data

    @staticmethod
    def get_rpd_line(id):
        query = "SELECT * FROM cattitle where cplanlines = %s and delete = 'f'"

        data = RPGEN.fetch(query, [id])

        return data

    @staticmethod
    def get_displ2semestr(id):
        query = "SELECT * FROM discpl2semestr where ctitle = %s"

        data = RPGEN.fetch(query, [id])

        return data

    @staticmethod
    def get_displ2lek(id):
        query = "SELECT * FROM discpl2lek where cdiscpl2semestr = %s"

        data = RPGEN.fetch(query, [id])

        return data

    @staticmethod
    def get_displ2sam(id):
        query = "SELECT * FROM discpl2sam where cdiscpl2lek = %s"

        data = RPGEN.fetch(query, [id])

        return data

    @staticmethod
    def get_displ2pract(id):
        query = "SELECT * FROM discpl2pract where cdiscpl2lek = %s"

        data = RPGEN.fetch(query, [id])

        return data

    @staticmethod
    def get_displ2lab(id):
        query = "SELECT * FROM discpl2lab where cdiscpl2lek = %s"

        data = RPGEN.fetch(query, [id])

        return data

    @staticmethod
    def get_mleha_planindikator(id):
        query = "SELECT * FROM mleha_planindikator where planlineid = %s"

        data = RPGEN.fetch(query, [id])

        return data

    @staticmethod
    def get_mleha_indikator(id):
        query = "SELECT * FROM mleha_indikator where id = %s"

        data = RPGEN.fetch(query, [id])

        return data


class PLXParser:
    study_prog = {
        1: 'подготовка специалистов',
        2: 'подготовка бакалавров',
        3: 'подготовка магистров',
        4: 'подготовка СПО',
        5: 'подготовка СПО',
        7: 'подготовка аспирантов',
    }


    fileNameRegex = r"([А-я]*)-(\d*)"
    parser = etree.XMLParser(encoding='UTF-8')


    def __init__(self, filePath, file_id=None):
        self.data = {}
        self.filePath = filePath
        self.file_id = file_id

        self.semesteroncource = None
        self.studylevel = None

        self.XMLNS = ""
        self.path = ""

        if isinstance(filePath, InMemoryUploadedFile) or isinstance(filePath, TemporaryUploadedFile):
            with NamedTemporaryFile(delete=False) as f:
                f.write(filePath.read())
                f.close()

                with open(f.name, "r", encoding="utf-16") as f:
                    self.tree = etree.parse(f, parser=self.parser)

            filePath.seek(0)
        else:
            with open((os.path.join(settings.BASE_DIR)) + unquote(self.filePath), "r", encoding="utf-16") as f:
                self.tree = etree.parse(f, parser=self.parser)

        self.root = self.tree.getroot()

        XHTML_NAMESPACE = self.root[0][0].nsmap[None]
        self.XMLNS = "{%s}" % XHTML_NAMESPACE
        self.path = ".//%s" % self.XMLNS

    def get_result_data(self):
        return self.data

    def update_db(self):
        if not self.file_id:
            return

        allwd_names = AllowedNames.objects.values_list('name', flat=True)
        allowed_names = [i.lower() for i in allwd_names]

        except_names = ExceptionNames.objects.values_list('name', flat=True)
        exception_names = [i.lower() for i in except_names]

        planData_result = []
        plnData = self.get_plan_data()
        planData = self.insert_plan_data(plnData)
        planData_result.append(planData)

        self.data['plan'] = planData_result

        if self.studylevel not in [4, 5]:
            competences_data = self.get_competences_data()

        indikators_data = self.get_indicators_data()

        lnsdata = self.get_lines_data(planData['id'], indikators_data)

        for key, item in lnsdata.items():

            if item['mustbesdudied'] == 0:
                lnsdata[key]['synchronize'] = False

            if item['type'] == 1 and not item['parent_id']:
                lnsdata[key]['synchronize'] = False

            if item['type'] in [5, 6]:
                lnsdata[key]['synchronize'] = False

            if item['type'] == 3:

                if self.studylevel == 7:
                    if item['viewpract'] not in [6, 7, 72]:
                        lnsdata[key]['synchronize'] = False
                else:
                    if item['viewpract'] not in [6, 7, 72, 8]:
                        lnsdata[key]['synchronize'] = False


        # Убрано, добавляем практику в РПД генератор
        # for key, item in lnsdata.items():
        #     for name in exception_names:
        #         if item['dis'].lower().find(name) != -1:
        #             lnsdata[key]['synchronize'] = False
        #
        #     for name in allowed_names:
        #         if item['dis'].lower().find(name) != -1:
        #             lnsdata[key]['synchronize'] = True

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

        lines_indicators = self.get_lines_ind_comp_bind_data()
        semester_data = self.get_semester_data()

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

        plan_files = self.get_documents_plan(lines_data, planData['id'], allowed_names)
        self.data['documents'] = plan_files

        # relations_data = self.get_competence_relations_data(planData['id'])
        # self.insert_competence_relations_data(relations_data)
        competence_data = self.get_competence_data(plan_id=planData['id'], lines_indicators=lines_indicators_res)
        self.insert_competence_data(competence_data)

        scheme_data = self.get_scheme_data(plan_id=planData['id'], lines_data=lines_data, semester_data=semester_data_res, lines_indicators=lines_indicators_res)
        self.insert_scheme_data(scheme_data)




    def get_plan_data(self):

        planData = {}

        planData['subtype'] = "Рабочий учебный план"
        planData['shifr'] = "SKYF"
        planData['studyform'] = self.root.attrib['КодФормыОбучения']  # модифицировать
        planData['studylevel'] = self.root.attrib.get('КодУровняОбразования')  # модифицировать
        self.studylevel = int(self.root.attrib.get('КодУровняОбразования'))
        planData['studyprog'] = self.study_prog[int(self.root.attrib.get('КодУровняОбразования'))]
        planData['elementsinweek'] = int(self.root.attrib['ЭлементовВНеделе'])
        planData['faculty'] = ''

        for child in self.root.findall(self.path + 'Планы'):
            # print(child.tag.strip(self.XMLNS), child.attrib)

            planData['species'] = child.attrib.get('Титул').rstrip().replace("\r\n", " ")
            planData['usernum'] = int(child.attrib.get('НомерПользователя'))
            planData['whoratif'] = child.attrib.get('ПланОдобрен', '-')

            planData['planname'] = child.attrib.get('ИмяФайла')
            planData['kafcode'] = int(child.attrib.get('КодПрофКафедры')) if child.attrib.get('КодПрофКафедры') else None
            planData['startyear'] = int(child.attrib.get('ГодНачалаПодготовки'))
            planData['dviga'] = True if child.attrib.get('ДвИГА') == 'true' else False
            planData['gviga'] = True if child.attrib.get('ГвИГА') == 'true' else False
            planData['igazetweek'] = float(child.attrib.get('ЧасовВКредите'))
            planData['igahourzet'] = float(child.attrib.get('ЗЕТвНеделю'))
            planData['semesteroncource'] = int(child.attrib.get('СеместровНаКурсе'))
            self.semesteroncource = int(child.attrib.get('СеместровНаКурсе'))
            planData['gosdocument'] = child.attrib.get('НомерФГОС') if child.attrib.get('НомерФГОС') else None
            planData['gostype'] = float(child.attrib.get('ТипГОСа'))
            planData['gosdate'] = datetime.fromisoformat((child.attrib.get('ДатаГОСа'))).strftime(
                "%Y-%m-%d") if child.attrib.get('ДатаГОСа') else None
            planData['gostype'] = float(child.attrib.get('ТипГОСа'))
            planData['napr_t'] = child.attrib.get('Титул').rstrip().replace("\r\n", " ")
            try:
                planData['abbrprofile'] = re.search(self.fileNameRegex, child.attrib.get('ИмяФайла').replace("_", "-"))[1]
            except:
                planData['abbrprofile'] = None

        # for child in self.root.findall(self.path + 'ПланыПрофили'):
        #     planData['cvalif'] = child.attrib.get('Квалификация')

        for child in self.root.findall(self.path + 'ООП'):
            if not child.attrib.get('КодРодительскогоООП'):
                planData['lastshifr'] = child.attrib.get('Шифр')
                planData['naprcode'] = child.attrib.get('Шифр')
                planData['napr_e'] = child.attrib.get('Название')

        for child in self.root.findall(self.path + 'Филиалы'):
            planData['vuzname'] = child.attrib['Полное_название']
            planData['head'] = child.attrib['Директор']

        for child in self.root.findall(self.path + 'Факультеты'):
            planData['faculty'] = child.attrib['Факультет']

        for child in self.root.findall(self.path + 'ФормаОбучения'):
            if child.attrib.get('Код') == planData['studyform']:
                planData['studyform'] = child.attrib.get('ФормаОбучения')
                break

        for child in self.root.findall(self.path + 'Уровень_образования'):
            if child.attrib.get('Код_записи') == planData['studylevel']:
                planData['studylevel'] = child.attrib.get('Уровень')
                break

        for child in self.root.findall(self.path + 'УровеньОбразования'):
            if child.attrib.get('Код') == planData['studyprog']:
                planData['studyprog'] = child.attrib.get('Уровень')
                break

        return planData

    def insert_plan_data(self, data):
        data['file_id'] = self.file_id

        instance = PlanData.objects.filter(
            abbrprofile=data['abbrprofile'],
            startyear=data['startyear'],
        ).first()

        obj = PlanDataSerializer(instance=instance, data=data)
        obj.is_valid(raise_exception=True)
        obj.save()

        RPDFile.objects.filter(id=self.file_id).update(plandata_id=obj.data['id'])

        data['id'] = obj.data['id']

        return data

    def get_lines_data(self, plan_id, indicators):

        lines_data = {}

        for child in self.root.findall(self.path + 'ПланыСтроки'):
            if child.attrib.get('Дисциплина'):
                temp_dict = {}
                temp_dict['plan_id'] = plan_id
                temp_dict['synchronize'] = True

                temp_dict['dis'] = child.attrib.get('Дисциплина')
                temp_dict['newdisid'] = child.attrib.get('ДисциплинаКод')
                temp_dict['mustbesdudied'] = int(child.attrib.get('ПодлежитИзучениюЧасов')) if child.attrib.get('ПодлежитИзучениюЧасов') else None
                temp_dict['hoursinzet'] = int(child.attrib.get('ЧасовВЗЕТ')) if child.attrib.get('ЧасовВЗЕТ') else None
                temp_dict['caf'] = int(child.attrib.get('КодКафедры')) if child.attrib.get('КодКафедры') else None
                temp_dict['nocalccontrol'] = True if child.attrib.get('НеСчитатьКонтроль') == 'true' else False
                temp_dict['type'] = int(child.attrib.get('ТипОбъекта')) if child.attrib.get('ТипОбъекта') else None
                temp_dict['viewpract'] = int(child.attrib.get('ВидПрактики')) if child.attrib.get('ВидПрактики') else None
                temp_dict['viewobject'] = int(child.attrib.get('ВидОбъекта')) if child.attrib.get('ВидОбъекта') else None
                temp_dict['parent_id'] = abs(int(child.attrib.get('КодРодителя'))) if child.attrib.get('КодРодителя') else None
                temp_dict['old_parent_id'] = abs(int(child.attrib.get('КодРодителя'))) if child.attrib.get('КодРодителя') else None

                lines_code = int(child.attrib.get('Код'))

                tmp = []
                for deep in self.root.findall(self.path + 'ПланыКомпетенцииДисциплины'):
                    indicators_code = abs(int(deep.attrib.get('КодКомпетенции')))

                    if lines_code == int(deep.attrib.get('КодСтроки')) and indicators_code in indicators:
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
            query |= Q(plan_id=i['plan_id'], dis=i['dis'].strip(), newdisid=i['newdisid'].strip())

        lines = LinesData.objects.filter(query)
        lines = {f"{i.plan_id}_{i.dis}_{i.newdisid}": i for i in lines}
        added_items = []

        for key, item in data.items():
            if not disciplines.get(item['dis']):
                obj = DisciplinesSerializer(data={'name': item['dis']})

                obj.is_valid(raise_exception=True)
                obj.save()

                item['disid_id'] = obj.data['id']
            else:
                item['disid_id'] = disciplines.get(item['dis'])

            key = f"{item['plan_id']}_{item['dis'].strip()}_{item['newdisid'].strip()}"
            if not lines.get(key):
                print(key)
            obj = LinesDataSerializer(instance=lines.get(key), data=item)
            obj.is_valid(raise_exception=True)
            obj.save()

            item['id'] = obj.data['id']
            item['old_parent_id'] = item['parent_id']
            added_items.append(item['id'])

        for key, items in data.items():
            if items['parent_id']:
                LinesData.objects.filter(id=items['id']).update(parent_id=data.get(items['old_parent_id'])['id'])

        ids_to_delete = [i.id for i in LinesData.objects.filter(plan__file_id=self.file_id) if i.id not in added_items]

        if data:
            if ids_to_delete:
                LinesData.objects.filter(id__in=ids_to_delete).delete()

        return data

    def get_semester_data(self):

        data = {}

        for child in self.root.findall(self.path + 'ПланыНовыеЧасы'):
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
                    'zet': float(child.attrib.get('Количество')) if child.attrib.get('КодВидаРаботы') == '50' else None,
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
        semester = {f"{i.planlineid_id}_{i.num}": i for i in semester}

        result = []
        ids_to_keep = []
        for item in data:
            key = f"{item['planlineid_id']}_{item['num']}"
            obj = SemesterDataSerializer(instance=semester.get(key), data=item)

            obj.is_valid(raise_exception=True)
            obj.save()

            result.append(obj.data)

            ids_to_keep.append(obj.data['id'])

        ids_to_delete = [i.id for i in semester.values() if i.id not in ids_to_keep]

        if data:
            if ids_to_delete:
                SemesterData.objects.filter(id__in=ids_to_delete).delete()

        return result

    def get_competences_data(self):
        competences_data = {}

        for child in self.root.findall(self.path + 'ПланыКомпетенции'):
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

    def get_indicators_data(self):
        indicators_data = {}

        for child in self.root.findall(self.path + 'ПланыКомпетенции'):
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

    def get_lines_ind_comp_bind_data(self):
        ind_comp_bind_data = {}

        for child in self.root.findall(self.path + 'ПланыКомпетенцииДисциплины'):
            ind_comp_bind_data[abs(int(child.attrib.get('Код')))] = {
                "КодКомпетенции": abs(int(child.attrib.get('КодКомпетенции'))),
                "КодСтроки": abs(int(child.attrib.get('КодСтроки'))),
                "find": False,}

        return ind_comp_bind_data

    def insert_lines_indicators(self, data):

        query = Q()

        for item in data:
            if self.studylevel in [4, 5]:
                query |= Q(planlineid_id=item['planlineid_id'], indicator_index=item['indicator_index'])
            else:
                query |= Q(planlineid_id=item['planlineid_id'], indicator_index=item['indicator_index'], competence_index=item['competence_index'])

        indicators = LinesIndicators.objects.filter(query)
        indicators = {f"{i.planlineid_id}_{i.indicator_index}": i for i in indicators}

        result = []
        ids_to_keep = []
        for item in data:
            key = f"{item['planlineid_id']}_{item['indicator_index']}"
            obj = LinesIndicatorsSerializer(instance=indicators.get(key), data=item)

            obj.is_valid(raise_exception=True)
            obj.save()

            result.append(obj.data)
            ids_to_keep.append(obj.data['id'])

        if data:
            ids_to_delete = [i.id for i in indicators.values() if i.id not in ids_to_keep]
            if ids_to_delete:
                LinesIndicators.objects.filter(id__in=ids_to_delete).delete()

        return result

    def get_documents_plan(self, data, plan_id, allowed_names):

        documents_data = []
        # Убрано, добавляем практика будет заполняться через РПД генератор
        # for key, items in data.items():
        #     for name in allowed_names:
        #         if items['dis'].lower().find(name) != -1:
        #             continue
        #
        #     if items['dis'].lower().find('практика') != -1:
        #         documents_data.append({
        #             'name': items['dis'].capitalize(),
        #             'type': items['type'],
        #             'synchronize': True,
        #         })

        query = Q()
        if self.studylevel == 1:
            query = Q(specialist=True)
        elif self.studylevel == 2:
            query = Q(bachelor=True)
        elif self.studylevel == 3:
            query = Q(magistrate=True)
        elif self.studylevel in [4, 5]:
            query = Q(spo=True)
        elif self.studylevel == 7:
            query = Q(aspirant=True)

        base_documents = BaseDocuments.objects.filter(query).values()
        document_types = {i.name: i.id for i in DocumentsTypes.objects.all()}

        for item in base_documents:
            documents_data.append({
                'name': item['name'],
                'type': item['type'],
                'new_type_id': document_types.get(f"{item['name']}"),
                'synchronize': True,
            })

        query = Q()

        result = []
        query |= Q(plan_id=plan_id)
        # for item in documents_data:
        #     query |= Q(plan_id=plan_id)

        documents = PlanDocuments.objects.filter(query).values()
        documents_by_id = {f"{plan_id}_{i['name']}": i for i in documents}

        for item in documents_data:
            item['plan_id'] = plan_id
            if not documents_by_id.get(f"{item['plan_id']}_{item['name'].strip()}"):
                obj = PlanDocumentsSerializer(data=item)

                obj.is_valid(raise_exception=True)
                obj.save()

                result.append(obj.data)
            else:
                result.append(documents_by_id.get(f"{item['plan_id']}_{item['name'].strip()}"))

        for item in documents:
            if item['manual']:
                result.append(item)

        return result
    
    def get_scheme_data(self, plan_id, lines_data, semester_data, lines_indicators):
        scheme_data = []

        # Семестры
        semesters_by_line = {}
        for sem in semester_data:
            line_id = sem.get('planlineid_id')
            if line_id not in semesters_by_line:
                semesters_by_line[line_id] = []
            semesters_by_line[line_id].append(sem)
        
        # Компетенции
        comps_by_line = {}
        for ind in lines_indicators:
            line_id = ind.get('planlineid_id')
            if line_id not in comps_by_line:
                comps_by_line[line_id] = set()
            comps_by_line[line_id].add(ind.get('competence_index'))

        # Записи схемы
        for line_key, line_item in lines_data.items():
            line_id = line_item.get('id')
            line_comps_indices = comps_by_line.get(line_id, set())

            existing_comps_map = {
                c.competence_index: c.id 
                for c in Competence.objects.filter(
                    plan_id=plan_id, 
                    competence_index__in=line_comps_indices
                )
            }

            for sem in semesters_by_line[line_id]:
                has_forms = any([
                    sem.get('ekz'), 
                    sem.get('zach'), 
                    (sem.get('zacho') and sem.get('zacho') > 0), 
                    sem.get('kp'), 
                    sem.get('kr')
                ])
                
                if not has_forms:
                    continue

                for comp_idx in line_comps_indices:
                    comp_id = existing_comps_map.get(comp_idx)

                    scheme_data.append({
                        'planlineid_id': line_id,
                        'competence_id': comp_id,
                        'competence_index': comp_idx,
                        'semester': sem.get('num'),
                        'ekz': bool(sem.get('ekz')),
                        'zach': bool(sem.get('zach')),
                        'zacho': bool(sem.get('zacho') and sem.get('zacho') > 0),
                        'kp': bool(sem.get('kp')),
                        'kr': bool(sem.get('kr'))
                    })
        return scheme_data

    def insert_scheme_data(self, data):
        discipline_ids = list(set(item['planlineid_id'] for item in data))
        competence_ids = list(set(item['competence_id'] for item in data))

        # Получаем существующие записи
        existing_schemes = Scheme.objects.filter(
                planlineid_id__in=discipline_ids,
                competence_id__in=competence_ids
        )

        existing_map = {
            (s.planlineid_id, s.competence_id, s.semester): s
            for s in existing_schemes
        }
        
        seen_keys = set()
        items_to_create = []
        items_to_update = []
        
        for item in data:
            key = (item['planlineid_id'], item['competence_index'], item['semester'])
            seen_keys.add(key)
            
            serializer_data = {
                'planlineid_id': item['planlineid_id'],
                'competence_id': item['competence_id'],
                'semester': item['semester'],
                'ekz': item['ekz'],
                'zach': item['zach'],
                'zacho': item['zacho'],
                'kp': item['kp'],
                'kr': item['kr']
            }
            
            if key in existing_map:
                serializer_data['id'] = existing_map[key].id
                items_to_update.append(serializer_data)
            else:
                items_to_create.append(serializer_data)
        
        result_ids = []

        for s_data in items_to_update:
            instance = existing_map[(s_data['planlineid_id'], s_data['competence_id'], s_data['semester'])]
            serializer = SchemeSerializer(instance=instance, data=s_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            result_ids.append(serializer.data['id'])

        for s_data in items_to_create:
            serializer = SchemeSerializer(data=s_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            result_ids.append(serializer.data['id'])

        keys_to_delete = set(existing_map.keys()) - seen_keys
        if keys_to_delete:
            ids_to_delete = [existing_map[k].id for k in keys_to_delete]
            Scheme.objects.filter(id__in=ids_to_delete).delete()
        
        return data

    
    def get_competence_data(self, plan_id, lines_indicators):
        unique_competences = {}

        for item in lines_indicators:
            c_index = item.get('competence_index')
                
            if c_index not in unique_competences:
                unique_competences[c_index] = {
                    'competence_index': c_index,
                    'competence': item.get('competence', ''),
                    'final_indicator': ''
                }
            else:
                # Поиск итогового индикатора
                ind_text = item.get('indicator', '')
                ind_idx = item.get('indicator_index', '')
                
                if 'Итоговый индикатор' in ind_idx:
                     if not unique_competences[c_index]['final_indicator']:
                         unique_competences[c_index]['final_indicator'] = ind_text

        competence_data = []
        for c_index, data in unique_competences.items():
            competence_data.append({
                'plan_id': plan_id,
                'competence_index': c_index,
                'competence': data['competence'],
                'relations': '',  # Оставляем пустым 
                'final_indicator': data['final_indicator']
            })
        
        return competence_data


    def insert_competence_data(self, data):
        plan_id = data[0]['plan_id']

        existing_competences = {
            c.competence_index: c
            for c in Competence.objects.filter(plan_id=plan_id)
        }
        
        seen_indices = set()
        
        for item in data:
            idx = item['competence_index']
            seen_indices.add(idx)

            serializer_data = {
                'plan_id': plan_id,
                'competence_index': idx,
                'competence': item['competence'],
                'final_indicator': item['final_indicator']
            }

            if idx in existing_competences:
                serializer_data['id'] = existing_competences[idx].id
                serializer_data['relations'] = existing_competences[idx].relations
            else:
                # Для новых записей relations = пустая строка
                serializer_data['relations'] = ""

            serializer = CompetenceFullSerializer(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        indices_to_delete = set(existing_competences.keys()) - seen_indices
        if indices_to_delete:
            Competence.objects.filter(
                plan_id=plan_id,
                competence_index__in=indices_to_delete
            ).delete()
        
        return data