<script setup lang="ts">

import {computed, onBeforeMount, onBeforeUnmount, onBeforeUpdate, onMounted, onUnmounted, ref} from "vue";
import {useQuasar} from "quasar";
import _ from "lodash";
import {api} from "boot/axios";
import {storeToRefs} from "pinia";
import usePlanViewStore from "stores/planViewStore";

const $q = useQuasar()

const planViewStore = usePlanViewStore()
const {
  cafData,
  sync_option,
  planData,
  disabled,
} = storeToRefs(planViewStore);


const columns = [
  {name: 'species', field: 'species', label: 'Направление', align: 'center'},
  {name: 'lastshifr', field: 'lastshifr', label: 'ОКСО', align: 'center'},
  {name: 'abbrprofile', field: 'abbrprofile', label: 'Аббревиатура', align: 'center'},
  {name: 'studyform', field: 'studyform', label: 'Форма обучения', align: 'center'},
  {name: 'studylevel', field: 'studylevel', label: 'Уровень подготовки', align: 'center'},
  {name: 'studyprog', field: 'studyprog', label: 'Программа', align: 'center'},
  {name: 'faculty', field: 'faculty', label: 'Факультет', align: 'center'},
  {name: 'kafcode', field: 'kafcode', label: 'Кафедра', align: 'center'},
  {name: 'startyear', field: 'startyear', label: 'Год начала подготовки', align: 'center'},
  {name: 'igahourzet', field: 'igahourzet', label: 'ЗЕТ в неделю', align: 'center'},
  {name: 'semesteroncource', field: 'semesteroncource', label: 'Семестров на курсе', align: 'center'},
]

async function updatePlan(values) {
  $q.loading.show()
  let r = await api.post("/api/upload/update-plan-data/", values)
  $q.loading.hide()
}

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

</script>

<template>
  <div style="width: 95%">
    <q-table
      title="Информация о плане"
      :rows="planData"
      :columns="columns"
      row-key="id"
      :rows-per-page-options="[0]"
      wrap-cells
      hide-bottom
    >

      <template v-slot:body-cell-abbrprofile="props">
          <q-td key="abbrprofile" :props :class="props.row.abbrprofile ? 'bg-green-2' : 'bg-red-2'">
            {{ props.row.abbrprofile }}
            <q-popup-edit v-model="props.row.abbrprofile" v-slot="scope" @update:modelValue="updatePlan(props.row)">
              <q-input
                v-model="scope.value"
                @focusout="scope.set"
                filled
                :readonly="disabled"
              >
              </q-input>
            </q-popup-edit>
          </q-td>
      </template>
      <template v-slot:body-cell-kafcode="props">
          <q-td key="kafcode" :props="props" :class="props.row.kafcode ? 'bg-green-2' : 'bg-red-2'">
            {{ cafDataById[props.row.kafcode]?.label }}
            <q-popup-edit v-model="props.row.kafcode" v-slot="scope" @update:modelValue="updatePlan(props.row)">
              <q-select
                v-model="scope.value"
                emit-value
                map-options
                :options="cafData"
                @popup-hide="scope.set"
                filled
                behavior="dialog"
                :readonly="disabled"
              >
              </q-select>
            </q-popup-edit>
          </q-td>
      </template>

    </q-table>
  </div>
</template>

<style scoped>

</style>
