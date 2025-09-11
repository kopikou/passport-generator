import {defineStore} from "pinia";
import {ref} from "vue";
import {RopMonitoring} from "src/types";
import {api} from "boot/axios";

const useRopMonitoringStore = defineStore("RopMonitoringStore", () => {
  const ropMonitoringList = ref<RopMonitoring[] | number[]>([]);
  const loadingRopMonitoringList = ref(false);

  async function getRopMonitoringList() {
    loadingRopMonitoringList.value = true;
    ropMonitoringList.value = [];
    let r = await api.get('api/rop-monitoring/');
    ropMonitoringList.value = r.data;
    loadingRopMonitoringList.value = false;
  }

  return {
    ropMonitoringList,
    loadingRopMonitoringList,
    getRopMonitoringList,
  }
});

export default useRopMonitoringStore;
