import {defineStore} from "pinia";
import {onAuthenticated} from "src/composables/onAuthenticated";
import {computed, ref} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import _ from "lodash";
import {PlanData} from "src/types";

const useUploadFileViewStore = defineStore('UploadFileViewStore', () => {

  const $q = useQuasar()

  const admissionData = ref<PlanData[]>([])
  const baseDocuments = ref([])

  async function getAdmissionData() {
    let r = await api.get('/api/upload/get-admission-data/')
    admissionData.value = r.data
  }

  async function getBaseDocuments() {
    let r = await api.get('/api/upload/get-base-documents/')
    baseDocuments.value = r.data
  }


  onAuthenticated(async () => {
    $q.loading.show({message: "Загрузка данных"})
    await getBaseDocuments()
    await getAdmissionData()
    $q.loading.hide()

  })

  return {
    admissionData,
    baseDocuments,
  }
})

export default useUploadFileViewStore
