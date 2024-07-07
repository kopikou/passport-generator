import os.path
from datetime import datetime

from django.conf import settings
from urllib.parse import unquote
from lxml import etree
import re

from rpd.models import PlanData
from rpd.serializer import PlanDataSerializer


class PLXParser:

    XMLNS = ""
    path = ""

    fileNameRegex = r"([А-я]*)-(\d*)"
    parser = etree.XMLParser(encoding='UTF-8')

    semesteroncource = None
    studylevel = None

    fileId = None

    def __init__(self, filePath, file_id):
        with open((os.path.join(settings.BASE_DIR)) + unquote(filePath), "r", encoding="utf-16") as f:
            self.parseXML(etree.parse(f, parser=self.parser), file_id)

    def parseXML(self, tree, file_id):
        self.fileId = file_id
        root = tree.getroot()

        XHTML_NAMESPACE = root[0][0].nsmap[None]
        self.XMLNS = "{%s}" % XHTML_NAMESPACE
        self.path = ".//%s" % self.XMLNS

        plnData = self.get_plan_data(root)
        planData = self.insert_plan_data(plnData)

        print(planData)

        indikators_data = self.get_indicators_data(root)
        competences_data = self.get_competences_data(root)

        # lines_data = self.get_lines_data(root)

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
            planData['kafcode'] = int(child.attrib.get('КодПрофКафедры'))
            planData['startyear'] = int(child.attrib.get('ГодНачалаПодготовки'))
            planData['dviga'] = True if child.attrib.get('ДвИГА') == 'true' else False
            planData['gviga'] = True if child.attrib.get('ГвИГА') == 'true' else False
            planData['igazetweek'] = float(child.attrib.get('ЧасовВКредите'))
            planData['igahourzet'] = float(child.attrib.get('ЗЕТвНеделю'))
            planData['semesteroncource'] = int(child.attrib.get('СеместровНаКурсе'))
            self.semesteroncource = int(child.attrib.get('СеместровНаКурсе'))
            planData['gosdate'] = datetime.fromisoformat((child.attrib.get('ДатаГОСа'))).strftime(
                "%Y-%m-%d") if child.attrib.get('ДатаГОСа') else None
            planData['gostype'] = int(child.attrib.get('ТипГОСа'))
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
            obj = PlanData.objects.get(file_id=self.fileId)
        except:
            obj = PlanDataSerializer(data=data)

            obj.is_valid(raise_exception=True)
            obj.save()

        return data

    def get_lines_data(self, root, plan_id, indicators):
        pass

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
            if self.studylevel in [4,5]:
                indicators_data[abs(int(child.attrib.get('Код')))] = {"code": child.attrib.get('Код'),
                                                                      "content": child.attrib.get('Наименование'),
                                                                      "index": child.attrib.get('ШифрКомпетенции'),
                                                                      "КодРодителя": child.attrib.get('КодРодителя')}
            else:
                if child.attrib.get('КодРодителя'):
                    indicators_data[abs(int(child.attrib.get('Код')))] = {"code": child.attrib.get('Код'),
                                                                          "content": child.attrib.get('Наименование'),
                                                                          "index": child.attrib.get('ШифрКомпетенции'),
                                                                          "КодРодителя": child.attrib.get(
                                                                              'КодРодителя')}

        return indicators_data

