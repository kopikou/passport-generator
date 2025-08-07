<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {LocalStorage, SessionStorage, useQuasar} from "quasar";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";

const planType = ref('myPlans')
const typeOptions = [
  {
    label: 'Мои планы',
    value: 'myPlans',
  },
  {
    label: 'Все планы',
    value: 'allPlans',
  },
]

const planCategory = ref('currentPlans')
const categoryOptions = [
  {
    label: 'Текущие',
    value: 'currentPlans',
  },
  {
    label: 'Архив',
    value: 'oldPlans',
  },
]

</script>

<template>
  <div style="display: grid; grid-template-columns: auto auto; gap: 8px">
    <q-select
      v-model="planType"
      :options="typeOptions"
      label="Тип планов"
      emit-value
      map-options
    />

    <q-select
      v-model="planCategory"
      :options="categoryOptions"
      label="Категория планов"
      emit-value
      map-options
    />
  </div>

  <q-table
    rows=""
  >

  </q-table>


</template>

<style scoped>

</style>
