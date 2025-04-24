import {defineStore} from "pinia";
import {computed, nextTick, ref, watch, watchEffect} from "vue";
import {api} from "boot/axios";
import {onAuthenticated} from "src/composables/onAuthenticated";
import {useQuasar} from "quasar";
import _ from "lodash";
import {
  DefaultRecources,
  DisciplineThemesData, DisciplineWorkHour, GeneratorBookData,
  GeneratorData, GeneratorFormControlData, GeneratorIndependentTypesData, GeneratorOborudData,
  GeneratorPlanLineData, GeneratorSoftwareData, OtherDiscipline, PlanIndicatorData, PlanSemestrData,
} from "src/types";
import {fasElevator} from "@quasar/extras/fontawesome-v6";

const useGeneratorViewStore = defineStore('GeneratorViewStore', () => {
  const cafData = ref([])
  const rpdData = ref<GeneratorData>({});
  const formControl = ref<GeneratorFormControlData[]>([])
  const independentTypes = ref<GeneratorIndependentTypesData[]>([])
  const activeRpdId = ref(null)

  const oldPlans = computed(() => {
    return _.orderBy(rpdData.value.old || [], x => -x.startyear)
  })

  const status = computed(() => {
    return rpdData.value?.status || -1
  })

  const statusVerbose = computed(() => {
    return rpdData.value?.status_verbose
  })

  const disabled = computed(() => {
    return [2, 3].includes(rpdData.value?.status || 0)
  })

  const indicatorsData = computed<PlanIndicatorData[]>(() => {
    return rpdData.value.planlines?.indicators || []
  })

  const planlinesData = computed<GeneratorPlanLineData[]>(() => {
    return rpdData.value?.planlines || []
  })

  const comment = computed(() => {
    return rpdData.value?.comment
  })

  const admissionData = computed(() => {
    return rpdData.value?.admission || []
  })

  const semestersData = computed<PlanSemestrData[]>(() => {
    return rpdData.value.planlines?.semesters || []
  })

  const otherDiscipline = computed<OtherDiscipline[]>(() => {
    return rpdData.value.other_discipline || []
  })

  const disciplineThemes = computed<DisciplineThemesData[]>(() => {
    return rpdData.value.discipline_themes || []
  })

  const disciplineThemesById = computed<DisciplineThemesData[]>(() => {
    return _.keyBy(disciplineThemes.value, x => x.id)
  })

  const disciplineLibrary = computed<GeneratorBookData[]>(() => {
    return _.filter(rpdData.value.additional_info, (x) => x.type == "library")
  })

  const disciplinePlace = computed(() => {
    return _.filter(rpdData.value.additional_info, (x) => x.type == "disciplinePlace")
  })

  const interactiveMethods = computed(() => {
    return _.filter(rpdData.value.additional_info, (x) => x.type == "interactiveMethods")
  })

  const disciplineSoftware = computed<GeneratorSoftwareData[]>(() => {
    return _.filter(rpdData.value.additional_info, (x) => x.type == "software")
  })

  const disciplineLogistics = computed<GeneratorOborudData[]>(() => {
    return _.filter(rpdData.value.additional_info, (x) => x.type == "logistics")
  })

  const resources = computed(() => {
    return _.filter(rpdData.value.additional_info, (x) => x.type == "resources")
  })

  const guidelines = computed(() => {
    return _.filter(rpdData.value.additional_info, (x) => x.type == "guidelines")[0]?.value || []
  })

  const tatInfo = computed(() => {
    return _.filter(rpdData.value.additional_info, (x) => x.type == "tat")[0]?.value || []
  })

  const fosInfo = computed(() => {
    return _.filter(rpdData.value.additional_info, (x) => x.type == "fos")[0]?.value || []
  })

  const disciplineGoal = computed(() => {
    return _.filter(rpdData.value.additional_info, (x) => x.type == "disciplineGoal")[0]?.value || ''
  })

  const additionalInfo = computed(() => {
    return rpdData.value.additional_info || []
  })

  const disciplineWorkHour = computed<DisciplineWorkHour[]>(() => {
    return rpdData.value.discipline_work_hour || []
  })

  const lecturesDisciplineWorkHour = computed<DisciplineWorkHour[]>(() => {
    return _.filter(rpdData.value.discipline_work_hour, (x) => x.type == 0) || []
  })

  const labDisciplineWorkHour = computed<DisciplineWorkHour[]>(() => {
    return _.filter(rpdData.value.discipline_work_hour, (x) => x.type == 3) || []
  })

  const independentDisciplineWorkHour = computed<DisciplineWorkHour[]>(() => {
    return _.filter(rpdData.value.discipline_work_hour, (x) => x.type == 2) || []
  })

  const practiceDisciplineWorkHour = computed<DisciplineWorkHour[]>(() => {
    return _.filter(rpdData.value.discipline_work_hour, (x) => x.type == 1) || []
  })

  const defaultResources = computed<DefaultRecources[]>(() => {
    return rpdData.value.resources || []
  })


  const criticalErrors = computed(() => {
    return _.filter(errors.value, x => x.level == 'critical')
  })

  const hasTat = computed(() => {
    return _.some(semestersData.value, x => {
      return x.ekz || x.zach || x.zacho || x.kp || x.kr
    })
  })


  const lekcHours = computed(() => _(semestersData.value).map(x => x.lekc).sum())
  const srsHours = computed(() => _(semestersData.value).map(x => x.srs).sum())
  const prHours = computed(() => _(semestersData.value).map(x => x.pr).sum())
  const labHours = computed(() => _(semestersData.value).map(x => x.lab).sum())

  const $q = useQuasar()

  async function getCafData() {
    let r = await api.get("/api/arim/kafs/")
    cafData.value = r.data
  }

  async function getFormControlData() {
    let r = await api.get('/api/generator/get-form-control-data/')
    formControl.value = r.data
  }

  async function getIndependentTypesData() {
    let r = await api.get('/api/generator/get-independent-types-data/')
    independentTypes.value = r.data
  }

  async function getData() {
    let r = await api.get(`/api/generator/${activeRpdId.value}/`)
    rpdData.value = r.data
  }

  const errors = ref<{
    url: string,
    title: string,
    text: string[],
    level: string,
  }[]>([]);

  async function checkErrors() {
    const admkind = rpdData.value.admission.cadmkind
    const data: {
      url: string,
      title: string,
      text: string[],
      level: string,
    }[] = []

    const indicators = _(indicatorsData.value)
      .map(x => x.discipline_indicator)
      .flatten()
      .value()
    if (indicators.length == 0) {
      data.push({
        url: 'indicators',
        title: 'Не начинал',
        text: ['Не начаты заполняться индикаторы по дисциплине'],
        level: 'critical',
      })
    } else {
      const text: string[] = []
      _.forEach(indicators, (x) => {
        const ind = _.find(indicatorsData.value, q => q.id == x.indicator_id)
        if (!x.know) text.push(`Не заполнены сведения о "Знать" для индикатора: ${ind?.indicator_index}`)
        if (!x.able) text.push(`Не заполнены сведения о "Уметь" для индикатора: ${ind?.indicator_index}`)
        if (!x.own) text.push(`Не заполнены сведения о "Владеть" для индикатора: ${ind?.indicator_index}`)
        if (!x.criteria) text.push(`Не заполнены сведения о "Критериях" для индикатора: ${ind?.indicator_index}`)
        if (!x.methods) text.push(`Не заполнены сведения о "Методах" для индикатора: ${ind?.indicator_index}`)
      })
      if (text.length != 0) {
        data.push({
          url: 'indicators',
          title: 'Не заполнены индикаторы по дисциплине',
          text: text,
          level: 'critical',
        })
      }
    }

    const structure = _.find(additionalInfo.value, (x) => x.type == 'interactiveMethods')
    if (!structure) {
      data.push({
        url: 'structure',
        title: 'Не начинал',
        text: ['Не заполнена информация об интерактивных методах обучения'],
        level: 'critical',
      })
    } else {
      if (!structure.value.interactiveMethods) data.push({
        url: 'structure',
        title: 'Не заполнил',
        text: ['Не заполнена информация об интерактивных методах обучения'],
        level: 'critical',
      })
    }


    const semesters = _(semestersData.value).map(x => x.num).uniq().value()
    const themes = disciplineThemes.value

    if (themes.length == 0) {
      data.push({
        url: 'discipline-theme',
        title: 'Нет назначены темы по дисциплины',
        text: ['Отсутствуют темы по дисциплине'],
        level: 'critical',
      })
    } else {
      _.forEach(semesters, (x) => {
        if (_.filter(themes, q => q.semester == x).length == 0) {
          data.push({
            url: 'discipline-theme',
            title: 'Не заполнил',
            text: [`Нет тем по дисциплине для семестра № ${x}`],
            level: 'critical',
          })
        }
      })
    }


    if (lekcHours.value) {
      const lectures = _.filter(disciplineWorkHour.value, x => x.type == 0)
      if (lectures.length == 0) {
        data.push({
          url: 'discipline-lectures',
          title: 'Не начинал',
          text: ['Не заполнена информация об лекционных занятиях'],
          level: 'critical',
        })
      } else {
        _.forEach(semesters, (x) => {
          const lekHour = _.get(_.find(semestersData.value, q => q.num == x), 'lekc', 0)
          const currentLekHour = _(lecturesDisciplineWorkHour.value).filter(q => q.semester == x).map(q => q.hours).sum()
          if (currentLekHour != lekHour && lekHour) {
            data.push({
              url: 'discipline-lectures',
              title: 'Неверное кол-во часов в лекционных занятиях',
              text: [`Количество часов в лекционных занятий не сходиться в семестре № ${x}`],
              level: 'critical',
            })
          }
        })
      }
    }

    if (labHours.value) {
      const laboratory = _.filter(disciplineWorkHour.value, x => x.type == 3)
      if (laboratory.length == 0) {
        data.push({
          url: 'discipline-lab',
          title: 'Не начинал',
          text: ['Не заполнена информация о лабораторных работах'],
          level: 'critical',
        })
      } else {
        _.forEach(semesters, (x) => {
          const labHour = _.get(_.find(semestersData.value, q => q.num == x), 'lab', 0)
          const currentLabHour = _(labDisciplineWorkHour.value).filter(q => q.semester == x).map(q => q.hours).sum()
          if (currentLabHour != labHour && labHour) {
            data.push({
              url: 'discipline-lab',
              title: 'Неверное кол-во часов в лабораторных работах',
              text: [`Количество часов в лабораторных работах не сходиться в семестре № ${x}`],
              level: 'critical',
            })
          }
        })
      }
    }

    if (prHours.value) {
      const practice = _.filter(disciplineWorkHour.value, x => x.type == 1)
      if (practice.length == 0) {
        data.push({
          url: 'discipline-practice',
          title: 'Не начинал',
          text: ['Не заполнена информация о практических занятиях'],
          level: 'critical',
        })
      } else {
        _.forEach(semesters, (x) => {
          const practHour = _.get(_.find(semestersData.value, q => q.num == x), 'pr', 0)
          let currentpractHour = _(practiceDisciplineWorkHour.value).filter(q => q.semester == x).map(q => q.hours).sum()
          if (currentpractHour != practHour && practHour) {
            data.push({
              url: 'discipline-practice',
              title: 'Неверное кол-во часов в практических занятиях',
              text: [`Количество часов в практических часов не сходиться в семестре № ${x}`],
              level: 'critical',
            })
          }
        })
      }
    }

    if (srsHours.value) {
      const independent = _.filter(disciplineWorkHour.value, x => x.type == 2)
      if (independent.length == 0) {
        data.push({
          url: 'discipline-independent',
          title: 'Не начинал',
          text: ['Не заполнена информация о самостоятельных работах'],
          level: 'critical',
        })
      } else {
        _.forEach(semesters, (x) => {
          const independentHour = _.get(_.find(semestersData.value, q => q.num == x), 'srs', 0)
          const currentindependentHour = _(independentDisciplineWorkHour.value).filter(q => q.semester == x).map(q => q.hours).sum()
          if (currentindependentHour != independentHour && independentHour) {
            data.push({
              url: 'discipline-independent',
              title: 'Неверное кол-во часов в самостоятельных работах',
              text: [`Количество часов в самостоятельных работах не сходиться в семестре № ${x}`],
              level: 'critical',
            })
          }
        })
      }
    }

    function checkGuidelines(type: string, errorText: string) {
      if (!_.get(guidelines.value, `[0].${type}`, null)) {
        data.push({
          url: 'guidelines',
          title: 'Нет данных для методических указаний',
          text: [errorText],
          level: 'critical',
        })
      }
    }

    if (guidelines.value.length == 0) {
      data.push({
        url: 'guidelines',
        title: 'Не заполнены методические указания',
        text: [`Не заполнены методические указания`],
        level: 'critical',
      })
    } else {
      let lab = false
      let pr = false
      let srs = false
      let kp = false

      _.forEach(semestersData.value, (x) => {
        if (x.lab) lab = true
        if (x.pr) pr = true
        if (x.srs) srs = true
        if (x.kp || x.kr) kp = true
      })

      if (lab) checkGuidelines('laboratory', 'Не заполнены методические указания для лабораторных работ')
      if (pr) checkGuidelines('practice', 'Не заполнены методические указания для практических занятий')
      if (srs) checkGuidelines('independent', 'Не заполнены методические указания для самостоятельных занятий')
      if (kp) checkGuidelines('course', 'Не заполнены методические указания для курсового проекта/работы ')
    }

    const fos = _.uniqBy(disciplineThemes.value, 'formcontrol_verbose')

    _.forEach(fos, (x) => {
      const r = _.find(fosInfo.value, q => q.type == x.formcontrol_id)
      if (!r) {
        data.push({
          url: 'fos',
          title: 'Нет данных по оценочным материалам',
          text: [`Не заполнена информация о "${x.formcontrol_verbose}"`],
          level: 'critical',
        })
      } else {
        if (!_.get(r, 'criteria', null)) {
          data.push({
            url: 'fos',
            title: 'Нет данных по оценочным материалам',
            text: [`Нет информации о критериях оценивания для "${x.formcontrol_verbose}"`],
            level: 'critical',
          })
        }
        if (!_.get(r, 'about', null)) {
          data.push({
            url: 'fos',
            title: 'Нет данных по оценочным материалам',
            text: [`Неи информации об описании процедуры для "${x.formcontrol_verbose}"`],
            level: 'critical',
          })
        }
      }
    })

    function checkTat(type: string, errorText: string) {
      const r = _.find(tatInfo.value, x => x.type == type)
      if (!r) {
        data.push({
          url: 'tat',
          title: 'Нет информации по типовым оценочным средствам',
          text: [`Нет информации о типовых оценочных средствах для "${errorText}"`],
          level: 'critical',
        })
      } else {
        if (!r.about) {
          data.push({
            url: 'tat',
            title: `Нет данных`,
            text: [`Нет описания процедуры по "${errorText}"`],
            level: 'critical',
          })
        }
        if (type == 'zach') {
          if (!r.passed) {
            data.push({
              url: 'tat',
              title: `Нет данных`,
              text: [`Нет критерия оценивания по оценке "Зачтено" для "${errorText}"`],
              level: 'critical',
            })
          }
          if (!r.unpassed) {
            data.push({
              url: 'tat',
              title: `Нет данных`,
              text: [`Нет критерия оценивания по оценке "Не зачтено" для "${errorText}"`],
              level: 'critical',
            })
          }
        } else {
          if (!r.great) {
            data.push({
              url: 'tat',
              title: `Нет данных`,
              text: [`Нет критерия оценивания по оценке "Отлично" для "${errorText}"`],
              level: 'critical',
            })
          }
          if (!r.good) {
            data.push({
              url: 'tat',
              title: `Нет данных`,
              text: [`Нет критерия оценивания по оценке "Хорошо" для "${errorText}"`],
              level: 'critical',
            })
          }
          if (!r.satisfactorily) {
            data.push({
              url: 'tat',
              title: `Нет данных`,
              text: [`Нет критерия оценивания по оценке "Удовлетворительно" для "${errorText}"`],
              level: 'critical',
            })
          }
          if (!r.unsatisfactory) {
            data.push({
              url: 'tat',
              title: `Нет данных`,
              text: [`Нет критерия оценивания по оценке "Неудовлетворительно" для "${errorText}"`],
              level: 'critical',
            })
          }
        }
      }
    }

    if (hasTat.value) {
      if (tatInfo.value.length == 0) {
        data.push({
          url: 'tat',
          title: 'Не заполнены типовые оценочные средства',
          text: [`Не заполнены типовые оценочные средства`],
          level: 'critical',
        })
      } else {
        let zach = false
        let zacho = false
        let ekz = false
        let kp = false

        _.forEach(semestersData.value, (x) => {
          if (x.zach) zach = true
          if (x.zacho) zacho = true
          if (x.ekz) ekz = true
          if (x.kp || x.kr) kp = true
        })

        if (zach) checkTat('zach', 'Зачет')
        if (zacho) checkTat('zacho', 'Дифференцированный зачет')
        if (ekz) checkTat('ekz', 'Экзамен')
        if (kp) checkTat('krkp', 'Курсовой проекта/работа')
      }
    }


    const library = _.get(disciplineLibrary.value, `[0].value`)
    if (!library) {
      data.push({
        url: 'library',
        title: 'Не начинал',
        text: ['Не выбрана литература'],
        level: 'critical',
      })
    } else {
      if (library.mainBook.length == 0) {
        data.push({
          url: 'library',
          title: 'Не начинал',
          text: ['Нет основной литературы'],
          level: 'critical',
        })
      }
      if (library.dopBook.length == 0) {
        data.push({
          url: 'library',
          title: 'Не начинал',
          text: ['Нет дополнительной литературы'],
          level: 'critical',
        })
      }
    }

    if (resources.value.length == 0) {
      data.push({
        url: 'resources',
        title: 'Не начинал',
        text: ['Не заполнен раздел'],
        level: 'warning',
      })
    }

    const soft = _.get(disciplineSoftware.value, '[0].value', [])
    if (soft.length == 0) {
      data.push({
        url: 'soft',
        title: 'Не начинал',
        text: ['Не выбрано используемое ПО'],
        level: 'warning',
      })
    }

    const logistics = _.get(disciplineLogistics.value, '[0].value', [])
    if (logistics.length == 0) {
      data.push({
        url: 'logistics',
        title: 'Не начинал',
        text: ['Не выбрано используемое МТО'],
        level: 'warning',
      })
    }

    if (admkind != 5) {
      const disPlace = _.find(additionalInfo.value, (x) => x.type == 'disciplinePlace')
      if (!disPlace) {
        data.push({
          url: 'discipline-place',
          title: 'Не начинал',
          text: ['Не начата заполняться информация о месте дисциплины в структуре ООП'],
          level: 'warning',
        })
      } else {
        const text = []
        if (disPlace.value.precedence.length == 0) text.push('Не заполнена информация об предшествующих дисциплинах')
        if (disPlace.value.subsequent.length == 0) text.push('Не заполнена информация о последующих дисциплинах')

        if (text.length != 0) {
          data.push({
            url: 'discipline-place',
            title: 'Не заполнено место дисциплины в структуре ООП',
            text: text,
            level: 'warning',
          })
        }
      }
    }
    errors.value = data
  }

  onAuthenticated(async () => {
    const loadingHelpers = $q.loading.show({
      group: 'first',
      message: 'Загрузка справочников',
    })

    await getCafData()
    await getFormControlData()
    await getIndependentTypesData()
    loadingHelpers()
  })

  watch(rpdData, () => {
    checkErrors()
  })

  watch(activeRpdId, async () => {
    const loadingData = $q.loading.show({
      group: 'second',
      message: 'Загрузка данных РПД',
    })

    if (activeRpdId.value) {
      await getData()
    }

    loadingData()
  }, {immediate: true})


  return {
    cafData,
    oldPlans,
    formControl,
    independentTypes,
    otherDiscipline,
    admissionData,
    disciplineThemes,
    disciplineThemesById,
    disciplineWorkHour,
    lecturesDisciplineWorkHour,
    labDisciplineWorkHour,
    independentDisciplineWorkHour,
    practiceDisciplineWorkHour,
    disciplineLibrary,
    disciplineSoftware,
    disciplineLogistics,
    disciplinePlace,
    interactiveMethods,
    defaultResources,
    resources,
    comment,
    guidelines,
    fosInfo,
    tatInfo,
    disciplineGoal,
    additionalInfo,
    status,
    statusVerbose,
    disabled,
    hasTat,
    errors,
    criticalErrors,

    activeRpdId,
    rpdData,
    indicatorsData,
    planlinesData,
    semestersData,
    getData,
    checkErrors,
    lekcHours,
    srsHours,
    prHours,
    labHours,
  }
})

export default useGeneratorViewStore;
