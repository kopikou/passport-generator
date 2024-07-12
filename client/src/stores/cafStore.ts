import {defineStore} from "pinia";
import {onBeforeMount, ref} from "vue";
import {api} from "boot/axios";

const useCafStore = defineStore('CafStore', () => {
    const cafData = ref([])

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
    }
})

export default useCafStore;
