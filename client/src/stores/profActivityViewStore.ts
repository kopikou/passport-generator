import {defineStore} from "pinia";
import {onAuthenticated} from "src/composables/onAuthenticated";
import {computed, ref} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import _ from "lodash";
import {PlanData} from "src/types";

const useProfActivityViewStore = defineStore('ProfActivityViewStore', () => {


  const $q = useQuasar()
  const admissionDataProfActivity = ref<PlanData[]>([])
  const areas_list = ref([])
  const types_list = ref([])
  const currentItem = ref()

  const admissionDataById = computed(() => {
    return _.keyBy(admissionDataProfActivity.value, x => x.id)
  })

  const areaById = computed(() => {
    return _.keyBy(areas_list.value, x => x.id)
  })

  const typeById = computed(() => {
    return _.keyBy(types_list.value, x => x.id)
  })

  async function getAdmissionDataForActivity() {
    let r = await api.get('/api/activity/get-admission-data/')
    admissionDataProfActivity.value = r.data
    if (!currentItem.value)
      currentItem.value = await _(r.data).map(x => x.id).first()
  }

  async function getAreasProfActivity() {
    let r = await api.get('/api/activity/get-areas-activity/')
    areas_list.value = r.data
  }

  async function getTypesProfActivity() {
    let r = await api.get('/api/activity/get-types-activity/')
    types_list.value = r.data
  }

  onAuthenticated(async () => {
    await getAreasProfActivity()
    await getTypesProfActivity()
    await getAdmissionDataForActivity()

  })


  return {
    admissionDataProfActivity,
    areas_list,
    types_list,
    currentItem,
    areaById,
    typeById,
    admissionDataById,

    getAdmissionDataForActivity,
  }

})


export default useProfActivityViewStore;
