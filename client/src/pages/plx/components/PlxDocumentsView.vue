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
  docTypes,
  disabled,
} = storeToRefs(planViewStore);

const filter = ref('')

const columns = [
  {name: 'name', field: 'name', label: 'Наименование', align: 'center'},
  {name: 'new_type_id', field: 'new_type_id', label: 'Тип', align: 'center'},
  // {name: 'synchronize', field: 'synchronize', label: 'Синхронизация с АИС', align: 'center'},
]

async function updateDocuments(values) {
  $q.loading.show()
  let r = await api.post("api/plx/update-document-data/", values)
  $q.loading.hide()
}

function addRow() {
  $q.dialog({
    component: addDocumentDialog,
  })
}

function removeRow(id) {
  _.unset(documentsData.value, `${id}`)
}

const synctDataByValue = computed(() => {
  return _.keyBy(sync_option.value, 'value')
})

const docNameByBalue = computed(() => {
  return _.keyBy(docTypes.value, 'id')
})

</script>

<template>
  <div>

    <q-table
      title="Информация о документах"
      :rows="documentsData"
      :columns="columns"
      row-key="id"
      :rows-per-page-options="[0]"
      wrap-cells
      hide-bottom
    >
      <template #top-left>
        <q-btn @click="addRow" color="primary" label="Добавить документ" :disable="disabled"/>
      </template>

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
              <q-btn icon="mdi-check" @click="updateDocuments(props.row)" flat color="green" />
              <q-btn icon="mdi-delete" @click="removeRow(props.row.key)" flat color="red"/>
            </span>
            {{ props.row.name }}
          </q-td>

          <q-td key="new_type_id" :props>
            {{ docNameByBalue[props.row.new_type_id]?.name }}
          </q-td>

<!--          <q-td key="synchronize" :props :class="props.row.synchronize ? 'bg-green-2' : 'bg-red-2'">-->
<!--            {{ synctDataByValue[props.row.synchronize]?.label }}-->
<!--            <q-popup-edit v-model="props.row.synchronize" v-slot="scope"-->
<!--                          @update:modelValue="updateDocuments(props.row)">-->
<!--              <q-select-->
<!--                v-model="scope.value"-->
<!--                emit-value-->
<!--                map-options-->
<!--                :options="sync_option"-->
<!--                @popup-hide="scope.set"-->
<!--                filled-->
<!--                :readonly="disabled"-->
<!--              >-->
<!--              </q-select>-->
<!--            </q-popup-edit>-->
<!--          </q-td>-->
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<style scoped>

</style>
