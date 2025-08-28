<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import _ from "lodash";

const props = defineProps({
  rows: {
    required: true,
  },
});

const columns = [
  { name: 'name', align: 'center', label: 'Наименование', field: 'name', sortable: true },
  { name: 'hours_count', align: 'center', label: 'Количество часов', field: 'hours_count', sortable: true },
  { name: 'control', align: 'center', label: 'Действия', field: 'control', sortable: true },
];

const works = ref();
const workToAdd = ref();

async function getWorks(){
  let r = await api.get(`/api/indplan/get-works/?type=educ_method`);
  works.value = r.data;
}

const rowsIdList = computed(() => {
  return _(props.rows)
    .map((row) =>{
    return row.id;
  })
    .values();
})

const worksList = computed(() =>{
    return _(works.value)
      .filter(x => {
        return !(rowsIdList.value.includes(x.id));
      })
      .value();
});

onBeforeMount(async() => {
  await getWorks();
})

async function addWork() {
  props.rows.push(workToAdd.value);
  workToAdd.value = null;
}

</script>

<template>
  <div style="display:grid; grid-template-columns: 5fr 1fr; gap: 12px; padding: 12px">
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
  />
</template>

<style scoped>

</style>
