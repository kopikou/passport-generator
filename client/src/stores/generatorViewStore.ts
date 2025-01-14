import {defineStore} from "pinia";
import {computed, ref, watch} from "vue";
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

    activeRpdId,
    rpdData,
    indicatorsData,
    planlinesData,
    semestersData,
  }
})

export default useGeneratorViewStore;
