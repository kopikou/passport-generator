from itertools import groupby
from pprint import pprint

from django.db.models import Q
from lxml import etree

from django.core.management import BaseCommand

from rpd.models import Disciplines, LinesData, PlanData, SemesterData, LinesIndicators
from rpd.serializer import DisciplinesSerializer, LinesDataSerializer, SemesterDataSerializer, LinesIndicatorsSerializer


def parseXML(tree):
    root = tree.getroot()
    XHTML_NAMESPACE = root[0][0].nsmap[None]
    XMLNS = "{%s}" % XHTML_NAMESPACE
    path = ".//%s" % XMLNS

    parent_code = 0
    for child in root.findall(path + 'ПланыСтроки'):
        if child.attrib.get('Дисциплина') == 'Дисциплины индивидуальной образовательной траектории*':
            parent_code = child.attrib.get('Код')

    if not parent_code:
        print('Не найдена родительский элемент дисциплин ИОТ')
        return

    semesteroncource = 0
    for child in root.findall(path + 'Планы'):
        semesteroncource = int(child.attrib.get('СеместровНаКурсе'))

    discpl = []
    for child in root.findall(path + 'ПланыСтроки'):
        if child.attrib.get('КодРодителя') == parent_code:
            discpl.append(child)

    discpl_ids = [i.attrib.get('Код') for i in discpl]
    semesters_data = []
    for child in root.findall(path + 'ПланыНовыеЧасы'):
        if child.attrib.get('КодОбъекта') in discpl_ids:

            if int(child.attrib.get('Семестр')) == 0:
                continue
            if int(child.attrib.get('Курс')) == 0:
                continue

            num = 0
            if int(child.attrib.get('Семестр')) > 0:
                num = (int(child.attrib.get('Курс')) - 1) * semesteroncource + int(child.attrib.get('Семестр'))

            semesters_data.append({
                'КодОбъекта': child.attrib.get('КодОбъекта'),
                'code': abs(int(child.attrib.get('Код'))),
                'num': num,
                'lekc': int(child.attrib.get('Количество')) if child.attrib.get(
                    'КодВидаРаботы') == '101' else None,
                'lab': int(child.attrib.get('Количество')) if child.attrib.get(
                    'КодВидаРаботы') == '102' else None,
                'pr': int(child.attrib.get('Количество')) if child.attrib.get(
                    'КодВидаРаботы') == '103' else None,
                'srs': int(child.attrib.get('Количество')) if child.attrib.get(
                    'КодВидаРаботы') == '107' else None,
                'ekzhour': int(child.attrib.get('Количество')) if child.attrib.get(
                    'КодВидаРаботы') == '108' else None,
                'zet': float(child.attrib.get('Количество')) if child.attrib.get(
                    'КодВидаРаботы') == '50' else None,
                'ekz': True if child.attrib.get('КодВидаРаботы') == '1' else None,
                'zach': True if child.attrib.get('КодВидаРаботы') == '2' else None,
                'kp_hour': int(child.attrib.get('Количество')) if child.attrib.get(
                    'КодВидаРаботы') == '4' else None,
                'kp': True if child.attrib.get('КодВидаРаботы') == '4' else None,
                'kr_hour': int(child.attrib.get('Количество')) if child.attrib.get(
                    'КодВидаРаботы') == '5' else None,
                'kr': True if child.attrib.get('КодВидаРаботы') == '5' else None,
                'zacho': 1 if child.attrib.get('КодВидаРаботы') == '3' else None,
                'eios': int(child.attrib.get('Количество')) if child.attrib.get(
                    'КодВидаРаботы') == '143' else None,
            })

    semesters_data_sorted = sorted(semesters_data, key=lambda x: x.get('КодОбъекта'))
    semesters_data_grouped = {key: list(i) for key, i in
                              groupby(semesters_data_sorted, key=lambda x: x.get('КодОбъекта'))}

    semester_data_res = []
    for key, items in semesters_data_grouped.items():
        temp = {**items[0]}
        for item in items:
            temp.update({k: v for k, v in item.items() if v is not None})
        semester_data_res.append(temp)

    semester_data_res_sorted = sorted(semester_data_res, key=lambda x: x.get('КодОбъекта'))
    semester_data_res_grouped = {key: list(i) for key, i in
                                 groupby(semester_data_res_sorted, key=lambda x: x.get('КодОбъекта'))}

    indicators_data = []
    for child in root.findall(path + 'ПланыКомпетенцииДисциплины'):
        if child.attrib.get('КодСтроки') in discpl_ids:
            indicators_data.append(child)

    indicators_data_sorted = sorted(indicators_data, key=lambda x: x.attrib.get('КодСтроки'))
    indicators_data_grouped = {key: list(i) for key, i in
                               groupby(indicators_data_sorted, key=lambda x: x.attrib.get('КодСтроки'))}

    ind_data = []
    comp_data = []
    for child in root.findall(path + 'ПланыКомпетенции'):
        if child.attrib.get('КодРодителя') is None:
            comp_data.append({
                "code": child.attrib.get('Код'),
                "content": child.attrib.get('Наименование'),
                "index": child.attrib.get('ШифрКомпетенции'),
            })
        else:
            ind_data.append({
                "code": child.attrib.get('Код'),
                "content": child.attrib.get('Наименование'),
                "index": child.attrib.get('ШифрКомпетенции'),
            })

    comp_data_by_id = {i.get('code'): i for i in comp_data}

    for child in root.findall(path + 'ПланыКомпетенции'):
        if child.attrib.get('КодРодителя') is not None:
            ind_data.append({
                "code": child.attrib.get('Код'),
                "content": child.attrib.get('Наименование'),
                "index": child.attrib.get('ШифрКомпетенции'),
                "competence": comp_data_by_id[child.attrib.get('КодРодителя')]
            })

    ind_data_by_id = {i.get('code'): i for i in ind_data}

    res = []
    for i in discpl:
        temp_dict = {}

        temp_dict['dis'] = i.attrib.get('Дисциплина')
        temp_dict['newdisid'] = i.attrib.get('ДисциплинаКод')
        temp_dict['mustbesdudied'] = int(i.attrib.get('ПодлежитИзучениюЧасов')) if i.attrib.get(
            'ПодлежитИзучениюЧасов') else None
        temp_dict['hoursinzet'] = int(i.attrib.get('ЧасовВЗЕТ')) if i.attrib.get('ЧасовВЗЕТ') else None
        temp_dict['caf'] = int(i.attrib.get('КодКафедры')) if i.attrib.get('КодКафедры') else None
        temp_dict['nocalccontrol'] = True if i.attrib.get('НеСчитатьКонтроль') == 'true' else False
        temp_dict['type'] = int(i.attrib.get('ТипОбъекта')) if i.attrib.get('ТипОбъекта') else None
        temp_dict['viewpract'] = int(i.attrib.get('ВидПрактики')) if i.attrib.get('ВидПрактики') else None
        temp_dict['viewobject'] = int(i.attrib.get('ВидОбъекта')) if i.attrib.get('ВидОбъекта') else None
        temp_dict['parent_id'] = None
        temp_dict['old_parent_id'] = None

        tmp = []
        for j in indicators_data_grouped.get(i.attrib.get('Код')):
            tmp.append(ind_data_by_id[j.attrib.get('КодКомпетенции')])

        temp_dict['kompetences'] = ','.join([i['index'] for i in tmp])
        temp_dict['indicators_data'] = tmp

        temp_dict['semesters'] = semester_data_res_grouped.get(i.attrib.get('Код'))

        res.append(temp_dict)

    return res


