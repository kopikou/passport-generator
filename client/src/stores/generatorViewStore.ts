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

const useGeneratorViewStore = defineStore('GeneratorViewStore', () => {
  const cafData = ref([])
  const rpdData = ref<GeneratorData[]>([])
  const formControl = ref<GeneratorFormControlData[]>([])
  const independentTypes = ref<GeneratorIndependentTypesData[]>([])
  const activeRpdId = ref(null)

  const oldPlans = computed(() => {
    return rpdData.value.old || []
  })

  const status = computed(() => {
    return rpdData.value?.status || -1
  })

  const statusVerbose = computed(() => {
    return rpdData.value?.status_verbose
  })

  const disabled = computed(() => {
    return [2, 3].includes(rpdData.value?.status)
  })

  const indicatorsData = computed<PlanIndicatorData[]>(() => {
    return rpdData.value.planlines?.indicators || []
  })

  const planlinesData = computed<GeneratorPlanLineData[]>(() => {
    return rpdData.value?.planlines || []
  })

  const comment = computed(() => {
    return rpdData.value?.comment || []
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

  const errors = ref([])

  function checkErrors() {
    const admkind = rpdData.value.admission.cadmkind
    const data = []

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
      const text = []
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
        if (currentLekHour != lekHour) {
          data.push({
            url: 'discipline-lectures',
            title: 'Неверное кол-во часов в лекционных занятиях',
            text: [`Количество часов в лекционных занятий не сходиться в семестре № ${x}`],
            level: 'critical',
          })
        }
      })
    }

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
        if (currentLabHour != labHour) {
          data.push({
            url: 'discipline-lab',
            title: 'Неверное кол-во часов в лабораторных работах',
            text: [`Количество часов в лабораторных работах не сходиться в семестре № ${x}`],
            level: 'critical',
          })
        }
      })
    }

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
        const currentpractHour = _(practiceDisciplineWorkHour.value).filter(q => q.semester == x).map(q => q.hours).sum()
        if (currentpractHour != practHour) {
          data.push({
            url: 'discipline-practice',
            title: 'Неверное кол-во часов в практических занятиях',
            text: [`Количество часов в практических часов не сходиться в семестре № ${x}`],
            level: 'critical',
          })
        }
      })
    }

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
        if (currentindependentHour != independentHour) {
          data.push({
            url: 'discipline-independent',
            title: 'Неверное кол-во часов в самостоятельных работах',
            text: [`Количество часов в самостоятельных работах не сходиться в семестре № ${x}`],
            level: 'critical',
          })
        }
      })
    }

    if (admkind != 5) {
      const disPlace = _.find(additionalInfo.value, (x) => x.type == 'disciplinePlace')
      if (!disPlace) {
        data.push({
          url: 'discipline-place',
          title: 'Не начинал',
          text: ['Не начата заполняться информация о месте дисциплины в структуре ООП'],
          level: 'critical',
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
            level: 'critical',
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
    checkErrors()

    loadingHelpers()
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
    errors,

    activeRpdId,
    rpdData,
    indicatorsData,
    planlinesData,
    semestersData,
    getData,
    checkErrors,
  }
})

export default useGeneratorViewStore;
