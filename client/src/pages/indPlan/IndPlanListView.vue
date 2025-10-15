<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {LocalStorage, SessionStorage, useQuasar} from "quasar";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";
import {useRouter} from "vue-router";

const router = useRouter();

const mainStore = useMainStore();
const {
  userId,
} = storeToRefs(mainStore);

const yearFilter = ref(null);

const textFilter = ref('');

const onlyMyPlans = ref(true);

const yearsList = computed(() => {
  let data = _(indPlanList.value)
      .map(item => {
        return item.year;
      })
      .value();

  data = [...new Set(data)]
  return data
});

const indPlanList = ref([]);

async function getIndPlans(){
  let r = await api.get(`/api/indplan/`);
  indPlanList.value = r.data;
}

onBeforeMount(async() => {
  await getIndPlans();
});

const columns = [
  { name: 'author', align: 'center', label: 'Автор', field: 'author', sortable: true },
  { name: 'year', align: 'center', label: 'Год', field: 'year', sortable: true },
  { name: 'status', align: 'center', label: 'Статус', field: 'status' },
];

const statuses = [
  {
    title: "Создан",
    color: "grey"
  },
  {
    title: "Ожидает рассмотрения",
    color: "orange-5"
  },
  {
    title: "Утвержден",
    color: "green"
  },
  {
    title: "Требуются правки",
    color: "red-5"
  },
];

const filteredIndPLanList = computed(() => {
  let txtFilter = textFilter.value.trim().toLowerCase();
  let data = _(indPlanList.value)
    .filter(x => {
      return ((onlyMyPlans.value && x.user_created.user_id === userId.value)
        || (!onlyMyPlans.value && (x.zav === userId.value || x.user_created.user_id === userId.value)))
          && (yearFilter.value === null || x.year === yearFilter.value)
          && (textFilter.value === ''
            || x.user_created.last_name.toLowerCase().includes(txtFilter)
            || x.user_created.first_name.toLowerCase().includes(txtFilter)
            || x.user_created.middle_name.toLowerCase().includes(txtFilter));
    })
    .value();

  return data;
});

</script>

<template>
  <div style="display: grid; grid-template-columns: 5fr 1fr 2fr; gap: 8px; margin: 8px;">
    <q-input outlined label="Поиск по разработчику плана" v-model="textFilter"
                   clearable @clear="textFilter = ''"/>

    <q-toggle
      v-model="onlyMyPlans"
      label="Только мои"
    />

    <q-select
      v-model="yearFilter"
      :options="yearsList"
      clearable
      label="Год"
      emit-value
      map-options
    />
  </div>

  <q-table
    :rows="filteredIndPLanList"
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
      <q-tr :props="props" class="cursor-pointer" @click="router.push(`/ind_plan/${props.row.id}/`)">
        <q-td key="author">
           {{ props.row.user_created.last_name }} {{ props.row.user_created.first_name }} {{ props.row.user_created.middle_name }}
        </q-td>

        <q-td key="year">
           {{ props.row.year }}
        </q-td>

        <q-td key="status" style="display: flex; justify-content: center; align-items: center">
          <q-badge :color="statuses[props.row.status].color" style="height: 20px; font-size: medium">{{ statuses[props.row.status].title }}</q-badge>
        </q-td>
      </q-tr>
    </template>
  </q-table>


</template>

<style scoped lang="scss">
  :deep(.table-header) {
    position: sticky;
    z-index: 1;
    top: 0;
    background: $blue-grey-2;
  }
</style>
