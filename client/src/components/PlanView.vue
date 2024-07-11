<script setup lang="ts">

import {ref} from "vue";

const props = defineProps({
  data: {
    require: true,
  }
})

const columns = [
  {name: 'species', field: 'species', label: 'Направление', align: 'left'},
  {name: 'lastshifr', field: 'lastshifr', label: 'ОКСО', align: 'left'},
  {name: 'abbrprofile', field: 'abbrprofile', label: 'Аббревиатура', align: 'left'},
  {name: 'studyform', field: 'studyform', label: 'Форма обучения', align: 'left'},
  {name: 'studylevel', field: 'studylevel', label: 'Уровень подготовки', align: 'left'},
  {name: 'studyprog', field: 'studyprog', label: 'Программа', align: 'left'},
  {name: 'faculty', field: 'faculty', label: 'Факультет', align: 'left'},
  {name: 'kafcode', field: 'kafcode', label: 'Кафедра', align: 'left'},
  {name: 'startyear', field: 'startyear', label: 'Год начала подготовки', align: 'left'},
  {name: 'igahourzet', field: 'igahourzet', label: 'ЗЕТ в неделю', align: 'left'},
  {name: 'semesteroncource', field: 'semesteroncource', label: 'Семестров на курсе', align: 'left'},
  {name: 'gosdate', field: 'gosdate', label: 'Дата ФГОС', align: 'left'},
  {name: 'gosdocument', field: 'gosdocument', label: 'Номер ФГОС', align: 'left'},
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
    >

    </q-table>
  {{ props.data }}
</div>
</template>

<style scoped>

</style>
