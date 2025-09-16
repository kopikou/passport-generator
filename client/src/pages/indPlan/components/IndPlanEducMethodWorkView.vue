<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import _ from "lodash";

const params = defineProps({
  rows: {
    required: true,
  },
  plan_id: {
    required: true,
  },
  canEdit: {
    required: true,
  },
  works: {
    required: true
  }
});

const columns = [
  { name: 'name', align: 'center', label: 'Наименование', field: 'name', sortable: true },
  { name: 'hours_count', align: 'center', label: 'Количество часов', field: 'hours_count', sortable: true },
  { name: 'control', align: 'center', label: 'Действия', field: 'control', sortable: true,  },
];

const workToAdd = ref(null);

const rowsNamesList = computed(() => {
  return _(params.rows)
    .map((row) =>{
    return row.name;
  })
    .values();
})

const worksList = computed(() =>{
    return _(params.works)
      .filter(x => {
        return !(rowsNamesList.value.includes(x.name));
      })
      .value();
});

async function addWork() {
  const formData = new FormData();
  formData.append('type', workToAdd.value.type);
  formData.append('hours_count', workToAdd.value.hours_count.toString());
  formData.append('plan_id', params.plan_id.toString());
  formData.append('name', workToAdd.value.name);

  const r = await api.post(`/api/planwork/`, formData);

  params.rows.push(workToAdd.value);
  workToAdd.value = null;
}

async function deleteWork(id: Number) {
  const r = await api.delete(`/api/planwork/${id}/`);

  params.rows.pop(id);
}

</script>

<template>
  <div style="display:grid; grid-template-columns: 5fr 1fr; gap: 12px; padding: 12px" v-if="params.canEdit">
    <q-select v-model="workToAdd"
          label="Работа"
          :options="worksList"
          option-label="name"
          emit-value
          map-options
          clearable
    />

     <q-btn
       label="Добавить"
      style="height: 100%"
      color="primary"
      @click="addWork"
       :disable="workToAdd === null"
    />
  </div>

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
    :visible-columns="canEdit ? ['name', 'hours_count', 'control'] : ['name', 'hours_count']"
  >
   <template v-slot:body-cell-control="props">
     <q-td style="display: flex; justify-content: center" :props="props">
      <q-btn
        icon="mdi-delete-forever"
        color="red"
        @click="deleteWork(props.row.id)"
        :disable="!params.canEdit"
      />
     </q-td>
   </template>
 </q-table>
</template>

<style scoped>

</style>
