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
  { name: 'formcntr', align: 'center', label: 'Вид работ', field: 'formcntr', sortable: true },
  { name: 'hours_count', align: 'center', label: 'Часы', field: 'hours_count', sortable: true },
];

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
      <q-tr :props="props" class="q-virtual-scroll--with-prev">
        <q-td colspan="100%">
          <span>{{ props.row.discpl }}</span>
          <span> ({{ props.row.items.reduce((acc, val) => acc + val.hours_count, 0).toFixed(2) }} часов)</span>
          <q-btn dense @click="props.row.expand = !props.row.expand" :icon="props.row.expand ? 'mdi-chevron-up' : 'mdi-chevron-down'" />
        </q-td>
      </q-tr>

      <q-tr :props="props" v-for="item in props.row.items" v-show="props.row.expand">
        <q-td key="sem">
          {{ item.sem }} ({{ item.kurs }} курс)
        </q-td>

        <q-td key="grup">
          {{ item.grup }}
        </q-td>

        <q-td key="formcntr">
          {{ item.formcntr }}
        </q-td>

        <q-td key="hours_count">
          {{ item.hours_count }}
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<style scoped>

</style>
