<script setup lang="ts">

import {ref} from "vue";

const props = defineProps({
  data: {
    require: true,
  }
})

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

</script>

<template>
<div style="width: 90%">
    <q-table
      title="Информация о плане"
      :rows="props.data"
      :columns="columns"
      row-key="id"
      rows-per-page-options="0"
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

          <q-td key="kafcode" :props>
            {{ props.row.kafcode }}
            <q-popup-edit v-model="kafcode" v-slot="scope">
              <q-select>

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
  {{ props.data }}
</div>
</template>

<style scoped>

</style>
