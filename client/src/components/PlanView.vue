<script setup lang="ts">

import {computed, onBeforeMount, onBeforeUnmount, onBeforeUpdate, onMounted, onUnmounted, ref} from "vue";
import {useQuasar} from "quasar";
import _ from "lodash";
import {api} from "boot/axios";

const $q = useQuasar()

const props = defineProps({
  data: {
    require: true,
  },
})

const cafData = ref([])

const columns = [
  {name: 'species', field: 'species', label: 'Направление', align: 'center'},
  {name: 'lastshifr', field: 'lastshifr', label: 'ОКСО', align: 'cnter'},
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
  let r = await api.post("api/upload/update-plan-data/", values)
  console.log(r.data)
  $q.loading.hide()
}

async function getCafData() {
  let r = await api.get("api/upload/get-caf-codes/")
  cafData.value = r.data.items
}

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

onBeforeMount(async () => {
  await getCafData()
})

</script>

<template>
<div style="width: 90%">
    <q-table
      title="Информация о плане"
      :rows="props.data"
      :columns="columns"
      row-key="id"
      :rows-per-page-options="[0]"
      wrap-cells
    >

      <template v-slot:body="props">
        <q-tr :props>
          <q-td key="species" :props>
            {{ props.row.species }}
          </q-td>

          <q-td key="lastshifr" :props>
            {{ props.row.lastshifr }}
          </q-td>

          <q-td key="abbrprofile" :props>
            {{ props.row.abbrprofile }}
          </q-td>

          <q-td key="studyform" :props>
            {{ props.row.studyform }}
          </q-td>

          <q-td key="studylevel" :props>
            {{ props.row.studylevel }}
          </q-td>

          <q-td key="studyprog" :props>
            {{ props.row.studyprog }}
          </q-td>

          <q-td key="faculty" :props>
            {{ props.row.faculty }}
          </q-td>

          <q-td key="kafcode" :props="props" class="bg-grey-4">
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
              >
              </q-select>
            </q-popup-edit>
          </q-td>

          <q-td key="startyear" :props>
            {{ props.row.startyear }}
          </q-td>

          <q-td key="igahourzet" :props>
            {{ props.row.igahourzet }}
          </q-td>

          <q-td key="semesteroncource" :props>
            {{ props.row.semesteroncource }}
          </q-td>
        </q-tr>

      </template>

    </q-table>
</div>
</template>

<style scoped>

</style>
