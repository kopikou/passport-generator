import {defineStore} from "pinia";
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import _ from "lodash";

const usePlanViewStore = defineStore('PlanViewStore', () => {
  const cafData = ref([])
  const sync_option = ref([
    {value: true, label: 'Да'},
    {value: false, label: 'Нет'},
  ])

  const fileData = ref([])
  const planData = ref([])
  const linesData = ref([])
  const semesterData = ref([])
  const indicatorsData = ref([])
  const documentsData = ref([])

  const activeFileId = ref(null)

  const $q = useQuasar()

  async function getData() {
    let r = await api.get("/api/arim/kafs/")
    cafData.value = r.data
  }

  async function getLinesData() {
    let r = await api.get("/api/plx/get-lines-data", {params: {id: activeFileId.value}})
    let data = r.data

    linesData.value = r.data.items
  }

  async function getFileData() {
    let r = await api.get(`/api/plx/${activeFileId.value}/`)

    fileData.value = r.data.items
    planData.value = r.data.parser.plan
    linesData.value = r.data.parser.lines
    semesterData.value = r.data.parser.semester
    indicatorsData.value = r.data.parser.indicators
    documentsData.value = r.data.parser.documents

  }

  const disabled = computed(() => {
    if (fileData.value.length == 0) {
      return false
    }
    if (fileData.value[0].status == 3) {
      return true
    }
    return false
  })

  const linesDataById = computed(() => {
    return _.keyBy(linesData.value, 'id');
  })

  onBeforeMount(async () => {
    const loadingData = $q.loading.show({
      group: 'first',
      message: 'Загрузка данных плана',
    })

    await getData()

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
    fileData,
    cafData,
    sync_option,
    planData,
    linesData,
    semesterData,
    indicatorsData,
    documentsData,
    linesDataById,
    disabled,
    getLinesData,
  }
})

export default usePlanViewStore;
