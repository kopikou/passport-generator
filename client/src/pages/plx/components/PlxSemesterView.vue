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
  linesDataById,
} = storeToRefs(planViewStore);

const filter = ref('')

const columns = [
  {name: 'planlineid_id', field: 'planlineid_id', label: 'Дисциплина', align: 'center'},
  {name: 'num', field: 'num', label: 'Семестр', align: 'center', sortable: true},
  {name: 'lekc', field: 'lekc', label: 'Лекции', align: 'center'},
  {name: 'lab', field: 'lab', label: 'Лабораторные', align: 'center'},
  {name: 'pr', field: 'pr', label: 'Практика', align: 'center'},
  {name: 'srs', field: 'srs', label: 'Самостоятельные', align: 'center'},
  {name: 'ekzhour', field: 'ekzhour', label: 'Экз. часы', align: 'center'},
  {name: 'zet', field: 'zet', label: 'ЗЕТ', align: 'center'},
  {name: 'view', field: 'view', label: 'Вид оценивания', align: 'center'},
  {name: 'kview', field: 'kview', label: 'Курсовые', align: 'center'},
  {name: 'khour', field: 'khour', label: 'Курсовые часы', align: 'center'},
  {name: 'eios', field: 'eios', label: 'ЭИОС', align: 'center'},
]

async function updateDocuments(values) {
  $q.loading.show()
  let r = await api.post("/api/upload/update-document-data/", values)
  $q.loading.hide()
}

const synctDataByValue = computed(() => {
  return _.keyBy(sync_option.value, 'value')
})

</script>

<template>
  <div>
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

      <template v-slot:body="props">
        <q-tr :props>
          <q-td key="planlineid_id" :props>
            {{ linesDataById[props.row.planlineid_id].dis }}
          </q-td>

          <q-td key="num" :props>
            {{ props.row.num }}
          </q-td>

          <q-td key="lekc" :props>
            {{ props.row.lekc }}
          </q-td>

          <q-td key="lab" :props>
            {{ props.row.lab }}
          </q-td>

          <q-td key="pr" :props>
            {{ props.row.pr }}
          </q-td>

          <q-td key="srs" :props>
            {{ props.row.srs }}
          </q-td>

          <q-td key="ekzhour" :props>
            {{ props.row.ekzhour }}
          </q-td>

          <q-td key="zet" :props>
            {{ props.row.zet }}
          </q-td>

          <q-td key="view" :props>
            <span v-if="props.row.zach">Зачет</span>
            <span v-else-if="props.row.ekz">Экзамен</span>
            <span v-else-if="props.row.zacho">Зачет с оценкой</span>
          </q-td>

          <q-td key="kview" :props>
            <span v-if="props.row.kp">Проект</span>
            <span v-if="props.row.kr"><br/>Работа</span>
          </q-td>

          <q-td key="khour" :props>
            <span v-if="props.row.kp_hour">{{ props.row.kp_hour }}</span>
            <span v-if="props.row.kr_hour"><br/>{{ props.row.kr_hour }}</span>
          </q-td>

          <q-td key="eios" :props>
            {{ props.row.eios }}
          </q-td>
        </q-tr>
      </template>


    </q-table>
  </div>
</template>

<style scoped>

</style>