class Command(BaseCommand):
    help = "Перенос данных о планах (план, дисциплины, семестры) из системы в АИС"

    def handle(self, *args, **options):
        XMLNS = ""
        path = ""
        parser = etree.XMLParser(encoding='UTF-8')

        file_path = "uploads/ИОТ.plx"
        with open(file_path, "r", encoding="UTF-16") as file:
            data = parseXML(etree.parse(file, parser=parser))


        plans = PlanData.objects.filter(studylevel='Аспирантура')

        disciplines = Disciplines.objects.filter(name__in=[i['dis'] for i in data])
        disciplines = {i.name: i.id for i in disciplines}
        for plan in plans:

            query = Q()
            for i in data:
                query |= Q(plan_id=plan.id, dis=i['dis'], newdisid=i['newdisid'])

            lines = LinesData.objects.filter(query)
            lines = {f"{plan.id}_{i['dis']}_{i['newdisid']}": i for i in lines.values()}

            for item in data:
                if not disciplines.get(item['dis']):
                    obj = DisciplinesSerializer(data={'name': item['dis']})

                    obj.is_valid(raise_exception=True)
                    obj.save()

                    item['disid_id'] = obj.data['id']
                else:
                    item['disid_id'] = disciplines.get(item['dis'])

                if not lines.get(f"{plan.id}_{item['dis']}_{item['newdisid']}"):
                    obj = LinesDataSerializer(data={**item, "plan_id": plan.id, "synchronize": True})

                    obj.is_valid(raise_exception=True)
                    obj.save()

                    item['id'] = obj.data['id']
                else:
                    item['id'] = lines.get(f"{plan.id}_{item['dis']}_{item['newdisid']}")['id']


            query = Q()
            for item in data:
                for i in item['semesters']:
                    query |= Q(planlineid_id=item['id'], num=i['num'])

            semester = SemesterData.objects.filter(query)
            semester = {f"{i['planlineid_id']}_{i['num']}": i for i in semester.values()}

            result = []
            for item in data:
                for i in item['semesters']:
                    if not semester.get(f"{item['id']}_{i['num']}"):
                        obj = SemesterDataSerializer(data={**i, "planlineid_id": item['id']})

                        obj.is_valid(raise_exception=True)
                        obj.save()

                        result.append(obj.data)
                    else:
                        result.append(semester.get(f"{item['id']}_{i['num']}"))

            query = Q()
            for item in data:
                for i in item['indicators_data']:
                    query |= Q(planlineid_id=item['id'], indicator_index=i['index'],
                               competence_index=i['competence']['index'])

            indicators = LinesIndicators.objects.filter(query)
            indicators = {f"{i['planlineid_id']}_{i['indicator_index']}": i for i in indicators.values()}

            result = []
            for item in data:
                for i in item['indicators_data']:
                    if not indicators.get(f"{item['id']}_{i['index']}"):
                        obj = LinesIndicatorsSerializer(data={
                            "planlineid_id": item['id'],
                            "competence_index": i['competence']['index'],
                            "competence":  i['competence']['content'],
                            "indicator_index": i['index'],
                            "indicator": i['content'],
                        })

                        obj.is_valid(raise_exception=True)
                        obj.save()

                        result.append(obj.data)
                    else:
                        result.append(indicators.get(f"{item['id']}_{i['index']}"))




