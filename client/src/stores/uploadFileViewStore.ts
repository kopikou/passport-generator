import {defineStore} from "pinia";
import {onAuthenticated} from "src/composables/onAuthenticated";
import {computed, ref} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import _ from "lodash";

const useUploadFileViewStore = defineStore('UploadFileViewStore', () => {

  const $q = useQuasar()

  const admissionData = ref([])

  async function getAdmissionData() {
    $q.loading.show({message: "Загрузка данных о планах"})
    let r = await api.get('api/upload/get-admission-data/')
    admissionData.value = r.data
    $q.loading.hide()
  }


  onAuthenticated(() => {
    getAdmissionData()
  })

  return {
    admissionData,
  }
})

export default useUploadFileViewStore
