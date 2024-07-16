import {defineStore} from "pinia";
import {onBeforeMount, ref} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";


const usePlanViewStore = defineStore('PlanViewStore', () => {
    const cafData = ref([])
    const sync_option = ref([
      {value: true, label: 'Да'},
      {value: false, label: 'Нет'},
    ])

    async function getData() {
        let r = await api.get("api/upload/get-caf-codes/")
        let data = r.data

        cafData.value = data.items
    }

    onBeforeMount(async () => {
        await getData()
    })

    return {
      cafData,
      sync_option,
    }
})

export default usePlanViewStore;
