<script setup lang="ts">

import {useQuasar} from "quasar";
import usePlanViewStore from "stores/planViewStore";
import {storeToRefs} from "pinia";
import {computed, ref} from "vue";
import {api} from "boot/axios";
import _ from "lodash";

const $q = useQuasar()

const planViewStore = usePlanViewStore()
const {
  cafData,
  sync_option,
  semesterData,
} = storeToRefs(planViewStore);

const disabled = ref(false)
const filter = ref('')

const columns = [
  {name: 'dis', field: 'dis', label: 'Дисциплина', align: 'center'},
  {name: 'num', field: 'num', label: 'Семестр', align: 'center'},
  {name: 'lekc', field: 'lekc', label: 'Лекции', align: 'center'},
  {name: 'lab', field: 'lab', label: 'Лабораторные', align: 'center'},
  {name: 'pr', field: 'pr', label: 'Практика', align: 'center'},
  {name: 'srs', field: 'srs', label: 'Самостоятельные', align: 'center'},
  {name: 'ekzhour', field: 'ekzhour', label: 'Экз. часы', align: 'center'},
  {name: 'zet', field: 'zet', label: 'ЗЕТ', align: 'center'},
  {name: 'ekz', field: 'ekz', label: 'Экзамен', align: 'center'},
  {name: 'zach', field: 'zach', label: 'Зачет', align: 'center'},
  {name: 'zacho', field: 'zacho', label: 'Зачет с оценкой', align: 'center'},
  {name: 'kp', field: 'kp', label: 'Курсовые проекты', align: 'center'},
  {name: 'kp_hour', field: 'kp_hour', label: 'Часы', align: 'center'},
  {name: 'kr', field: 'kr', label: 'Курсовая работа', align: 'center'},
  {name: 'kr_hour', field: 'kr_hour', label: 'Часы', align: 'center'},
  {name: 'eios', field: 'eios', label: 'хз', align: 'center'},
]

async function updateDocuments(values) {
  $q.loading.show()
  let r = await api.post("api/upload/update-document-data/", values)
  $q.loading.hide()
}

const synctDataByValue = computed(() => {
  return _.keyBy(sync_option.value, 'value')
})

</script>

<template>
  {{ semesterData }}
  <div style="width: 95%;">
    <q-table
      title="Информация о семестрах"
      :rows="semesterData"
      :columns="columns"
      row-key="id"
      :rows-per-page-options="[0]"
      wrap-cells
      hide-bottom
    >
      <template v-slot:top-right>
        <q-input outlined dense debounce="300" v-model="filter" placeholder="Поиск" class="bg-grey-2">
          <template v-slot:append>
            <q-icon name="search"/>
          </template>
        </q-input>
      </template>


    </q-table>
  </div>
</template>

<style scoped>

</style>
