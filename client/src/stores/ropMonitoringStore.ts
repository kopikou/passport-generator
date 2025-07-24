import {defineStore} from "pinia";
import {ref} from "vue";
import {RopMonitoring} from "src/types";
import api from "axios";

const useRopMonitoringStore = defineStore("RopMonitoringStore", () => {
  const ropMonitorings = ref<RopMonitoring[] | number[]>([]);
  const loadingRopMonitorings = ref(false);

  async function getRopMonitorings() {
    loadingRopMonitorings.value = true;
    ropMonitorings.value = [];
    let r = await api.get('api/rop-monitoring/');
    ropMonitorings.value = r.data;
    loadingRopMonitorings.value = false;
  }

  return {
    ropMonitorings,
    getRopMonitorings,
  }
});

export default useRopMonitoringStore;
