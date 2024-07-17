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
  documentsData,
} = storeToRefs(planViewStore);

const disabled = ref(false)
const filter = ref('')

const columns = [
  {name: 'name', field: 'name', label: 'Наименование', align: 'center'},
  {name: 'type', field: 'type', label: 'Тип', align: 'center'},
  {name: 'synchronize', field: 'synchronize', label: 'Синхронизация с АИС', align: 'center'},
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
  <div style="width: 95%;">
    <q-table
      title="Информация о плане"
      :rows="documentsData"
      :columns="columns"
      row-key="id"
      :rows-per-page-options="[0]"
      wrap-cells
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
          <q-td key="name" :props>
            {{ props.row.name }}
          </q-td>

          <q-td key="type" :props>
            {{ props.row.type }}
          </q-td>

          <q-td key="synchronize" :props :class="props.row.synchronize ? 'bg-green-2' : 'bg-red-2'">
            {{ synctDataByValue[props.row.synchronize]?.label }}
            <q-popup-edit v-model="props.row.synchronize" v-slot="scope"
                          @update:modelValue="updateDocuments(props.row)">
              <q-select
                v-model="scope.value"
                emit-value
                map-options
                :options="sync_option"
                @popup-hide="scope.set"
                filled
                :readonly="disabled"
              >
              </q-select>
            </q-popup-edit>
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<style scoped>

</style>
