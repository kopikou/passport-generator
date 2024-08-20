import {defineStore} from "pinia";
import {computed, ref, watch} from "vue";
import {api} from "boot/axios";
import {onAuthenticated} from "src/composables/onAuthenticated";
import {useQuasar} from "quasar";
import _ from "lodash";
import {GeneratorData} from "src/types";

const useGeneratorViewStore = defineStore('GeneratorViewStore', () => {
  const cafData = ref([])
  const rpdData = ref<GeneratorData[]>([])
  const activeRpdId = ref(null)

  const indicatorsData = computed(() => {
      return rpdData.value.planlines?.indicators || []
  })

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

    if (activeRpdId.value != null)
      await getData()

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
    indicatorsData,
  }
})

export default useGeneratorViewStore;
