<script setup lang="ts">

import {storeToRefs} from "pinia";
import {api} from "boot/axios";
import {computed, ref} from "vue";
import _ from "lodash";
import {useQuasar} from "quasar";
import usePlanViewStore from "stores/planViewStore";

const $q = useQuasar()

const props = defineProps({
  data: {
    require: true,
  }
});

const planViewStore = usePlanViewStore()
const {
  cafData,
  sync_option,
} = storeToRefs(planViewStore);

const disabled = ref(false)
const filter = ref('')

const columns = [
  {name: 'dis', field: 'dis', label: 'Дисциплина', align: 'center'},
  {name: 'newdisid', field: 'newdisid', label: 'Код', align: 'center'},
  {name: 'mustbesdudied', field: 'mustbesdudied', label: 'Изучению часов', align: 'center'},
  {name: 'hoursinzet', field: 'hoursinzet', label: 'Часов в ЗЕТ', align: 'center'},
  {name: 'caf', field: 'caf', label: 'Кафедра', align: 'center'},
  {name: 'kompetences', field: 'kompetences', label: 'Компетенции', align: 'center'},
  {name: 'synchronize', field: 'synchronize', label: 'Синхронизация с АИС', align: 'center'},
]

async function updateLines(values) {
  $q.loading.show()
  let r = await api.post("api/upload/update-lines-data/", values)
  $q.loading.hide()
}

const synctDataByValue = computed(() => {
  return _.keyBy(sync_option.value, 'value')
})


const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

</script>

<template>
  <div>
    <q-table
      title="Информация о дисциплинах плана"
      :rows="props.data"
      :columns="columns"
      row-key="id"
      :rows-per-page-options="[0]"
      wrap-cells
      :filter="filter"
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
          <q-td key="dis" :props>
            {{ props.row.dis }}
          </q-td>

          <q-td key="newdisid" :props>
            {{ props.row.newdisid }}
          </q-td>

          <q-td key="mustbesdudied" :props>
            {{ props.row.mustbesdudied }}
          </q-td>

          <q-td key="hoursinzet" :props>
            {{ props.row.hoursinzet }}
          </q-td>

          <q-td key="caf" :props class="bg-grey-4">
            {{ cafDataById[props.row.caf]?.label }}
            <q-popup-edit v-model="props.row.caf" v-slot="scope" @update:modelValue="updateLines(props.row)">
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

          <q-td key="kompetences" :props>
            {{ props.row.kompetences }}
          </q-td>

          <q-td key="synchronize" :props class="bg-grey-4">
            {{ synctDataByValue[props.row.synchronize]?.label }}
            <q-popup-edit v-model="props.row.synchronize" v-slot="scope" @update:modelValue="updateLines(props.row)">
              <q-select
                v-model="scope.value"
                emit-value
                map-options
                :options="sync_option"
                @popup-hide="scope.set"
                filled
                behavior="dialog"
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
