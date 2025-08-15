<script setup lang="ts">
import {computed, ref, watch} from "vue";

const props = defineProps({
  rows: {
    required: true,
  },
});

const columns = [
  { name: 'sem', align: 'center', label: 'Семестр', field: 'sem', sortable: true },
  { name: 'grup', align: 'center', label: 'Группа', field: 'grup', sortable: true },
  { name: 'discpl', align: 'center', label: 'Дисциплина', field: 'discpl', sortable: true },
  { name: 'hours_count', align: 'center', label: 'Часы', field: 'hours_count', sortable: true },
  { name: 'is_new', align: 'center', label: 'Впервые', field: 'is_new', sortable: true },
];

const discpl_names = {
  'new_labs_and_practices': 'Подготовка к новым для преподавателя лабораторным, практическим, семинарским занятиям',
  'old_labs_and_practices': 'Подготовка к ранее проводимым преподавателем лабораторным, практическим, семинарским занятиям',
  'check_labs': 'Проверка отчетов по лабораторным работам',
  'new_lectures': 'Подготовка нового лекционного курса',
  'old_lectures': 'Подготовка к лекциям по ранее читаемой дисциплине',
};

</script>

<template>
 <q-table
    :rows="props.rows"
    :columns="columns"
    virtual-scroll
    style="overflow-y: auto; height: 100%;"
    wrap-cells
    flat
    bordered
    separator="cell"
    :rows-per-page-options="[0]"
    table-header-class="table-header"
  >
    <template v-slot:body="props">
      <q-tr :props="props" v-if="props.row.items.labs_and_practices > 0">
        <q-td key="sem">
          {{ props.row.sem }} ({{ props.row.kurs }} курс)
        </q-td>

        <q-td key="grup">
          {{ props.row.grup }}
        </q-td>

        <q-td key="discpl">
          {{props.row.discpl}}: {{discpl_names.old_labs_and_practices}}
        </q-td>

        <q-td key="hours_count">
          <q-input
            v-model="props.row.items.labs_and_practices"
            input-class="text-right"
            type="number"
            dense
            borderless
          />
        </q-td>

        <q-td key="is_new">
          1
        </q-td>
      </q-tr>

      <q-tr :props="props" v-if="props.row.items.lectures > 0">
        <q-td key="sem">
          {{ props.row.sem }} ({{ props.row.kurs }} курс)
        </q-td>

        <q-td key="grup">
          {{ props.row.grup }}
        </q-td>

        <q-td key="discpl">
          {{props.row.discpl}}: {{discpl_names.old_lectures}}
        </q-td>

        <q-td key="hours_count">
          <q-input
            v-model="props.row.items.lectures"
            input-class="text-right"
            type="number"
            dense
            borderless
          />
        </q-td>

        <q-td key="is_new">
          1
        </q-td>
      </q-tr>

      <q-tr :props="props" v-if="props.row.items.labs > 0">
         <q-td key="sem">
          {{ props.row.sem }} ({{ props.row.kurs }} курс)
        </q-td>

        <q-td key="grup">
          {{ props.row.grup }}
        </q-td>

        <q-td key="discpl">
          {{props.row.discpl}}: {{discpl_names.check_labs}}
        </q-td>

        <q-td key="hours_count">
          <q-input
            v-model="props.row.items.labs"
            input-class="text-right"
            type="number"
            dense
            borderless
          />
        </q-td>

        <q-td key="is_new">
          1
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<style scoped>

</style>
