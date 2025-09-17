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
});

const columns = [
  { name: 'name', align: 'center', label: 'Описание', field: 'name', sortable: true },
  { name: 'control', align: 'center', label: 'Действия', field: 'control', sortable: true },
];

const workToAdd = ref(null);

onBeforeMount(async() => {
  await getWorks();
});

async function addWork() {
  const formData = new FormData();
  formData.append('type', 'Работа с обучающимися и абитуриентами');
  formData.append('plan_id', params.plan_id.toString());
  formData.append('name', workToAdd.value);

  const r = await api.post(`/api/planwork/`, formData);

  params.rows.push(r.data);
  workToAdd.value = null;
}

async function deleteWork(id: Number) {
  const r = await api.delete(`/api/planwork/${id}/`);

  params.rows.pop(id);
}

async function updateWork(id: Number, name: String) {
  const formData = new FormData();
  formData.append('name', name);

  const r  = await api.put(`/api/planwork/${id}/`, formData);
}
</script>

<template>
<div style="display:grid; grid-template-columns: 5fr 1fr; gap: 12px; padding: 12px" v-if="params.canEdit">
    <q-input outlined label="Наименогвание работы" v-model="workToAdd"
         clearable @clear="clearFilter"/>

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
    :visible-columns="canEdit ? ['name', 'control'] : ['name']"
  >
   <template v-slot:body-cell-name="props">
     <q-td  :props="props">
         {{props.row.name}}
          <q-popup-edit
            v-if="params.canEdit"
            v-model="props.row.name"
            v-slot="scope"
            buttons
            persistent
            @before-hide="updateWork(props.row.id, props.row.name)"
          >
            <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
          </q-popup-edit>
       </q-td>
   </template>
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
