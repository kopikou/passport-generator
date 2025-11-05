import json

DATA_KAFS_CODES = json.loads("""
[
    {
        "value": 24,
        "label": "Машиностроительный колледж университета (24)",
        "ckaf2istu": 1988516,
        "id": 1,
        "ckaf2rpgen": 24,
        "name2rpgen": "Машиностроительный колледж университета",
        "ckaf2asp": null
    },
    {
        "value": 17,
        "label": "Химико-технологический техникум (17)",
        "ckaf2istu": 1988587,
        "id": 3,
        "ckaf2rpgen": 17,
        "name2rpgen": "Химико-технологический техникум",
        "ckaf2asp": null
    },
    {
        "value": 26,
        "label": "Геологоразведочный техникум университета (26)",
        "ckaf2istu": 1988517,
        "id": 26,
        "ckaf2rpgen": 26,
        "name2rpgen": "Геологоразведочный техникум университета",
        "ckaf2asp": null
    },
    {
        "value": 101,
        "label": "Центр компетенций по анализу и управлению на основе данных (101)",
        "ckaf2istu": 1988634,
        "id": 101,
        "ckaf2rpgen": 101,
        "name2rpgen": "Центр компетенций по анализу и управлению на основе данных",
        "ckaf2asp": 0
    },
    {
        "value": 102,
        "label": "Автомобильного транспорта (102)",
        "ckaf2istu": 1988553,
        "id": 102,
        "ckaf2rpgen": 102,
        "name2rpgen": "Автомобильного транспорта",
        "ckaf2asp": 50
    },
    {
        "value": 103,
        "label": "СДМ и гидравлических систем (103)",
        "ckaf2istu": 1988530,
        "id": 103,
        "ckaf2rpgen": 103,
        "name2rpgen": "СДМ и гидравлических систем",
        "ckaf2asp": 51
    },
    {
        "value": 104,
        "label": "Самолетостроения и эксплуатации авиационной техники (104)",
        "ckaf2istu": 1988554,
        "id": 104,
        "ckaf2rpgen": 104,
        "name2rpgen": "Самолетостроения и эксплуатации авиационной техники",
        "ckaf2asp": 52
    },
    {
        "value": 105,
        "label": "Менеджмента (105)",
        "ckaf2istu": 1988578,
        "id": 105,
        "ckaf2rpgen": 105,
        "name2rpgen": "Менеджмента",
        "ckaf2asp": 21
    },
    {
        "value": 106,
        "label": "Архитектурного проектирования (106)",
        "ckaf2istu": 1988543,
        "id": 106,
        "ckaf2rpgen": 106,
        "name2rpgen": "Архитектурного проектирования",
        "ckaf2asp": 37
    },
    {
        "value": 108,
        "label": "Строительного производства (108)",
        "ckaf2istu": 1988546,
        "id": 108,
        "ckaf2rpgen": 108,
        "name2rpgen": "Строительного производства",
        "ckaf2asp": 40
    },
    {
        "value": 109,
        "label": "Автомобильных дорог (109)",
        "ckaf2istu": 1988547,
        "id": 109,
        "ckaf2rpgen": 109,
        "name2rpgen": "Автомобильных дорог",
        "ckaf2asp": 41
    },
    {
        "value": 110,
        "label": "Биотехнология и биоинформатика (110)",
        "ckaf2istu": 1988604,
        "id": 110,
        "ckaf2rpgen": 110,
        "name2rpgen": "Биотехнология и биоинформатика",
        "ckaf2asp": 8
    },
    {
        "value": 112,
        "label": "Разработки месторождений полезных ископаемых (112)",
        "ckaf2istu": 1988539,
        "id": 112,
        "ckaf2rpgen": 112,
        "name2rpgen": "Разработки месторождений полезных ископаемых",
        "ckaf2asp": 28
    },
    {
        "value": 114,
        "label": "Маркшейдерского дела и геодезии (114)",
        "ckaf2istu": 1988537,
        "id": 114,
        "ckaf2rpgen": 114,
        "name2rpgen": "Маркшейдерского дела и геодезии",
        "ckaf2asp": 29
    },
    {
        "value": 115,
        "label": "Горных машин и электромеханических систем (115)",
        "ckaf2istu": 1988538,
        "id": 115,
        "ckaf2rpgen": 115,
        "name2rpgen": "Горных машин и электромеханических систем",
        "ckaf2asp": 30
    },
    {
        "value": 117,
        "label": "Прикладной геологии, геофизики и геоинформационных систем (117)",
        "ckaf2istu": 1988620,
        "id": 117,
        "ckaf2rpgen": 117,
        "name2rpgen": "Прикладной геологии, геофизики и геоинформационных систем",
        "ckaf2asp": 31
    },
    {
        "value": 119,
        "label": "Сибирская школа геонаук (119)",
        "ckaf2istu": 1988636,
        "id": 119,
        "ckaf2rpgen": 119,
        "name2rpgen": "Сибирская школа геонаук",
        "ckaf2asp": 0
    },
    {
        "value": 120,
        "label": "Автоматизированных систем (120)",
        "ckaf2istu": 20,
        "id": 120,
        "ckaf2rpgen": 120,
        "name2rpgen": "Автоматизированных систем",
        "ckaf2asp": 9
    },
    {
        "value": 121,
        "label": "Институт информационных технологий и анализа данных (121)",
        "ckaf2istu": 1988626,
        "id": 121,
        "ckaf2rpgen": 121,
        "name2rpgen": "Институт информационных технологий и анализа данных",
        "ckaf2asp": 10
    },
    {
        "value": 123,
        "label": "Экономики и цифровых бизнес-технологий (123)",
        "ckaf2istu": 1988616,
        "id": 123,
        "ckaf2rpgen": 123,
        "name2rpgen": "Экономики и цифровых бизнес-технологий",
        "ckaf2asp": 22
    },
    {
        "value": 124,
        "label": "Технология и оборудование машиностроительных производств (124)",
        "ckaf2istu": 1988606,
        "id": 124,
        "ckaf2rpgen": 124,
        "name2rpgen": "Технология и оборудование машиностроительных производств",
        "ckaf2asp": 46
    },
    {
        "value": 125,
        "label": "Металлургии легких металлов (125)",
        "ckaf2istu": 1988622,
        "id": 125,
        "ckaf2rpgen": 125,
        "name2rpgen": "Металлургии легких металлов",
        "ckaf2asp": 5
    },
    {
        "value": 126,
        "label": "Материаловедения, сварочных и аддитивных технологий (126)",
        "ckaf2istu": 1988557,
        "id": 126,
        "ckaf2rpgen": 126,
        "name2rpgen": "Материаловедения, сварочных и аддитивных технологий",
        "ckaf2asp": 47
    },
    {
        "value": 127,
        "label": "Нефтегазового дела (127)",
        "ckaf2istu": 1988535,
        "id": 127,
        "ckaf2rpgen": 127,
        "name2rpgen": "Нефтегазового дела",
        "ckaf2asp": 32
    },
    {
        "value": 128,
        "label": "Авиамашиностроения (128)",
        "ckaf2istu": 1988602,
        "id": 128,
        "ckaf2rpgen": 128,
        "name2rpgen": "Авиамашиностроения",
        "ckaf2asp": 53
    },
    {
        "value": 129,
        "label": "Металлургии цветных металлов (129)",
        "ckaf2istu": 27,
        "id": 129,
        "ckaf2rpgen": 129,
        "name2rpgen": "Металлургии цветных металлов",
        "ckaf2asp": 4
    },
    {
        "value": 130,
        "label": "МФТИ (130)",
        "ckaf2istu": 1988642,
        "id": 130,
        "ckaf2rpgen": 130,
        "name2rpgen": "МФТИ",
        "ckaf2asp": 0
    },
    {
        "value": 131,
        "label": "Обогащения полезных ископаемых и охраны окружающей среды им. С.Б. Леонова (131)",
        "ckaf2istu": 1988583,
        "id": 131,
        "ckaf2rpgen": 131,
        "name2rpgen": "Обогащения полезных ископаемых и охраны окружающей среды им. С.Б. Леонова",
        "ckaf2asp": 33
    },
    {
        "value": 132,
        "label": "Автоматизации и управления (132)",
        "ckaf2istu": 30,
        "id": 132,
        "ckaf2rpgen": 132,
        "name2rpgen": "Автоматизации и управления",
        "ckaf2asp": 6
    },
    {
        "value": 134,
        "label": "Инженерных коммуникаций и систем жизнеобеспечения (134)",
        "ckaf2istu": 1988613,
        "id": 134,
        "ckaf2rpgen": 134,
        "name2rpgen": "Инженерных коммуникаций и систем жизнеобеспечения",
        "ckaf2asp": 42
    },
    {
        "value": 135,
        "label": "Химии и биотехнологии имени В.В. Тутуриной (135)",
        "ckaf2istu": 1988592,
        "id": 135,
        "ckaf2rpgen": 135,
        "name2rpgen": "Химии и биотехнологии имени В.В. Тутуриной",
        "ckaf2asp": 7
    },
    {
        "value": 136,
        "label": "Химической технологии им. Н.И. Ярополова (136)",
        "ckaf2istu": 35,
        "id": 136,
        "ckaf2rpgen": 136,
        "name2rpgen": "Химической технологии им. Н.И. Ярополова",
        "ckaf2asp": 3
    },
    {
        "value": 137,
        "label": "Экспертиза и управление недвижимостью (137)",
        "ckaf2istu": 1988551,
        "id": 137,
        "ckaf2rpgen": 137,
        "name2rpgen": "Экспертиза и управление недвижимостью",
        "ckaf2asp": 43
    },
    {
        "value": 138,
        "label": "Теплоэнергетики (138)",
        "ckaf2istu": 36,
        "id": 138,
        "ckaf2rpgen": 138,
        "name2rpgen": "Теплоэнергетики",
        "ckaf2asp": 13
    },
    {
        "value": 139,
        "label": "Электрических станций, сетей и систем (139)",
        "ckaf2istu": 37,
        "id": 139,
        "ckaf2rpgen": 139,
        "name2rpgen": "Электрических станций, сетей и систем",
        "ckaf2asp": 14
    },
    {
        "value": 140,
        "label": "Электроснабжения и электротехники (140)",
        "ckaf2istu": 38,
        "id": 140,
        "ckaf2rpgen": 140,
        "name2rpgen": "Электроснабжения и электротехники",
        "ckaf2asp": 15
    },
    {
        "value": 141,
        "label": "Электропривода и электрического транспорта (141)",
        "ckaf2istu": 39,
        "id": 141,
        "ckaf2rpgen": 141,
        "name2rpgen": "Электропривода и электрического транспорта",
        "ckaf2asp": 16
    },
    {
        "value": 142,
        "label": "Энергетические системы и комплексы (142)",
        "ckaf2istu": 1988594,
        "id": 142,
        "ckaf2rpgen": 142,
        "name2rpgen": "Энергетические системы и комплексы",
        "ckaf2asp": 18
    },
    {
        "value": 143,
        "label": "Радиоэлектроники и телекоммуникационных систем (143)",
        "ckaf2istu": 1988529,
        "id": 143,
        "ckaf2rpgen": 143,
        "name2rpgen": "Радиоэлектроники и телекоммуникационных систем",
        "ckaf2asp": 1
    },
    {
        "value": 144,
        "label": "Юриспруденции (144)",
        "ckaf2istu": 1988611,
        "id": 144,
        "ckaf2rpgen": 144,
        "name2rpgen": "Юриспруденции",
        "ckaf2asp": 24
    },
    {
        "value": 145,
        "label": "Электроэнергетические системы (145)",
        "ckaf2istu": 1988600,
        "id": 145,
        "ckaf2rpgen": 145,
        "name2rpgen": "Электроэнергетические системы",
        "ckaf2asp": 19
    },
    {
        "value": 146,
        "label": "Теплоэнергетические системы (146)",
        "ckaf2istu": 1988601,
        "id": 146,
        "ckaf2rpgen": 146,
        "name2rpgen": "Теплоэнергетические системы",
        "ckaf2asp": 20
    },
    {
        "value": 148,
        "label": "Институт квантовой физики (148)",
        "ckaf2istu": 1988506,
        "id": 147,
        "ckaf2rpgen": 148,
        "name2rpgen": "Институт квантовой физики",
        "ckaf2asp": null
    },
    {
        "value": 150,
        "label": "Городского строительства и хозяйства (150)",
        "ckaf2istu": 1988548,
        "id": 150,
        "ckaf2rpgen": 150,
        "name2rpgen": "Городского строительства и хозяйства",
        "ckaf2asp": 44
    },
    {
        "value": 151,
        "label": "Теории права, конституционного и административного права (151)",
        "ckaf2istu": 1988625,
        "id": 151,
        "ckaf2rpgen": 151,
        "name2rpgen": "Теории права, конституционного и административного права",
        "ckaf2asp": 59
    },
    {
        "value": 154,
        "label": "Монументально-декоративной живописи и дизайна им. В.Г. Смагина (154)",
        "ckaf2istu": 1988609,
        "id": 154,
        "ckaf2rpgen": 154,
        "name2rpgen": "Монументально-декоративной живописи и дизайна им. В.Г. Смагина",
        "ckaf2asp": null
    },
    {
        "value": 155,
        "label": "Социологии и психологии (155)",
        "ckaf2istu": 1988614,
        "id": 155,
        "ckaf2rpgen": 155,
        "name2rpgen": "Социологии и психологии",
        "ckaf2asp": 25
    },
    {
        "value": 157,
        "label": "Монументально-декоративной живописи (157)",
        "ckaf2istu": 1988609,
        "id": 157,
        "ckaf2rpgen": 157,
        "name2rpgen": "Монументально-декоративной живописи",
        "ckaf2asp": 36
    },
    {
        "value": 201,
        "label": "Истории и философии (201)",
        "ckaf2istu": 1988573,
        "id": 201,
        "ckaf2rpgen": 201,
        "name2rpgen": "Истории и философии",
        "ckaf2asp": 27
    },
    {
        "value": 205,
        "label": "Брикс кафедра (205)",
        "ckaf2istu": 1988624,
        "id": 205,
        "ckaf2rpgen": 205,
        "name2rpgen": "Брикс кафедра",
        "ckaf2asp": 54
    },
    {
        "value": 206,
        "label": "Кафедра иностранных языков № 1 (206)",
        "ckaf2istu": 1988588,
        "id": 206,
        "ckaf2rpgen": 206,
        "name2rpgen": "Кафедра иностранных языков № 1",
        "ckaf2asp": 55
    },
    {
        "value": 207,
        "label": "Кафедра иностранных языков № 2 (207)",
        "ckaf2istu": 1988589,
        "id": 207,
        "ckaf2rpgen": 207,
        "name2rpgen": "Кафедра иностранных языков № 2",
        "ckaf2asp": 56
    },
    {
        "value": 208,
        "label": "Центр спортивной подготовки (208)",
        "ckaf2istu": 69727,
        "id": 208,
        "ckaf2rpgen": 208,
        "name2rpgen": "Центр спортивной подготовки",
        "ckaf2asp": 58
    },
    {
        "value": 209,
        "label": "Русского языка и межкультурной коммуникации (209)",
        "ckaf2istu": 1988608,
        "id": 209,
        "ckaf2rpgen": 209,
        "name2rpgen": "Русского языка и межкультурной коммуникации",
        "ckaf2asp": 57
    },
    {
        "value": 210,
        "label": "Департамент гуманитарных наук (210)",
        "ckaf2istu": 1988640,
        "id": 210,
        "ckaf2rpgen": 210,
        "name2rpgen": "Департамент гуманитарных наук",
        "ckaf2asp": 0
    },
    {
        "value": 213,
        "label": "Рекламы и журналистики (213)",
        "ckaf2istu": 1988570,
        "id": 213,
        "ckaf2rpgen": 213,
        "name2rpgen": "Рекламы и журналистики",
        "ckaf2asp": 26
    },
    {
        "value": 214,
        "label": "Психологии (214)",
        "ckaf2istu": 1988614,
        "id": 214,
        "ckaf2rpgen": 214,
        "name2rpgen": "Психологии",
        "ckaf2asp": null
    },
    {
        "value": 301,
        "label": "Математики (301)",
        "ckaf2istu": 69715,
        "id": 301,
        "ckaf2rpgen": 301,
        "name2rpgen": "Математики",
        "ckaf2asp": 11
    },
    {
        "value": 302,
        "label": "Отделение прикладной математики и информатики (302)",
        "ckaf2istu": 1988627,
        "id": 302,
        "ckaf2rpgen": 302,
        "name2rpgen": "Отделение прикладной математики и информатики",
        "ckaf2asp": 12
    },
    {
        "value": 303,
        "label": "Физики (303)",
        "ckaf2istu": 69714,
        "id": 303,
        "ckaf2rpgen": 303,
        "name2rpgen": "Физики",
        "ckaf2asp": 17
    },
    {
        "value": 305,
        "label": "Управление качеством и механики (305)",
        "ckaf2istu": 1988575,
        "id": 305,
        "ckaf2rpgen": 305,
        "name2rpgen": "Управление качеством и механики",
        "ckaf2asp": null
    },
    {
        "value": 306,
        "label": "Механика и сопротивление материалов (306)",
        "ckaf2istu": 1988544,
        "id": 306,
        "ckaf2rpgen": 306,
        "name2rpgen": "Механика и сопротивление материалов",
        "ckaf2asp": 45
    },
    {
        "value": 307,
        "label": "Конструирования и стандартизации в машиностроении (307)",
        "ckaf2istu": 1988556,
        "id": 307,
        "ckaf2rpgen": 307,
        "name2rpgen": "Конструирования и стандартизации в машиностроении",
        "ckaf2asp": 48
    },
    {
        "value": 310,
        "label": "Инженерной и компьютерной графики (310)",
        "ckaf2istu": 1988555,
        "id": 310,
        "ckaf2rpgen": 310,
        "name2rpgen": "Инженерной и компьютерной графики",
        "ckaf2asp": 49
    },
    {
        "value": 318,
        "label": "Общеинженерной подготовки (318)",
        "ckaf2istu": 69735,
        "id": 318,
        "ckaf2rpgen": 318,
        "name2rpgen": "Общеинженерной подготовки",
        "ckaf2asp": null
    },
    {
        "value": 401,
        "label": "Промышленной экологии и безопасности жизнедеятельности (401)",
        "ckaf2istu": 1988536,
        "id": 401,
        "ckaf2rpgen": 401,
        "name2rpgen": "Промышленной экологии и безопасности жизнедеятельности",
        "ckaf2asp": 34
    },
    {
        "value": 402,
        "label": "Центр проектного обучения (402)",
        "ckaf2istu": 1988628,
        "id": 402,
        "ckaf2rpgen": 402,
        "name2rpgen": "Центр проектного обучения",
        "ckaf2asp": null
    },
    {
        "value": 406,
        "label": "Архитектуры и градостроительства (406)",
        "ckaf2istu": 1988540,
        "id": 406,
        "ckaf2rpgen": 406,
        "name2rpgen": "Архитектуры и градостроительства",
        "ckaf2asp": 38
    },
    {
        "value": 407,
        "label": "Рисунка, основ проектирования и историко-архитектурного наследия (407)",
        "ckaf2istu": 1988610,
        "id": 407,
        "ckaf2rpgen": 407,
        "name2rpgen": "Рисунка, основ проектирования и историко-архитектурного наследия",
        "ckaf2asp": 39
    },
    {
        "value": 410,
        "label": "Центр образовательных программ магистратуры и аспирантуры (410)",
        "ckaf2istu": 1988607,
        "id": 410,
        "ckaf2rpgen": 410,
        "name2rpgen": "Центр образовательных программ магистратуры и аспирантуры",
        "ckaf2asp": 0
    },
    {
        "value": 412,
        "label": "Управления промышленными предприятиями (412)",
        "ckaf2istu": 1988576,
        "id": 412,
        "ckaf2rpgen": 412,
        "name2rpgen": "Управления промышленными предприятиями",
        "ckaf2asp": 23
    },
    {
        "value": 413,
        "label": "Ювелирного дизайна и технологии (413)",
        "ckaf2istu": 1988531,
        "id": 413,
        "ckaf2rpgen": 413,
        "name2rpgen": "Ювелирного дизайна и технологии",
        "ckaf2asp": 35
    },
    {
        "value": 414,
        "label": "Брикс кафедра (414)",
        "ckaf2istu": 1988624,
        "id": 414,
        "ckaf2rpgen": 414,
        "name2rpgen": "Брикс кафедра",
        "ckaf2asp": 0
    },
    {
        "value": 122,
        "label": "БГЭУ(Белоруссия) (122)",
        "ckaf2istu": 1988641,
        "id": 415,
        "ckaf2rpgen": 122,
        "name2rpgen": "БГЭУ(Белоруссия)",
        "ckaf2asp": null
    }
]            
            """)

