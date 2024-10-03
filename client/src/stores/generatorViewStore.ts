import {defineStore} from "pinia";
import {computed, ref, watch} from "vue";
import {api} from "boot/axios";
import {onAuthenticated} from "src/composables/onAuthenticated";
import {useQuasar} from "quasar";
import _ from "lodash";
import {
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

  const indicatorsData = computed<PlanIndicatorData[]>(() => {
    return rpdData.value.planlines?.indicators || []
  })

  const planlinesData = computed<GeneratorPlanLineData[]>(() => {
    return rpdData.value?.planlines || []
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

  const disciplineLibrary = computed<GeneratorBookData[]>(() => {
    return _.filter(rpdData.value.additional_info, (x) => x.type == "library")
  })

  const disciplineSoftware = computed<GeneratorSoftwareData[]>(() => {
    return rpdData.value.software || []
  })

  const disciplineLogistics = computed<GeneratorOborudData[]>(() => {
    return rpdData.value.logistics || []
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
    formControl,
    independentTypes,
    otherDiscipline,
    disciplineThemes,
    lecturesDisciplineWorkHour,
    labDisciplineWorkHour,
    independentDisciplineWorkHour,
    practiceDisciplineWorkHour,
    disciplineLibrary,
    disciplineSoftware,
    disciplineLogistics,

    activeRpdId,
    rpdData,
    indicatorsData,
    planlinesData,
    semestersData,
  }
})

export default useGeneratorViewStore;
