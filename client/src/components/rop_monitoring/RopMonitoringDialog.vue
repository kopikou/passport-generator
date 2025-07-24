<script setup lang="ts">
import {ref} from "vue";
import {RopMonitoring} from "src/types";
import {storeToRefs} from "pinia";
import useRopMonitoringStore from "stores/ropMonitoringStore";
import useRulesStore from "stores/rulesStore";
import api from "axios";
import {useQuasar} from "quasar";

const $q = useQuasar()
const formRef = ref(null)

const selectedRopMonitoring = ref<RopMonitoring | Number>();
const ropMonitoringData = ref<RopMonitoring>({});
const emit = defineEmits(['dialogClosed']);

function closeDialog() {
  emit('dialogClosed');
}

const rulesStore = useRulesStore();
const ropMonitoringStore = useRopMonitoringStore();
const {
  ropMonitorings,
} = storeToRefs(ropMonitoringStore);

async function validateForm() {
  return formRef.value.validate()
}

async function createRopMonitoring() {
  const valid = await validateForm()
  if (!valid) return

  let r = await api.post('api/rop-monitoring/', ropMonitoringData.value);
  if (r.status == 201) {
    selectedRopMonitoring.value = 0;
    $q.notify({
      message: `Мониторинг "${ropMonitoringData.value?.name}" создан!`,
      color: "secondary",
      position: "bottom-right",
      html: true,
    })

    closeDialog();
  }
}

async function deleteRopMonitoring() {
  $q.dialog({
    title: "Удалить мониторинг",
    message: `Вы уверены что хотите удалить мониторинг "${ropMonitoringData.value?.name}"?`,
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
        message: `Мониторинг "${ropMonitoringData.value?.name}" удалён!`,
        color: "secondary",
        position: "bottom-right",
        html: true,
      })
      await ropMonitoringStore.getRopMonitorings();
      closeDialog();
    }
  })
}

async function updateRopMonitoring() {
  const valid = await validateForm()
  if (!valid) return

  let r = await api.patch(`api/rop-monitoring/${selectedRopMonitoring.value}/`, ropMonitoringData.value);
  if (r.status == 200) {
    selectedRopMonitoring.value = 0;
    $q.notify({
      message: `Мониторинг "${ropMonitoringData.value?.name}" обновлён!`,
      color: "secondary",
      position: "bottom-right",
      html: true,
    })
    await ropMonitoringStore.getRopMonitorings();
    closeDialog();
  }
}

</script>

<template>
  <q-card ref="formRef" @submit.prevent>
    <q-card-section style="display: flex; flex-direction: row; justify-content: end; padding: 0">
      <q-btn icon="close" flat round @click="closeDialog"/>
    </q-card-section>
    <div style="display: grid; grid-template-rows: 1fr 1fr auto; overflow: hidden; gap:8px; padding: 8px 16px 16px;">
      <q-select
        label="Мониторинги"
        emit-value
        map-options
        clearable
        outlined
        :options="ropMonitorings"
        v-model="selectedRopMonitoring"
      />
      <q-input outlined label="Название" v-model="ropMonitoringData.name"
               lazy-rules :rules="[rulesStore.required()]"/>
      <div style="display: flex; flex-direction: row; gap: 8px">
        <q-btn
          icon="mdi-plus-thick"
          color="green-7"
          label="Создать"
          @click="createRopMonitoring"
          v-if="!ropMonitoringData.id"
        />
        <q-btn
          icon="mdi-pencil"
          color="blue-7"
          label="Обновить"
          @click="updateRopMonitoring"
          v-if="ropMonitoringData.id"
        />
        <q-btn
          icon="mdi-delete-empty"
          color="pink-7"
          label="Удалить"
          @click="deleteRopMonitoring"
          :disable="!selectedRopMonitoring"
        />
      </div>
    </div>
  </q-card>
</template>

<style scoped>

</style>
