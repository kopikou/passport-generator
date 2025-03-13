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
  indicatorsData,
  linesDataById,
} = storeToRefs(planViewStore);

const filter = ref('')

const columns = [
  {name: 'planlineid_id', field: 'planlineid_id', label: 'Дисциплина', align: 'center'},
  {name: 'competence', field: 'competence', label: 'Наименование компетенции', align: 'center'},
  {name: 'competence_index', field: 'competence_index', label: 'Индекс компетенции', align: 'center'},
  {name: 'indicator', field: 'indicator', label: 'Наименование индикатора', align: 'center'},
  {name: 'indicator_index', field: 'indicator_index', label: 'Индекс индикатора', align: 'center'},
]

async function updateDocuments(values) {
  $q.loading.show()
  let r = await api.post("api/plx/update-document-data/", values)
  $q.loading.hide()
}

const synctDataByValue = computed(() => {
  return _.keyBy(sync_option.value, 'value')
})

</script>

<template>
    <q-table
      title="Информация о индикаторах"
      :rows="indicatorsData"
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

          <q-td key="competence" :props>
            {{ props.row.competence }}
          </q-td>

          <q-td key="competence_index" :props>
            {{ props.row.competence_index }}
          </q-td>

          <q-td key="indicator" :props>
            {{ props.row.indicator }}
          </q-td>

          <q-td key="indicator_index" :props>
            {{ props.row.indicator_index }}
          </q-td>
        </q-tr>
      </template>
    </q-table>
</template>

<style scoped>

</style>
