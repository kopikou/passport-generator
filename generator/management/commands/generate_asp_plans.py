import pendulum
from django.core.management import BaseCommand
from django.db.models import Q
from tqdm import tqdm

from app.utils import RPGEN, Mira, shortify_name
from arim.models import CatPerson
from generator.models import PlanLinesLink, ScientificData
from generator.services import ReportService
from generator.services.generator_service import GeneratorService
from rpgen.models import AspPlan, AspParamValue


class Command(BaseCommand):
    query_insert_plan = 'INSERT INTO asp_plan (admis_id, plan_id, start_date, edit_date, author_id) VALUES ($1, $2, $3, $3, $4) RETURNING id'
    query_insert_value = 'INSERT INTO asp_param_value (plan_id, type_id, value) VALUES ($1, $2, $3) RETURNING id'
    query_insert_value_sort = 'INSERT INTO asp_param_value (plan_id, type_id, value, sort) VALUES ($1, $2, $3, $4) RETURNING id'
    query_insert_2value = 'INSERT INTO asp_param_value (plan_id, type_id, value, linked_id, sort) VALUES ($1, $2, $3, $4, $5)'
    query_select_param_types = 'SELECT * FROM asp_param_type'
    query_select_params = 'SELECT * FROM asp_param_value WHERE plan_id = $1 order by type_id, linked_id, sort, id'
    query_select_r2p_values = '''SELECT mi.index, mi.content
		FROM mleha_planindikator mpi
			JOIN mleha_planlines mpl ON mpi.planlineid=mpl.id
			JOIN mleha_indikator mi ON mi.id=mpi.indikid
		WHERE mpl.planid=$1 AND mi.index LIKE \'Р-2%\' ORDER BY mi.index'''
    query_select_r2_value = '''SELECT mc.index, mc.content
		FROM mleha_plancompetence mpc
			JOIN mleha_planlines mpl ON mpc.planlineid=mpl.id
			JOIN mleha_competences mc ON mc.id=mpc.competenceid
		WHERE mpl.planid=$1 AND mc.index LIKE \'Р-2%\' ORDER BY mc.index'''
    query_update_plan_id = 'UPDATE asp_plan SET plan_id = $2 WHERE plan_id=$1'
    query_update_values_plan_id = 'UPDATE asp_param_value SET plan_id = $2 WHERE plan_id = $1'


    def generate_for_admission_id(self, cadmission_id):
        result = RPGEN.fetch("SELECT * FROM asp_plan WHERE admis_id=%s", [cadmission_id])
        # if result:
        #     return

        mira_plan = Mira.fetch_one_or_none("""
SELECT (select name from catperson where id=p.cperson) as rukovod, datediff(year, a.datebegin, a.dateend) as duration, k.name as kaf, k.zav, f.name as fac, f.dean, p.* 
FROM uchplan_plan p 
       JOIN catkaf k on k.id=p.ckaf 
       join catfaculty f on f.id = k.cfac
       join catadmission a on a.id = p.cadmission 
where cadmission=%s and fordel='f'
        """, [cadmission_id])

        if not mira_plan or not mira_plan['rukovod']:
            return

        now = pendulum.now()

        plan, updated = AspPlan.objects.update_or_create(
            admis_id=mira_plan['cadmission'],
            defaults=dict(
                plan_id=mira_plan['id'],
                start_date=now,
                edit_date=now,
                author_id=mira_plan['cperson'],
            )
        )

        prorektor = CatPerson.objects.filter(doljnost_nauch__contains='Проректор по учебной работе').first()

        basic_data = {
			'2': mira_plan['species'],
			'3': mira_plan['kaf'],
			'4': mira_plan['fac'],
			'5': mira_plan['duration'],
			'6': mira_plan['studyform'],
			'7': mira_plan['startyear'],
			'8': '№ 951 от 20.10.2021',
			'9': shortify_name(prorektor.name),
			'10': shortify_name(mira_plan['dean']),
			'11': shortify_name(mira_plan['zav']),
			'12': shortify_name(mira_plan['rukovod']),
			'13': pendulum.now().year
        }

        for key, value in basic_data.items():
            AspParamValue.objects.update_or_create(
                type_id=key,
                plan_id=mira_plan['id'],
                defaults={
                "value":value,
                }
            )

        scientific_data = list(ScientificData.objects.filter(
            plan__mira_id=mira_plan['id'],
        ))
        scientific_data_grouped = {}
        for i in scientific_data:
            if i.parameters['part'] == 0:
                sem_item = scientific_data_grouped.setdefault(i.parameters['part'], {})
                sem_item.setdefault(i.parameters['semester'], []).append(i)
            else:
                scientific_data_grouped.setdefault(i.parameters['part'], []).append(i)

        for part in [0,1,2]:
            if part == 0:
                for sem, items in scientific_data_grouped[part].items():
                    param, created = AspParamValue.objects.get_or_create(
                        type_id=15,
                        value=sem,
                        plan_id=mira_plan['id'],
                    )

                    for i in items:
                        AspParamValue.objects.get_or_create(
                            type_id=16,
                            value=i.text,
                            plan_id=mira_plan['id'],
                            linked_id=param.id,
                        )
            elif part == 1:
                for item in scientific_data_grouped[part]:
                    param, created = AspParamValue.objects.get_or_create(
                        type_id=17,
                        value=item.text,
                        plan_id=mira_plan['id'],
                        sort=item.parameters['order'],
                    )
            elif part == 2:
                for item in scientific_data_grouped[part]:
                    param, created = AspParamValue.objects.get_or_create(
                        type_id=18,
                        value=item.text,
                        plan_id=mira_plan['id'],
                        sort=item.parameters['order'],
                    )


    def handle(self, *args, **options):
        ids=[
            25166,
            25167,
            25168,
            25169,
            25170,
            25171,
            25172,
            25173,
            25174,
            25175,
            25176,
            25177,
            25178,
            25179,
            25180,
            25181,
            25182,
            25183,
            25184,
            25185,
            25186,
            25187,
            25188,
            25189,
            25190,
            25192,
            25193,
            25194,
            25195,
            25196,
            25197,
            25198,
            25199,
            25200,
            25201,
            25202,
            25203,
            25204,
            25205,
            25206,
            25209,
            25211,
            25212,
            25213,
            25214,
            25215,
            25216,
            25217,
            25218,
            25219,
            25220,
            25224,
            25225,
        ]
        for i in ids:
            self.generate_for_admission_id(i)
