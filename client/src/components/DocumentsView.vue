<script setup lang="ts">

import {useQuasar} from "quasar";
import usePlanViewStore from "stores/planViewStore";
import addDocumentDialog from "components/AddDocumentDialog.vue";
import {storeToRefs} from "pinia";
import {computed, onBeforeMount, ref} from "vue";
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

function addRow() {
  let freeId = _.findLastIndex(documentsData.value) + 1
  _.set(documentsData.value, `${freeId}`, {name: 'test', type: 1, synchronize: false, added: true, key: freeId})

  $q.dialog({
    component: addDocumentDialog,
    componentProps: {
      id: freeId,
    }
  }).onOk(() => {
    console.log("ok")
  })

}

function removeRow(id) {
  _.unset(documentsData.value, `${id}`)
}

function saveRow(values) {
  console.log(values)
}

const synctDataByValue = computed(() => {
  return _.keyBy(sync_option.value, 'value')
})

</script>

<template>
  <div style="width: 95%;">
    <div class="q-pb-md">
      <q-btn @click="addRow" color="primary" label="Добавить документ"/>
    </div>

    <q-table
      title="Информация о документах"
      :rows="documentsData"
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
          <q-td key="name" :props>
            <span v-if="props.row.added">
              <q-btn icon="mdi-check" @click="saveRow(props.row)" flat color="green" />
              <q-btn icon="mdi-delete" @click="removeRow(props.row.key)" flat color="red"/>
            </span>
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
