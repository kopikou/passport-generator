<script setup lang="ts">
import {computed, ref, watch} from "vue";
import {api} from "boot/axios";

const params = defineProps({
  rows: {
    required: true,
  },
  isAuthor: {
    required: true,
  },
});
const columns = [
  { name: 'name', align: 'center', label: 'Наименование', field: 'name', sortable: true },
  { name: 'hours_count', align: 'center', label: 'Часы', field: 'hours_count', sortable: true },
  { name: 'is_new', align: 'center', label: 'Впервые', field: 'is_new', sortable: true },
];

async function updateNewField(id: Number, is_new: Boolean) {
  const formData = new FormData();
  formData.append('is_new', is_new.toString());
  const r = await api.put(`/api/planwork/${id}/`, formData);
  params.rows.find(item => item.id === id).is_new = is_new;
  params.rows.find(item => item.id === id).hours_count = r.data.hours_count;
  params.rows.find(item => item.id === id).max_hours_count = r.data.max_hours_count;
}

async function updateHoursCount(id: Number, hours_count: Number) {
  hours_count = parseFloat(hours_count);
  const formData = new FormData();
  formData.append('hours_count', hours_count.toString());
  const r = await api.put(`/api/planwork/${id}/`, formData);
}
</script>

<template>
 <q-table
    :rows="params.rows"
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
            :readonly="!params.isAuthor"
            @update:model-value="updateHoursCount(props.row.id, props.row.hours_count)"
          />
        </q-td>

        <q-td key="is_new">
           <q-checkbox
             v-if="props.row.is_new !== null"
             v-model="props.row.is_new"
             @click="updateNewField(props.row.id, props.row.is_new)"
             :disable="!params.isAuthor"
           />
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<style scoped>

</style>