"""
	$result = pg_query_params($query_select_plans, [$admiss_id]);

	if (pg_num_rows($result) == 0) {
	
		$result = pg_query_params($query_insert_plan, [$mira_plan['cadmission'], $mira_plan['id'], date_create()->format('c'), $mira_plan['cperson']]);
		$aspplanid = (pg_fetch_array($result))['id'];
		$prorektor = getMIRA('wizard.sql', ['q' => "select name from catperson where doljnost_nauch like '%Проректор по учебной работе%'"])['RecordSet'][0];
		
		
	
		$srplan[1]= [
			'Ознакомление с тематикой исследовательских работ в выбранной области',
			'Определение направления и темы исследования',
			'Формулировка обоснования темы исследования (актуальность, новизна, гипотеза и т. д.)',
			'Формулировка рабочих гипотез исследования',
			'Поиск теоретической научной базы исследования',
			'Изучение источников литературы по теме исследования'
		];
		$srplan[2] = [
			'Формулировка характеристики современного состояния изучаемой проблемы',
			'Разработка основных направлений теоретической концепции научного исследования',
			'Анализ основных результатов и положений, полученных ведущими специалистами в области проводимого исследования, оценка их применимости в рамках исследования',
			'Разработка программы и инструментария собственного исследования, подбор методов исследования'
		];
		$srplan[$mira_plan['duration']*2-1] = [
			'Анализ, оценка и интерпретация результатов',
			'Апробация и внедрение разработанных методик (методов), оборудования'
		];
		$srplan[$mira_plan['duration']*2] = [
			'Оформление текста диссертации в соответствии с требованиями Р 7.0.11 – 2011. Диссертация и автореферат диссертации',
			'Оформление автореферата и подготовка доклада по результатам исследования в соответствии с требованиями ГОСТ 7.0.11 – 2011'
		];
		foreach ($srplan as $key => $value) {
			$result = pg_query_params($query_insert_value, [$mira_plan['id'], 15, $key]);
			$id = (pg_fetch_array($result))['id'];
			if (!empty($value)) {
				foreach ($value as $kv => $v) {
					pg_query_params($query_insert_2value, [$mira_plan['id'], 16, $v, $id, $kv]);
				}
			}
		}
		$dpplan = [
			'Выбор тематики диссертационного исследования',
			'Анализ соответствия тематики диссертационного исследования современным тенденциям в науке и паспорту специальности',
			'Формирование списка литературы, соответствующего тематике диссертационного исследования',
			'Анализ теоретических источников диссертационного исследования (статьи, монографии, диссертации) по теме исследования',
			'Формулировка цели, задач исследования, предмета и объекта исследования, выбор и обоснование методов исследования',
			'Формулировка гипотезы и научной идеи, положений научной новизны, теоретической и практической значимости работы',
			'Определение понятийного аппарата диссертационного исследования',
			'Подготовка раздела диссертации «Введение»',
			'Подготовка части главы диссертации об объектах и методах исследования',
			'Оформление части главы по результатам аналитических и иных исследований объекта исследований',
			'Выводы и рекомендации из теоретико-методологического раздела диссертационного исследования',
			'Подготовка главы по теоретическому обоснованию проводимых исследований',
			'Выбор вида теоретической/технической модели, соответствующей теме диссертации',
			'Описание математической модели объекта/предмета научного исследования, соответствующей теме диссертации',
			'Подготовка главы, посвященной выбору метода математического моделирования',
			'Анализ и обработка экспериментальных данных, работа над экспериментальной главой диссертации',
			'Оформление главы диссертации по результатам эксперимента',
			'Подготовка главы диссертации с описанием основных результатов исследования',
			'Подготовка раздела диссертации «Заключение»',
			'Оформление списка использованных источников и литературы диссертационного исследования в соответствии с требованиями ГОСТ',
			'Оформление текста диссертации и автореферата в соответствии с требованиями ВАК и ГОСТ ',
			'Визуализация материалов диссертационного исследования (оформление приложений, создание презентации диссертационного исследования)',
			'Работа с рецензентами'
		];
		foreach ($dpplan as $key => $value) {
			pg_query_params($query_insert_value_sort, [$mira_plan['id'], 17, $value, $key]);
		}
		$ppplan = [
			'Составление списка научных журналов, в которых публикуются результаты исследований по тематике диссертации',
			'Подготовка заявок на патенты на изобретения, полезные модели, промышленные образцы, селекционные достижения, свидетельства о государственной регистрации программ для электронных вычислительных машин, баз данных, топологий интегральных микросхем (подготовка публикаций и (или) заявок на патенты на изобретения и другие виды интеллектуальной собственности)',
			'Подготовка и публикация доклада в материалах всероссийской конференции',
			'Подготовка и публикация доклада в материалах международной конференции',
			'Подготовка и публикация статьи в рецензируемых научных изданиях, входящих в перечень изданий, рекомендованных высшей аттестационной комиссии при Министерстве науки и высшего образования Российской Федерации',
			'Подготовка и публикация статьи в рецензируемых научных изданиях (научная база РИНЦ)',
			'Подготовка и публикация статьи в рецензируемых научных изданиях, индексируемых в наукометрической базе данных Russian Science Citation Index (RSCI)',
			'Подготовка к публикации статьи в рецензируемых научных изданиях, индексируемых в международных базах данных Web of Science и Scopus '
		];
		foreach ($ppplan as $key => $value) {
			pg_query_params($query_insert_value_sort, [$mira_plan['id'], 18, $value, $key]);
		}
		return getDataLocal($admiss_id)
"""