DATA_GROUPS_PROGRAM = json.loads("""
[
    {
        "discpl": "Web-программирование",
        "planlin": 309372,
        "id_discpl": 949,
        "newdisid": "Б1.В.02.08",
        "razrab": 15727,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Каташевцев Михаил Дмитриевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 3885,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_Web-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_3885_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-20",
        "confirm_date": "2025-06-20",
        "discode": "Б1.В.02.08",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Адаптивная физическая культура",
        "planlin": 309445,
        "id_discpl": 8885,
        "newdisid": "Б1.Б.05.02.ДВ.01.07",
        "razrab": 1038,
        "zavkaf": 1853,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Демидов Александр Геннадьевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Рыбина Людмила Дмитриевна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7016,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 208,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%90%D0%B4%D0%B0%D0%BF%D1%82%D0%B8%D0%B2%D0%BD%D0%B0%D1%8F_%D1%84%D0%B8%D0%B7%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D1%83%D1%80%D0%B0_7016_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 360,
        "user_accepted_name": "Демидов Александр Геннадьевич",
        "accept_date": "2025-06-18",
        "confirm_date": null,
        "discode": "Б1.Б.05.02.ДВ.01.07",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Анализ бизнес-процессов",
        "planlin": 309423,
        "id_discpl": 1062,
        "newdisid": "Б1.В.02.07",
        "razrab": 19984,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Петров Павел Александрович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4036,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7_%D0%B1%D0%B8%D0%B7%D0%BD%D0%B5%D1%81-%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D0%B2_4036_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-11",
        "confirm_date": "2025-06-11",
        "discode": "Б1.В.02.07",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Архитектура информационных систем",
        "planlin": 309413,
        "id_discpl": 976,
        "newdisid": "Б1.Б.03.08",
        "razrab": 82,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Бахвалов Сергей Владимирович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4037,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%90%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0_%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D1%85_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC_4037_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-11",
        "confirm_date": "2025-06-12",
        "discode": "Б1.Б.03.08",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Архитектура ЭВМ и систем",
        "planlin": 309412,
        "id_discpl": 9417,
        "newdisid": "Б1.Б.03.04",
        "razrab": 25395,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Игумнов Иннокентий Васильевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4038,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%90%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0_%D0%AD%D0%92%D0%9C_%D0%B8_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC_4038_accepted_arhWAiT.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-09",
        "confirm_date": "2025-05-25",
        "discode": "Б1.Б.03.04",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Атлетическая гимнастика",
        "planlin": 309431,
        "id_discpl": 8890,
        "newdisid": "Б1.Б.05.02.ДВ.01.02",
        "razrab": 846,
        "zavkaf": 1853,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Демидов Александр Геннадьевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Несмеянов Андрей Иванович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7017,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 208,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%90%D1%82%D0%BB%D0%B5%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%B3%D0%B8%D0%BC%D0%BD%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0_7017_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": true,
        "user_confirmed_name": null,
        "user_accepted": 360,
        "user_accepted_name": "Демидов Александр Геннадьевич",
        "accept_date": "2025-06-19",
        "confirm_date": null,
        "discode": "Б1.Б.05.02.ДВ.01.02",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Аэробика",
        "planlin": 309443,
        "id_discpl": 8892,
        "newdisid": "Б1.Б.05.02.ДВ.01.05",
        "razrab": 551,
        "zavkaf": 1853,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Демидов Александр Геннадьевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Койпышева Елена Александровна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7018,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 208,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%90%D1%8D%D1%80%D0%BE%D0%B1%D0%B8%D0%BA%D0%B0_7018_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 360,
        "user_accepted_name": "Демидов Александр Геннадьевич",
        "accept_date": "2025-06-19",
        "confirm_date": null,
        "discode": "Б1.Б.05.02.ДВ.01.05",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Базы данных",
        "planlin": 309416,
        "id_discpl": 926,
        "newdisid": "Б1.Б.03.05",
        "razrab": 5359,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Копайгородский Алексей Николаевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4039,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%91%D0%B0%D0%B7%D1%8B_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85_4039_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-11",
        "confirm_date": "2025-06-11",
        "discode": "Б1.Б.03.05",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Безопасность жизнедеятельности",
        "planlin": 309398,
        "id_discpl": 36,
        "newdisid": "Б1.Б.01.09",
        "razrab": 352,
        "zavkaf": 1223,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Тимофеева Светлана Семеновна",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Дроздова Татьяна Ивановна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1558,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 401,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%91%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D1%8C_%D0%B6%D0%B8%D0%B7%D0%BD%D0%B5%D0%B4%D0%B5%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D0%B8_1558_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 23,
        "user_accepted_name": "Тимофеева Светлана Семеновна",
        "accept_date": "2025-05-27",
        "confirm_date": null,
        "discode": "Б1.Б.01.09",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Бокс",
        "planlin": 309432,
        "id_discpl": 8895,
        "newdisid": "Б1.Б.05.02.ДВ.01.03",
        "razrab": 22083,
        "zavkaf": 1853,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Демидов Александр Геннадьевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Кривенков Максим Юрьевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7019,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 208,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%91%D0%BE%D0%BA%D1%81_7019_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 360,
        "user_accepted_name": "Демидов Александр Геннадьевич",
        "accept_date": "2025-06-18",
        "confirm_date": null,
        "discode": "Б1.Б.05.02.ДВ.01.03",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Введение в AR/VR технологии",
        "planlin": 309391,
        "id_discpl": 11510,
        "newdisid": "Б1.В.03.03",
        "razrab": 5779,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Говорков Алексей Сергеевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4040,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/VR_%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8_4040_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-11",
        "confirm_date": "2025-06-11",
        "discode": "Б1.В.03.03",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Введение в веб-технологии",
        "planlin": 309411,
        "id_discpl": 11511,
        "newdisid": "Б1.Б.03.01",
        "razrab": 15727,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Каташевцев Михаил Дмитриевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4021,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5_%D0%B2_%D0%B2%D0%B5%D0%B1-%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8_4021_accepted_Oq77YhT.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": true,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-23",
        "confirm_date": "2025-06-22",
        "discode": "Б1.Б.03.01",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Военно-прикладная физическая подготовка",
        "planlin": 309446,
        "id_discpl": 9264,
        "newdisid": "Б1.Б.05.02.ДВ.01.08",
        "razrab": 25405,
        "zavkaf": 1853,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Демидов Александр Геннадьевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Гальцев Сергей Александрович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7020,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 208,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%92%D0%BE%D0%B5%D0%BD%D0%BD%D0%BE-%D0%BF%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%B0%D1%8F_%D1%84%D0%B8%D0%B7%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%BF%D0%BE%D0%B4%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%BA%D0%B0_7020_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 360,
        "user_accepted_name": "Демидов Александр Геннадьевич",
        "accept_date": "2025-06-19",
        "confirm_date": null,
        "discode": "Б1.Б.05.02.ДВ.01.08",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Гиревой спорт",
        "planlin": 309450,
        "id_discpl": 12486,
        "newdisid": "Б1.Б.05.02.ДВ.01.10",
        "razrab": 24753,
        "zavkaf": 1853,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Демидов Александр Геннадьевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Малыхин Анатолий Васильевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7021,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 208,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%93%D0%B8%D1%80%D0%B5%D0%B2%D0%BE%D0%B9_%D1%81%D0%BF%D0%BE%D1%80%D1%82_7021_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 360,
        "user_accepted_name": "Демидов Александр Геннадьевич",
        "accept_date": "2025-06-19",
        "confirm_date": null,
        "discode": "Б1.Б.05.02.ДВ.01.10",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Инженерная графика",
        "planlin": 309409,
        "id_discpl": 9560,
        "newdisid": "Б1.Б.02.03",
        "razrab": 100,
        "zavkaf": 3723,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Перелыгина Александра Юрьевна",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Белокрылова Ольга Вениаминовна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 2667,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 310,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%98%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%BD%D0%B0%D1%8F_%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%B0_2667_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 288,
        "user_accepted_name": "Перелыгина Александра Юрьевна",
        "accept_date": "2025-06-17",
        "confirm_date": "2025-06-16",
        "discode": "Б1.Б.02.03",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Иностранный язык",
        "planlin": 309392,
        "id_discpl": 1,
        "newdisid": "Б1.Б.01.01",
        "razrab": 25850,
        "zavkaf": 15811,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Колмакова Ольга Анатольевна",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Керешун Александра Вячеславовна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1945,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 206,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%98%D0%BD%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%BD%D1%8B%D0%B9_%D1%8F%D0%B7%D1%8B%D0%BA_1945_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 200,
        "user_accepted_name": "Колмакова Ольга Анатольевна",
        "accept_date": "2025-06-18",
        "confirm_date": null,
        "discode": "Б1.Б.01.01",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Интеллектуальные системы и технологии",
        "planlin": 309417,
        "id_discpl": 982,
        "newdisid": "Б1.Б.03.11",
        "razrab": 773,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Массель Людмила Васильевна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4041,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%98%D0%BD%D1%82%D0%B5%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B_%D0%B8_%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8_4041_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-23",
        "confirm_date": "2025-06-22",
        "discode": "Б1.Б.03.11",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Интернет вещей ",
        "planlin": 309401,
        "id_discpl": 9594,
        "newdisid": "ФТД.01",
        "razrab": 20004,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Кононенко Роман Владимирович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 12780,
        "status": 0,
        "status_verbose": "Назначен",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": null,
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": null,
        "user_accepted_name": null,
        "accept_date": null,
        "confirm_date": null,
        "discode": "ФТД.01",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Инфокоммуникационные системы и сети",
        "planlin": 309441,
        "id_discpl": 979,
        "newdisid": "Б1.Б.03.07",
        "razrab": 23367,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Лукьянов Никита Дмитриевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4042,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%98%D0%BD%D1%84%D0%BE%D0%BA%D0%BE%D0%BC%D0%BC%D1%83%D0%BD%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B_%D0%B8_%D1%81%D0%B5%D1%82%D0%B8_4042_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-19",
        "confirm_date": "2025-06-18",
        "discode": "Б1.Б.03.07",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Информатика",
        "planlin": 309408,
        "id_discpl": 237,
        "newdisid": "Б1.Б.03.03",
        "razrab": 1823,
        "zavkaf": 359,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Дударева Оксана Витальевна",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Фунтикова Евгения Александровна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1946,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 302,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0_1946_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 297,
        "user_accepted_name": "Дударева Оксана Витальевна",
        "accept_date": "2025-06-16",
        "confirm_date": "2025-06-16",
        "discode": "Б1.Б.03.03",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Исследование операций",
        "planlin": 309421,
        "id_discpl": 944,
        "newdisid": "Б1.В.02.03",
        "razrab": 22009,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Маланова Татьяна Валерьевна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4043,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%98%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D0%BE%D0%BF%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B9_4043_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-16",
        "confirm_date": "2025-06-16",
        "discode": "Б1.В.02.03",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "История России",
        "planlin": 309393,
        "id_discpl": 12043,
        "newdisid": "Б1.Б.01.07",
        "razrab": 17376,
        "zavkaf": 1681,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Новиков Павел Александрович",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Чирикова Марина Владимировна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1640,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 201,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8_1640_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 138,
        "user_accepted_name": "Новиков Павел Александрович",
        "accept_date": "2025-06-19",
        "confirm_date": null,
        "discode": "Б1.Б.01.07",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Компьютерная графика",
        "planlin": 309389,
        "id_discpl": 75,
        "newdisid": "Б1.В.03.01",
        "razrab": 28212,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Провоторов Вадим Александрович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4044,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9A%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%8F_%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%B0_4044_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-19",
        "confirm_date": "2025-06-20",
        "discode": "Б1.В.03.01",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Корпоративные информационные системы",
        "planlin": 309424,
        "id_discpl": 990,
        "newdisid": "Б1.В.02.16",
        "razrab": 82,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Бахвалов Сергей Владимирович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4045,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9A%D0%BE%D1%80%D0%BF%D0%BE%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B5_%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B_4045_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-11",
        "confirm_date": "2025-06-15",
        "discode": "Б1.В.02.16",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Критическое и системное мышление",
        "planlin": 309426,
        "id_discpl": 10842,
        "newdisid": "Б1.Б.01.04",
        "razrab": 24421,
        "zavkaf": 1681,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Новиков Павел Александрович",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Васенкин Алексей Вадимович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 708,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 201,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9A%D1%80%D0%B8%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5_%D0%B8_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D0%BE%D0%B5_%D0%BC%D1%8B%D1%88%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_708_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 138,
        "user_accepted_name": "Новиков Павел Александрович",
        "accept_date": "2025-05-15",
        "confirm_date": null,
        "discode": "Б1.Б.01.04",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Математика",
        "planlin": 309440,
        "id_discpl": 236,
        "newdisid": "Б1.Б.02.01",
        "razrab": 217,
        "zavkaf": 359,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Дударева Оксана Витальевна",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Власов Валерий Георгиевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1947,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 302,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9C%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0_1947_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 297,
        "user_accepted_name": "Дударева Оксана Витальевна",
        "accept_date": "2025-06-03",
        "confirm_date": null,
        "discode": "Б1.Б.02.01",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Математическая логика и дискретная математика",
        "planlin": 309371,
        "id_discpl": 13027,
        "newdisid": "Б1.В.02.02",
        "razrab": 876,
        "zavkaf": 359,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Дударева Оксана Витальевна",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Носырева Людмила Леонидовна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1948,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 302,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9C%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%BB%D0%BE%D0%B3%D0%B8%D0%BA%D0%B0_%D0%B8_%D0%B4%D0%B8%D1%81%D0%BA%D1%80%D0%B5%D1%82%D0%BD%D0%B0%D1%8F_%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0_1948_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 297,
        "user_accepted_name": "Дударева Оксана Витальевна",
        "accept_date": "2025-06-18",
        "confirm_date": "2025-06-18",
        "discode": "Б1.В.02.02",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Методы анализа данных",
        "planlin": 309435,
        "id_discpl": 9763,
        "newdisid": "Б1.В.02.05",
        "razrab": 15122,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Бучнев Олег Сергеевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4046,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9C%D0%B5%D1%82%D0%BE%D0%B4%D1%8B_%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85_4046_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-11",
        "confirm_date": "2025-06-06",
        "discode": "Б1.В.02.05",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Моделирование процессов и систем",
        "planlin": 309382,
        "id_discpl": 995,
        "newdisid": "Б1.В.02.09",
        "razrab": 927,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Петров Александр Васильевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4047,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9C%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D0%B2_%D0%B8_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC_4047_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-17",
        "confirm_date": "2025-06-17",
        "discode": "Б1.В.02.09",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Мониторинг безопасности информационных систем",
        "planlin": 309387,
        "id_discpl": 10885,
        "newdisid": "Б1.В.02.ДВ.02.01",
        "razrab": 14881,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Аршинский Вадим Леонидович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4048,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9C%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3_%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D0%B8_%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D1%85_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC_4048_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-19",
        "confirm_date": "2025-06-19",
        "discode": "Б1.В.02.ДВ.02.01",
        "type": [
            "person",
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Надежность информационных систем",
        "planlin": 309437,
        "id_discpl": 1011,
        "newdisid": "Б1.В.02.17",
        "razrab": 14945,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Барахтенко Евгений Алексеевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4049,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9D%D0%B0%D0%B4%D0%B5%D0%B6%D0%BD%D0%BE%D1%81%D1%82%D1%8C_%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D1%85_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC_4049_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-19",
        "confirm_date": "2025-06-18",
        "discode": "Б1.В.02.17",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Нейросетевые технологии",
        "planlin": 309415,
        "id_discpl": 9842,
        "newdisid": "Б1.Б.03.10",
        "razrab": 16472,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Осипова Елизавета Алексеевна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4050,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9D%D0%B5%D0%B9%D1%80%D0%BE%D1%81%D0%B5%D1%82%D0%B5%D0%B2%D1%8B%D0%B5_%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8_4050_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-18",
        "confirm_date": "2025-06-17",
        "discode": "Б1.Б.03.10",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Образовательный форсайт",
        "planlin": 309402,
        "id_discpl": 9338,
        "newdisid": "ФТД.02",
        "razrab": 14881,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Аршинский Вадим Леонидович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4106,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D1%84%D0%BE%D1%80%D1%81%D0%B0%D0%B9%D1%82_4106_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-11",
        "confirm_date": "2025-05-25",
        "discode": "ФТД.02",
        "type": [
            "person",
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Общая физическая подготовка",
        "planlin": 309430,
        "id_discpl": 8921,
        "newdisid": "Б1.Б.05.02.ДВ.01.01",
        "razrab": 14820,
        "zavkaf": 1853,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Демидов Александр Геннадьевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Амбарцумян Рима Агасовна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7022,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 208,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D0%B1%D1%89%D0%B0%D1%8F_%D1%84%D0%B8%D0%B7%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%BF%D0%BE%D0%B4%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%BA%D0%B0_7022_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 360,
        "user_accepted_name": "Демидов Александр Геннадьевич",
        "accept_date": "2025-06-19",
        "confirm_date": null,
        "discode": "Б1.Б.05.02.ДВ.01.01",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Объектно-ориентированное программирование",
        "planlin": 309438,
        "id_discpl": 923,
        "newdisid": "Б1.В.02.04",
        "razrab": 14881,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Аршинский Вадим Леонидович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4107,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BD%D0%BE-%D0%BE%D1%80%D0%B8%D0%B5%D0%BD%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_4107_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-16",
        "confirm_date": "2025-06-11",
        "discode": "Б1.В.02.04",
        "type": [
            "person",
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Оздоровительная физическая культура",
        "planlin": 309444,
        "id_discpl": 8922,
        "newdisid": "Б1.Б.05.02.ДВ.01.06",
        "razrab": 15964,
        "zavkaf": 1853,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Демидов Александр Геннадьевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Кузнецова Лариса Владимировна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7023,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 208,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D0%B7%D0%B4%D0%BE%D1%80%D0%BE%D0%B2%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_%D1%84%D0%B8%D0%B7%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D1%83%D1%80%D0%B0_7023_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 360,
        "user_accepted_name": "Демидов Александр Геннадьевич",
        "accept_date": "2025-06-18",
        "confirm_date": null,
        "discode": "Б1.Б.05.02.ДВ.01.06",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Операционные системы",
        "planlin": 309420,
        "id_discpl": 924,
        "newdisid": "Б1.Б.03.06",
        "razrab": 15727,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Каташевцев Михаил Дмитриевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4112,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D0%BF%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B_4112_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-23",
        "confirm_date": "2025-06-22",
        "discode": "Б1.Б.03.06",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Основы Big Data",
        "planlin": 309448,
        "id_discpl": 11518,
        "newdisid": "Б1.В.02.13",
        "razrab": 25902,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Харахинов Владимир Александрович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4113,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B_Big_Data_4113_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-23",
        "confirm_date": "2025-06-22",
        "discode": "Б1.В.02.13",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Основы DevOps",
        "planlin": 309388,
        "id_discpl": 11519,
        "newdisid": "Б1.В.02.ДВ.02.02",
        "razrab": 25902,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Харахинов Владимир Александрович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4114,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B_DevOps_4114_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-23",
        "confirm_date": "2025-06-22",
        "discode": "Б1.В.02.ДВ.02.02",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Основы деловой коммуникации",
        "planlin": 309396,
        "id_discpl": 9287,
        "newdisid": "Б1.Б.01.02",
        "razrab": 37,
        "zavkaf": 15136,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Вайрах Юлия Викторовна",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Апончук Ирина Игоревна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1949,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 213,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B_%D0%B4%D0%B5%D0%BB%D0%BE%D0%B2%D0%BE%D0%B9_%D0%BA%D0%BE%D0%BC%D0%BC%D1%83%D0%BD%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8_1949_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": true,
        "user_confirmed_name": null,
        "user_accepted": 109,
        "user_accepted_name": "Вайрах Юлия Викторовна",
        "accept_date": "2025-06-11",
        "confirm_date": null,
        "discode": "Б1.Б.01.02",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Основы инклюзивного взаимодействия",
        "planlin": 309425,
        "id_discpl": 10843,
        "newdisid": "Б1.Б.01.03",
        "razrab": 1851,
        "zavkaf": 1681,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Новиков Павел Александрович",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Пуляевская Ольга Владимировна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1698,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 201,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B_%D0%B8%D0%BD%D0%BA%D0%BB%D1%8E%D0%B7%D0%B8%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE_%D0%B2%D0%B7%D0%B0%D0%B8%D0%BC%D0%BE%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D1%8F_1698_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 138,
        "user_accepted_name": "Новиков Павел Александрович",
        "accept_date": "2025-06-17",
        "confirm_date": null,
        "discode": "Б1.Б.01.03",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Основы информационной безопасности",
        "planlin": 309414,
        "id_discpl": 1102,
        "newdisid": "Б1.Б.03.09",
        "razrab": 16162,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Мамедов Эльшан Фахраддинович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4115,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B_%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B9_%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D0%B8_4115_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-11",
        "confirm_date": "2025-06-09",
        "discode": "Б1.Б.03.09",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Основы мобильной разработки",
        "planlin": 309418,
        "id_discpl": 11521,
        "newdisid": "Б1.В.02.11",
        "razrab": 25902,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Харахинов Владимир Александрович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4116,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B_%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9_%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8_4116_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-23",
        "confirm_date": "2025-06-22",
        "discode": "Б1.В.02.11",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Основы проектной деятельности",
        "planlin": 309410,
        "id_discpl": 954,
        "newdisid": "Б1.Б.04.01",
        "razrab": 17375,
        "zavkaf": 17375,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": null,
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Чимитов Павел Евгеньевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 8742,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 402,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BD%D0%BE%D0%B9_%D0%B4%D0%B5%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D0%B8_8742_accepted_PYlJmWt.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 128,
        "user_accepted_name": "Чимитов Павел Евгеньевич",
        "accept_date": "2025-05-22",
        "confirm_date": null,
        "discode": "Б1.Б.04.01",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Основы российской государственности",
        "planlin": 309449,
        "id_discpl": 12055,
        "newdisid": "Б1.Б.01.10",
        "razrab": 1681,
        "zavkaf": 1681,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Новиков Павел Александрович",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Новиков Павел Александрович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 555,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 201,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B_%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8_555_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 138,
        "user_accepted_name": "Новиков Павел Александрович",
        "accept_date": "2025-05-20",
        "confirm_date": null,
        "discode": "Б1.Б.01.10",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Основы СППР",
        "planlin": 309370,
        "id_discpl": 1010,
        "newdisid": "Б1.В.02.14",
        "razrab": 773,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Массель Людмила Васильевна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4117,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B_%D0%A1%D0%9F%D0%9F%D0%A0_4117_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-23",
        "confirm_date": "2025-06-22",
        "discode": "Б1.В.02.14",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Подготовка к сдаче квалификационного экзамена по иностранному языку",
        "planlin": 309403,
        "id_discpl": 9290,
        "newdisid": "ФТД.03",
        "razrab": 25850,
        "zavkaf": 15811,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Колмакова Ольга Анатольевна",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Керешун Александра Вячеславовна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1950,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 206,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9F%D0%BE%D0%B4%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%BA%D0%B0_%D0%BA_%D1%81%D0%B4%D0%B0%D1%87%D0%B5_%D0%BA%D0%B2%D0%B0%D0%BB%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE_%D1%8D%D0%BA%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B0_%D0%BF%D0%BE_%D0%B8%D0%BD%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%BC%D1%83_%D1%8F%D0%B7_akRVa5z.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 200,
        "user_accepted_name": "Колмакова Ольга Анатольевна",
        "accept_date": "2025-06-18",
        "confirm_date": "2025-05-27",
        "discode": "ФТД.03",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Правоведение",
        "planlin": 309397,
        "id_discpl": 306,
        "newdisid": "Б1.Б.01.05",
        "razrab": 26641,
        "zavkaf": 16015,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Курышова Ирина Васильевна",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Егорова Юлия Владимировна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1951,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 151,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9F%D1%80%D0%B0%D0%B2%D0%BE%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5_1951_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 29,
        "user_accepted_name": "Курышова Ирина Васильевна",
        "accept_date": "2025-06-18",
        "confirm_date": null,
        "discode": "Б1.Б.01.05",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Программирование на языке высокого уровня",
        "planlin": 309434,
        "id_discpl": 985,
        "newdisid": "Б1.Б.03.02",
        "razrab": 1729,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Бахвалова Зинаида Андреевна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4118,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D0%BD%D0%B0_%D1%8F%D0%B7%D1%8B%D0%BA%D0%B5_%D0%B2%D1%8B%D1%81%D0%BE%D0%BA%D0%BE%D0%B3%D0%BE_%D1%83%D1%80%D0%BE%D0%B2%D0%BD%D1%8F_4118_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-23",
        "confirm_date": "2025-06-22",
        "discode": "Б1.Б.03.02",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Проектирование информационных систем",
        "planlin": 309436,
        "id_discpl": 960,
        "newdisid": "Б1.В.02.15",
        "razrab": 14881,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Аршинский Вадим Леонидович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4119,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9F%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D1%85_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC_4119_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-23",
        "confirm_date": "2025-06-23",
        "discode": "Б1.В.02.15",
        "type": [
            "person",
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Проектная деятельность",
        "planlin": 309439,
        "id_discpl": 9342,
        "newdisid": "Б1.В.01.01",
        "razrab": 14881,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Аршинский Вадим Леонидович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4120,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9F%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BD%D0%B0%D1%8F_%D0%B4%D0%B5%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D1%8C_4120_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-11",
        "confirm_date": "2025-06-16",
        "discode": "Б1.В.01.01",
        "type": [
            "person",
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Производственная практика: преддипломная практика",
        "planlin": 309376,
        "id_discpl": 11794,
        "newdisid": "Б2.В.02(Пд)",
        "razrab": 14881,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Аршинский Вадим Леонидович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 9955,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9F%D1%80%D0%BE%D0%B8%D0%B7%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F_%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0_%D0%BF%D1%80%D0%B5%D0%B4%D0%B4%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC%D0%BD%D0%B0%D1%8F_%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0_9955_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-19",
        "confirm_date": "2025-06-19",
        "discode": "Б2.В.02(Пд)",
        "type": [
            "person",
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Производственная практика: технологическая (проектно-технологическая) практика",
        "planlin": 309375,
        "id_discpl": 12942,
        "newdisid": "Б2.В.01(П)",
        "razrab": 14881,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Аршинский Вадим Леонидович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 9956,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%9F%D1%80%D0%BE%D0%B8%D0%B7%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F_%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0_%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BD%D0%BE-%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA_rxonfMU.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-16",
        "confirm_date": "2025-06-17",
        "discode": "Б2.В.01(П)",
        "type": [
            "person",
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Распределённые вычисления",
        "planlin": 309384,
        "id_discpl": 10887,
        "newdisid": "Б1.В.02.ДВ.01.01",
        "razrab": 14881,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Аршинский Вадим Леонидович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4121,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A0%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B5_%D0%B2%D1%8B%D1%87%D0%B8%D1%81%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F_4121_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-16",
        "confirm_date": "2025-06-16",
        "discode": "Б1.В.02.ДВ.01.01",
        "type": [
            "person",
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Спортивные игры",
        "planlin": 309447,
        "id_discpl": 11313,
        "newdisid": "Б1.Б.05.02.ДВ.01.09",
        "razrab": 1839,
        "zavkaf": 1853,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Демидов Александр Геннадьевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Грицай Елена Николаевна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7024,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 208,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B5_%D0%B8%D0%B3%D1%80%D1%8B_7024_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 360,
        "user_accepted_name": "Демидов Александр Геннадьевич",
        "accept_date": "2025-06-18",
        "confirm_date": null,
        "discode": "Б1.Б.05.02.ДВ.01.09",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Спортивные танцы",
        "planlin": 309442,
        "id_discpl": 9297,
        "newdisid": "Б1.Б.05.02.ДВ.01.04",
        "razrab": 23103,
        "zavkaf": 1853,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Демидов Александр Геннадьевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Шишлянникова Ольга Александровна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7025,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 208,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B5_%D1%82%D0%B0%D0%BD%D1%86%D1%8B_7025_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 360,
        "user_accepted_name": "Демидов Александр Геннадьевич",
        "accept_date": "2025-06-19",
        "confirm_date": null,
        "discode": "Б1.Б.05.02.ДВ.01.04",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Теория вероятностей и математическая статистика",
        "planlin": 309433,
        "id_discpl": 406,
        "newdisid": "Б1.В.02.01",
        "razrab": 927,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Петров Александр Васильевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4621,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A2%D0%B5%D0%BE%D1%80%D0%B8%D1%8F_%D0%B2%D0%B5%D1%80%D0%BE%D1%8F%D1%82%D0%BD%D0%BE%D1%81%D1%82%D0%B5%D0%B9_%D0%B8_%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0_4621_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-16",
        "confirm_date": "2025-06-17",
        "discode": "Б1.В.02.01",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Технологии блокчейн",
        "planlin": 309419,
        "id_discpl": 10889,
        "newdisid": "Б1.В.02.ДВ.01.02",
        "razrab": 24478,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Хритова Мария Анатольевна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4622,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A2%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8_%D0%B1%D0%BB%D0%BE%D0%BA%D1%87%D0%B5%D0%B9%D0%BD_4622_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-19",
        "confirm_date": "2025-06-18",
        "discode": "Б1.В.02.ДВ.01.02",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Технологии программирования",
        "planlin": 309422,
        "id_discpl": 962,
        "newdisid": "Б1.В.02.06",
        "razrab": 15727,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Каташевцев Михаил Дмитриевич",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4581,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A2%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_4581_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-21",
        "confirm_date": "2025-06-21",
        "discode": "Б1.В.02.06",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Технологии разработки программных комплексов",
        "planlin": 309383,
        "id_discpl": 932,
        "newdisid": "Б1.В.02.12",
        "razrab": 1729,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Бахвалова Зинаида Андреевна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4623,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A2%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8_%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D1%8B%D1%85_%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%81%D0%BE%D0%B2_4623_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-23",
        "confirm_date": "2025-06-22",
        "discode": "Б1.В.02.12",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Технологическое предпринимательство",
        "planlin": 309390,
        "id_discpl": 10321,
        "newdisid": "Б1.В.03.02",
        "razrab": 249,
        "zavkaf": 374,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Елшин Виктор Владимирович",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Галяутдинов Ильдус Ильясович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7026,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 132,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A2%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5_%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D0%BD%D0%B8%D0%BC%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D1%82%D0%B2%D0%BE_7026_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 76,
        "user_accepted_name": "Елшин Виктор Владимирович",
        "accept_date": "2025-06-20",
        "confirm_date": "2025-06-06",
        "discode": "Б1.В.03.02",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Управление проектами",
        "planlin": 309385,
        "id_discpl": 263,
        "newdisid": "Б1.В.02.10",
        "razrab": 19984,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Петров Павел Александрович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4122,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A3%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0%D0%BC%D0%B8_4122_accepted.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-11",
        "confirm_date": "2025-06-12",
        "discode": "Б1.В.02.10",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Учебная практика: технологическая (проектно-технологическая) практика",
        "planlin": 309373,
        "id_discpl": 12950,
        "newdisid": "Б2.Б.01(У)",
        "razrab": 14881,
        "zavkaf": 5779,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Говорков Алексей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Аршинский Вадим Леонидович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 9957,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 121,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A3%D1%87%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F_%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0_%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BD%D0%BE-%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8_iyRriDI.pdf",
        "user_confirmed": 102,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": "Аршинский Вадим Леонидович",
        "user_accepted": 104,
        "user_accepted_name": "Говорков Алексей Сергеевич",
        "accept_date": "2025-06-11",
        "confirm_date": "2025-06-06",
        "discode": "Б2.Б.01(У)",
        "type": [
            "person",
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": false
    },
    {
        "discpl": "Физика",
        "planlin": 309407,
        "id_discpl": 43,
        "newdisid": "Б1.Б.02.02",
        "razrab": 16498,
        "zavkaf": 569,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Коновалов Николай Петрович",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Павлова Татьяна Олеговна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1952,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 303,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A4%D0%B8%D0%B7%D0%B8%D0%BA%D0%B0_1952_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 74,
        "user_accepted_name": "Коновалов Николай Петрович",
        "accept_date": "2025-06-19",
        "confirm_date": null,
        "discode": "Б1.Б.02.02",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Физическая культура и спорт",
        "planlin": 309427,
        "id_discpl": 8882,
        "newdisid": "Б1.Б.05.01",
        "razrab": 15840,
        "zavkaf": 1853,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Демидов Александр Геннадьевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Коновалова Татьяна Геннадьевна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 7027,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 208,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A4%D0%B8%D0%B7%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D1%83%D1%80%D0%B0_%D0%B8_%D1%81%D0%BF%D0%BE%D1%80%D1%82_7027_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 360,
        "user_accepted_name": "Демидов Александр Геннадьевич",
        "accept_date": "2025-06-19",
        "confirm_date": null,
        "discode": "Б1.Б.05.01",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Философия",
        "planlin": 309394,
        "id_discpl": 3,
        "newdisid": "Б1.Б.01.06",
        "razrab": 1222,
        "zavkaf": 1681,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Новиков Павел Александрович",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Тетенькин Алексей Владимирович",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 1756,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 201,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%A4%D0%B8%D0%BB%D0%BE%D1%81%D0%BE%D1%84%D0%B8%D1%8F_1756_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 138,
        "user_accepted_name": "Новиков Павел Александрович",
        "accept_date": "2025-06-16",
        "confirm_date": null,
        "discode": "Б1.Б.01.06",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    },
    {
        "discpl": "Экономика",
        "planlin": 309395,
        "id_discpl": 4,
        "newdisid": "Б1.Б.01.08",
        "razrab": 1970,
        "zavkaf": 6395,
        "rop": 14881,
        "fac": 5779,
        "zavkaf_name": "Нечаев Андрей Сергеевич",
        "fac_name": "Говорков Алексей Сергеевич",
        "razrab_name": "Таюрская Ольга Валентиновна",
        "rop_name": "Аршинский Вадим Леонидович",
        "id_admission": 25064,
        "id": 4051,
        "status": 3,
        "status_verbose": "Утвержден",
        "kafcode": 123,
        "can_upload_file_directly": false,
        "last_accepted_file_url": "/uploads/rpd_generator/%D0%98%D0%A1%D0%A2%D0%B1_2025_%D0%AD%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0_4051_accepted.pdf",
        "user_confirmed": null,
        "can_be_copied_by_anyone": false,
        "user_confirmed_name": null,
        "user_accepted": 47,
        "user_accepted_name": "Нечаев Андрей Сергеевич",
        "accept_date": "2025-06-15",
        "confirm_date": null,
        "discode": "Б1.Б.01.08",
        "type": [
            "rop"
        ],
        "plan_id": 10179,
        "only_zav_required": true
    }
]            
            """)

