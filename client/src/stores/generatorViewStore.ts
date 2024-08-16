import {defineStore} from "pinia";
import {ref, watch} from "vue";
import {api} from "boot/axios";
import {onAuthenticated} from "src/composables/onAuthenticated";
import {useQuasar} from "quasar";

const useGeneratorViewStore = defineStore('GeneratorViewStore', () => {
  const cafData = ref([])
  const rpdData = ref([])
  const activeRpdId = ref(null)

  const $q = useQuasar()

  async function getCafData() {
    let r = await api.get("/api/arim/kafs/")
    cafData.value = r.data
  }

  async function getData() {
    let r = await api.get(`/api/generator/${activeRpdId.value}/`)
    rpdData.value = r.data
  }

  onAuthenticated(async () => {
    const loadingCafData = $q.loading.show({
      group: 'first',
      message: 'Загрузка данных кафедр',
    })

    await getCafData()

    loadingCafData()
  })

  watch(activeRpdId, async () => {
    const loadingData = $q.loading.show({
      group: 'second',
      message: 'Загрузка данных РПД',
    })

    if (activeRpdId.value != null)
      await getData()

    loadingData()
  }, {immediate: true})


  return {
    cafData,

    activeRpdId,
    rpdData,
  }
})

export default useGeneratorViewStore;
