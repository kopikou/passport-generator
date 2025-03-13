import {defineStore} from "pinia";
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import _ from "lodash";
import {PlanData, PlanDocumentData, PlanFileData, PlanIndicatorData, PlanLineData, PlanSemestrData} from "src/types";
import {useRoute, useRouter} from "vue-router";
import router from "src/router";
import {onAuthenticated} from "src/composables/onAuthenticated";

const usePlanViewStore = defineStore('PlanViewStore', () => {
  const cafData = ref([])
  const docTypes = ref([])
  const sync_option = ref([
    {value: true, label: 'Да'},
    {value: false, label: 'Нет'},
  ])

  const fileData = ref<PlanFileData>([])
  const planData = ref<PlanData[]>([])
  const linesData = ref<PlanLineData[]>([])
  const semesterData = ref<PlanSemestrData[]>([])
  const indicatorsData = ref<PlanIndicatorData[]>([])
  const documentsData = ref<PlanDocumentData[]>([])
  const files = ref<PlanFileData[]>([])

  const activeFileId = ref(null)

  const $q = useQuasar()


  const router = useRouter();
  const route = useRoute();

  const activeFile = computed({
    get() {
      let matchFiles = files.value.filter(x => x.id == activeFileId.value)
      return matchFiles.length > 0 ? matchFiles[0] : null
    },
    async set(value) {
      if (value) {
        await router.push({name: route.name, params: {id: value.id}})
      }
    }
  })


  const disabled = computed(() => {
    return fileData.value.status >= 2
  })

  const linesDataById = computed(() => {
    return _.keyBy(linesData.value, 'id');
  })

  const indicatorsDataById = computed(() => {
    return _.keyBy(indicatorsData.value, 'indicator_index')
  })

  async function getCafData() {
    let r = await api.get("api/arim/kafs/")
    cafData.value = r.data
  }

  async function getDocTypesData() {
    let r = await api.get("api/plx/get-document-types/")
    docTypes.value = r.data
  }

  async function getLinesData() {
    let r = await api.get("api/plx/get-lines-data", {params: {id: activeFileId.value}})
    let data = r.data
    linesData.value = r.data.items
  }

  async function getFileData() {
    let r = await api.get(`api/plx/${activeFileId.value}/`)

    fileData.value = r.data.items
    planData.value = r.data.parser.plan
    linesData.value = r.data.parser.lines
    semesterData.value = r.data.parser.semester
    indicatorsData.value = r.data.parser.indicators
    documentsData.value = r.data.parser.documents

  }

  async function fetchPlxFiles() {
    $q.loading.show()
    let r = await api.get("api/plx/")
    files.value = _.sortBy(r.data, 'title')

    for (let f of files.value) {
      let m = f.title.match(/(\d{2}.\d{2}.\d{2})\s*\(([А-Яа-я]+)-(\d{2})/)
      if (m) {
        f.code = m[1]
        f.abbr = m[2]
        f.year = '20' + m[3]
      }
    }

    $q.loading.hide()
  }


  onAuthenticated(async () => {
    const loadingData = $q.loading.show({
      group: 'first',
      message: 'Загрузка данных плана',
    })

    await getCafData()
    await getDocTypesData()
    await fetchPlxFiles();

    loadingData()
  })

  watch(activeFileId, async () => {
    const loadingCafData = $q.loading.show({
      group: 'second',
      message: 'Загрузка данных кафедр',
    })

    if (activeFileId.value != null)
      await getFileData()

    loadingCafData()
  }, {immediate: true})


  return {
    activeFileId,
    activeFile,

    planData,
    linesData,
    semesterData,
    indicatorsData,
    documentsData,
    linesDataById,
    indicatorsDataById,
    fileData,
    cafData,
    docTypes,
    sync_option,
    disabled,
    files,

    getLinesData,
    fetchPlxFiles,
  }
})

export default usePlanViewStore;
