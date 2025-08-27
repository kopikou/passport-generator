<script setup lang="ts">
import {computed, ref, watch} from "vue";

const props = defineProps({
  rows: {
    required: true,
  },
});

const columns = [
  { name: 'name', align: 'center', label: 'Наименование', field: 'name', sortable: true },
  { name: 'hours_count', align: 'center', label: 'Часы', field: 'hours_count', sortable: true },
  { name: 'is_new', align: 'center', label: 'Впервые', field: 'is_new', sortable: true },
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
      <q-tr :props="props">

        <q-td key="name">
          {{props.row.name}}
        </q-td>

        <q-td key="hours_count">
          <q-input
            v-model="props.row.hours_count"
            input-class="text-right"
            type="number"
            :max="props.row.max_hours_count"
            dense
            borderless
          />
        </q-td>

        <q-td key="is_new">
           <q-checkbox v-model="props.row.is_new" />
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<style scoped>

</style>
