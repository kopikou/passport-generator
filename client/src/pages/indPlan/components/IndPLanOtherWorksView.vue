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
  isAuthor: {
    required: true,
  },
});

const columns = [
  { name: 'type', align: 'center', label: 'Тип', field: 'type', sortable: true },
  { name: 'name', align: 'center', label: 'Наименование', field: 'name', sortable: true },
  { name: 'hours_count', align: 'center', label: 'Количество часов', field: 'hours_count', sortable: true },
  { name: 'control', align: 'center', label: 'Действия', field: 'control', sortable: true },
];

const works = ref();
const workToAdd = ref();

async function getWorks(){
  let r = await api.get(`/api/indplan/get-works/?type=other`);
  works.value = r.data;
}

const worksList = computed(() =>{
  return _(works.value)
    .filter(x => {
      return !(params.rows.includes(x));
    })
    .value();
});

onBeforeMount(async() => {
  await getWorks();
})

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
<div style="display:grid; grid-template-columns: 2fr 2fr 1fr; gap: 12px; padding: 12px" v-if="params.isAuthor">
  <q-select v-model="workToAdd"
          label="Тип работы"
          :options="worksList"
          option-label="type"
          emit-value
          map-options
          clearable
    />

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
  >
    <template v-slot:body-cell-control="props">
     <q-td style="display: flex; justify-content: center" :props="props">
      <q-btn
        icon="mdi-delete-forever"
        color="red"
        @click="deleteWork(props.row.id)"
        :disable="!params.isAuthor"
      />
     </q-td>
   </template>
 </q-table>

</template>

<style scoped>

</style>
