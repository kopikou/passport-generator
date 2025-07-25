<script setup lang="ts">
import {ref} from "vue";
import {RopMonitoring} from "src/types";
import {storeToRefs} from "pinia";
import useRopMonitoringStore from "stores/ropMonitoringStore";
import useRulesStore from "stores/rulesStore";
import {useQuasar} from "quasar";
import {api} from "boot/axios";

const $q = useQuasar()
const formRef = ref(null)

const selectedRopMonitoring = ref<RopMonitoring | Number>();
const selectedRopMonitoringData = ref<RopMonitoring>({});

const rulesStore = useRulesStore();
const ropMonitoringStore = useRopMonitoringStore();
const {
  ropMonitoringList,
} = storeToRefs(ropMonitoringStore);

async function validateForm() {
  return formRef.value.validate()
}

async function createRopMonitoring() {
  const valid = await validateForm()
  if (!valid) return

  let r = await api.post('api/rop-monitoring/', selectedRopMonitoringData.value);
  if (r.status == 201) {
    selectedRopMonitoring.value = 0;
    $q.notify({
      message: `Мониторинг "${selectedRopMonitoringData.value?.name}" создан!`,
      color: "secondary",
      position: "bottom-right",
      html: true,
    })
  }
}

async function deleteRopMonitoring() {
  $q.dialog({
    title: "Удалить мониторинг",
    message: `Вы уверены что хотите удалить мониторинг "${selectedRopMonitoringData.value?.name}"?`,
    cancel: {
      label: 'Отмена',
      flat: true,
      color: 'negative',
    },
    ok: {
      label: "Да",
      flat: true
    },
  }).onOk(async () => {
    let r = await api.delete(`api/rop-monitoring/${selectedRopMonitoring.value}/`);
    if (r.status == 200) {
      selectedRopMonitoring.value = 0;
      $q.notify({
        message: `Мониторинг "${selectedRopMonitoringData.value?.name}" удалён!`,
        color: "secondary",
        position: "bottom-right",
        html: true,
      })
      await ropMonitoringStore.getRopMonitoringList();
    }
  })
}

async function updateRopMonitoring() {
  const valid = await validateForm()
  if (!valid) return

  let r = await api.patch(`api/rop-monitoring/${selectedRopMonitoring.value}/`, selectedRopMonitoringData.value);
  if (r.status == 200) {
    selectedRopMonitoring.value = 0;
    $q.notify({
      message: `Мониторинг "${selectedRopMonitoringData.value?.name}" обновлён!`,
      color: "secondary",
      position: "bottom-right",
      html: true,
    })
    await ropMonitoringStore.getRopMonitoringList();
  }
}

</script>

<template>
  <q-form
    @submit.prevent ref="formRef"
    style="display: grid; grid-template-rows: auto auto; padding: 8px;">
    <div style="display: flex; justify-content: center;">
      <q-input
        outlined
        label="Название"
        v-model="selectedRopMonitoringData.name"
        lazy-rules
        :rules="[rulesStore.required()]"
        style="max-width: 300px; width: 100%;"
      />
    </div>
    <div style="display: flex; justify-content: center; gap: 8px;">
      <q-btn
        icon="mdi-plus-thick"
        color="green-7"
        label="Создать"
        type="submit"
        @click="createRopMonitoring"
        v-if="!selectedRopMonitoringData.id"
      />
      <q-btn
        icon="mdi-pencil"
        color="blue-7"
        label="Обновить"
        type="submit"
        @click="updateRopMonitoring"
        v-if="selectedRopMonitoringData.id"
      />
      <q-btn
        icon="mdi-delete-empty"
        color="pink-7"
        label="Удалить"
        @click="deleteRopMonitoring"
        :disable="!selectedRopMonitoring"
        type="reset"
      />
    </div>
  </q-form>
</template>


<style scoped>

</style>
