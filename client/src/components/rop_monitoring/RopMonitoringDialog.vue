<script setup lang="ts">
import {ref} from "vue";
import {RopMonitoring} from "src/types";
import {storeToRefs} from "pinia";
import useRopMonitoringStore from "stores/ropMonitoringStore";

const ropMonitoringStore = useRopMonitoringStore();
const {
  ropMonitorings,
} = storeToRefs(ropMonitoringStore);

const selectedRopMonitoring = ref<RopMonitoring | Number>();
const ropMonitoringData = ref<RopMonitoring>({});
const emit = defineEmits(['dialogClosed']);

function closeDialog() {
  emit('dialogClosed');
}

</script>

<template>
  <q-card>
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
      <q-input outlined label="Название" v-model="ropMonitoringData.name"/>
      <div style="display: flex; flex-direction: row; gap: 8px">
        <q-btn
          icon="mdi-plus-thick"
          color="green-7"
          label="Создать"
          @click=""
          v-if="!ropMonitoringData.id"
        />
        <q-btn
          icon="mdi-pencil"
          color="blue-7"
          label="Обновить"
          @click=""
          v-if="ropMonitoringData.id"
        />
        <q-btn
          icon="mdi-delete-empty"
          color="pink-7"
          label="Удалить"
          @click=""
          :disable="!selectedRopMonitoring"
        />
      </div>
    </div>
  </q-card>
</template>

<style scoped>

</style>
