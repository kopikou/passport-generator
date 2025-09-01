<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import _ from "lodash";

const props = defineProps({
  rows: {
    required: true,
  },
  plan_id: {
    required: true,
  },
});

const columns = [
  { name: 'name', align: 'center', label: 'Описание', field: 'name', sortable: true },
  { name: 'control', align: 'center', label: 'Действия', field: 'control', sortable: true },
];

const works = ref();
const workToAdd = ref();

async function getWorks(){
  let r = await api.get(`/api/indplan/get-works/?type=work_with_students`);
  works.value = r.data;
}

onBeforeMount(async() => {
  await getWorks();
});

async function addWork() {
  const formData = new FormData();
  formData.append('type', 'Работа с обучающимися и абитуриентами');
  formData.append('plan_id', props.plan_id.toString());
  formData.append('name', workToAdd.value);

  const r = await api.post(`/api/planwork/`, formData);

  props.rows.push({
    name: workToAdd.value,
  });
  workToAdd.value = null;
}

async function deleteWork(id: Number) {
  const r = await api.delete(`/api/planwork/${id}/`);

  props.rows.pop(id);
}

async function updateWork(id: Number, name: String) {
  const formData = new FormData();
  formData.append('name', name);

  const r  = await api.put(`/api/planwork/${id}/`, formData);
}
</script>

<template>
<div style="display:grid; grid-template-columns: 5fr 1fr; gap: 12px; padding: 12px">
    <q-input outlined label="Наименогвание работы" v-model="workToAdd"
         clearable @clear="clearFilter"/>

     <q-btn
       label="Добавить"
      style="height: 100%"
      color="primary"
      @click="addWork"
    />
  </div>

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
       <q-td  key="name">
         {{props.row.name}}
          <q-popup-edit v-model="props.row.name" v-slot="scope" buttons persistent @before-hide="updateWork(props.row.id, props.row.name)">
            <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
          </q-popup-edit>
       </q-td>
       <q-td key="control" style="display: flex; justify-content: center; gap: 8px">
         <q-btn
          icon="mdi-delete-forever"
          color="red"
          @click="deleteWork(props.row.id)"
        />
       </q-td>
     </q-tr>
   </template>
 </q-table>

</template>

<style scoped>

</style>