DATA_GROUP_LIST = [
    {
        "abbr": "ИСТб",
        "types": [
            "person",
            "rop"
        ],
        "plan_id": 10179,
        "statuses": {
            "Назначен": 1,
            "Заполняется": 0,
            "Требует моего согласования/утверждения": 0,
            "Отправлен на проверку": 0,
            "Требуются правки": 0,
            "Утвержден": 66
        },
        "yr": "2025",
        "plx_file": [
            "https://app.istu.edu/oop/uploads/rpd_plan/2025-04-07/09.03.02_%D0%98%D0%A1%D0%A2%D0%B1-25.plx"
        ]
    },
]

DATA_GENERATOR_4107 = {
    "admission": {
        "id": 25064,
        "yr": 2025,
        "abbr": "ИСТб",
        "cuchplan_id": 10179,
        "spec_name": "Информационные системы и технологии в административном управлении",
        "direct_name": "Информационные системы и технологии",
        "kvalif_name": "Бакалавр",
        "ckaf_id": 1988626,
        "cfac_id": 46,
        "ckaf__name": "Информационных технологий и анализа данных",
        "ckaf__ccatdep__nameshort": "Институт информационных технологий и анализа данных ",
        "cfac__name": "Институт информационных технологий и анализа данных",
        "cadmkind": 2,
        "cadmkind__name": "бакалавры",
        "cadmkind__name_prof": "профиль",
        "cdirection": 812733,
        "cdirection__name": "Информационные системы и технологии",
        "cdirection__cod": "09.03.02",
        "cspec": None,
        "cspec__name": None,
        "cspec__code": None,
        "cfob": 1,
        "cfob__name": "очная"
    },
    "other_discipline": [
        {
            "disid": 2076,
            "dis": "Web-программирование",
            "id": 10411,
            "semesters": [
                4,
                5
            ]
        },
        {
            "disid": 316,
            "dis": "Производственная практика: научно-исследовательская работа",
            "id": 10426,
            "semesters": [
                6
            ]
        },
        {
            "disid": 1417,
            "dis": "Моделирование процессов и систем",
            "id": 10417,
            "semesters": [
                5
            ]
        },
        {
            "disid": 136,
            "dis": "Интернет вещей",
            "id": 10451,
            "semesters": [
                6
            ]
        },
        {
            "disid": 202,
            "dis": "Элективные курсы по физической культуре и спорту",
            "id": 10475,
            "semesters": [
                2,
                3,
                4
            ]
        },
        {
            "disid": 2108,
            "dis": "Программирование на языке высокого уровня",
            "id": 10410,
            "semesters": [
                1,
                2
            ]
        },
        {
            "disid": 2051,
            "dis": "Исследование операций",
            "id": 10467,
            "semesters": [
                3
            ]
        },
        {
            "disid": 2111,
            "dis": "Распределённые вычисления",
            "id": 10420,
            "semesters": [
                6
            ]
        },
        {
            "disid": 1531,
            "dis": "Управление проектами",
            "id": 10421,
            "semesters": [
                5
            ]
        },
        {
            "disid": 2112,
            "dis": "Мониторинг безопасности информационных систем",
            "id": 10423,
            "semesters": [
                7
            ]
        },
        {
            "disid": 2113,
            "dis": "Основы DevOps",
            "id": 10424,
            "semesters": [
                7
            ]
        },
        {
            "disid": 297,
            "dis": "Компьютерная графика",
            "id": 10433,
            "semesters": [
                6
            ]
        },
        {
            "disid": 1975,
            "dis": "Технологическое предпринимательство",
            "id": 10434,
            "semesters": [
                6
            ]
        },
        {
            "disid": 2115,
            "dis": "Введение в AR/VR технологии",
            "id": 10435,
            "semesters": [
                7
            ]
        },
        {
            "disid": 8,
            "dis": "Иностранный язык",
            "id": 10437,
            "semesters": [
                1,
                2,
                3,
                4,
                5,
                8
            ]
        },
        {
            "disid": 186,
            "dis": "История России",
            "id": 10438,
            "semesters": [
                7
            ]
        },
        {
            "disid": 187,
            "dis": "Философия",
            "id": 10439,
            "semesters": [
                6
            ]
        },
        {
            "disid": 188,
            "dis": "Экономика",
            "id": 10440,
            "semesters": [
                7
            ]
        },
        {
            "disid": 189,
            "dis": "Основы деловой коммуникации",
            "id": 10441,
            "semesters": [
                1
            ]
        },
        {
            "disid": 190,
            "dis": "Правоведение",
            "id": 10442,
            "semesters": [
                5
            ]
        },
        {
            "disid": 1005,
            "dis": "Учебная практика: технологическая (проектно-технологическая) практика",
            "id": 10425,
            "semesters": [
                2
            ]
        },
        {
            "disid": 140,
            "dis": "Производственная практика: технологическая (проектно-технологическая) практика",
            "id": 10427,
            "semesters": [
                4
            ]
        },
        {
            "disid": 141,
            "dis": "Производственная практика: преддипломная практика",
            "id": 10428,
            "semesters": [
                8
            ]
        },
        {
            "disid": 191,
            "dis": "Безопасность жизнедеятельности",
            "id": 10443,
            "semesters": [
                8
            ]
        },
        {
            "disid": 2064,
            "dis": "Информатика",
            "id": 10447,
            "semesters": [
                1
            ]
        },
        {
            "disid": 199,
            "dis": "Основы проектной деятельности",
            "id": 10450,
            "semesters": [
                4
            ]
        },
        {
            "disid": 2116,
            "dis": "Введение в веб-технологии",
            "id": 10455,
            "semesters": [
                1
            ]
        },
        {
            "disid": 2117,
            "dis": "Архитектура ЭВМ и систем",
            "id": 10456,
            "semesters": [
                2
            ]
        },
        {
            "disid": 221,
            "dis": "Образовательный форсайт",
            "id": 10452,
            "semesters": [
                6
            ]
        },
        {
            "disid": 216,
            "dis": "Подготовка к сдаче квалификационного экзамена по иностранному языку",
            "id": 10453,
            "semesters": [
                8
            ]
        },
        {
            "disid": 2118,
            "dis": "Архитектура информационных систем",
            "id": 10457,
            "semesters": [
                4
            ]
        },
        {
            "disid": 2119,
            "dis": "Основы информационной безопасности",
            "id": 10458,
            "semesters": [
                5
            ]
        },
        {
            "disid": 2121,
            "dis": "Нейросетевые технологии",
            "id": 10460,
            "semesters": [
                5
            ]
        },
        {
            "disid": 2073,
            "dis": "Базы данных",
            "id": 10461,
            "semesters": [
                3
            ]
        },
        {
            "disid": 2122,
            "dis": "Интеллектуальные системы и технологии",
            "id": 10462,
            "semesters": [
                7
            ]
        },
        {
            "disid": 2123,
            "dis": "Основы мобильной разработки",
            "id": 10463,
            "semesters": [
                5,
                6
            ]
        },
        {
            "disid": 2124,
            "dis": "Технологии блокчейн",
            "id": 10465,
            "semesters": [
                6
            ]
        },
        {
            "disid": 2072,
            "dis": "Операционные системы",
            "id": 10466,
            "semesters": [
                3
            ]
        },
        {
            "disid": 2092,
            "dis": "Технологии программирования",
            "id": 10468,
            "semesters": [
                4
            ]
        },
        {
            "disid": 2125,
            "dis": "Анализ бизнес-процессов",
            "id": 10469,
            "semesters": [
                4
            ]
        },
        {
            "disid": 2126,
            "dis": "Корпоративные информационные системы",
            "id": 10470,
            "semesters": [
                8
            ]
        },
        {
            "disid": 224,
            "dis": "Основы инклюзивного взаимодействия",
            "id": 10471,
            "semesters": [
                2
            ]
        },
        {
            "disid": 225,
            "dis": "Критическое и системное мышление",
            "id": 10472,
            "semesters": [
                3
            ]
        },
        {
            "disid": 201,
            "dis": "Физическая культура и спорт",
            "id": 10474,
            "semesters": [
                1
            ]
        },
        {
            "disid": 816,
            "dis": "Общая физическая подготовка",
            "id": 10477,
            "semesters": [
                2,
                3,
                4
            ]
        },
        {
            "disid": 205,
            "dis": "Атлетическая гимнастика",
            "id": 10478,
            "semesters": [
                2,
                3,
                4
            ]
        },
        {
            "disid": 206,
            "dis": "Бокс",
            "id": 10479,
            "semesters": [
                2,
                3,
                4
            ]
        },
        {
            "disid": 2053,
            "dis": "Методы анализа данных",
            "id": 10412,
            "semesters": [
                4
            ]
        },
        {
            "disid": 2090,
            "dis": "Проектирование информационных систем",
            "id": 10414,
            "semesters": [
                7,
                8
            ]
        },
        {
            "disid": 2110,
            "dis": "Надежность информационных систем",
            "id": 10415,
            "semesters": [
                8
            ]
        },
        {
            "disid": 2050,
            "dis": "Объектно-ориентированное программирование",
            "id": 10418,
            "semesters": [
                3,
                4
            ]
        },
        {
            "disid": 193,
            "dis": "Математика",
            "id": 10445,
            "semesters": [
                1,
                2
            ]
        },
        {
            "disid": 2120,
            "dis": "Инфокоммуникационные системы и сети",
            "id": 10459,
            "semesters": [
                3
            ]
        },
        {
            "disid": 207,
            "dis": "Спортивные танцы",
            "id": 10480,
            "semesters": [
                2,
                3,
                4
            ]
        },
        {
            "disid": 208,
            "dis": "Аэробика",
            "id": 10481,
            "semesters": [
                2,
                3,
                4
            ]
        },
        {
            "disid": 209,
            "dis": "Оздоровительная физическая культура",
            "id": 10482,
            "semesters": [
                2,
                3,
                4
            ]
        },
        {
            "disid": 210,
            "dis": "Адаптивная физическая культура",
            "id": 10483,
            "semesters": [
                2,
                3,
                4
            ]
        },
        {
            "disid": 222,
            "dis": "Военно-прикладная физическая подготовка",
            "id": 10484,
            "semesters": [
                2,
                3,
                4
            ]
        },
        {
            "disid": 228,
            "dis": "Спортивные игры",
            "id": 10485,
            "semesters": [
                2,
                3,
                4
            ]
        },
        {
            "disid": 2127,
            "dis": "Основы Big Data",
            "id": 10486,
            "semesters": [
                6
            ]
        },
        {
            "disid": 229,
            "dis": "Основы российской государственности",
            "id": 10487,
            "semesters": [
                1
            ]
        },
        {
            "disid": 230,
            "dis": "Гиревой спорт",
            "id": 10488,
            "semesters": [
                2,
                3,
                4
            ]
        },
        {
            "disid": 2106,
            "dis": "Теория вероятностей и математическая статистика",
            "id": 10408,
            "semesters": [
                2
            ]
        },
        {
            "disid": 2107,
            "dis": "Математическая логика и дискретная математика",
            "id": 10409,
            "semesters": [
                3
            ]
        },
        {
            "disid": 2109,
            "dis": "Основы СППР",
            "id": 10413,
            "semesters": [
                7
            ]
        },
        {
            "disid": 2059,
            "dis": "Технологии разработки программных комплексов",
            "id": 10419,
            "semesters": [
                6
            ]
        },
        {
            "disid": 212,
            "dis": "Проектная деятельность",
            "id": 10431,
            "semesters": [
                5,
                6,
                7,
                8
            ]
        },
        {
            "disid": 194,
            "dis": "Физика",
            "id": 10446,
            "semesters": [
                1,
                2
            ]
        },
        {
            "disid": 2049,
            "dis": "Инженерная графика",
            "id": 10448,
            "semesters": [
                2
            ]
        }
    ],
    "resources": [
        {
            "id": 1,
            "name": "http://library.istu.edu/",
            "type": 0,
            "url": "http://library.istu.edu/"
        },
        {
            "id": 2,
            "name": "https://e.lanbook.com/",
            "type": 0,
            "url": "https://e.lanbook.com/"
        },
        {
            "id": 3,
            "name": "http://new.fips.ru/",
            "type": 1,
            "url": "http://new.fips.ru/"
        },
        {
            "id": 4,
            "name": "http://www1.fips.ru/",
            "type": 1,
            "url": "http://www1.fips.ru/"
        }
    ],
    "comment": None,
    "users": {
        "accepted": "Говорков Алексей Сергеевич",
        "developer": "Аршинский Вадим Леонидович",
        "confirmed": "Аршинский Вадим Леонидович"
    },
    "old": [
        {
            "abbrprofile": "ИСТб",
            "startyear": 2014,
            "id": 4077,
            "species": "Направление подготовки 09.03.02 \"Информационные системы и технологии\"Профиль \"Информационные системы и технологии в административном управлении\""
        },
        {
            "abbrprofile": "ИСТб",
            "startyear": 2015,
            "id": 4132,
            "species": "Направление 09.03.02 \"Информационные системы и технологии\"Профиль \"Информационные системы и технологии в административном управлении\""
        },
        {
            "abbrprofile": "ИСТб",
            "startyear": 2016,
            "id": 4187,
            "species": "Направление 09.03.02 \"Информационные системы и технологии\"Профиль \"Информационные системы и технологии в административном управлении\""
        },
        {
            "abbrprofile": "ИСТб",
            "startyear": 2018,
            "id": 40814,
            "species": "09.03.02 Информационные системы и технологии"
        },
        {
            "abbrprofile": "ИСТб",
            "startyear": 2019,
            "id": 66478,
            "species": "09.03.02 Информационные системы и технологии"
        },
        {
            "abbrprofile": "ИСТб",
            "startyear": 2020,
            "id": 66557,
            "species": "09.03.02 Информационные системы и технологии"
        },
        {
            "abbrprofile": "ИСТб",
            "startyear": 2021,
            "id": 79030,
            "species": "09.03.02 Информационные системы и технологии"
        },
        {
            "abbrprofile": "ИСТб",
            "startyear": 2022,
            "id": 91557,
            "species": "09.03.02 Информационные системы и технологии"
        },
        {
            "abbrprofile": "ИСТб",
            "startyear": 2023,
            "id": 104676,
            "species": "09.03.02 Информационные системы и технологии"
        },
        {
            "abbrprofile": "ИСТб",
            "startyear": 2024,
            "id": 117620,
            "species": "09.03.02 Информационные системы и технологии"
        }
    ],
    "new": [
        {
            "abbrprofile": "ИСТб",
            "species": "Учебная практика: технологическая (проектно-технологическая) практика",
            "startyear": 2025,
            "id": 9957
        },
        {
            "abbrprofile": "ИСТб",
            "species": "Производственная практика: технологическая (проектно-технологическая) практика",
            "startyear": 2025,
            "id": 9956
        },
        {
            "abbrprofile": "ИСТб",
            "species": "Производственная практика: преддипломная практика",
            "startyear": 2025,
            "id": 9955
        },
        {
            "abbrprofile": "ИСТб",
            "species": "Распределённые вычисления",
            "startyear": 2025,
            "id": 4121
        },
        {
            "abbrprofile": "ИСТб",
            "species": "Мониторинг безопасности информационных систем",
            "startyear": 2025,
            "id": 4048
        },
        {
            "abbrprofile": "ИСТб",
            "species": "Образовательный форсайт",
            "startyear": 2025,
            "id": 4106
        },
        {
            "abbrprofile": "ИСТб",
            "species": "Проектирование информационных систем",
            "startyear": 2025,
            "id": 4119
        },
        {
            "abbrprofile": "ИСТб",
            "species": "Объектно-ориентированное программирование",
            "startyear": 2025,
            "id": 4107
        },
        {
            "abbrprofile": "ИСТб",
            "species": "Проектная деятельность",
            "startyear": 2025,
            "id": 4120
        },
        {
            "abbrprofile": "АСУб",
            "species": "Объектно-ориентированное программирование",
            "startyear": 2025,
            "id": 4108
        },
        {
            "abbrprofile": "ЭВМбз",
            "species": "Объектно-ориентированное программирование",
            "startyear": 2025,
            "id": 4109
        },
        {
            "abbrprofile": "ЭВМб",
            "species": "Объектно-ориентированное программирование",
            "startyear": 2025,
            "id": 4110
        },
        {
            "abbrprofile": "АСУбз",
            "species": "Объектно-ориентированное программирование",
            "startyear": 2025,
            "id": 4111
        }
    ],
    "common": [
        {
            "abbrprofile": "ЭЛб",
            "species": "Аэродинамика (прикладная)",
            "startyear": 2025,
            "id": 9327
        },
        {
            "abbrprofile": "аТМД",
            "species": "Теоретическая механика, динамика машин",
            "startyear": 2025,
            "id": 482
        },
        {
            "abbrprofile": "ЭЛбз",
            "species": "Учебная практика: авиационно-механическая практика",
            "startyear": 2025,
            "id": 10910
        },
        {
            "abbrprofile": "БЖТбз",
            "species": "Учебная практика:ознакомительная практика",
            "startyear": 2025,
            "id": 10110
        },
        {
            "abbrprofile": "ЭЛбз",
            "species": "Производственная практика: технологическая (проектно-технологическая) практика",
            "startyear": 2025,
            "id": 10906
        },
        {
            "abbrprofile": "ЭЛбз",
            "species": "Производственная практика: эксплуатационная практика",
            "startyear": 2025,
            "id": 10909
        },
        {
            "abbrprofile": "ВЭАм",
            "species": "Иностранный язык в сфере профессиональной коммуникации / Forign Language in Professional Communication",
            "startyear": 2025,
            "id": 11699
        },
        {
            "abbrprofile": "АСПм",
            "species": "Защита металлов от коррозии",
            "startyear": 2025,
            "id": 8549
        },
        {
            "abbrprofile": "КТбз",
            "species": "Электротехника",
            "startyear": 2025,
            "id": 9571
        },
        {
            "abbrprofile": "ЭПАб",
            "species": "Математика / Mathematics",
            "startyear": 2025,
            "id": 9673
        },
        {
            "abbrprofile": "ЭСТм",
            "species": "Производственная практика: технологическая практика",
            "startyear": 2025,
            "id": 11037
        },
        {
            "abbrprofile": "ЭСТм",
            "species": "Производственная практика: преддипломная практика",
            "startyear": 2025,
            "id": 11036
        },
        {
            "abbrprofile": "МТбз",
            "species": "Технология и оборудование термической резки",
            "startyear": 2025,
            "id": 8592
        },
        {
            "abbrprofile": "ЭЛб",
            "species": "Безопасность полетов и сохранение летной годности",
            "startyear": 2025,
            "id": 9330
        },
        {
            "abbrprofile": "МАСм",
            "species": "Инфраструктура и дизайн архитектурной среды",
            "startyear": 2025,
            "id": 309
        },
        {
            "abbrprofile": "БЖТбз",
            "species": "Правоведение",
            "startyear": 2025,
            "id": 2279
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Анализ делового текста / Business Text Analysis",
            "startyear": 2025,
            "id": 11213
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Терминоведение / Terminology",
            "startyear": 2025,
            "id": 11275
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Спецкурс по английскому произношению / English pronunciation special course",
            "startyear": 2025,
            "id": 11761
        },
        {
            "abbrprofile": "ЖКб",
            "species": "Общая физическая подготовка  / General Physical Training",
            "startyear": 2025,
            "id": 8656
        },
        {
            "abbrprofile": "МЦбз",
            "species": "Математика",
            "startyear": 2025,
            "id": 2418
        },
        {
            "abbrprofile": "ММб",
            "species": "Физика",
            "startyear": 2025,
            "id": 4788
        },
        {
            "abbrprofile": "ММб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7889
        },
        {
            "abbrprofile": "ММб",
            "species": "Проектная деятельность",
            "startyear": 2025,
            "id": 821
        },
        {
            "abbrprofile": "ММб",
            "species": "Проектирование кинематики механизмов",
            "startyear": 2025,
            "id": 819
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Практикум по культуре речевого общения (первый иностранный язык)",
            "startyear": 2025,
            "id": 11853
        },
        {
            "abbrprofile": "ЭЛб",
            "species": "Производственная практика: ремонтная практика",
            "startyear": 2025,
            "id": 10785
        },
        {
            "abbrprofile": "ЛИМб",
            "species": "Физика",
            "startyear": 2025,
            "id": 4789
        },
        {
            "abbrprofile": "ЛИМб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 9293
        },
        {
            "abbrprofile": "АМПб",
            "species": "Аэробика",
            "startyear": 2025,
            "id": 8916
        },
        {
            "abbrprofile": "АМПб",
            "species": "Военно-прикладная физическая подготовка",
            "startyear": 2025,
            "id": 8926
        },
        {
            "abbrprofile": "АМПб",
            "species": "Спортивные игры",
            "startyear": 2025,
            "id": 8993
        },
        {
            "abbrprofile": "ЭПбз",
            "species": "Изоляция и перенапряжения",
            "startyear": 2025,
            "id": 5802
        },
        {
            "abbrprofile": "аММП",
            "species": "Математическое моделирование, численные методы и комплексы программ",
            "startyear": 2025,
            "id": 4156
        },
        {
            "abbrprofile": "ИИКб",
            "species": "Учебная практика: технологическая (проектно-технологическая) практика /  Educational Practice: Technological Practice",
            "startyear": 2025,
            "id": 11656
        },
        {
            "abbrprofile": "МТб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 8541
        },
        {
            "abbrprofile": "МТб",
            "species": "Технология и оборудование термической резки",
            "startyear": 2025,
            "id": 1155
        },
        {
            "abbrprofile": "ТД",
            "species": "Правоведение",
            "startyear": 2025,
            "id": 2247
        },
        {
            "abbrprofile": "ППТм",
            "species": "Проектирование технологической оснастки",
            "startyear": 2025,
            "id": 1173
        },
        {
            "abbrprofile": "МТбз",
            "species": "Производство сварных конструкций северного исполнения",
            "startyear": 2025,
            "id": 8577
        },
        {
            "abbrprofile": "МТбз",
            "species": "Химия",
            "startyear": 2025,
            "id": 7055
        },
        {
            "abbrprofile": "ЭПЭБз",
            "species": "Правоведение",
            "startyear": 2025,
            "id": 2256
        },
        {
            "abbrprofile": "АТПРб",
            "species": "Вычислительные системы и сети",
            "startyear": 2025,
            "id": 4911
        },
        {
            "abbrprofile": "АТПРб",
            "species": "Физика",
            "startyear": 2025,
            "id": 4795
        },
        {
            "abbrprofile": "АТПРб",
            "species": "Электроника и цифровая техника",
            "startyear": 2025,
            "id": 4976
        },
        {
            "abbrprofile": "ЭЛб",
            "species": "Производственная практика: технологическая (проектно-технологическая) практика",
            "startyear": 2025,
            "id": 10786
        },
        {
            "abbrprofile": "ЭЛб",
            "species": "Производственная практика: эксплуатационная практика",
            "startyear": 2025,
            "id": 10787
        },
        {
            "abbrprofile": "ЭЛб",
            "species": "Производственная практика: преддипломная практика",
            "startyear": 2025,
            "id": 10782
        },
        {
            "abbrprofile": "МАСм",
            "species": "Методология устойчивой архитектурной среды",
            "startyear": 2025,
            "id": 322
        },
        {
            "abbrprofile": "КТбз",
            "species": "Физика",
            "startyear": 2025,
            "id": 4794
        },
        {
            "abbrprofile": "КТбз",
            "species": "Процессы формообразования и металлообрабатывающий инструмент",
            "startyear": 2025,
            "id": 824
        },
        {
            "abbrprofile": "ЭЛб",
            "species": "Расследование авиапроиcшествий",
            "startyear": 2025,
            "id": 9497
        },
        {
            "abbrprofile": "КТбз",
            "species": "Проектирование и производство изделий из композиционных материалов",
            "startyear": 2025,
            "id": 818
        },
        {
            "abbrprofile": "ЭМЭНм",
            "species": "Возобновляемые источники энергии",
            "startyear": 2025,
            "id": 9370
        },
        {
            "abbrprofile": "ЭМЭНм",
            "species": "Экономический анализ и стратегическое управление",
            "startyear": 2025,
            "id": 3164
        },
        {
            "abbrprofile": "ММб",
            "species": "Процессы формообразования и металлообрабатывающий инструмент",
            "startyear": 2025,
            "id": 823
        },
        {
            "abbrprofile": "МИРб",
            "species": "Диагностика и надежность технологических систем",
            "startyear": 2025,
            "id": 4922
        },
        {
            "abbrprofile": "МИРб",
            "species": "Физика",
            "startyear": 2025,
            "id": 4793
        },
        {
            "abbrprofile": "МИРб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 9294
        },
        {
            "abbrprofile": "ЭВМб",
            "species": "Дискретная математика",
            "startyear": 2025,
            "id": 2721
        },
        {
            "abbrprofile": "ИИмз",
            "species": "Эконометрика (продвинутый уровень)",
            "startyear": 2025,
            "id": 1252
        },
        {
            "abbrprofile": "ЛИМбз",
            "species": "Физика",
            "startyear": 2025,
            "id": 4791
        },
        {
            "abbrprofile": "ИИм",
            "species": "Иностранный язык для магистрантов",
            "startyear": 2025,
            "id": 4084
        },
        {
            "abbrprofile": "ИИм",
            "species": "Экономический анализ и стратегическое управление",
            "startyear": 2025,
            "id": 1253
        },
        {
            "abbrprofile": "ЭЛб",
            "species": "Теория механизмов и машин",
            "startyear": 2025,
            "id": 4958
        },
        {
            "abbrprofile": "ААбз",
            "species": "Физика",
            "startyear": 2025,
            "id": 4792
        },
        {
            "abbrprofile": "ААбз",
            "species": "Химия",
            "startyear": 2025,
            "id": 6090
        },
        {
            "abbrprofile": "ААбз",
            "species": "Философия",
            "startyear": 2025,
            "id": 1733
        },
        {
            "abbrprofile": "НДДб",
            "species": "Введение в профессиональную деятельность",
            "startyear": 2025,
            "id": 8326
        },
        {
            "abbrprofile": "ГГз",
            "species": "Математика",
            "startyear": 2025,
            "id": 1819
        },
        {
            "abbrprofile": "ВДмз",
            "species": "Экономический анализ и стратегическое управление",
            "startyear": 2025,
            "id": 911
        },
        {
            "abbrprofile": "НДДб",
            "species": "Производственная практика: технологическая практика",
            "startyear": 2025,
            "id": 11999
        },
        {
            "abbrprofile": "ИЭб",
            "species": "Атлетическая гимнастика / Powerlifting",
            "startyear": 2025,
            "id": 9303
        },
        {
            "abbrprofile": "ИЭб",
            "species": "Второй иностранный язык (продвинутый курс) / Second Foreign Language (advanced level)",
            "startyear": 2025,
            "id": 11835
        },
        {
            "abbrprofile": "ИЭб",
            "species": "Спецкурс по английскому произношению / English pronunciation special course",
            "startyear": 2025,
            "id": 11756
        },
        {
            "abbrprofile": "МБб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 6404
        },
        {
            "abbrprofile": "МБб",
            "species": "Региональная экономика",
            "startyear": 2025,
            "id": 2708
        },
        {
            "abbrprofile": "МБб",
            "species": "Экономический анализ",
            "startyear": 2025,
            "id": 2713
        },
        {
            "abbrprofile": "ЭТЭКб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 5194
        },
        {
            "abbrprofile": "ЭТЭКб",
            "species": "Нефтегазовое дело",
            "startyear": 2025,
            "id": 8333
        },
        {
            "abbrprofile": "ЭТЭКб",
            "species": "Экономический анализ",
            "startyear": 2025,
            "id": 1431
        },
        {
            "abbrprofile": "ЭТЭКб",
            "species": "Основы экономической оценки инвестиций",
            "startyear": 2025,
            "id": 5690
        },
        {
            "abbrprofile": "НДДб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 8358
        },
        {
            "abbrprofile": "ФКб",
            "species": "Философия",
            "startyear": 2025,
            "id": 1516
        },
        {
            "abbrprofile": "ФКб",
            "species": "Экономика",
            "startyear": 2025,
            "id": 1425
        },
        {
            "abbrprofile": "ФКб",
            "species": "Основы деловой коммуникации",
            "startyear": 2025,
            "id": 1512
        },
        {
            "abbrprofile": "ФКб",
            "species": "Физическая культура и спорт",
            "startyear": 2025,
            "id": 5925
        },
        {
            "abbrprofile": "ФКб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 5915
        },
        {
            "abbrprofile": "ФНб",
            "species": "Второй иностранный язык (продвинутый курс) / Second Foreign Language (advanced level)",
            "startyear": 2025,
            "id": 11834
        },
        {
            "abbrprofile": "ФНб",
            "species": "Атлетическая гимнастика / Powerlifting",
            "startyear": 2025,
            "id": 9302
        },
        {
            "abbrprofile": "ФНб",
            "species": "Спецкурс по английскому произношению / English pronunciation special course",
            "startyear": 2025,
            "id": 11755
        },
        {
            "abbrprofile": "ФНб",
            "species": "Второй иностранный язык / Second Foreign Language",
            "startyear": 2025,
            "id": 11837
        },
        {
            "abbrprofile": "НДм",
            "species": "Нефтегазопромысловое дело",
            "startyear": 2025,
            "id": 7800
        },
        {
            "abbrprofile": "НДб",
            "species": "Реконструкция и восстановление скважин",
            "startyear": 2025,
            "id": 8340
        },
        {
            "abbrprofile": "НДм",
            "species": "Производственная практика: технологическая практика",
            "startyear": 2025,
            "id": 10849
        },
        {
            "abbrprofile": "НДм",
            "species": "Капитальный ремонт скважин",
            "startyear": 2025,
            "id": 8330
        },
        {
            "abbrprofile": "НДб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 8357
        },
        {
            "abbrprofile": "РРб",
            "species": "Производственная практика: проектно-технологическая практика",
            "startyear": 2025,
            "id": 9818
        },
        {
            "abbrprofile": "РРб",
            "species": "Архитектурно-реставрационное материаловедение",
            "startyear": 2025,
            "id": 1259
        },
        {
            "abbrprofile": "РРб",
            "species": "История пространственных искусств Сибири",
            "startyear": 2025,
            "id": 7474
        },
        {
            "abbrprofile": "ИГ",
            "species": "Производственная практика: преддипломная практика",
            "startyear": 2025,
            "id": 10681
        },
        {
            "abbrprofile": "ГРб",
            "species": "Основы теории градостроительства",
            "startyear": 2025,
            "id": 7586
        },
        {
            "abbrprofile": "ГРб",
            "species": "Архитектурно-строительное проектирование",
            "startyear": 2025,
            "id": 7395
        },
        {
            "abbrprofile": "ГРб",
            "species": "Основы градостроительной статистики",
            "startyear": 2025,
            "id": 8532
        },
        {
            "abbrprofile": "ГРб",
            "species": "Основы градостроительного мониторинга",
            "startyear": 2025,
            "id": 7573
        },
        {
            "abbrprofile": "ГРб",
            "species": "Проектирование набережных в городском благоустройстве",
            "startyear": 2025,
            "id": 7602
        },
        {
            "abbrprofile": "ГРб",
            "species": "Городское озеленение и благоустройство",
            "startyear": 2025,
            "id": 7438
        },
        {
            "abbrprofile": "ГРб",
            "species": "Спортивные танцы",
            "startyear": 2025,
            "id": 7628
        },
        {
            "abbrprofile": "ДСб",
            "species": "Производственная практика: проектно-технологическая практика",
            "startyear": 2025,
            "id": 385
        },
        {
            "abbrprofile": "ДСб",
            "species": "История дизайна городской среды",
            "startyear": 2025,
            "id": 311
        },
        {
            "abbrprofile": "ДСб",
            "species": "Предметное наполнение архитектурной среды",
            "startyear": 2025,
            "id": 338
        },
        {
            "abbrprofile": "ДСб",
            "species": "Основы теории формирования среды",
            "startyear": 2025,
            "id": 335
        },
        {
            "abbrprofile": "ДСб",
            "species": "Современные проблемы архитектурной среды городов Сибири",
            "startyear": 2025,
            "id": 351
        },
        {
            "abbrprofile": "ДСб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 6100
        },
        {
            "abbrprofile": "БЖТбз",
            "species": "Электротехника и электроника",
            "startyear": 2025,
            "id": 9731
        },
        {
            "abbrprofile": "ЭЛбз",
            "species": "Производственная практика: ремонтная практика",
            "startyear": 2025,
            "id": 10904
        },
        {
            "abbrprofile": "ГРм",
            "species": "Методы реконструкции градостроительных объектов",
            "startyear": 2025,
            "id": 7511
        },
        {
            "abbrprofile": "ЭСб",
            "species": "Иностранный язык",
            "startyear": 2025,
            "id": 2774
        },
        {
            "abbrprofile": "РРб",
            "species": "Теория архитектуры, исследования памятников архитектуры",
            "startyear": 2025,
            "id": 7640
        },
        {
            "abbrprofile": "РРб",
            "species": "Компьютерное моделирование",
            "startyear": 2025,
            "id": 7479
        },
        {
            "abbrprofile": "РРб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7398
        },
        {
            "abbrprofile": "ЭЛбз",
            "species": "Производственная практика: преддипломная практика",
            "startyear": 2025,
            "id": 10898
        },
        {
            "abbrprofile": "АРб",
            "species": "Ландшафтная архитектура",
            "startyear": 2025,
            "id": 315
        },
        {
            "abbrprofile": "ЭСб",
            "species": "Правоведение",
            "startyear": 2025,
            "id": 2268
        },
        {
            "abbrprofile": "АРб",
            "species": "Ландшафтосообразность архитектурного развития",
            "startyear": 2025,
            "id": 318
        },
        {
            "abbrprofile": "АРб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 6099
        },
        {
            "abbrprofile": "АРб",
            "species": "Бокс",
            "startyear": 2025,
            "id": 6103
        },
        {
            "abbrprofile": "АРб",
            "species": "Адаптивная физическая культура",
            "startyear": 2025,
            "id": 6097
        },
        {
            "abbrprofile": "АРб",
            "species": "История архитектуры и градостроительства",
            "startyear": 2025,
            "id": 3992
        },
        {
            "abbrprofile": "АРб",
            "species": "Архитектурное  проектирование",
            "startyear": 2025,
            "id": 302
        },
        {
            "abbrprofile": "АРб",
            "species": "Рисунок",
            "startyear": 2025,
            "id": 3998
        },
        {
            "abbrprofile": "АРб",
            "species": "Военно-прикладная физическая подготовка",
            "startyear": 2025,
            "id": 6105
        },
        {
            "abbrprofile": "АРб",
            "species": "Спортивные игры",
            "startyear": 2025,
            "id": 6119
        },
        {
            "abbrprofile": "ЭПАб",
            "species": "Атлетическая гимнастика / Powerlifting",
            "startyear": 2025,
            "id": 9304
        },
        {
            "abbrprofile": "ЭПАб",
            "species": "Второй иностранный язык / Second Foreign Language",
            "startyear": 2025,
            "id": 11692
        },
        {
            "abbrprofile": "ЭПб",
            "species": "Электрические машины",
            "startyear": 2025,
            "id": 7176
        },
        {
            "abbrprofile": "ЭПб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7132
        },
        {
            "abbrprofile": "ЭСб",
            "species": "Электрические машины",
            "startyear": 2025,
            "id": 5425
        },
        {
            "abbrprofile": "ЭПб",
            "species": "Изоляция и перенапряжения",
            "startyear": 2025,
            "id": 5801
        },
        {
            "abbrprofile": "ЭПб",
            "species": "Испытание и диагностика электрической изоляции и кабельных изделий",
            "startyear": 2025,
            "id": 5803
        },
        {
            "abbrprofile": "ЭСб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 5207
        },
        {
            "abbrprofile": "ВЭАм",
            "species": "Современные проблемы электроэнергетики и электротехники / Modern problems of power engineering and electrical engineering",
            "startyear": 2025,
            "id": 9697
        },
        {
            "abbrprofile": "БЖТбз",
            "species": "Иностранный язык",
            "startyear": 2025,
            "id": 1578
        },
        {
            "abbrprofile": "ИЭм",
            "species": "Современные проблемы электроэнергетики и электротехники",
            "startyear": 2025,
            "id": 8143
        },
        {
            "abbrprofile": "ИЭм",
            "species": "Избранные вопросы теории цепей",
            "startyear": 2025,
            "id": 5610
        },
        {
            "abbrprofile": "ЭЛбз",
            "species": "Расследование авиапроиcшествий",
            "startyear": 2025,
            "id": 9090
        },
        {
            "abbrprofile": "ЭУм",
            "species": "Тепловизионная диагностика",
            "startyear": 2025,
            "id": 5807
        },
        {
            "abbrprofile": "АМПб",
            "species": "Физика",
            "startyear": 2025,
            "id": 6455
        },
        {
            "abbrprofile": "АТПб",
            "species": "Физика",
            "startyear": 2025,
            "id": 4797
        },
        {
            "abbrprofile": "МЦбз",
            "species": "Моделирование процессов и объектов в металлургии",
            "startyear": 2025,
            "id": 1019
        },
        {
            "abbrprofile": "МЦбз",
            "species": "Металлургия вторичных металлов",
            "startyear": 2025,
            "id": 1009
        },
        {
            "abbrprofile": "АТПбз",
            "species": "Химия",
            "startyear": 2025,
            "id": 3768
        },
        {
            "abbrprofile": "ЭПмз",
            "species": "Надежность систем электроснабжения",
            "startyear": 2025,
            "id": 7091
        },
        {
            "abbrprofile": "ЭПмз",
            "species": "Системы коммерческого учета энергоресурсов",
            "startyear": 2025,
            "id": 7102
        },
        {
            "abbrprofile": "ЭПмз",
            "species": "Потребители электрической энергии и энергосбережение",
            "startyear": 2025,
            "id": 8081
        },
        {
            "abbrprofile": "ЭПмз",
            "species": "Физические основы нетрадиционных и возобновляемых источников энергии",
            "startyear": 2025,
            "id": 8164
        },
        {
            "abbrprofile": "АСУб",
            "species": "Дискретная математика",
            "startyear": 2025,
            "id": 2720
        },
        {
            "abbrprofile": "АСУб",
            "species": "Математическая логика и теория алгоритмов",
            "startyear": 2025,
            "id": 2737
        },
        {
            "abbrprofile": "АСУб",
            "species": "Компьютерная графика",
            "startyear": 2025,
            "id": 2731
        },
        {
            "abbrprofile": "АСУб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 8789
        },
        {
            "abbrprofile": "АСУб",
            "species": "Военно-прикладная физическая подготовка",
            "startyear": 2025,
            "id": 8795
        },
        {
            "abbrprofile": "БТб",
            "species": "Общая физическая подготовка",
            "startyear": 2025,
            "id": 7929
        },
        {
            "abbrprofile": "БТб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7923
        },
        {
            "abbrprofile": "БТб",
            "species": "Основы проектирования биотехнологических предприятий",
            "startyear": 2025,
            "id": 195
        },
        {
            "abbrprofile": "БТб",
            "species": "Гиревой спорт",
            "startyear": 2025,
            "id": 7927
        },
        {
            "abbrprofile": "ЭПбз",
            "species": "Проектная деятельность",
            "startyear": 2025,
            "id": 9087
        },
        {
            "abbrprofile": "ЭПбз",
            "species": "Силовая электроника",
            "startyear": 2025,
            "id": 6822
        },
        {
            "abbrprofile": "ЭПбз",
            "species": "Надежность систем электроснабжения",
            "startyear": 2025,
            "id": 6777
        },
        {
            "abbrprofile": "ЭПбз",
            "species": "Испытание и диагностика электрической изоляции и кабельных изделий",
            "startyear": 2025,
            "id": 5804
        },
        {
            "abbrprofile": "ЭПбз",
            "species": "Правоведение",
            "startyear": 2025,
            "id": 2274
        },
        {
            "abbrprofile": "НБ",
            "species": "Физическая культура и спорт",
            "startyear": 2025,
            "id": 6385
        },
        {
            "abbrprofile": "НБ",
            "species": "Политические аспекты национальной безопасности",
            "startyear": 2025,
            "id": 878
        },
        {
            "abbrprofile": "МЦб",
            "species": "Экономика",
            "startyear": 2025,
            "id": 2422
        },
        {
            "abbrprofile": "МЦб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 5527
        },
        {
            "abbrprofile": "МЦТб",
            "species": "Физическая культура и спорт",
            "startyear": 2025,
            "id": 5440
        },
        {
            "abbrprofile": "МЦТб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 5431
        },
        {
            "abbrprofile": "МЦТб",
            "species": "Металлургия вторичных металлов",
            "startyear": 2025,
            "id": 5154
        },
        {
            "abbrprofile": "МЦТб",
            "species": "Математическое моделирование эксперимента",
            "startyear": 2025,
            "id": 5176
        },
        {
            "abbrprofile": "МЦТб",
            "species": "Сухая газоочистка цехов электролиза",
            "startyear": 2025,
            "id": 5168
        },
        {
            "abbrprofile": "ЭОСб",
            "species": "Атлетическая гимнастика / Powerlifting",
            "startyear": 2025,
            "id": 5242
        },
        {
            "abbrprofile": "ЭОСб",
            "species": "Бокс / Boxing",
            "startyear": 2025,
            "id": 5244
        },
        {
            "abbrprofile": "ЭОСб",
            "species": "Иностранный язык / First foreign language",
            "startyear": 2025,
            "id": 11743
        },
        {
            "abbrprofile": "БЖТм",
            "species": "Наилучшие доступные технологии (\"зеленые\" технологии)",
            "startyear": 2025,
            "id": 3522
        },
        {
            "abbrprofile": "ПБмз",
            "species": "Основы производственной и пожарной автоматики",
            "startyear": 2025,
            "id": 3525
        },
        {
            "abbrprofile": "ЭПОб",
            "species": "Оценка бизнеса",
            "startyear": 2025,
            "id": 6343
        },
        {
            "abbrprofile": "ЭПОб",
            "species": "Закупочная деятельность в строительстве",
            "startyear": 2025,
            "id": 6298
        },
        {
            "abbrprofile": "НГДДСз",
            "species": "Капитальный и текущий ремонт скважин",
            "startyear": 2025,
            "id": 8193
        },
        {
            "abbrprofile": "НГДДСз",
            "species": "Подземная гидромеханика",
            "startyear": 2025,
            "id": 8419
        },
        {
            "abbrprofile": "НГДДСз",
            "species": "Экономика",
            "startyear": 2025,
            "id": 3133
        },
        {
            "abbrprofile": "НГДДСз",
            "species": "Основы нефтегазового дела",
            "startyear": 2025,
            "id": 7914
        },
        {
            "abbrprofile": "НГДСз",
            "species": "Разрушение горных пород",
            "startyear": 2025,
            "id": 8242
        },
        {
            "abbrprofile": "НГДСз",
            "species": "Реконструкция и восстановление скважин",
            "startyear": 2025,
            "id": 8245
        },
        {
            "abbrprofile": "НГДСз",
            "species": "Основы нефтегазового дела",
            "startyear": 2025,
            "id": 7915
        },
        {
            "abbrprofile": "ЭПОб",
            "species": "Экономический анализ",
            "startyear": 2025,
            "id": 3163
        },
        {
            "abbrprofile": "НГЛСз",
            "species": "Основные технологии нефтегазового производства",
            "startyear": 2025,
            "id": 8306
        },
        {
            "abbrprofile": "НГЛСз",
            "species": "Организация и безопасность движения на месторождениях",
            "startyear": 2025,
            "id": 8410
        },
        {
            "abbrprofile": "НГЛСз",
            "species": "Компьютерное моделирование транспортно-логистического сопровождения",
            "startyear": 2025,
            "id": 8382
        },
        {
            "abbrprofile": "НГЛСз",
            "species": "Планировка объектов жизнеобеспечения на месторождении",
            "startyear": 2025,
            "id": 8417
        },
        {
            "abbrprofile": "НГЛСз",
            "species": "Технологические процессы приёма, хранения и отгрузки УВС",
            "startyear": 2025,
            "id": 8342
        },
        {
            "abbrprofile": "НГЛСз",
            "species": "Производственная практика: эксплуатационная практика",
            "startyear": 2025,
            "id": 10124
        },
        {
            "abbrprofile": "НГЛСз",
            "species": "Технологические процессы трубопроводного транспорта",
            "startyear": 2025,
            "id": 8450
        },
        {
            "abbrprofile": "НГЛСз",
            "species": "Интеллектуальные транспортные системы в нефтегазовом комплексе",
            "startyear": 2025,
            "id": 8377
        },
        {
            "abbrprofile": "НГЛСз",
            "species": "Мультимодальные транспортные системы",
            "startyear": 2025,
            "id": 8400
        },
        {
            "abbrprofile": "НГЛСз",
            "species": "Основы нефтегазового дела",
            "startyear": 2025,
            "id": 8335
        },
        {
            "abbrprofile": "АСУбз",
            "species": "Дискретная математика",
            "startyear": 2025,
            "id": 3445
        },
        {
            "abbrprofile": "АСУбз",
            "species": "Математическая логика и теория алгоритмов",
            "startyear": 2025,
            "id": 3450
        },
        {
            "abbrprofile": "НГЛСз",
            "species": "Правоведение",
            "startyear": 2025,
            "id": 2280
        },
        {
            "abbrprofile": "ИРб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 9052
        },
        {
            "abbrprofile": "УОБТб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 5390
        },
        {
            "abbrprofile": "УПб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 5401
        },
        {
            "abbrprofile": "УПб",
            "species": "Управление бизнес-процессами и ERP-системы",
            "startyear": 2025,
            "id": 145
        },
        {
            "abbrprofile": "АСУбз",
            "species": "Физика",
            "startyear": 2025,
            "id": 3453
        },
        {
            "abbrprofile": "ИСИб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 8788
        },
        {
            "abbrprofile": "ИИКб",
            "species": "Введение в специальность / Introduction to the specialty",
            "startyear": 2025,
            "id": 11492
        },
        {
            "abbrprofile": "ИИКб",
            "species": "Второй иностранный язык (продвинутый курс) / Second Foreign Language (advanced level)",
            "startyear": 2025,
            "id": 11828
        },
        {
            "abbrprofile": "ЭВМб",
            "species": "Защита информации",
            "startyear": 2025,
            "id": 4842
        },
        {
            "abbrprofile": "ЭВМб",
            "species": "Интеллектные вычислительные системы",
            "startyear": 2025,
            "id": 5308
        },
        {
            "abbrprofile": "ЭВМб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 5262
        },
        {
            "abbrprofile": "ЭВМбз",
            "species": "Математика",
            "startyear": 2025,
            "id": 3690
        },
        {
            "abbrprofile": "ИСТб",
            "species": "Основы деловой коммуникации",
            "startyear": 2025,
            "id": 1949
        },
        {
            "abbrprofile": "ИСТб",
            "species": "Введение в веб-технологии",
            "startyear": 2025,
            "id": 4021
        },
        {
            "abbrprofile": "ИСТб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7017
        },
        {
            "abbrprofile": "ИИКб",
            "species": "Атлетическая гимнастика / Powerlifting",
            "startyear": 2025,
            "id": 9305
        },
        {
            "abbrprofile": "ГА",
            "species": "Иностранный язык",
            "startyear": 2025,
            "id": 1208
        },
        {
            "abbrprofile": "ИИКб",
            "species": "Военно-прикладная физическая подготовка / Military-applied Physical Training",
            "startyear": 2025,
            "id": 9365
        },
        {
            "abbrprofile": "ГАз",
            "species": "Физика",
            "startyear": 2025,
            "id": 3760
        },
        {
            "abbrprofile": "ГАз",
            "species": "Электроснабжение горного производства",
            "startyear": 2025,
            "id": 4543
        },
        {
            "abbrprofile": "ИИКб",
            "species": "Спецкурс по английскому произношению / English pronunciation special course",
            "startyear": 2025,
            "id": 11757
        },
        {
            "abbrprofile": "ИИКб",
            "species": "Практикум по культуре профессиональной коммуникации (второй иностранный язык) / Practical course for professional communication (Second foreign language)",
            "startyear": 2025,
            "id": 11831
        },
        {
            "abbrprofile": "ГАз",
            "species": "Иностранный язык",
            "startyear": 2025,
            "id": 1210
        },
        {
            "abbrprofile": "ГГ",
            "species": "Математика",
            "startyear": 2025,
            "id": 1820
        },
        {
            "abbrprofile": "ГГ",
            "species": "Адаптивная физическая культура",
            "startyear": 2025,
            "id": 8661
        },
        {
            "abbrprofile": "ИИКб",
            "species": "Спортивные игры / Sport games",
            "startyear": 2025,
            "id": 9508
        },
        {
            "abbrprofile": "ИИКб",
            "species": "Второй иностранный язык / Second Foreign Language",
            "startyear": 2025,
            "id": 11829
        },
        {
            "abbrprofile": "ГГз",
            "species": "Электроснабжение горного производства",
            "startyear": 2025,
            "id": 4019
        },
        {
            "abbrprofile": "ГМ",
            "species": "Основы электротехники",
            "startyear": 2025,
            "id": 8628
        },
        {
            "abbrprofile": "ГМ",
            "species": "Иностранный язык",
            "startyear": 2025,
            "id": 1207
        },
        {
            "abbrprofile": "ГМ",
            "species": "Спортивные танцы",
            "startyear": 2025,
            "id": 8633
        },
        {
            "abbrprofile": "ГМз",
            "species": "Электроснабжение горного производства",
            "startyear": 2025,
            "id": 4541
        },
        {
            "abbrprofile": "ГМз",
            "species": "Иностранный язык",
            "startyear": 2025,
            "id": 1205
        },
        {
            "abbrprofile": "ГО",
            "species": "Основы электротехники",
            "startyear": 2025,
            "id": 8276
        },
        {
            "abbrprofile": "ГП",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7188
        },
        {
            "abbrprofile": "ГПз",
            "species": "Электроснабжение горного производства",
            "startyear": 2025,
            "id": 4542
        },
        {
            "abbrprofile": "ГПз",
            "species": "Геомеханика и управление массивом",
            "startyear": 2025,
            "id": 6172
        },
        {
            "abbrprofile": "ОП",
            "species": "Иностранный язык",
            "startyear": 2025,
            "id": 1206
        },
        {
            "abbrprofile": "ОПз",
            "species": "Электроснабжение горного производства",
            "startyear": 2025,
            "id": 4238
        },
        {
            "abbrprofile": "ОПз",
            "species": "Иностранный язык",
            "startyear": 2025,
            "id": 1209
        },
        {
            "abbrprofile": "СДМ",
            "species": "Теория механизмов и машин",
            "startyear": 2025,
            "id": 4957
        },
        {
            "abbrprofile": "СДМ",
            "species": "Физика",
            "startyear": 2025,
            "id": 6456
        },
        {
            "abbrprofile": "СДМз",
            "species": "Математика",
            "startyear": 2025,
            "id": 3589
        },
        {
            "abbrprofile": "СДМз",
            "species": "Физика",
            "startyear": 2025,
            "id": 3612
        },
        {
            "abbrprofile": "ЭПмз",
            "species": "Учебная практика: ознакомительная практика",
            "startyear": 2025,
            "id": 10674
        },
        {
            "abbrprofile": "НГДСз",
            "species": "Учебная практика: ознакомительная практика",
            "startyear": 2025,
            "id": 9909
        },
        {
            "abbrprofile": "ЭПб",
            "species": "Учебная практика: ознакомительная практика",
            "startyear": 2025,
            "id": 10672
        },
        {
            "abbrprofile": "ММб",
            "species": "Учебная практика: ознакомительная практика",
            "startyear": 2025,
            "id": 10788
        },
        {
            "abbrprofile": "ЛИМбз",
            "species": "Производственная практика: технологическая (производственно-технологическая) практика",
            "startyear": 2025,
            "id": 12118
        },
        {
            "abbrprofile": "НДм",
            "species": "Производственная практика: научно-исследовательская работа",
            "startyear": 2025,
            "id": 10847
        },
        {
            "abbrprofile": "ЛИМбз",
            "species": "Производственная практика: технологическая (производственно-технологическая) практика",
            "startyear": 2025,
            "id": 610
        },
        {
            "abbrprofile": "ГРб",
            "species": "Производственная практика: технологическая (проектно-технологическая) практика",
            "startyear": 2025,
            "id": 11016
        },
        {
            "abbrprofile": "ЛИМб",
            "species": "Производственная практика: технологическая (производственно-технологическая) практика",
            "startyear": 2025,
            "id": 12117
        },
        {
            "abbrprofile": "ИИТм",
            "species": "Производственная практика: технологическая (проектно-технологическая) практика",
            "startyear": 2025,
            "id": 11688
        },
        {
            "abbrprofile": "РРб",
            "species": "Производственная практика: преддипломная практика",
            "startyear": 2025,
            "id": 9817
        },
        {
            "abbrprofile": "АТПб",
            "species": "Производственная практика: преддипломная практика",
            "startyear": 2025,
            "id": 10717
        },
        {
            "abbrprofile": "УЛм",
            "species": "Деловой английский язык / Business English",
            "startyear": 2025,
            "id": 11752
        },
        {
            "abbrprofile": "УЛм",
            "species": "Иностранный язык в сфере профессиональной коммуникации / Foreign Language in Professional Communication",
            "startyear": 2025,
            "id": 11329
        },
        {
            "abbrprofile": "ИМбз",
            "species": "Физическая культура и спорт",
            "startyear": 2025,
            "id": 6872
        },
        {
            "abbrprofile": "ИМбз",
            "species": "Основы нефтегазового дела",
            "startyear": 2025,
            "id": 8336
        },
        {
            "abbrprofile": "ИМбз",
            "species": "Супервайзинг в инновационной деятельности",
            "startyear": 2025,
            "id": 6839
        },
        {
            "abbrprofile": "ИМбз",
            "species": "Реверс технологии в нефтегазовом комплексе",
            "startyear": 2025,
            "id": 6821
        },
        {
            "abbrprofile": "УКб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 6482
        },
        {
            "abbrprofile": "РТз",
            "species": "Правоведение",
            "startyear": 2025,
            "id": 2295
        },
        {
            "abbrprofile": "ХТОб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 8094
        },
        {
            "abbrprofile": "ЭЛб",
            "species": "Физика",
            "startyear": 2025,
            "id": 6460
        },
        {
            "abbrprofile": "ЭЛб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7890
        },
        {
            "abbrprofile": "ЭЛбз",
            "species": "Образовательный форсайт",
            "startyear": 2025,
            "id": 9081
        },
        {
            "abbrprofile": "ЭЛбз",
            "species": "Математика",
            "startyear": 2025,
            "id": 6759
        },
        {
            "abbrprofile": "ЭПОб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 6264
        },
        {
            "abbrprofile": "ГСХб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 5950
        },
        {
            "abbrprofile": "ПГСб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 5984
        },
        {
            "abbrprofile": "ХТТб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 8093
        },
        {
            "abbrprofile": "УСТб",
            "species": "Оценка стоимости предприятия",
            "startyear": 2025,
            "id": 7594
        },
        {
            "abbrprofile": "УСТб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7401
        },
        {
            "abbrprofile": "СНГб",
            "species": "Технология подземного хранения газа",
            "startyear": 2025,
            "id": 9115
        },
        {
            "abbrprofile": "СНГб",
            "species": "Гидравлика и нефтегазовая гидромеханика",
            "startyear": 2025,
            "id": 8227
        },
        {
            "abbrprofile": "СНГб",
            "species": "Основы автоматизации технологических процессов нефтегазового производства",
            "startyear": 2025,
            "id": 5754
        },
        {
            "abbrprofile": "СНГб",
            "species": "Проектирование трубопроводного транспорта и хранилищ",
            "startyear": 2025,
            "id": 6540
        },
        {
            "abbrprofile": "СНГб",
            "species": "Проектирование объектов нефтегазового комплекса",
            "startyear": 2025,
            "id": 6539
        },
        {
            "abbrprofile": "СНГб",
            "species": "Устройство подземных нефтегазопроводов",
            "startyear": 2025,
            "id": 10736
        },
        {
            "abbrprofile": "СНГб",
            "species": "Подготовка к транспорту нефти и газа",
            "startyear": 2025,
            "id": 6537
        },
        {
            "abbrprofile": "СНГб",
            "species": "Нефтегазопромысловое оборудование",
            "startyear": 2025,
            "id": 5750
        },
        {
            "abbrprofile": "СНГб",
            "species": "Оценка инновационных решений в нефтегазовом комплексе",
            "startyear": 2025,
            "id": 9112
        },
        {
            "abbrprofile": "СНГб",
            "species": "Повышение эффективности и надежности функционирования магистральных нефтегазопроводов",
            "startyear": 2025,
            "id": 6536
        },
        {
            "abbrprofile": "СНГб",
            "species": "Геоинформационные технологии транспорта и хранения нефти и газа",
            "startyear": 2025,
            "id": 10735
        },
        {
            "abbrprofile": "СНГб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7399
        },
        {
            "abbrprofile": "СНГб",
            "species": "Проектная деятельность",
            "startyear": 2025,
            "id": 6541
        },
        {
            "abbrprofile": "СНГб",
            "species": "Техническое обслуживание, ремонт и диагностическое обследование нефтегазового оборудования",
            "startyear": 2025,
            "id": 9748
        },
        {
            "abbrprofile": "ЭУНб",
            "species": "Оценка бизнеса",
            "startyear": 2025,
            "id": 7591
        },
        {
            "abbrprofile": "ЭУНб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7403
        },
        {
            "abbrprofile": "ХТОб",
            "species": "Аналитическая химия и физико-химические методы анализа",
            "startyear": 2025,
            "id": 7036
        },
        {
            "abbrprofile": "ХТОб",
            "species": "Технология химико-фармацевтических препаратов",
            "startyear": 2025,
            "id": 8004
        },
        {
            "abbrprofile": "ТГВм",
            "species": "Моделирование в решении научно-технических задач строительства",
            "startyear": 2025,
            "id": 5749
        },
        {
            "abbrprofile": "ТГВм",
            "species": "Методология прогнозирования параметров систем теплогазоснабжения и вентиляции",
            "startyear": 2025,
            "id": 6530
        },
        {
            "abbrprofile": "ЮРУб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 6268
        },
        {
            "abbrprofile": "УСТм",
            "species": "Оценка стоимости предприятия (бизнеса)",
            "startyear": 2025,
            "id": 7596
        },
        {
            "abbrprofile": "ТМПм",
            "species": "Фундаментальные и прикладные исследования в строительстве и жилищно-коммунальном хозяйстве",
            "startyear": 2025,
            "id": 5761
        },
        {
            "abbrprofile": "АД",
            "species": "Механика грунтов и основания и фундаменты транспортных сооружений",
            "startyear": 2025,
            "id": 3915
        },
        {
            "abbrprofile": "АД",
            "species": "Эксплуатация и техническое прикрытие автомобильных дорог",
            "startyear": 2025,
            "id": 3938
        },
        {
            "abbrprofile": "АД",
            "species": "Физика",
            "startyear": 2025,
            "id": 6470
        },
        {
            "abbrprofile": "АД",
            "species": "Физическая культура и спорт",
            "startyear": 2025,
            "id": 7669
        },
        {
            "abbrprofile": "АД",
            "species": "Общая физическая подготовка",
            "startyear": 2025,
            "id": 7541
        },
        {
            "abbrprofile": "АД",
            "species": "Военно-прикладная физическая подготовка",
            "startyear": 2025,
            "id": 7428
        },
        {
            "abbrprofile": "ИБб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 8730
        },
        {
            "abbrprofile": "РДбз",
            "species": "Математика",
            "startyear": 2025,
            "id": 6760
        },
        {
            "abbrprofile": "РДб",
            "species": "Схемотехника аналоговых электронных устройств",
            "startyear": 2025,
            "id": 9105
        },
        {
            "abbrprofile": "РДб",
            "species": "Цифровая обработка сигналов",
            "startyear": 2025,
            "id": 9108
        },
        {
            "abbrprofile": "РДб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 9143
        },
        {
            "abbrprofile": "ИФб",
            "species": "Цифровая обработка сигналов",
            "startyear": 2025,
            "id": 9107
        },
        {
            "abbrprofile": "ИФб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 9142
        },
        {
            "abbrprofile": "ПОм",
            "species": "Мониторинг безопасности",
            "startyear": 2025,
            "id": 2561
        },
        {
            "abbrprofile": "ЮРГб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 6267
        },
        {
            "abbrprofile": "ЮРГб",
            "species": "Аэробика",
            "startyear": 2025,
            "id": 6273
        },
        {
            "abbrprofile": "КНб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7400
        },
        {
            "abbrprofile": "ТХб",
            "species": "Ювелирное искусство",
            "startyear": 2025,
            "id": 9575
        },
        {
            "abbrprofile": "ТХб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 9296
        },
        {
            "abbrprofile": "ТХб",
            "species": "Правовое обеспечение профессиональной деятельности в ювелирной отрасли",
            "startyear": 2025,
            "id": 3948
        },
        {
            "abbrprofile": "МДБб",
            "species": "Иностранный язык / First foreign language",
            "startyear": 2025,
            "id": 11697
        },
        {
            "abbrprofile": "МДБб",
            "species": "Атлетическая гимнастика / Powerlifting",
            "startyear": 2025,
            "id": 9306
        },
        {
            "abbrprofile": "МДБб",
            "species": "Спецкурс по английскому произношению / English pronunciation special course",
            "startyear": 2025,
            "id": 11698
        },
        {
            "abbrprofile": "СМ",
            "species": "Введение в профессиональную деятельность",
            "startyear": 2025,
            "id": 8853
        },
        {
            "abbrprofile": "СМ",
            "species": "Технология заготовительно-штамповочных работ",
            "startyear": 2025,
            "id": 8882
        },
        {
            "abbrprofile": "СМ",
            "species": "Образовательный форсайт",
            "startyear": 2025,
            "id": 8866
        },
        {
            "abbrprofile": "СМ",
            "species": "Безопасность жизнедеятельности",
            "startyear": 2025,
            "id": 3483
        },
        {
            "abbrprofile": "СМ",
            "species": "Физика",
            "startyear": 2025,
            "id": 6468
        },
        {
            "abbrprofile": "ИТГб",
            "species": "Практикум по культуре профессиональной коммуникации (второй иностранный язык) / Practical course for professional communication (Second foreign language)",
            "startyear": 2025,
            "id": 11848
        },
        {
            "abbrprofile": "ИТГб",
            "species": "Атлетическая гимнастика / Powerlifting",
            "startyear": 2025,
            "id": 6504
        },
        {
            "abbrprofile": "ИТГб",
            "species": "Адаптивная физическая культура / Adapted Physical Education",
            "startyear": 2025,
            "id": 6503
        },
        {
            "abbrprofile": "ИТГб",
            "species": "Военно-прикладная физическая подготовка / Military-applied Physical Training",
            "startyear": 2025,
            "id": 6507
        },
        {
            "abbrprofile": "аАУП",
            "species": "Инженерный анализ работы типовых конструктивных элементов машин",
            "startyear": 2025,
            "id": 12733
        },
        {
            "abbrprofile": "аТМД",
            "species": "Инженерный анализ работы типовых конструктивных элементов машин",
            "startyear": 2025,
            "id": 12489
        },
        {
            "abbrprofile": "аМН",
            "species": "Инженерный анализ работы типовых конструктивных элементов машин",
            "startyear": 2025,
            "id": 12714
        },
        {
            "abbrprofile": "аБЗТ",
            "species": "Специфика научного исследования в технических науках",
            "startyear": 2025,
            "id": 6651
        },
        {
            "abbrprofile": "аГКЛ",
            "species": "Инженерный анализ работы типовых конструктивных элементов машин",
            "startyear": 2025,
            "id": 12750
        },
        {
            "abbrprofile": "СТЭб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 6021
        },
        {
            "abbrprofile": "ЭАПЭб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 7133
        },
        {
            "abbrprofile": "ЭАПЭб",
            "species": "Автономное электроснабжение потребителей",
            "startyear": 2025,
            "id": 7129
        },
        {
            "abbrprofile": "ЦЭм",
            "species": "Специальные вопросы надежности систем электроснабжения",
            "startyear": 2025,
            "id": 6133
        },
        {
            "abbrprofile": "ПИМ",
            "species": "Проектирование предприятий пищевой отрасли",
            "startyear": 2025,
            "id": 8573
        },
        {
            "abbrprofile": "СТЭбз",
            "species": "Правоведение",
            "startyear": 2025,
            "id": 3731
        },
        {
            "abbrprofile": "ТПбз",
            "species": "Аналитическая химия",
            "startyear": 2025,
            "id": 4033
        },
        {
            "abbrprofile": "ТПбз",
            "species": "Производственная практика: преддипломная практика, в том числе научно-исследовательская работа",
            "startyear": 2025,
            "id": 9798
        },
        {
            "abbrprofile": "КТЭм",
            "species": "Современные проблемы электроэнергетики и электротехники",
            "startyear": 2025,
            "id": 8148
        },
        {
            "abbrprofile": "КБКб",
            "species": "Мнемотехника / Mnemonics",
            "startyear": 2025,
            "id": 11238
        },
        {
            "abbrprofile": "КБКб",
            "species": "Учебная практика: педагогическая практика / Company Internership 1 (Pedagogical Internship)",
            "startyear": 2025,
            "id": 11278
        },
        {
            "abbrprofile": "КБКб",
            "species": "Письменный перевод специальных текстов / Written Translation of Special Texts",
            "startyear": 2025,
            "id": 11251
        },
        {
            "abbrprofile": "КБКб",
            "species": "Физическая культура и спорт / Physical Education and Sport",
            "startyear": 2025,
            "id": 9559
        },
        {
            "abbrprofile": "КБКб",
            "species": "Стилистика / Stylistics",
            "startyear": 2025,
            "id": 11268
        },
        {
            "abbrprofile": "КБКб",
            "species": "Современные методы в гуманитарных науках / Contemporary Methods in the Humanities",
            "startyear": 2025,
            "id": 11265
        },
        {
            "abbrprofile": "КБКб",
            "species": "Практикум по культуре профессиональной коммуникации (второй иностранный язык) / Practical course for professional communication (Second foreign language)",
            "startyear": 2025,
            "id": 11849
        },
        {
            "abbrprofile": "КБКб",
            "species": "Анализ художественного текста / Literary Text Analysis",
            "startyear": 2025,
            "id": 11214
        },
        {
            "abbrprofile": "КБКб",
            "species": "Экономический перевод / Economic Interpreting and Translation",
            "startyear": 2025,
            "id": 11281
        },
        {
            "abbrprofile": "КБКб",
            "species": "Бизнес-коммуникации / Commucation in Business",
            "startyear": 2025,
            "id": 11218
        },
        {
            "abbrprofile": "КБКб",
            "species": "Сопровождение международных проектов / International Projects Management",
            "startyear": 2025,
            "id": 11266
        },
        {
            "abbrprofile": "КБКб",
            "species": "Основы деловой коммуникации / Basics of Business Communication",
            "startyear": 2025,
            "id": 11242
        },
        {
            "abbrprofile": "КБКб",
            "species": "Проектная деятельность / Project Development Practicum",
            "startyear": 2025,
            "id": 11254
        },
        {
            "abbrprofile": "КБКб",
            "species": "Психология в бизнесе / Psychology in Business",
            "startyear": 2025,
            "id": 11262
        },
        {
            "abbrprofile": "КБКб",
            "species": "Лексикология / Lexicology",
            "startyear": 2025,
            "id": 11228
        },
        {
            "abbrprofile": "КБКб",
            "species": "Педагогика / Pedagogy",
            "startyear": 2025,
            "id": 11249
        },
        {
            "abbrprofile": "КБКб",
            "species": "Этика делового общения / Ethics in Business Communication",
            "startyear": 2025,
            "id": 11283
        },
        {
            "abbrprofile": "КБКб",
            "species": "Иностранный язык / First foreign language",
            "startyear": 2025,
            "id": 11844
        },
        {
            "abbrprofile": "КБКб",
            "species": "Теоретическая грамматика / Theoretical Grammar",
            "startyear": 2025,
            "id": 11269
        },
        {
            "abbrprofile": "КБКб",
            "species": "Академическое письмо / Academic Writing",
            "startyear": 2025,
            "id": 11832
        },
        {
            "abbrprofile": "КБКб",
            "species": "Межкультурная коммуникация / Cross-Cultural Communication",
            "startyear": 2025,
            "id": 11233
        },
        {
            "abbrprofile": "КБКб",
            "species": "Кросс-культурная коммуникация в парадигме делового общения / Cross-cultural Communication in Business Communication Paradigm",
            "startyear": 2025,
            "id": 11227
        },
        {
            "abbrprofile": "КБКб",
            "species": "Методика преподавания китайского языка как иностранного: практическая грамматика / Methods of Teaching Chinese asa Foreign Language: Practical Grammar",
            "startyear": 2025,
            "id": 11236
        },
        {
            "abbrprofile": "ТВб",
            "species": "Автоматизация и управление процессами",
            "startyear": 2025,
            "id": 5727
        },
        {
            "abbrprofile": "ТВб",
            "species": "Введение в профессиональную деятельность",
            "startyear": 2025,
            "id": 5729
        },
        {
            "abbrprofile": "ТВб",
            "species": "Основы автоматизированного проектирования",
            "startyear": 2025,
            "id": 5755
        },
        {
            "abbrprofile": "ТВб",
            "species": "Оптимизация систем жизнеобеспечения",
            "startyear": 2025,
            "id": 6157
        },
        {
            "abbrprofile": "ТВб",
            "species": "Безопасность жизнедеятельности",
            "startyear": 2025,
            "id": 11105
        },
        {
            "abbrprofile": "ТВб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 5443
        },
        {
            "abbrprofile": "ТВб",
            "species": "Насосы, вентиляторы и компрессоры в системах теплогазоснабжения и вентиляции",
            "startyear": 2025,
            "id": 6156
        },
        {
            "abbrprofile": "РГ",
            "species": "Разведочная геофизика",
            "startyear": 2025,
            "id": 7774
        },
        {
            "abbrprofile": "РГ",
            "species": "Геотектоника и основы региональной геологии",
            "startyear": 2025,
            "id": 8179
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Этика делового общения / Ethics in Business Communication",
            "startyear": 2025,
            "id": 11284
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Методы лингвистического анализа / Research Methods in Linguistics",
            "startyear": 2025,
            "id": 11237
        },
        {
            "abbrprofile": "ЖКб",
            "species": "Аэробика / Aerobics",
            "startyear": 2025,
            "id": 9325
        },
        {
            "abbrprofile": "ЖКб",
            "species": "Спецкурс по английскому произношению / English pronunciation special course",
            "startyear": 2025,
            "id": 11760
        },
        {
            "abbrprofile": "ЖКб",
            "species": "Реклама в медиабизнесе / Advertising in the mediabusiness",
            "startyear": 2025,
            "id": 11615
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Практикум по корпоративному общению / Corporate Communication Workshop",
            "startyear": 2025,
            "id": 11252
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Анализ художественного текста / Literary Text Analysis",
            "startyear": 2025,
            "id": 11215
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Практикум по культуре профессиональной коммуникации (второй иностранный язык) / Practical course for professional communication (Second foreign language)",
            "startyear": 2025,
            "id": 11850
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Научные исследования в лингвистике  / Linguistic Research",
            "startyear": 2025,
            "id": 11239
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Экономический перевод / Economic Interpreting and Translation",
            "startyear": 2025,
            "id": 11282
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Юридический перевод / Legal Interpreting and Translation",
            "startyear": 2025,
            "id": 11286
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Производственная практика: научно-исследовательская работа / Undergraduate Practice 1",
            "startyear": 2025,
            "id": 11257
        },
        {
            "abbrprofile": "ЖКб",
            "species": "Второй иностранный язык (продвинутый курс) / Second Foreign Language (advanced level)",
            "startyear": 2025,
            "id": 11836
        },
        {
            "abbrprofile": "ЖКб",
            "species": "Иностранный язык / First foreign language",
            "startyear": 2025,
            "id": 11753
        },
        {
            "abbrprofile": "ГИС",
            "species": "Дистанционное зондирование Земли",
            "startyear": 2025,
            "id": 7742
        },
        {
            "abbrprofile": "РМ",
            "species": "Учебная практика:  геологическая  практика",
            "startyear": 2025,
            "id": 11288
        },
        {
            "abbrprofile": "РМ",
            "species": "Адаптивная физическая культура",
            "startyear": 2025,
            "id": 9282
        },
        {
            "abbrprofile": "РМ",
            "species": "Геологическое картирование",
            "startyear": 2025,
            "id": 8178
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Сопровождение международных проектов / International Projects Management",
            "startyear": 2025,
            "id": 11267
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Основы деловой коммуникации / Basics of Business Communication",
            "startyear": 2025,
            "id": 11243
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Производственная практика: переводческая практика / Company Internership 2",
            "startyear": 2025,
            "id": 11259
        },
        {
            "abbrprofile": "ЛБКб",
            "species": "Проектная деятельность / Project Development Practicum",
            "startyear": 2025,
            "id": 11255
        },
        {
            "abbrprofile": "РТ",
            "species": "Основы стратиграфии и структурная геология",
            "startyear": 2025,
            "id": 8184
        },
        {
            "abbrprofile": "ГИС",
            "species": "Геоинформационные системы в геонауках",
            "startyear": 2025,
            "id": 7730
        },
        {
            "abbrprofile": "ГИС",
            "species": "Аэробика",
            "startyear": 2025,
            "id": 8681
        },
        {
            "abbrprofile": "ГИС",
            "species": "Адаптивная физическая культура",
            "startyear": 2025,
            "id": 8677
        },
        {
            "abbrprofile": "ГИС",
            "species": "Военно-прикладная физическая подготовка",
            "startyear": 2025,
            "id": 8685
        },
        {
            "abbrprofile": "РКИб",
            "species": "Межкультурная коммуникация",
            "startyear": 2025,
            "id": 11754
        },
        {
            "abbrprofile": "РКИб",
            "species": "Теория перевода первого иностранного языка",
            "startyear": 2025,
            "id": 11821
        },
        {
            "abbrprofile": "НМб",
            "species": "Атлетическая гимнастика",
            "startyear": 2025,
            "id": 9301
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Научные парадигмы лингвистики и перевода",
            "startyear": 2025,
            "id": 11293
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Междисциплинарные исследования в лингвистике",
            "startyear": 2025,
            "id": 11291
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Информационные технологии в лингвистике и переводе",
            "startyear": 2025,
            "id": 12699
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Теория текста",
            "startyear": 2025,
            "id": 12708
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Методы лингвистического анализа",
            "startyear": 2025,
            "id": 12701
        },
        {
            "abbrprofile": "СПРКм",
            "species": "История лингвистических учений и перевода",
            "startyear": 2025,
            "id": 12700
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Практикум по культуре научной и профессиональной коммуникации",
            "startyear": 2025,
            "id": 12704
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Теория и практика письменного специализированного перевода",
            "startyear": 2025,
            "id": 12706
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Терминоведение",
            "startyear": 2025,
            "id": 12709
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Научная коммуникация",
            "startyear": 2025,
            "id": 12702
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Производственная практика: преддипломная практика",
            "startyear": 2025,
            "id": 11300
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Корпусная лингвистика и перевод",
            "startyear": 2025,
            "id": 11290
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Второй иностранный язык",
            "startyear": 2025,
            "id": 11833
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Учебная практика: переводческая практика",
            "startyear": 2025,
            "id": 11304
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Проектное мышление",
            "startyear": 2025,
            "id": 11298
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Теория и практика межкультурной коммуникации",
            "startyear": 2025,
            "id": 11302
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Практикум по переводу: коммерческий перевод",
            "startyear": 2025,
            "id": 11296
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Перевод в сфере туризма",
            "startyear": 2025,
            "id": 11295
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Перевод в сфере международных отношений",
            "startyear": 2025,
            "id": 11294
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Производственная практика: научно-исследовательская работа",
            "startyear": 2025,
            "id": 12705
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Академическое письмо",
            "startyear": 2025,
            "id": 11289
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Практикум по переводу: технический перевод",
            "startyear": 2025,
            "id": 11297
        },
        {
            "abbrprofile": "СПРКм",
            "species": "Производственная практика: научно-исследовательская работа (научно-исследовательский семинар)",
            "startyear": 2025,
            "id": 11299
        },
        {
            "abbrprofile": "ЭСТм",
            "species": "Производственная практика:  научно-исследовательская работа (научно-исследовательский семинар)",
            "startyear": 2025,
            "id": 12373
        },
        {
            "abbrprofile": "ЭСТм",
            "species": "Производственная практика:  научно-исследовательская работа (научно-исследовательский семинар)",
            "startyear": 2025,
            "id": 12052
        },
        {
            "abbrprofile": "НДм",
            "species": "Производственная практика: научно-исследовательская работа (научно-исследовательский семинар)",
            "startyear": 2025,
            "id": 10848
        },
        {
            "abbrprofile": "гГП",
            "species": "Информатика",
            "startyear": 2025,
            "id": 11854
        }
    ],
    "plx_file": "https://app.istu.edu/oop/uploads/rpd_plan/2025-04-07/09.03.02_%D0%98%D0%A1%D0%A2%D0%B1-25.plx",
    "planlines": {
        "id": 10418,
        "plan_id": 220,
        "disid_id": 2050,
        "dis": "Объектно-ориентированное программирование",
        "newdisid": "Б1.В.02.04",
        "mustbesdudied": 288,
        "hoursinzet": 36,
        "caf": 121,
        "nocalccontrol": False,
        "type": 2,
        "viewpract": None,
        "viewobject": 1,
        "kompetences": "ПКС-2.1,ПКС-2.2",
        "synchronize": True,
        "semesters": [
            {
                "id": 18136,
                "planlineid_id": 10418,
                "num": 3,
                "lekc": 16,
                "lab": 48,
                "pr": None,
                "srs": 80,
                "ekzhour": None,
                "zet": 4.0,
                "ekz": None,
                "zach": True,
                "kp_hour": None,
                "kp": None,
                "kr_hour": None,
                "kr": None,
                "zacho": None,
                "eios": None
            },
            {
                "id": 18137,
                "planlineid_id": 10418,
                "num": 4,
                "lekc": 16,
                "lab": 32,
                "pr": None,
                "srs": 60,
                "ekzhour": 36,
                "zet": 4.0,
                "ekz": True,
                "zach": None,
                "kp_hour": 1,
                "kp": True,
                "kr_hour": None,
                "kr": None,
                "zacho": None,
                "eios": None
            }
        ],
        "indicators": [
            {
                "id": 28164,
                "planlineid_id": 10418,
                "competence_index": "ПКС-2",
                "competence": "Способен разрабатывать программное обеспечение (ПО), включая проектирование, отладку, проверку работоспособности и модификацию ПО",
                "indicator_index": "ПКС-2.1",
                "indicator": "Способен выполнять объектную декомпозицию задачи и реализовывать классы с использованием объектно-ориентированного языка программирования",
                "discipline_indicator": [
                    {
                        "id": 1186,
                        "indicator_id": 28164,
                        "planlineid_id": 10418,
                        "know": "основные понятия и принципы объектного подхода;  синтаксис и основные конструкции изучаемого языка программирования",
                        "able": "выполнять объектную декомпозицию задачи; реализовывать выделенные в ходе анализа задачи классы с использованием объектно-ориентированного языка программирования",
                        "own": "современным объектно-ориентированным языком программирования; современной интегрированной средой разработки",
                        "criteria": "Уверенно демонстрирует полученные знания, приводит примеры, отвечает на вопросы. Способен с использованием современного объектно-ориентированного языка программирования реализовывать классы на основе результатов объектного анализа задачи",
                        "methods": "Устное собеседование по теоретическим вопросам и выполнение практического задания"
                    }
                ]
            },
            {
                "id": 28165,
                "planlineid_id": 10418,
                "competence_index": "ПКС-2",
                "competence": "Способен разрабатывать программное обеспечение (ПО), включая проектирование, отладку, проверку работоспособности и модификацию ПО",
                "indicator_index": "ПКС-2.2",
                "indicator": "Способен использовать объектно-ориентированный подход в процессе создания программного обеспечения",
                "discipline_indicator": [
                    {
                        "id": 1185,
                        "indicator_id": 28165,
                        "planlineid_id": 10418,
                        "know": "методы и технологии объектно-ориентированного программирования;\r\nосновные шаблоны проектирования",
                        "able": "применять объектно-ориентированную методологию программирования;\r\nиспользовать современные программные библиотеки и фреймворки",
                        "own": "методологией объектно-ориентированного подхода к разработке программного обеспечения;\r\nстандартными средствами проектирования, отладки и тестирования программного обеспечения",
                        "criteria": "Уверенно демонстрирует полученные знания, приводит примеры, отвечает на вопросы. Способен с использованием современного объектно-ориентированного языка программирования реализовывать фрагмент программного обеспечения на основе результатов объектного анализа предметной области",
                        "methods": "Устное собеседование по теоретическим вопросам и выполнение практического задания"
                    }
                ]
            }
        ],
        "plan": {
            "id": 220,
            "file_id": 146,
            "subtype": "Рабочий учебный план",
            "shifr": "SKYF",
            "abbrprofile": "ИСТб",
            "studyform": "Очная",
            "studylevel": "ВПО-Бакалавры",
            "studyprog": "подготовка бакалавров",
            "elementsinweek": 6,
            "species": "09.03.02 Информационные системы и технологии",
            "usernum": 1006070,
            "whoratif": "План одобрен Ученым советом вуза",
            "planname": "09.03.02 (ИСТб-25).plx",
            "kafcode": 121,
            "startyear": 2025,
            "dviga": True,
            "gviga": True,
            "igazetweek": 36.0,
            "igahourzet": 1.5,
            "semesteroncource": 2,
            "gosdate": None,
            "lastshifr": "09.03.02",
            "napr_e": "Информационные системы и технологии",
            "napr_t": "09.03.02 Информационные системы и технологии",
            "vuzname": "федеральное государственное бюджетное образовательное учреждение высшего образования «Иркутский национальный исследовательский технический университет»",
            "head": "",
            "faculty": "Информационных технологий и анализа данных",
            "mira_id": 10179
        }
    },
    "id": 4107,
    "cadmission": 25064,
    "mira_id": 309438,
    "person": 14881,
    "status": 3,
    "status_verbose": "Утвержден",
    "protocol_number": "8",
    "protocol_date": "2025-02-24",
    "user_accepted_id": 104,
    "user_confirmed_id": 102,
    "user_type": None,
    "meeting": "заседании Совета института ИТиАД им. Е.И.Попова",
    "can_be_copied_by_anyone": False,
    "review_date": "2025-06-11",
    "accept_date": "2025-06-16",
    "confirm_date": "2025-06-11",
    "discipline_themes": [
        {
            "id": 2978,
            "planlineslink_id": 4107,
            "name": "Основы объектно-ориентированного подхода и базовые средства выражения объектной абстракции",
            "semester": 3,
            "formcontrol_id": 19,
            "formcontrol_list": [
                19
            ],
            "formcontrol_verbose": "Отчет по лабораторной работе",
            "comment": "Понятия объекта и класса. Краткая информация о платформе Java. Основные языковые конструкции Java: объявление классов, примитивные типы данных, объявление переменных и методов, операторы управления порядком выполнения. Ссылочные типы данных и создание объектов. Инкапсуляция. Модификаторы доступа. Конструкторы. Контекст выполнения this. Массивы и строки. Пакеты Java. Статические поля и методы.",
            "num": 2
        },
        {
            "id": 2977,
            "planlineslink_id": 4107,
            "name": "Введение в объектно-ориентированное программирование",
            "semester": 3,
            "formcontrol_id": 19,
            "formcontrol_list": [
                19
            ],
            "formcontrol_verbose": "Отчет по лабораторной работе",
            "comment": "Сложность разработки программного обеспечения. Способы борьбы со сложностью - абстракция, декомпозиция, обобщение. Эволюция средств выражения абстракции в языках программирования. Роль проектирования в процессе разработки программного обеспечения. Основы синтаксиса современного объектно-ориентированного языка программирования.",
            "num": 1
        },
        {
            "id": 2979,
            "planlineslink_id": 4107,
            "name": "Объектно-ориентированный подход к обработке ошибок и тестированию",
            "semester": 3,
            "formcontrol_id": 19,
            "formcontrol_list": [
                19
            ],
            "formcontrol_verbose": "Отчет по лабораторной работе",
            "comment": "Проблема реализации системы ввода-вывода и объектный подход к её решению. Понятие потока данных в Java, иерархия классов потоков данных. Низкоуровневые и высокоуровневые потоки данных. Наследование. Исключительная ситуация как объект. Механизм обработки исключений, Делегирование обработки исключений. Механизм генерации (возбуждения) исключений. Модульные тесты.",
            "num": 3
        },
        {
            "id": 2980,
            "planlineslink_id": 4107,
            "name": "Основные принципы объектно-ориентированного подхода",
            "semester": 3,
            "formcontrol_id": 19,
            "formcontrol_list": [
                19
            ],
            "formcontrol_verbose": "Отчет по лабораторной работе",
            "comment": "Инкапсуляция, полиморфизм, наследование и их взаимосвязь. Применение абстрактных классов. Проблема множественного наследования, интерфейсы, переопределение методов. Обобщения (генерики). Механизмы рефлексии (интроспекция).",
            "num": 4
        },
        {
            "id": 2981,
            "planlineslink_id": 4107,
            "name": "Применение объектно-ориентированного подхода при разработке приложений с графическим пользовательским интерфейсом",
            "semester": 4,
            "formcontrol_id": 19,
            "formcontrol_list": [
                19
            ],
            "formcontrol_verbose": "Отчет по лабораторной работе",
            "comment": "Понятие графического пользовательского интерфейса и подходы к его реализации при разработке приложений. Концепция Модель/Вид/Контроллер (MVC). Интерфейсы программирования приложений (API) и понятие компонента графического интерфейса. Базовые библиотеки и инструменты создания GUI Java (AWT, Swing, JavaFX). Иерархия компонентов и контейнеров и работа с ними. Событийно-управляемый механизм взаимодействия объектов. Шаблон программирования Listener. Реализация обработчиков событий объектов прослушивания.",
            "num": 1
        },
        {
            "id": 2982,
            "planlineslink_id": 4107,
            "name": "Объектный подход к организации работы с базами данных",
            "semester": 4,
            "formcontrol_id": 19,
            "formcontrol_list": [
                19
            ],
            "formcontrol_verbose": "Отчет по лабораторной работе",
            "comment": "Создание подключения к базе данных и технология JDBC. Понятие JDBC-драйвера. Встраиваемая СУБД SQLite. Объектно-реляционное отображение (ORM). Классы-сущности и фабрики сессий.",
            "num": 2
        },
        {
            "id": 2983,
            "planlineslink_id": 4107,
            "name": "Применение объектно-ориентированного подхода при разработке Android-приложений",
            "semester": 4,
            "formcontrol_id": 19,
            "formcontrol_list": [
                19
            ],
            "formcontrol_verbose": "Отчет по лабораторной работе",
            "comment": "Инструментальные средства разработки и структура Android-проекта. ViewGroup и основные контейнеры. Инструмент отладки Logcat. Реализация динамического интерфейса. Адаптеры списков.",
            "num": 3
        }
    ],
    "discipline_work_hour": [
        {
            "id": 9167,
            "planlineslink_id": 4107,
            "theme_id": 2977,
            "type": 0,
            "name": "Введение в объектно-ориентированное программирование",
            "hours": 4.0,
            "semester": 3,
            "num": 4
        },
        {
            "id": 9168,
            "planlineslink_id": 4107,
            "theme_id": 2977,
            "type": 2,
            "name": "Подготовка к практическим занятиям (лабораторным работам)",
            "hours": 4.0,
            "semester": 3,
            "num": 1
        },
        {
            "id": 9170,
            "planlineslink_id": 4107,
            "theme_id": 2977,
            "type": 2,
            "name": "Подготовка к сдаче и защите отчетов",
            "hours": 2.0,
            "semester": 3,
            "num": 3
        },
        {
            "id": 9171,
            "planlineslink_id": 4107,
            "theme_id": 2977,
            "type": 2,
            "name": "Проработка разделов теоретического материала",
            "hours": 6.0,
            "semester": 3,
            "num": 13
        },
        {
            "id": 9172,
            "planlineslink_id": 4107,
            "theme_id": 2977,
            "type": 2,
            "name": "Подготовка к зачёту",
            "hours": 16.0,
            "semester": 3,
            "num": 17
        },
        {
            "id": 9175,
            "planlineslink_id": 4107,
            "theme_id": 2978,
            "type": 2,
            "name": "Оформление отчетов по лабораторным и практическим работам",
            "hours": 2.0,
            "semester": 3,
            "num": 6
        },
        {
            "id": 9176,
            "planlineslink_id": 4107,
            "theme_id": 2978,
            "type": 2,
            "name": "Подготовка к практическим занятиям (лабораторным работам)",
            "hours": 4.0,
            "semester": 3,
            "num": 7
        },
        {
            "id": 9178,
            "planlineslink_id": 4107,
            "theme_id": 2978,
            "type": 2,
            "name": "Проработка разделов теоретического материала",
            "hours": 8.0,
            "semester": 3,
            "num": 14
        },
        {
            "id": 9179,
            "planlineslink_id": 4107,
            "theme_id": 2978,
            "type": 3,
            "name": "Разработка классов и их использование",
            "hours": 10.0,
            "semester": 3,
            "num": 2
        },
        {
            "id": 9181,
            "planlineslink_id": 4107,
            "theme_id": 2979,
            "type": 2,
            "name": "Подготовка к практическим занятиям (лабораторным работам)",
            "hours": 4.0,
            "semester": 3,
            "num": 5
        },
        {
            "id": 9182,
            "planlineslink_id": 4107,
            "theme_id": 2979,
            "type": 2,
            "name": "Оформление отчетов по лабораторным и практическим работам",
            "hours": 2.0,
            "semester": 3,
            "num": 8
        },
        {
            "id": 9183,
            "planlineslink_id": 4107,
            "theme_id": 2979,
            "type": 2,
            "name": "Подготовка к сдаче и защите отчетов",
            "hours": 2.0,
            "semester": 3,
            "num": 9
        },
        {
            "id": 9184,
            "planlineslink_id": 4107,
            "theme_id": 2979,
            "type": 2,
            "name": "Проработка разделов теоретического материала",
            "hours": 8.0,
            "semester": 3,
            "num": 15
        },
        {
            "id": 9185,
            "planlineslink_id": 4107,
            "theme_id": 2979,
            "type": 3,
            "name": "Разработка приложения работающего с потоками данных",
            "hours": 16.0,
            "semester": 3,
            "num": 3
        },
        {
            "id": 9187,
            "planlineslink_id": 4107,
            "theme_id": 2980,
            "type": 2,
            "name": "Подготовка к практическим занятиям (лабораторным работам)",
            "hours": 4.0,
            "semester": 3,
            "num": 10
        },
        {
            "id": 9188,
            "planlineslink_id": 4107,
            "theme_id": 2980,
            "type": 2,
            "name": "Оформление отчетов по лабораторным и практическим работам",
            "hours": 2.0,
            "semester": 3,
            "num": 11
        },
        {
            "id": 9189,
            "planlineslink_id": 4107,
            "theme_id": 2980,
            "type": 2,
            "name": "Подготовка к сдаче и защите отчетов",
            "hours": 2.0,
            "semester": 3,
            "num": 12
        },
        {
            "id": 9190,
            "planlineslink_id": 4107,
            "theme_id": 2980,
            "type": 2,
            "name": "Проработка разделов теоретического материала",
            "hours": 10.0,
            "semester": 3,
            "num": 16
        },
        {
            "id": 9192,
            "planlineslink_id": 4107,
            "theme_id": 2981,
            "type": 0,
            "name": "Применение объектно-ориентированного подхода при разработке приложений с графическим пользовательским интерфейсом",
            "hours": 8.0,
            "semester": 4,
            "num": 1
        },
        {
            "id": 9193,
            "planlineslink_id": 4107,
            "theme_id": 2981,
            "type": 2,
            "name": "Написание курсового проекта (работы)",
            "hours": 30.0,
            "semester": 4,
            "num": 1
        },
        {
            "id": 9194,
            "planlineslink_id": 4107,
            "theme_id": 2981,
            "type": 2,
            "name": "Подготовка к практическим занятиям (лабораторным работам)",
            "hours": 2.0,
            "semester": 4,
            "num": 5
        },
        {
            "id": 9195,
            "planlineslink_id": 4107,
            "theme_id": 2981,
            "type": 2,
            "name": "Подготовка к сдаче и защите отчетов",
            "hours": 2.0,
            "semester": 4,
            "num": 4
        },
        {
            "id": 9196,
            "planlineslink_id": 4107,
            "theme_id": 2981,
            "type": 2,
            "name": "Оформление отчетов по лабораторным и практическим работам",
            "hours": 2.0,
            "semester": 4,
            "num": 6
        },
        {
            "id": 9197,
            "planlineslink_id": 4107,
            "theme_id": 2981,
            "type": 2,
            "name": "Проработка разделов теоретического материала",
            "hours": 4.0,
            "semester": 4,
            "num": 11
        },
        {
            "id": 9198,
            "planlineslink_id": 4107,
            "theme_id": 2981,
            "type": 3,
            "name": "Разработка приложения с графическим пользовательским интерфейсом",
            "hours": 12.0,
            "semester": 4,
            "num": 1
        },
        {
            "id": 9200,
            "planlineslink_id": 4107,
            "theme_id": 2982,
            "type": 2,
            "name": "Подготовка к практическим занятиям (лабораторным работам)",
            "hours": 2.0,
            "semester": 4,
            "num": 7
        },
        {
            "id": 9201,
            "planlineslink_id": 4107,
            "theme_id": 2982,
            "type": 2,
            "name": "Подготовка к сдаче и защите отчетов",
            "hours": 2.0,
            "semester": 4,
            "num": 8
        },
        {
            "id": 9202,
            "planlineslink_id": 4107,
            "theme_id": 2982,
            "type": 2,
            "name": "Оформление отчетов по лабораторным и практическим работам",
            "hours": 2.0,
            "semester": 4,
            "num": 3
        },
        {
            "id": 9203,
            "planlineslink_id": 4107,
            "theme_id": 2982,
            "type": 2,
            "name": "Проработка разделов теоретического материала",
            "hours": 4.0,
            "semester": 4,
            "num": 12
        },
        {
            "id": 9204,
            "planlineslink_id": 4107,
            "theme_id": 2982,
            "type": 3,
            "name": "Организация работы с базой данных",
            "hours": 8.0,
            "semester": 4,
            "num": 2
        },
        {
            "id": 9205,
            "planlineslink_id": 4107,
            "theme_id": 2983,
            "type": 0,
            "name": "Применение объектно-ориентированного подхода при разработке Android-приложений",
            "hours": 4.0,
            "semester": 4,
            "num": 2
        },
        {
            "id": 9206,
            "planlineslink_id": 4107,
            "theme_id": 2983,
            "type": 2,
            "name": "Оформление отчетов по лабораторным и практическим работам",
            "hours": 2.0,
            "semester": 4,
            "num": 2
        },
        {
            "id": 9207,
            "planlineslink_id": 4107,
            "theme_id": 2983,
            "type": 2,
            "name": "Подготовка к практическим занятиям (лабораторным работам)",
            "hours": 2.0,
            "semester": 4,
            "num": 9
        },
        {
            "id": 9208,
            "planlineslink_id": 4107,
            "theme_id": 2983,
            "type": 2,
            "name": "Подготовка к сдаче и защите отчетов",
            "hours": 2.0,
            "semester": 4,
            "num": 10
        },
        {
            "id": 9209,
            "planlineslink_id": 4107,
            "theme_id": 2983,
            "type": 2,
            "name": "Проработка разделов теоретического материала",
            "hours": 4.0,
            "semester": 4,
            "num": 13
        },
        {
            "id": 9210,
            "planlineslink_id": 4107,
            "theme_id": 2983,
            "type": 3,
            "name": "Разработка Android-приложения",
            "hours": 12.0,
            "semester": 4,
            "num": 3
        },
        {
            "id": 9173,
            "planlineslink_id": 4107,
            "theme_id": 2977,
            "type": 3,
            "name": "Разработка консольного приложения",
            "hours": 8.0,
            "semester": 3,
            "num": 1
        },
        {
            "id": 9191,
            "planlineslink_id": 4107,
            "theme_id": 2980,
            "type": 3,
            "name": "Разработка библиотеки классов с использованием механизмов наследования, полиморфизма и инкапсуляции",
            "hours": 14.0,
            "semester": 3,
            "num": 4
        },
        {
            "id": 9169,
            "planlineslink_id": 4107,
            "theme_id": 2977,
            "type": 2,
            "name": "Оформление отчетов по лабораторным и практическим работам",
            "hours": 2.0,
            "semester": 3,
            "num": 2
        },
        {
            "id": 9186,
            "planlineslink_id": 4107,
            "theme_id": 2980,
            "type": 0,
            "name": "Основные принципы объектно-ориентированного подхода",
            "hours": 4.0,
            "semester": 3,
            "num": 3
        },
        {
            "id": 9180,
            "planlineslink_id": 4107,
            "theme_id": 2979,
            "type": 0,
            "name": "Объектно-ориентированный подход к обработке ошибок и тестированию",
            "hours": 4.0,
            "semester": 3,
            "num": 2
        },
        {
            "id": 9174,
            "planlineslink_id": 4107,
            "theme_id": 2978,
            "type": 0,
            "name": "Основы объектно-ориентированного подхода и базовые средства выражения объектной абстракции",
            "hours": 4.0,
            "semester": 3,
            "num": 1
        },
        {
            "id": 9177,
            "planlineslink_id": 4107,
            "theme_id": 2978,
            "type": 2,
            "name": "Подготовка к сдаче и защите отчетов",
            "hours": 2.0,
            "semester": 3,
            "num": 1
        },
        {
            "id": 9199,
            "planlineslink_id": 4107,
            "theme_id": 2982,
            "type": 0,
            "name": "Объектный подход к организации работы с базами данных",
            "hours": 4.0,
            "semester": 4,
            "num": 3
        }
    ],
    "additional_info": [
        {
            "id": 17805,
            "planlineslink_id": 4107,
            "type": "disciplinePlace",
            "value": {
                "precedence": [
                    2073,
                    2064,
                    209,
                    2072,
                    2108,
                    1005,
                    2107
                ],
                "subsequent": [
                    2123,
                    2059,
                    212
                ]
            }
        },
        {
            "id": 17806,
            "planlineslink_id": 4107,
            "type": "interactiveMethods",
            "value": {
                "interactiveMethods": "Видеолекция, Лекция-провокация, Метод проектов"
            }
        },
        {
            "id": 1980,
            "planlineslink_id": 4107,
            "type": "resources",
            "value": {
                "bd": "Не используются\n",
                "web": "1. http://library.istu.edu/\n2. https://e.lanbook.com/\n"
            }
        },
        {
            "id": 57481,
            "planlineslink_id": 4107,
            "type": "software",
            "value": [
                {
                    "id": -1,
                    "clicense__name": "Свободно распространяемое программное обеспечение Java Development Kit (версия JDK8 или выше)",
                    "clicense__type": "Свободное"
                },
                {
                    "id": -1,
                    "clicense__name": "Свободно распространяемое программное обеспечение JetBrains AndroidStudio (последняя версия)",
                    "clicense__type": "Свободное"
                },
                {
                    "id": -1,
                    "clicense__name": "Свободно распространяемое программное обеспечение JetBrains IntelliJ IDEA Community Edition (последняя версия)",
                    "clicense__type": "Свободное"
                }
            ]
        },
        {
            "id": 57483,
            "planlineslink_id": 4107,
            "type": "logistics",
            "value": [
                {
                    "id": 25864,
                    "name": "Проектор Epson EB-460i LCD или аналогичный по техническим характеристикам"
                },
                {
                    "id": 8141,
                    "name": "Компьютер \"i5-4440(3.1)/8Gb/500Gb/VGA/23\"\" или аналогичный по техническим характеристикам: не менее 16 шт."
                }
            ]
        },
        {
            "id": 44682,
            "planlineslink_id": 4107,
            "type": "fos",
            "value": [
                {
                    "num": "3",
                    "type": 19,
                    "about": "Выполнение каждой лабораторной работы состоит из двух частей: практической части в ходе которой необходимо выполнить индивидуальное задание и подготовка и защита отчета по лабораторной работе. Реализация решения индивидуального задания осуществляется средствами платформы Java. В ходе выполнения лабораторной работы студент должен применить теоретические знания об объектном подходе к программированию, полученные в ходе изучения курса, а также приобрести практические навыки использования объектно-ориентированного языка программирования Java для решения типовых задач. Подготовка отчета по лабораторной работе необходима для закрепления и переосмысления полученных знаний и навыков. Для успешной сдачи лабораторной работы необходимо продемонстрировать работу программы, реализующую индивидуальное задание, устранить выявленные преподавателем недостатки, подготовить и защитить отчет.\nТребования к оформлению программного кода, а также содержанию отчета указаны в соответствующем разделе методических указаний для каждой лабораторной работы.\n\nСписок тем контрольных вопросов для защиты отчета:\n\nК лабораторной работе №1\n1. Создание и запуск Java-программ и состав платформы Java.\n2. Точка входа в программу и назначение аргумента метода main(String[] args).\n3. Блоки кода и видимость переменных в Java.\n4. Объявление переменных и работа с массивами в Java.\n5. Типы данных в Java.\n6. Операторы цикла Java.\n7. Условные операторы Java.\n8. Константы в Java, назначение и использование.\n9. Глобальные, локальные и временные (temporary) переменные в Java.\n\nК лабораторной работе №2:\n1. Интегрированная среда разработки (IDE), её интерфейс и основные возможности.\n2. Пакеты java.\n3. Классы и объекты.\n4. Объявление класса.\n5. Члены класса: поля и методы.\n6. Модификаторы доступа.\n7. Создание объекта.\n8. Конструкторы и их вызов.\n9. Вызов методов объекта.\n10. Передача параметров при вызове методов.\n11. Сигнатура метода.\n\nК лабораторной работе №3:\n1. Система ввода/вывода.\n2. Понятие потока данных.\n3. Байтовые и символьные потоки данных.\n4. Низкоуровневые и высокоуровневые потоки данных.\n5. Цепочки потоков данных.\n6. Исключения в java.\n7. Проверяемые исключения.\n8. Блок finally.\n9. Возбуждение исключения.\n10. Модификатор static.\n11. Вызов статических методов.\n12. Статические поля.\n\nК лабораторной работе №4:\n1. Наследование.\n2. Инкапсуляция.\n3. Полиморфизм.\n4. Абстрактный класс, абстрактные методы.\n5. Переопределение метода.\n6. Реализация интерфейса, множественное наследование.\n7. Отношение классов «агрегирование».\n8. Основные коллекции java (ArrayList, LinkedList, HashTable).",
                    "title": "семестр 3 | Отчет по лабораторной работе",
                    "criteria": "В процессе защиты отчета по лабораторной работе, студенту задаются контрольные вопросы теоретического и практического характера, соответствующие теме работы. Для успешной защиты отчета студенту необходимо дать краткое изложение основных результатов полученных в ходе выполнения лабораторной работы, устно ответить на теоретические вопросы по теме лабораторной работы, а также продемонстрировать умение ориентироваться в написанном программном коде. Успешная защита отчета является необходимым условием для выставления оценки «зачтено» по соответствующей лабораторной работе."
                },
                {
                    "num": "4",
                    "type": 19,
                    "about": "Выполнение каждой лабораторной работы состоит из двух частей: практической части в ходе которой необходимо выполнить индивидуальное задание и подготовка и защита отчета по лабораторной работе. Реализация решения индивидуального задания осуществляется средствами платформы Java. В ходе выполнения лабораторной работы студент должен применить теоретические знания об объектном подходе к программированию, полученные в ходе изучения курса, а также приобрести практические навыки использования объектно-ориентированного языка программирования Java для решения типовых задач. Подготовка отчета по лабораторной работе необходима для закрепления и переосмысления полученных знаний и навыков. Для успешной сдачи лабораторной работы необходимо продемонстрировать работу программы, реализующую индивидуальное задание, устранить выявленные преподавателем недостатки, подготовить и защитить отчет.\nТребования к оформлению программного кода, а также содержанию отчета указаны в соответствующем разделе методических указаний для каждой лабораторной работы.\n\nСписок тем контрольных вопросов для защиты отчета:\n\nК лабораторной работе №1(5):\n1. Понятие компонента графического пользовательского интерфейса.\n2. Назначение контейнеров Swing.\n3. Назначение планировщиков раскладки компонентов.\n4. Наиболее распространённые планировщики раскладки.\n5. Создание своего планировщика раскладки.\n6. Обработка событий.\n7. Интерфейс ActionListener.\n8. Архитектурный паттерн MVC.\n\nК лабораторной работе №2(6):\n1. Определение понятий БД и СУБД, какова их роль в программной разработке?\n2. Назначение JDBC-драйверов и их виды.\n3. Общая схема работы с БД базовыми средствами Java.\n4. Классы Statement, Connection и ResultSet.\n5. Общие принципы объектно-реляционного отображения.\n6. Технология работы с ORM-фреймворками.\n\nК лабораторной работе №3(7):\n1. Структура Android-проекта.\n2. Разметка экранов приложения.\n3. Работа с ресурсами Android-проекта.\n4. Жизненный цикл Activity и основные callback-методы.\n5. Инструмент Logcat.\n6. Какие бывают GroupView и для чего какой использовать?\n7. Основные View в Android и работа с ними.\n8. RecyclerView и RecyclerViewAdapter.",
                    "title": "семестр 4 | Отчет по лабораторной работе",
                    "criteria": "В процессе защиты отчета по лабораторной работе, студенту задаются контрольные вопросы теоретического и практического характера, соответствующие теме работы. Для успешной защиты отчета студенту необходимо дать краткое изложение основных результатов полученных в ходе выполнения лабораторной работы, устно ответить на теоретические вопросы по теме лабораторной работы, а также продемонстрировать умение ориентироваться в написанном программном коде. Успешная защита отчета является необходимым условием для выставления оценки «зачтено» по соответствующей лабораторной работе."
                }
            ]
        },
        {
            "id": 39688,
            "planlineslink_id": 4107,
            "type": "tat",
            "value": [
                {
                    "num": 4,
                    "good": "хорошее понимание теоретических основ объектно-ориентированного программирования и знания основных понятий объектно-ориентированного подхода, владеет понятийным аппаратом и методами объектной декомпозиции для решения типовых задач в рамках предметной области, незначительные ошибки при ответах на заданные вопросы, демонстрирует хорошее владение объектно-ориентированным языком программирования и\nпрограммно-инструментальными средствами",
                    "type": "ekz",
                    "about": "Экзамен проводится в устной форме, для допуска до экзамена необходимо сдать все лабораторные работы. Оформляются 15 билетов, в каждом билете 2 теоретических вопроса и один практический. Оценка выставляется по результатам собеседования по вопросам.\n\nВопросы к экзамену:\n1. Исторические предпосылки возникновения объектно-ориентированного подхода.\n2. Сложность разработки программного обеспечения: из чего складывается, чем обуславливается?\n3. Способы борьбы со сложностью разработки программного обеспечения.\n4. Структурная и объектная декомпозиция. В чем разница? Примеры.\n5. Определение объектно-ориентированного проектирования и программирования и их взаимосвязь.\n6. Объектно-ориентированные языки программирования: признаки таких языков, примеры.\n7. Объекты и классы: дать определение этих понятий и раскрыть их взаимосвязь. Проиллюстрировать на примерах.\n8. Взаимодействие объектов, активные и пассивные объекты.\n9. Механизмы ограничения доступа к членам класса в Java. Пояснить, зачем они нужны.\n10. Конструкторы: назначение и использование. Привести примеры объявления и вызова Java.\n11. Поведение и состояние объекта (формальные определения и пример).\n12. Понятие инкапсуляции в объектно-ориентированном программировании. Почему это один из основополагающих принципов ООП?\n13. Наследование в объектно-ориентированном программировании. Почему это один из основополагающих принципов ООП? Как реализуется в Java?\n14. Полиморфизм в объектно-ориентированном программировании. Почему это один из основополагающих принципов ООП? Статический и динамический полиморфизм в Java\n15. Статичные члены класса в Java. Назначение и применение.\n16. Объявление класса в Java, какие могут быть члены у класса? Привести примеры.\n17. Абстрактные классы: назначение, использование.\n18. Множественное наследование, «проблема ромба».\n19. Вызов методов суперкласса в Java. Привести примеры.\n20. Множественное наследование в Java: реализация интерфейсов.\n21. Переопределение унаследованных методов. Привести примеры.\n22. Какие компоненты входят в состав платформы Java и их назначение?\n23. Создание объекта и вызов его методов в Java.\n24. Назначение метода public static void main() и его аргументы.\n25. Пакеты Java: назначение и использование.\n26. Объявление и особенности работы с массивами в Java, примеры.\n27. Основные конструкции языка Java (примеры).\n28. Сигнатура метода и его аргументы.\n29. Область видимости переменных в Java: какие возможны варианты и для чего?\n30. Использование модификатора final в Java: где можно применять и какой эффект оказывает?\n31. Байтовые потоки ввода/вывода Java. Примеры.\n32. Символьные потоки ввода/вывода Java. Примеры.\n33. Низкоуровневые и высокоуровневые потоки ввода/вывода Java. Примеры.\n34. Цепочки (chains) потоков ввода/вывода. Примеры.\n35. Обработка исключительных ситуаций (Exceptions) в Java.\n36. Проверяемые (checked) и непроверяемые (runtime) исключения Java.\n37. Делегирование обработка исключительных ситуаций ( throws exceptions) в Java.\n38. Примитивные и ссылочные типы Java. В чем между ними разница? Примеры.\n39. Что нужно для создания и/или запуска Java-приложений? Продемонстрировать технологию запуска java-приложения из консоли.\n40. Использование псевдонима объекта (this) в контексте выполнения его методов в Java.\n41. Анонимные классы в Java – определение и примеры использования.\n42. Шаблон проектирования MVC.\n43. Компоненты и контейнеры Swing.\n44. Планировщики раскладки компонентов. Примеры.\n45. Обработка событий: шаблон Listener.\n46. Работа с компонентом Swing JTable.\n47. Коллекции Java: ArrayList и LinkedList (на примере).\n48. Общая схема работы с БД базовыми средствами Java.\n49. Понятие ORM и общая схема работы в Java.\n50. UML: диаграмма классов, виды отношений между классами.",
                    "great": "глубокое понимание теоретических основ объектно-ориентированного программирования, отличные знания основных понятий объектно-ориентированного подхода к разработке программного обеспечения, уверенное владение понятийным аппаратом и техниками объектно-ориентированного подхода при решении типовых задач в рамках предметной\nобласти, грамотное и логически стройное изложение материала при ответах на все вопросы из билета, знание дополнительно рекомендованной  литературы",
                    "title": "Экзамен",
                    "example": "Типовой билет к экзамену:\n1. Поведение и состояние объекта (формальные определения и пример).\n2. Понятие ORM и общая схема работы в Java.\n3. Обработка событий: шаблон Listener.",
                    "satisfactorily": "понимание теоретических основ объектно-ориентированного программирования с незначительными пробелами, знает основные понятия и\nметоды объектно-ориентированного подхода, изложение ответов с ошибками, уверенно исправляемыми после дополнительных вопросов, необходимость наводящих вопросов для получения верного ответа от студента",
                    "unsatisfactory": "наличие грубых ошибок в ответе, непонимание сущности излагаемого вопроса, неуверенность и неточность ответов на дополнительные и\nнаводящие вопросы, отсутствие навыков владения объектно-ориентированным языком программирования.\n"
                },
                {
                    "num": 3,
                    "type": "zach",
                    "about": "Зачет ставится по результатам выполнения лабораторных работ в 3 семестре, посещения лекций и ответов на вопросы из билета к зачету. Для допуска к зачету должны быть выполнены и защищены все лабораторные работы за 3 семестр. На зачете студент должен устно ответить на вопросы билета, а также быть способен составить программный код по тематике вопроса по требованию преподавателя.\nСтудент вправе не отвечать на вопросы билета и получить зачет по дисциплине, если он не пропустил ни одной лекции по дисциплине в течение 3 семестра и активно работал в ходе лабораторного практикума. Студент вправе отвечать только на один из вопросов билета (по своему выбору) и получить зачет по дисциплине, если он пропустил не более 2 лекций по дисциплине в 3 семестре. Допускается письменный ответ на вопросы билета на зачете (по решению преподавателя).\n\nСписок вопросов к зачёту:\n1. Предпосылки возникновения объектно-ориентированного подхода.\n2. Сложность разработки программного обеспечения.\n3. Способы борьбы со сложностью разработки программного обеспечения.\n4. Структурная и объектная декомпозиция.\n5. Объектно-ориентированные языки программирования.\n6. Объекты и классы: определение этих понятий и их взаимосвязь.\n7. Спецификация (определение) класса, его члены.\n8. Конструкторы, деструкторы: назначение и использование. Пояснить на примерах.\n9. Сигнатура метода и его аргументы. Привести примеры несовместных сигнатур.\n10. Поведение и состояние объекта. Раскрыть понятия и проиллюстрировать примером.\n11. Механизмы ограничения доступа к членам класса. Пояснить, зачем они нужны.\n12. Статичные члены класса: определение и использование. Привести примеры.\n13. Инкапсуляция в объектно-ориентированном программировании.\n14. Взаимодействие объектов, активные и пассивные объекты.\n15. Создание объекта и вызов его методов в Java.\n16. Использование псевдонима объекта в контексте выполнения его методов (this)\n17. Перечислить основные составляющие платформы Java и их назначение.\n18. Технология сборки и запуска Java-приложений.\n19. Основные конструкции языка Java. Привести примеры.\n20. Примитивные и ссылочные типы Java. Примеры объявления переменных.\n21. Назначение метода public static void main() и его аргументы.\n22. Работа с массивами в Java. Привести примеры.\n23. Модификатор final в Java. Примеры использования.\n24. Область видимости переменных (scope) в Java. Привести примеры.\n25. Пакеты Java: назначение и использование. Привести примеры стандартных пакетов.\n26. Понятие потока ввода/вывода Java. Привести примеры.\n27. Низкоуровневые и высокоуровневые потоки ввода/вывода Java.\n28. Цепочки потоков ввода/вывода.\n29. Классы Reader и Writer: назначение и отличия от Input/OutputStream\n30. Обработка исключительных ситуаций (Exceptions). Привести примеры.\n31. Делегирование исключительных ситуаций (Exceptions). Привести примеры.\n32. Проверяемые (checked) и непроверяемые (runtime) исключения Java.\n33. Наследование в объектно-ориентированном программировании.\n34. Полиморфизм в объектно-ориентированном программировании.\n35. Множественное наследование: реализация интерфейсов Java.",
                    "title": "Зачет",
                    "passed": "демонстрирует понимание основ объектно-ориентированного программирования и знания основных понятий объектно-ориентированного\nподхода, владеет понятийным аппаратом и методами объектной декомпозиции для решения типовых задач в рамках предметной области, владеет объектно-ориентированным языком программирования на базовом уровне: способен описывать классы, создавать объекты и вызывать их методы для решения типовых задач.",
                    "example": "Типовой билет к зачёту:\nВопрос 1:\nОбъекты и классы: определение этих понятий и их взаимосвязь.\nВопрос 2:\nОбработка исключительных ситуаций (Exceptions). Продемонстрировать на примере",
                    "unpassed": "наличие грубых ошибок в ответах на вопросы, непонимание сущности излагаемого вопроса, отсутствие навыков использования объектно-ориентированного программирования для решения типовых задач\n"
                },
                {
                    "num": 4,
                    "good": "Продемонстрировано хорошее понимание теоретических основ объектно-ориентированного подхода к разработке программного обеспечения. Бизнес-логика приложения не содержит зависимостей от классов осуществляющих ввод/вывод данных, а также от классов реализующих пользовательский интерфейс. Поставленная задача решена полностью с применением изученных в рамках курса программных библиотек и инструментальных средств.",
                    "type": "krkp",
                    "about": "Промежуточная аттестация в виде защиты курсового проекта проводится в последнюю неделю 4-го семестра обучения. По результатам аттестации выставляются оценки: «отлично», «хорошо», «удовлетворительно», «неудовлетворительно». Целью курсового проектирования является закрепление теоретических знаний полученных в процессе изучения курса «Объектно-ориентированное программирование» и развитие практических навыков применения объектного подхода в ходе решения\nконкретной практической задачи – разработки приложения с использованием объектно-ориентированного подхода, а также развитие способностей к обоснованному принятию самостоятельных решений в ходе проектной деятельности и получение базового опыта разработки программного обеспечения с использованием объектно-ориентированного подхода.\n\nЗадание на курсовое проектирование: студенты должны в соответствии с индивидуальным заданием спроектировать и реализовать приложение (или библиотеку классов) применяя объектно-ориентированный подход к разработке программного\nобеспечения. Реализованное программное обеспечение обязательно должно быть протестировано.\nТема курсового проекта формулируется руководителем курсового проектирования, но может быть предложена студентом самостоятельно.\nПо мере выполнения курсового проекта, студент показывают руководителю для предварительной проверки законченные главы пояснительной записки, а также программный код или его фрагменты. Готовые курсовые проекты защищаются студентами. В процессе защиты студент должен ответить на вопросы преподавателя по содержанию разделов пояснительной записки и быть готов пояснить проектные решения и дать комментарии по программному коду.\nНа защиту студент должен предоставить пояснительную записку по курсовому проекту, содержащую исчерпывающее описание всех разделов курсового проекта и корректное обоснование проектных решений, а также ссылку на репозиторий с исходным кодом проекта, оформленную в соответствии с требованиями СТО ИРНИТУ.\n\nПримерные темы курсовых проектов:\n1. Разработка приложения для работы с базой объектов недвижимости.\n2. Моделирование работы цеха производящего изделия из набора деталей.\n3. Моделирование замкнутой биологической системы (корм, травоядное, хищник).\n4. Разработка библиотеки классов для реализации моделей систем массового обслуживания различных типов.\n5. Библиотека классов для реализации различных структур данных (например, «Обобщённый массив» позволяющий эффективно хранить данные произвольных типов).\n6. Библиотека классов для реализации журнала успеваемости студентов по предмету.\n7. Приложение для ведения клиентской базы организации.\n8. Разработка библиотеки классов для работы с различными геометрическими объектами.\n9. Разработка записной книжки с различными видами записей (контакты, пароли, напоминания и т.п.).\n10. Разработка библиотеки классов для реализации искусственной нейронной сети прямого распространения.\n11. Приложение для учета товаров на складе.\n12. Библиотека классов для автоматического разбора и анализа текста.\n13. Приложение для учета кадров в организации.\n14. Разработка графической оболочки для экспертной системы на основе CLIPS/Drools.\n15. Разработка игрового приложения.\n16. Разработка мобильного приложения работающего с удаленными сервисами.",
                    "great": "Продемонстрировано глубокое понимание теоретических основ\nобъектно-ориентированного подхода к разработке программного обеспечения. Программная архитектура разделена на слои для обеспечения гибкости и простоты дальнейшего развития функциональности. Бизнес-логика приложения не содержит зависимостей от инфраструктурных слоев и фреймворков. Поставленная задача решена полностью, в процессе решения были применены самостоятельно изученные программные библиотеки и\nинструментальные средства, использованы дополнительные информационные источники и на них имеются ссылки по тексту пояснительной записки.",
                    "title": "Курсовая работа/проект",
                    "example": "",
                    "satisfactorily": "Демонстрирует понимание теоретических основ объектно-ориентированного\nподхода к разработке программного обеспечения с незначительными пробелами. Бизнес-логика приложения может содержать зависимости от классов осуществляющих ввод/вывод данных, или от классов реализующих пользовательский интерфейс. Поставленная задача решена частично.",
                    "unsatisfactory": "Неспособность дать пояснения по пояснительной записке и программному коду, отсутствуют выводы; несоответствие оглавления главам и разделам работы; несогласованность темы работы и её содержания; отсутствие или\nфальсификация ссылок на литературные источники; грубые ошибки в работе, непонимание сущности излагаемого вопроса, неуверенность и неточность ответов на дополнительные или наводящие вопросы. Поставленная задача не\nрешена."
                }
            ]
        },
        {
            "id": 57467,
            "planlineslink_id": 4107,
            "type": "library",
            "value": {
                "dopBook": [
                    {
                        "id": 1743515,
                        "cnt": 1,
                        "idd": 106119,
                        "place": None,
                        "title": "UML 2.0. Объектно-ориентированное моделирование и разработка",
                        "avtors": "Рамбо, Джеймс; Блаха, Майкл",
                        "irbisid": "004.42'236/Р21-753028",
                        "rubrica": "Объектно-ориентированное программирование",
                        "bib_disc": "Рамбо Дж. UML 2.0. Объектно-ориентированное моделирование и разработка / Дж. Рамбо, М. Блаха, 2007. - 540.",
                        "izd_type": "традиционный",
                        "year_izd": 2007,
                        "http_link": None
                    },
                    {
                        "id": 1773014,
                        "cnt": 1,
                        "idd": 135817,
                        "place": None,
                        "title": "Объектно-ориентированное программирование и проектирование : учебное пособие",
                        "avtors": "Горбунова, Татьяна Николаевна; Казанский, Александр Анатольевич",
                        "irbisid": "004.42'236(075.8)-349660704",
                        "rubrica": "Объектно-ориентированное программирование",
                        "bib_disc": "Горбунова Т. Н. Объектно-ориентированное программирование и проектирование : учебное пособие / Т. Н. Горбунова, 2011. - 97.",
                        "izd_type": "традиционный",
                        "year_izd": 2011,
                        "http_link": None
                    },
                    {
                        "id": 1780692,
                        "cnt": 2,
                        "idd": 143505,
                        "place": None,
                        "title": "Философия Java : монография",
                        "avtors": "Эккель, Брюс",
                        "irbisid": "004.43-351661647",
                        "rubrica": "Программирования языки",
                        "bib_disc": "Эккель Б. Философия Java : монография / Б. Эккель, 2015. - 1165.",
                        "izd_type": "традиционный",
                        "year_izd": 2015,
                        "http_link": None
                    },
                    {
                        "id": 1780784,
                        "cnt": 3,
                        "idd": 143597,
                        "place": None,
                        "title": "Java 7 : [наиболее полное руководство]: для программистов",
                        "avtors": "Хабибуллин, Ильдар Шаукатович",
                        "irbisid": "004.43-809517647",
                        "rubrica": "Программирования языки",
                        "bib_disc": "Хабибуллин И. Ш. Java 7 : [наиболее полное руководство]: для программистов / И. Ш. Хабибуллин, 2014. - 768.",
                        "izd_type": "традиционный",
                        "year_izd": 2014,
                        "http_link": None
                    },
                    {
                        "id": 1780688,
                        "cnt": 2,
                        "idd": 143501,
                        "place": None,
                        "title": "Паттерны проектирования",
                        "avtors": "Фримен, Эрик; Фримен, Элизабет; Сьерра, Кэтти; Бейтс, Берт",
                        "irbisid": "-039947",
                        "rubrica": "Программирование",
                        "bib_disc": "Паттерны проектирования / Э. Фримен, Э. Фримен при участии К. Сьерра и Б. Бейтса, 2015. - 645.",
                        "izd_type": "традиционный",
                        "year_izd": 2015,
                        "http_link": None
                    }
                ],
                "mainBook": [
                    {
                        "id": 1769618,
                        "cnt": 15,
                        "idd": 132404,
                        "place": None,
                        "title": "Java. Объектно-ориентированное программирование : для магистров и бакалавров: базовый курс по объектно-ориентированному программированию",
                        "avtors": "Васильев, Алексей Николаевич",
                        "irbisid": "004/В 19-432723200",
                        "rubrica": "Программирования языки",
                        "bib_disc": "Васильев А. Н. Java. Объектно-ориентированное программирование : для магистров и бакалавров: базовый курс по объектно-ориентированному программированию / А. Н. Васильев, 2012. - 395.",
                        "izd_type": "традиционный",
                        "year_izd": 2012,
                        "http_link": None
                    },
                    {
                        "id": 1885684,
                        "cnt": 0,
                        "idd": 489868,
                        "place": None,
                        "title": " Объектно-ориентированное программирование : учебник для вузов",
                        "avtors": "Барков И. А.",
                        "irbisid": "004.42'236(075.8)-556031189",
                        "rubrica": "Объектно-ориентированное программирование ",
                        "bib_disc": "Барков И. А.  Объектно-ориентированное программирование : учебник для вузов / И. А. Барков, 2023. - 700.",
                        "izd_type": "электронный",
                        "year_izd": 2023,
                        "http_link": "https://e.lanbook.com/book/329549"
                    },
                    {
                        "id": 1791191,
                        "cnt": 1,
                        "idd": 154025,
                        "place": None,
                        "title": "Объектно-ориентированное программирование : методические указания по выполнению лабораторных работ",
                        "avtors": "Аршинский, Вадим Леонидович",
                        "irbisid": "004.42'236(076.5)/О-29-614430302",
                        "rubrica": "Объектно-ориентированное программирование",
                        "bib_disc": "Объектно-ориентированное программирование : методические указания по выполнению лабораторных работ / Иркут. нац. исслед. техн. ун-т, 2017. - 24.",
                        "izd_type": "электронный",
                        "year_izd": 2017,
                        "http_link": "http://elib.istu.edu/viewer/view.php?file=/files/er-1565.pdf"
                    }
                ]
            }
        },
        {
            "id": 57399,
            "planlineslink_id": 4107,
            "type": "guidelines",
            "value": [
                {
                    "course": "Аршинский В.Л. Объектно-ориентированное программирование : электронный курс / В.Л. Аршинский, Маланова Т.В. https://el.istu.edu/course/view.php?id=4237",
                    "laboratory": "1. Аршинский В.Л. Объектно-ориентированное программирование : электронный курс / В.Л. Аршинский, Маланова Т.В. https://el.istu.edu/course/view.php?id=4237\n2. Аршинский В.Л. Объектно-ориентированное программирование [Электронный ресурс] : методические указания по выполнению лабораторных работ / Иркут. нац. исслед. техн. унт, 2017. - 24 с. Режим доступа: http://elib.istu.edu/viewer/view.php?file=/files/er-1565.pdf",
                    "independent": "Аршинский В.Л. Объектно-ориентированное программирование : электронный курс / В.Л. Аршинский, Маланова Т.В. https://el.istu.edu/course/view.php?id=4237"
                }
            ]
        }
    ]
}
