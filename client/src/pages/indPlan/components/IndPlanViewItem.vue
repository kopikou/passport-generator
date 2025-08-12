<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";

const tab = ref('first');

const nagr = ref([]);
const rows = ref();
const expanded = ref();

const columns = [
  { name: 'kurs', align: 'center', label: 'Курс', field: 'kurs', sortable: true },
  { name: 'sem', align: 'center', label: 'Семестр', field: 'sem', sortable: true },
  { name: 'grup', align: 'center', label: 'Группа', field: 'grup', sortable: true },
  { name: 'formcntr', align: 'center', label: 'Вид работ', field: 'formcntr', sortable: true },
  { name: 'hours_count', align: 'center', label: 'Часы', field: 'hours_count', sortable: true },
]

async function getNagr(){
  let r = await api.get(`/api/indplan/self/`);
  nagr.value = r.data;

  rows.value = nagr.value.map(r => r.items);

  nagr.value.forEach(item => {
    item.items.forEach(row => {
      rows.value.push(row)
    });
  });

  rows.value.splice(0,11);
  expanded.value = nagr.value.map(r => r.discpl);
}

onBeforeMount(async() => {
  await getNagr();
});

</script>

<template>
  <q-tabs
    v-model="tab"
    class="text-teal"
  >
    <q-tab name="first" label="1 - Учебная нагрузка" />
    <q-tab name="second" label="2 - Подготовка к учебным занятиям" />
    <q-tab name="third" label="3 - Учебно-методическая работа" />
    <q-tab name="fourth" label="4 - Иные виды работ" />
    <q-tab name="fifth" label="5 - Работа с обучающимися и абитуриентами" />
  </q-tabs>

  <q-table
    :rows="rows"
    :columns="columns"
    virtual-scroll
    style="overflow-y: auto; height: 100%;"
    wrap-cells
    flat
    bordered
    separator="cell"
    :rows-per-page-options="[0]"
    v-model:expanded="expanded"
  >
    <template v-slot:body="props">
      <q-tr v-show="props.expand" :props="props"  class="q-virtual-scroll--with-prev">
        <q-td colspan="100%">
          <div class="text-left">{{ props.row.discpl}}.</div>
        </q-td>
      </q-tr>

      <q-tr :props="props" :key="`m_${props.row.discpl}`">
      <q-td
        v-for="col in props.cols"
        :props="props"
        :key="col.name"
      >
        {{ col.value }}
      </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<style scoped>

</style>
